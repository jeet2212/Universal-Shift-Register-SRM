`default_nettype none
`timescale 1ns / 1ps

/* 
   Testbench for Universal Shift Register (USR).
   This is a simple cocotb-compatible TB: 
   - Dumps VCD for waveform viewing
   - Provides convenient wires for driving/observing signals
*/
module tb ();

  // Dump signals to a VCD file for GTKWave
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Inputs/outputs
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiate your Universal Shift Register
  tt_um_universal_shift_register user_project (
      // Include power ports for Gate Level simulation
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: input path
      .uio_out(uio_out),  // IOs: output path
      .uio_oe (uio_oe),   // IOs: output enable
      .ena    (ena),      // enable (when high, design active)
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // active-low reset
  );

  // Generate a simple clock for RTL sim (10ns period = 100MHz)
  initial begin
    clk = 0;
    forever #5 clk = ~clk;
  end

  // Simple reset + enable sequencing
  initial begin
    rst_n = 0;
    ena   = 0;
    ui_in = 8'b0;
    uio_in = 8'b0;

    #20;         // hold reset for 20ns
    rst_n = 1;   // release reset
    ena   = 1;   // enable design
  end

endmodule
