# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`kx132`
================================================================================

CircuitPython Driver for the Kionix KX132 Accelerometer


* Author(s): Jose D. Montoya


"""

from micropython import const
from adafruit_bus_device import i2c_device
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bits import RWBits

try:
    from busio import I2C
    from typing import Tuple
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_KX132.git"


class KX132:
    """Driver for the KX132 Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the KX132 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x69`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`KX132` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        import board
        import kx132

    Once this is done you can define your `board.I2C` object and define your sensor object

    .. code-block:: python

        i2c = board.I2C()  # uses board.SCL and board.SDA
        kx132 = kx132.KX132(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    def __init__(self, i2c_bus: I2C, address: int = xxx) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != xxx:
            raise RuntimeError("Failed to find KX132")