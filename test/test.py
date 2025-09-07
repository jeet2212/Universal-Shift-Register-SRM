# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_universal_shift_register(dut):
    dut._log.info("Starting Universal Shift Register Test")

    # Clock: 10us period
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # --- Test Parallel Load (Mode = 11) ---
    dut._log.info("Testing Parallel Load")
    parallel_data = 0b1101  # 13 decimal
    dut.ui_in.value = 0b11      # mode = 11 (parallel load)
    dut.uio_in.value = parallel_data
    await ClockCycles(dut.clk, 1)
    actual = int(dut.uo_out.value & 0xF)  # Only lower 4 bits
    assert actual == parallel_data, f"Parallel load failed: expected {parallel_data:04b}, got {actual:04b}"

    # --- Test Shift Right (Mode = 01) ---
    dut._log.info("Testing Shift Right")
    dut.ui_in.value = 0b01 | (0 << 2)  # mode = 01, serial_in_left=0
    await ClockCycles(dut.clk, 1)
    expected_sr = (parallel_data >> 1) | (0 << 3)
    actual = int(dut.uo_out.value & 0xF)
    assert actual == expected_sr, f"Shift Right failed: expected {expected_sr:04b}, got {actual:04b}"

    # --- Test Shift Left (Mode = 10) ---
    dut._log.info("Testing Shift Left")
    dut.ui_in.value = 0b10 | (1 << 3)  # mode = 10, serial_in_right=1
    await ClockCycles(dut.clk, 1)
    expected_sl = ((expected_sr << 1) & 0xF) | 1
    actual = int(dut.uo_out.value & 0xF)
    assert actual == expected_sl, f"Shift Left failed: expected {expected_sl:04b}, got {actual:04b}"

    # --- Test Hold (Mode = 00) ---
    dut._log.info("Testing Hold")
    dut.ui_in.value = 0b00  # mode = 00 (hold)
    await ClockCycles(dut.clk, 2)
    actual = int(dut.uo_out.value & 0xF)
    assert actual == expected_sl, f"Hold failed: expected {expected_sl:04b}, got {actual:04b}"

    dut._log.info("Universal Shift Register Test Passed!")



    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
