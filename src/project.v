/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_universal_shift_register (
    input  wire [7:0] ui_in,    // Control & data inputs
    output wire [7:0] uo_out,   // Register output
    input  wire [7:0] uio_in,   // Not used
    output wire [7:0] uio_out,  // Not used
    output wire [7:0] uio_oe,   // Not used

    input  wire clk,            // clock
    input  wire rst_n,          // reset (active low)
    input  wire ena             // enable
);

    // Control signals
    wire [1:0] mode = ui_in[1:0];       // 00=Hold, 01=Shift Right, 10=Shift Left, 11=Parallel Load
    wire serial_in_left  = ui_in[2];
    wire serial_in_right = ui_in[3];
    wire [7:0] parallel_in = uio_in;    // Use uio_in as parallel input

    reg [7:0] q;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 8'b0;
        else if (ena) begin
            case (mode)
                2'b00: q <= q; // Hold
                2'b01: q <= {serial_in_left, q[7:1]}; // Shift Right
                2'b10: q <= {q[6:0], serial_in_right}; // Shift Left
                2'b11: q <= parallel_in; // Parallel Load
                default: q <= q;
            endcase
        end
    end

    assign uo_out = q;

    // No bidirectional IOs used
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

endmodule

