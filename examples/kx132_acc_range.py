# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import kx132

i2c = board.I2C()  # uses board.SCL and board.SDA
kx = kx132.KX132(i2c)

kx.acc_range = kx132.ACC_RANGE_16

while True:
    for acc_range in kx132.acc_range_values:
        print("Current Acc range setting: ", kx.acc_range)
        for _ in range(10):
            accx, accy, accz = kx.acceleration
            print("x:{:.2f}m/s2, y:{:.2f}m/s2, z:{:.2f}m/s2".format(accx, accy, accz))
            time.sleep(0.5)
        kx.acc_range = acc_range
