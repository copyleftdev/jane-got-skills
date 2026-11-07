let usage =
  "usage: live.exe <trace.ctf>                      allocation sites live at the end\n\
  \       live.exe <trace.ctf> --at SECONDS          heap snapshot at a time\n\
  \       live.exe <trace.ctf> --lifetimes DEFNAME   median lifetime over time\n"

let print_sites sites =
  List.iteri
    (fun i (s : Memtrace_live.site) ->
      if i < 10 then Printf.printf "%10.1f KB %5.1f%%  %s\n" (s.bytes /. 1024.) (100. *. s.share) s.name)
    sites
;;

let () =
  match Array.to_list Sys.argv |> List.tl with
  | [ file ] -> print_sites (Memtrace_live.live_at_end file)
  | [ file; "--at"; t ] -> print_sites (Memtrace_live.snapshot file ~at_seconds:(float_of_string t))
  | [ file; "--lifetimes"; frame ] ->
    List.iter
      (fun (t, median) ->
        match median with
        | Some m -> Printf.printf "allocated at %7.3fs  median lifetime %7.3fs\n" t m
        | None -> Printf.printf "allocated at %7.3fs  (no samples)\n" t)
      (Memtrace_live.lifetimes file ~frame ~slices:8)
  | _ ->
    prerr_string usage;
    exit 2
;;
