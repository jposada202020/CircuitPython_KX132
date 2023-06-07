# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import kx132

i2c = board.I2C()  # uses board.SCL and board.SDA
kx = kx132.KX132(i2c)

kx.tap_doubletap_enable = kx132.TDTE_ENABLED

while True:
    print(f"Status: {kx.tap_doubletap_report}")
    kx.interrupt_release()
    time.sleep(0.3)
