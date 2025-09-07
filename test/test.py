# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_usr(dut):
    dut._log.info("Starting Universal Shift Register test")

    # 100 KHz clock (10 us period)
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

    # Helper: drive inputs
    def set_inputs(S1, S0, SL, SR, D3, D2, D1, D0):
        dut.ui_in.value = (D3 << 7) | (D2 << 6) | (D1 << 5) | (D0 << 4) \
                        | (SR << 3) | (SL << 2) | (S1 << 1) | (S0 << 0)

    # --- Test sequence ---

    # 1. Parallel load D=1011
    dut._log.info("Parallel load D=1011")
    set_inputs(S1=1, S0=1, SL=0, SR=0, D3=1, D2=0, D1=1, D0=1)
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer & 0xF == 0b1011, f"Expected 1011, got {dut.uo_out.value.binstr}"

    # 2. Hold
    dut._log.info("Hold")
    set_inputs(S1=0, S0=0, SL=0, SR=0, D3=0, D2=0, D1=0, D0=0)
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer & 0xF == 0b1011

    # 3. Shift right, SR=1
    dut._log.info("Shift right, SR=1")
    set_inputs(S1=0, S0=1, SL=0, SR=1, D3=0, D2=0, D1=0, D0=0)
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer & 0xF == 0b1101, f"Expected 1101, got {dut.uo_out.value.binstr}"

    # 4. Shift left, SL=1
    dut._log.info("Shift left, SL=1")
    set_inputs(S1=1, S0=0, SL=1, SR=0, D3=0, D2=0, D1=0, D0=0)
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value.integer & 0xF == 0b1011, f"Expected 1011, got {dut.uo_out.value.binstr}"

    dut._log.info("USR test completed successfully")
