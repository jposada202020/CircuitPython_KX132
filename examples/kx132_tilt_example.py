# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import kx132

i2c = board.I2C()  # uses board.SCL and board.SDA
kx = kx132.KX132(i2c)

kx.tilt_position_enable = kx132.TILT_ENABLED

while True:
    print(f"Current position {kx.tilt_position}")
    time.sleep(0.3)
