Universal Shift Register (8-bit)
How it works

This project implements an 8-bit Universal Shift Register (USR) using Verilog for the TinyTapeout platform.
A Universal Shift Register is a versatile digital circuit that can:

Hold its current data

Shift Left (insert data from the right side)

Shift Right (insert data from the left side)

Parallel Load an 8-bit value in a single clock cycle

The mode of operation is controlled using two bits (ui[1:0]):

00 → Hold

01 → Shift Right

10 → Shift Left

11 → Parallel Load

Additional pins:

ui[2] → Serial input (Left side)

ui[3] → Serial input (Right side)

uio[7:0] → Parallel input (8 bits)

uo[7:0] → Register contents (8 bits)

On reset (rst_n = 0), the register clears to 0000_0000.
When enabled (ena = 1), it updates its contents on each clock cycle according to the selected mode.

How to test

Reset the design by setting rst_n = 0, then release it (rst_n = 1).

Set ena = 1 to enable the register.

Apply the desired mode on ui[1:0]:

11 → Load data from uio[7:0]

01 → Shift right (use ui[2] for incoming data)

10 → Shift left (use ui[3] for incoming data)

00 → Hold current value

Observe the output on uo[7:0].

Provide a clock signal on clk (e.g., 50 MHz for testing).

Example sequence:

Load 10101010 into the register by setting uio = 8'b10101010 and ui[1:0] = 2'b11.

Shift right twice by setting ui[1:0] = 2'b01 and toggling clk.

Hold the current value by setting ui[1:0] = 2'b00.

External hardware

No external hardware is required.
The project uses only TinyTapeout standard pins (ui, uio, uo, clk, rst_n, ena).

Optional:

You can connect the outputs (uo[7:0]) to LEDs to visualize shifting operations.

Inputs (uio[7:0]) can be connected to DIP switches or microcontroller GPIOs for parallel loading
