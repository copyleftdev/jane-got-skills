let a = reg spec ~enable:vdd d in                       (* H001 *)
let b = (x +: y) -- "b" in                              (* H002 *)
let c = of_int_trunc ~width:8 255 in                    (* H003 *)
let n = Bits.to_int !(outputs.count) in                 (* H004 *)
type 'a t = { x : 'a } [@@deriving sexp_of, hardcaml]   (* H005 *)
let d = (~:) foo in                                     (* H006 *)

let e = uresize f 8 in
let g = a +: b -: d in                                  (* H008 *)
let h = a <: b &: e >: f in                             (* H008 *)
module Sim = Hardcaml_event_driven_sim.Make (Logic)     (* H009 *)
let _special_code_1 = 1                                 (* H010 *)
