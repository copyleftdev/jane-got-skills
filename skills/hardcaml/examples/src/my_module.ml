open! Core
open! Hardcaml
open! Signal

module type Config = sig
  val data_bits : int

  (** Cycles from [start] to [result.valid]. *)
  val latency : int
end

module Make (Config : Config) = struct
  module I = struct
    type 'a t =
      { clocking : 'a Clocking.t
      ; data_in : 'a [@bits Config.data_bits]
      ; data_in_valid : 'a
      }
    [@@deriving hardcaml]
  end

  module O = struct
    type 'a t = { result : 'a With_valid.t [@bits Config.data_bits] }
    [@@deriving hardcaml]
  end

  let create scope ({ clocking; data_in; data_in_valid } : _ I.t) : _ O.t =
    let spec = Clocking.to_spec clocking in
    let%hw data_q = reg spec ~enable:data_in_valid data_in in
    let%hw valid_q = reg spec data_in_valid in
    { O.result = { valid = valid_q; value = data_q } }
  ;;

  let hierarchical ?instance scope i =
    let module H = Hierarchy.In_scope (I) (O) in
    H.hierarchical ?instance ~scope ~name:"my_module" create i
  ;;
end

module Precedence = struct
  let create scope ~a ~b ~d ~e ~f =
    let%hw sum = (a +: b) -: d in               (* not  a +: b -: d        *)
    let%hw ok = (a <: b) &: (e >: f) in         (* not  a <: b &: e >: f   *)
    sum, ok
  ;;
end
