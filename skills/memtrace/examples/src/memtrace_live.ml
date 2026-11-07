open Memtrace.Trace

type site =
  { name : string
  ; bytes : float
  ; share : float
  }

type sample =
  { at : Timedelta.t
  ; frames : Location.t list
  ; words : float
  }

let us t = Int64.to_float (Timedelta.to_int64 t) /. 1e6

let is_stdlib (l : Location.t) =
  String.length l.defname >= 7 && String.sub l.defname 0 7 = "Stdlib_"

(* The allocating frame, or the first frame outside Stdlib, so [Hashtbl.replace] is charged to its caller. *)
let label frames =
  let named = List.rev frames in
  let site = List.find_opt (fun l -> not (is_stdlib l)) named in
  match site, named with
  | Some l, _ -> Printf.sprintf "%s (%s:%d)" l.defname l.filename l.line
  | None, l :: _ -> Location.to_string l
  | None, [] -> "<unknown>"
;;

let read filename =
  let trace = Reader.open_ ~filename in
  let info = Reader.info trace in
  let per_sample_words = 1. /. info.sample_rate in
  let live = Obj_id.Tbl.create 1024 in
  let collected = ref [] in
  let last = ref None in
  Reader.iter trace (fun time ev ->
    last := Some time;
    match ev with
    | Alloc a ->
      let frames =
        List.concat_map
          (Reader.lookup_location_code trace)
          (Array.to_list (Array.sub a.backtrace_buffer 0 a.backtrace_length))
      in
      Obj_id.Tbl.replace
        live
        a.obj_id
        { at = time; frames; words = float a.nsamples *. per_sample_words }
    | Collect (id, _) ->
      (match Obj_id.Tbl.find_opt live id with
       | Some s ->
         collected := (s, time) :: !collected;
         Obj_id.Tbl.remove live id
       | None -> ())
    | Promote _ -> ());
  let word_bytes = float (info.word_size / 8) in
  Reader.close trace;
  let survivors = Obj_id.Tbl.fold (fun _ s acc -> s :: acc) live [] in
  survivors, !collected, !last, word_bytes
;;

let rank ~word_bytes samples =
  let tbl = Hashtbl.create 64 in
  List.iter
    (fun s ->
      let k = label s.frames in
      Hashtbl.replace tbl k (s.words +. Option.value (Hashtbl.find_opt tbl k) ~default:0.))
    samples;
  let total = Hashtbl.fold (fun _ w acc -> acc +. w) tbl 0. in
  Hashtbl.fold
    (fun name w acc -> { name; bytes = w *. word_bytes; share = w /. total } :: acc)
    tbl
    []
  |> List.sort (fun a b -> compare b.bytes a.bytes)
;;

(* Allocations that were never collected: what a leak leaves behind. *)
let live_at_end filename =
  let survivors, _, _, word_bytes = read filename in
  rank ~word_bytes survivors
;;

(* Every sampled allocation, freed or not: what an allocation profiler ranks by. *)
let allocated filename =
  let survivors, collected, _, word_bytes = read filename in
  rank ~word_bytes (survivors @ List.map fst collected)
;;

(* Allocated before [t] and still live after it: the heap as it stood at time [t]. *)
let snapshot filename ~at_seconds =
  let survivors, collected, _, word_bytes = read filename in
  let before s = us s.at <= at_seconds in
  rank
    ~word_bytes
    (List.filter before survivors
     @ List.filter_map
         (fun (s, freed) -> if before s && us freed > at_seconds then Some s else None)
         collected)
;;

(* Median lifetime, per slice of allocation time, of allocations whose backtrace mentions [frame].
   Never-collected allocations count as freed at the end of the trace, as in the Memtrace blog. *)
let lifetimes filename ~frame ~slices =
  let survivors, collected, last, _ = read filename in
  let last = Option.fold last ~none:0. ~some:us in
  let mentions s = List.exists (fun (l : Location.t) -> l.defname = frame) s.frames in
  let pairs =
    List.filter_map
      (fun (s, freed) -> if mentions s then Some (us s.at, us freed -. us s.at) else None)
      collected
    @ List.filter_map
        (fun s -> if mentions s then Some (us s.at, last -. us s.at) else None)
        survivors
  in
  match pairs with
  | [] -> []
  | _ ->
    let t_end = List.fold_left (fun m (a, _) -> Float.max m a) 0. pairs in
    let width = t_end /. float slices +. 1e-9 in
    List.init slices (fun i ->
      let lo = float i *. width in
      let lives =
        List.filter_map
          (fun (a, l) -> if a >= lo && a < lo +. width then Some l else None)
          pairs
        |> List.sort compare
      in
      match lives with
      | [] -> lo, None
      | _ -> lo, Some (List.nth lives (List.length lives / 2)))
;;

module Workloads = Workloads
