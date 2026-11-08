open! Core
open! Hardcaml
open Hardcaml_lws

module Dut = My_design.My_module.Make (struct
    let data_bits = 16
    let latency = 1
  end)

module Harness = Hardcaml_test_harness.Lws_harness.Make (Dut.I) (Dut.O)

let%expect_test "accumulates" =
  Harness.run ~create:Dut.hierarchical (fun (h @ local) ~inputs ~outputs ->
    let open Bits in
    inputs.data_in <--. 42;
    inputs.data_in_valid := vdd;
    Lws.step h;
    print_s [%message (!(outputs.after_edge.result.value) : Bits.Unsigned_int.t)]);
  [%expect {| ("!(((outputs.after_edge).result).value)" 16'd42) |}]
;;
