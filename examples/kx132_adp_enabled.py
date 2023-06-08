# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import kx132

i2c = board.I2C()  # uses board.SCL and board.SDA
kx = kx132.KX132(i2c)

while True:
    kx.adp_enabled = kx132.ADP_DISABLED
    print("Current ADP setting: ", kx.adp_enabled)
    for _ in range(10):
        adpx, adpy, adpz = kx.advanced_data_path
        print("x:{:.2f}g, y:{:.2f}g, z:{:.2f}g".format(adpx, adpy, adpz))
        time.sleep(0.5)
    kx.adp_enabled = kx132.ADP_ENABLED
    print("Current ADP setting: ", kx.adp_enabled)
    for _ in range(10):
        adpx, adpy, adpz = kx.advanced_data_path
        print("x:{:.2f}g, y:{:.2f}g, z:{:.2f}g".format(adpx, adpy, adpz))
        time.sleep(0.5)
    kx.soft_reset()
