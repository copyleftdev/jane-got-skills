open! Core
open! Hardcaml

module Dut = My_design.My_module.Make (struct
    let data_bits = 16
    let latency = 1
  end)

let%expect_test "accumulates" =
  let module Sim = Cyclesim.With_interface (Dut.I) (Dut.O) in
  let scope = Scope.create ~flatten_design:true () in
  let sim = Sim.create ~config:Cyclesim.Config.trace_all (Dut.create scope) in
  let waves, sim = Cyclesim.Waveform.create sim in
  let display_rules =
    [ Hardcaml_waveterm.Display_rule.port_name_matches
        ~wave_format:(Bit_or Unsigned_int) (Glob "*")
    ]
  in
  let inputs = Cyclesim.inputs sim in
  let outputs = Cyclesim.outputs sim in
  inputs.data_in := Bits.of_unsigned_int ~width:16 42;
  inputs.data_in_valid := Bits.vdd;
  Cyclesim.cycle sim;
  print_s [%message (Bits.to_unsigned_int !(outputs.result.value) : int)];
  Hardcaml_waveterm.Waveform.print ~display_rules waves;
  [%expect {|
    ("Bits.to_unsigned_int (!((outputs.result).value))" 42)
    ┌Signals────────┐┌Waves──────────────────────────────────────────────┐
    │clear          ││                                                   │
    │               ││────────                                           │
    │clock          ││────┐                                              │
    │               ││    └───                                           │
    │               ││────────                                           │
    │data_in        ││ 42                                                │
    │               ││────────                                           │
    │data_in_valid  ││────────                                           │
    │               ││                                                   │
    │result$valid   ││                                                   │
    │               ││────────                                           │
    │               ││────────                                           │
    │result$value   ││ 0                                                 │
    │               ││────────                                           │
    │               ││────────                                           │
    │data_q         ││ 0                                                 │
    │               ││────────                                           │
    │valid_q        ││                                                   │
    │               ││────────                                           │
    └───────────────┘└───────────────────────────────────────────────────┘
    |}]
;;

let%expect_test "holds its value while data_in_valid is low" =
  let module Sim = Cyclesim.With_interface (Dut.I) (Dut.O) in
  let sim = Sim.create (Dut.create (Scope.create ~flatten_design:true ())) in
  let inputs = Cyclesim.inputs sim in
  let outputs = Cyclesim.outputs sim in
  let step ~data ~valid =
    inputs.data_in := Bits.of_unsigned_int ~width:16 data;
    inputs.data_in_valid := Bits.of_bool valid;
    Cyclesim.cycle sim;
    printf
      "in %2d valid %b -> value %2d valid %d\n"
      data
      valid
      (Bits.to_unsigned_int !(outputs.result.value))
      (Bits.to_unsigned_int !(outputs.result.valid))
  in
  step ~data:42 ~valid:true;
  step ~data:7 ~valid:false;
  step ~data:9 ~valid:false;
  step ~data:5 ~valid:true;
  [%expect {|
    in 42 valid true -> value 42 valid 1
    in  7 valid false -> value 42 valid 0
    in  9 valid false -> value 42 valid 0
    in  5 valid true -> value  5 valid 1
    |}]
;;
