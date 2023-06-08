# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import kx132

i2c = board.I2C()  # uses board.SCL and board.SDA
kx = kx132.KX132(i2c)

while True:
    kx.performance_mode = kx132.HIGH_PERFORMANCE_MODE
    kx.output_data_rate = 12  # 3200 Hz
    print("Current Performance Mode setting: ", kx.performance_mode)
    for _ in range(10):
        accx, accy, accz = kx.acceleration
        print("x:{:.2f}m/s2, y:{:.2f}m/s2, z:{:.2f}m/s2".format(accx, accy, accz))
        time.sleep(0.5)
    kx.performance_mode = kx132.LOW_POWER_MODE
    kx.output_data_rate = 3  # 6.25 Hz
    print("Current Performance Mode setting: ", kx.performance_mode)
    for _ in range(10):
        accx, accy, accz = kx.acceleration
        print("x:{:.2f}m/s2, y:{:.2f}m/s2, z:{:.2f}m/s2".format(accx, accy, accz))
        time.sleep(0.5)
