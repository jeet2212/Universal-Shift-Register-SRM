`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a VCD file
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Inputs and outputs
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;    // [1:0] mode, [2] serial_in_left, [3] serial_in_right
  reg [7:0] uio_in;   // parallel_in
  wire [7:0] uo_out;  // current register content
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

`ifdef GL_TEST
  wire VPWR = 1'b1;
  wire VGND = 1'b0;
`endif

  // Instantiate the Universal Shift Register
  tt_um_universal_shift_register user_project (
`ifdef GL_TEST
      .VPWR(VPWR),
      .VGND(VGND),
`endif
      .ui_in  (ui_in),
      .uo_out (uo_out),
      .uio_in (uio_in),
      .uio_out(uio_out),
      .uio_oe (uio_oe),
      .ena    (ena),
      .clk    (clk),
      .rst_n  (rst_n)
  );

  // Clock generation (20 ns period = 50 MHz)
  always #10 clk = ~clk;

  // Test sequence
  initial begin
    // Initial conditions
    clk = 0;
    rst_n = 0;
    ena = 0;
    ui_in = 8'b0;
    uio_in = 8'b0;

    // Release reset and enable design
    #25 rst_n = 1;
    ena = 1;

    // 1) Parallel load: mode = 11
    uio_in = 8'b10101010;   // Load pattern
    ui_in[1:0] = 2'b11;     // Parallel load
    #20;

    // 2) Shift right: mode = 01, serial_in_left = 1
    ui_in[1:0] = 2'b01;
    ui_in[2] = 1'b1;
    #40;

    // 3) Shift left: mode = 10, serial_in_right = 1
    ui_in[1:0] = 2'b10;
    ui_in[3] = 1'b1;
    #40;

    // 4) Hold: mode = 00
    ui_in[1:0] = 2'b00;
    #40;


  end

endmodule
