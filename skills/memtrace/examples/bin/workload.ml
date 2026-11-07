let () =
  Memtrace.trace_if_requested ();
  match Sys.argv with
  | [| _; "leak" |] -> Memtrace_live.Workloads.leaky_server ~requests:20_000
  | [| _; "backlog" |] -> Memtrace_live.Workloads.backlogged_pipeline ~ticks:200_000
  | _ ->
    prerr_endline "usage: workload.exe leak|backlog";
    exit 2
;;
