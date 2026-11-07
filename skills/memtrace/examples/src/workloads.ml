(* A cache that is written on every request and never evicted. *)
let cache : (int, Bytes.t) Hashtbl.t = Hashtbl.create 16
let remember i = Hashtbl.replace cache i (Bytes.create 1024)
let scratch () = ignore (Sys.opaque_identity (Array.make 64 0))

let leaky_server ~requests =
  for i = 1 to requests do
    remember i;
    for _ = 1 to 10 do
      scratch ()
    done
  done
;;

(* A producer that enqueues twice as fast as the consumer drains, with no backpressure. *)
let work_queue : Bytes.t Queue.t = Queue.create ()
let produce () = Queue.add (Bytes.create 256) work_queue

let consume () =
  if not (Queue.is_empty work_queue) then ignore (Sys.opaque_identity (Queue.pop work_queue))
;;

let pipeline ~ticks ~produced_per_tick =
  for _ = 1 to ticks do
    for _ = 1 to produced_per_tick do
      produce ()
    done;
    consume ();
    for _ = 1 to 50 do
      scratch ()
    done
  done;
  Queue.clear work_queue
;;

let backlogged_pipeline ~ticks = pipeline ~ticks ~produced_per_tick:2
let balanced_pipeline ~ticks = pipeline ~ticks ~produced_per_tick:1
