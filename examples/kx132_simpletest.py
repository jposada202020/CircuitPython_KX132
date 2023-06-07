# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import kx132

i2c = board.I2C()  # uses board.SCL and board.SDA
kx = kx132.KX132(i2c)

while True:
    accx, accy, accz = kx.acceleration
    print("x:{:.2f}g, y:{:.2f}g, z:{:.2f}g".format(accx, accy, accz))
    time.sleep(0.1)
