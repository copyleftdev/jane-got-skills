let trace_to_file ~f =
  let filename = Filename.temp_file "memtrace_live" ".ctf" in
  let tracer = Memtrace.start_tracing ~context:None ~sampling_rate:1e-3 ~filename in
  f ();
  Memtrace.stop_tracing tracer;
  filename
;;

let top n sites =
  List.iteri
    (fun i (s : Memtrace_live.site) ->
      if i < n then Printf.printf "%s, majority: %b\n" s.name (s.share > 0.5))
    sites
;;

let%expect_test "allocation volume points at the churn, survivors point at the leak" =
  let file = trace_to_file ~f:(fun () -> Memtrace_live.Workloads.leaky_server ~requests:20_000) in
  print_endline "ranked by allocation volume:";
  top 1 (Memtrace_live.allocated file);
  print_endline "ranked by what is still live at the end:";
  top 1 (Memtrace_live.live_at_end file);
  [%expect {|
    ranked by allocation volume:
    Memtrace_live__Workloads.scratch (src/workloads.ml:4), majority: true
    ranked by what is still live at the end:
    Memtrace_live__Workloads.remember (src/workloads.ml:3), majority: true
    |}]
;;

let peak_median_lifetime file =
  Memtrace_live.lifetimes file ~frame:"Memtrace_live__Workloads.produce" ~slices:8
  |> List.filter_map snd
  |> List.fold_left Float.max 0.
;;

let%expect_test "a backlogged queue shows up as lifetimes that grow with time" =
  let balanced =
    trace_to_file ~f:(fun () -> Memtrace_live.Workloads.balanced_pipeline ~ticks:100_000)
  in
  let backlogged =
    trace_to_file ~f:(fun () -> Memtrace_live.Workloads.backlogged_pipeline ~ticks:100_000)
  in
  let b = peak_median_lifetime balanced
  and q = peak_median_lifetime backlogged in
  Printf.printf "backlogged peak median lifetime > 10x balanced: %b\n" (q > 10. *. b);
  [%expect {| backlogged peak median lifetime > 10x balanced: true |}]
;;

let%expect_test "a mid-run snapshot of the backlogged heap is mostly queued work" =
  let file =
    trace_to_file ~f:(fun () -> Memtrace_live.Workloads.backlogged_pipeline ~ticks:100_000)
  in
  let last =
    Memtrace_live.lifetimes file ~frame:"Memtrace_live__Workloads.produce" ~slices:2
    |> List.rev
    |> List.hd
    |> fst
  in
  let s = List.hd (Memtrace_live.snapshot file ~at_seconds:last) in
  Printf.printf "%s holds the majority: %b\n" s.name (s.share > 0.5);
  [%expect {| Memtrace_live__Workloads.produce (src/workloads.ml:17) holds the majority: true |}]
;;
