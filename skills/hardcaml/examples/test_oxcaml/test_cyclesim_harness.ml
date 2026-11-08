open! Core
open! Hardcaml
open Hardcaml_test_harness

module Dut = My_design.My_module.Make (struct
    let data_bits = 16
    let latency = 1
  end)

module Harness = Cyclesim_harness.Make (Dut.I) (Dut.O)

let ( <--. ) = Bits.( <--. )

let%expect_test "accumulates" =
  Harness.run_advanced ~create:Dut.hierarchical (fun sim ->
    let inputs = Cyclesim.inputs sim in
    let outputs = Cyclesim.outputs ~clock_edge:After sim in
    inputs.clocking.clear := Bits.vdd;
    Cyclesim.cycle sim;
    inputs.clocking.clear := Bits.gnd;
    inputs.data_in <--. 42;
    inputs.data_in_valid := Bits.vdd;
    Cyclesim.cycle sim;
    print_s [%message (Bits.to_unsigned_int !(outputs.result.value) : int)]);
  [%expect {| ("Bits.to_unsigned_int (!((outputs.result).value))" 42) |}]
;;
