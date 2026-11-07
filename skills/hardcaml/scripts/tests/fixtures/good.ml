open! Core
open! Hardcaml
open! Signal

let create scope ({ clocking; data_in; enable } : _ I.t) : _ O.t =
  let spec = Clocking.to_spec clocking in
  let%hw a = reg spec ~enable data_in in
  let%hw b = (a +: data_in) -: one 8 in
  let%hw c = (a <: b) &: (data_in >: b) in
  let%hw d = ~:(c) in
  let%hw e = of_unsigned_int ~width:8 255 in
  (* widening the 8-bit count into the 16-bit accumulator is intended *)
  let%hw f = uresize e ~width:16 in
  let%hw g = sel_bottom f ~width:8 in
  let msg = "a -- \"b\" ~enable:vdd" in
  let%hw sum = a +: b +: e in
  ignore (msg, d, g, sum : string * Signal.t * Signal.t * Signal.t);
  { O.out = c }
;;

let%expect_test "x" =
  printf "%d\n" (Bits.to_unsigned_int !(outputs.after_edge.count));
  [%expect {| 1 |}]
;;

(* A derivation kept in a comment must not be linted:
   t2.g |: (t1.g &: t2.p) &: t3.p = (t2.g &: t3.p)
   and neither must  x -- "name"  or  of_int_trunc  *)
let s = {| a +: b -: c ~enable:vdd |}

let round x = Float.to_int x
let k = Int63.to_int_trunc y
