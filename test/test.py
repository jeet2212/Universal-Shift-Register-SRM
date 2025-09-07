# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_universal_shift_register(dut):
    dut._log.info("Starting Universal Shift Register Test")

    # Set clock: 10 us period = 100 kHz
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Initial conditions
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 1

    # Asynchronous Clear (CLR = ui[5])
    dut._log.info("Asserting Clear")
    dut.ui_in.value = (1 << 5)  # CLR = 1
    await ClockCycles(dut.clk, 2)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 2)

   # Parallel Load (ui[4]=1, CLK_EN=1, data=Q3..Q0 on ui[3:0])
    parallel_data = 0b1101  # Load into Q3..Q0
    dut._log.info(f"Parallel Loading {parallel_data:04b}")
    dut.ui_in.value = (1 << 6) | (1 << 4) | (parallel_data & 0xF)  # Add CLK_EN
    await ClockCycles(dut.clk, 1)


    # Check parallel load result
    actual = int(dut.uo_out.value & 0xF)
    assert actual == parallel_data, f"Parallel load failed: expected {parallel_data:04b}, got {actual:04b}"

    # Shift Left (MODE = 01, SER_L = 1)
    dut._log.info("Shifting Left")
    dut.ui_in.value = (1 << 6) | (1 << 2) | (1 << 0)  # CLK_EN=1, MODE0=1, SER_L=1
    await ClockCycles(dut.clk, 1)
    expected = ((parallel_data << 1) | 1) & 0xF
    actual = int(dut.uo_out.value & 0xF)
    assert actual == expected, f"Shift left failed: expected {expected:04b}, got {actual:04b}"

    # Shift Right (MODE = 10, SER_R = 1)
    dut._log.info("Shifting Right")
    dut.ui_in.value = (1 << 6) | (1 << 3) | (1 << 1)  # CLK_EN=1, MODE1=1, SER_R=1
    await ClockCycles(dut.clk, 1)
    expected = (expected >> 1) | (1 << 3)
    actual = int(dut.uo_out.value & 0xF)
    assert actual == expected, f"Shift right failed: expected {expected:04b}, got {actual:04b}"

    # Hold (MODE = 00)
    dut._log.info("Holding State")
    dut.ui_in.value = (1 << 6)  # CLK_EN=1, MODE=00
    await ClockCycles(dut.clk, 1)
    actual = int(dut.uo_out.value & 0xF)
    assert actual == expected, f"Hold failed: expected {expected:04b}, got {actual:04b}"

    dut._log.info("Universal Shift Register Test PASSED")


    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
