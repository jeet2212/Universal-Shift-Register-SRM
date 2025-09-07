/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none


module tt_um_universal_shift_register (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: input path (unused)
    output wire [7:0] uio_out,  // IOs: output path (unused)
    output wire [7:0] uio_oe,   // IOs: enable path (0 = input, 1 = output)

    input  wire clk,            // clock
    input  wire rst_n,          // reset (active low, synchronous)
    input  wire ena             // enable
);

    // Control inputs
    wire S0 = ui_in[0];
    wire S1 = ui_in[1];
    wire SL = ui_in[2];
    wire SR = ui_in[3];
    wire [3:0] D = ui_in[7:4];

    // 4-bit shift register
    reg [3:0] Q;

    always @(posedge clk) begin
        if (!rst_n) begin
            Q <= 4'b0000;
        end else if (ena) begin
            case ({S1, S0})
                2'b00: Q <= Q;                             // HOLD
                2'b01: Q <= {SR, Q[3:1]};                  // SHIFT RIGHT
                2'b10: Q <= {Q[2:0], SL};                  // SHIFT LEFT
                2'b11: Q <= D;                             // PARALLEL LOAD
            endcase
        end
    end

    // Drive outputs
    assign uo_out[3:0] = Q;
    assign uo_out[7:4] = 4'b0000;

    // No bidirectional IOs used
    assign uio_out = 8'b0000_0000;
    assign uio_oe  = 8'b0000_0000;

endmodule



