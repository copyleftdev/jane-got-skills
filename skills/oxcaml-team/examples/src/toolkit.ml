open Stdlib_upstream_compatible

(* One compiled use of each shape in the oxcaml-team skill's "OxCaml Toolkit" table. *)

(* Locality: a local parameter, a stack-allocated record, and exclave_ to return one. *)
type point = { x : int; y : int }

let manhattan (p : point @ local) = abs p.x + abs p.y

let distance_from_origin x y =
  let p = stack_ { x; y } in
  manhattan p [@nontail]
;;

let local_pair x y = exclave_ stack_ { x; y }
let use_local_pair x y = manhattan (local_pair x y) [@nontail]

(* Zero-alloc: checked at compile time by -zero-alloc-check. *)
let[@zero_alloc] add_scaled a b k = a + (b * k)

(* Unboxed types: float#, int64_u-style unboxed int64, and an unboxed product. *)
let unboxed_mean (a : float#) (b : float#) : float# =
  Float_u.div (Float_u.add a b) #2.0

let sum_and_diff (a : int64#) (b : int64#) : #(int64# * int64#) =
  #(Int64_u.add a b, Int64_u.sub a b)

(* Layouts in a kind annotation. *)
type ('a : float64) boxed_float64 = { contents : 'a }

(* or_null: absence without an allocated option. *)
let find_positive (xs : int list) : int or_null =
  match List.find_opt (fun x -> x > 0) xs with
  | Some x -> This x
  | None -> Null
;;

(* Uniqueness and linearity modes. *)
let consume (r : point @ unique) = r.x + r.y
let call_once (f : (unit -> int) @ once) = f ()

(* Contention / portability: a portable closure for fork_join2. Reading a mutable [array] from
   both tasks is rejected as a possible data race; an immutable [iarray] can be shared. *)
let parallel_sum par (xs : int iarray) =
  let n = Base.Iarray.length xs in
  let half = n / 2 in
  let sum lo hi =
    let s = ref 0 in
    for i = lo to hi - 1 do
      s := !s + Base.Iarray.get xs i
    done;
    !s
  in
  let #(a, b) = Parallel.fork_join2 par (fun _ -> sum 0 half) (fun _ -> sum half n) in
  a + b
;;

(* More layouts and the contention axis named explicitly. *)
type ('a : bits64) boxed_bits64 = { bits : 'a }

let length_of_shared (s : string @ contended) = String.length s
let (increment @ portable) x = x + 1
