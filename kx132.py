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
from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit

try:
    from busio import I2C
    from typing import Tuple
except ImportError:
    pass


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_KX132.git"

_REG_WHOAMI = const(0x13)
_CNTL1 = const(0x1B)
_ACC = const(0x08)

STANDBY_MODE = const(0b0)
NORMAL_MODE = const(0b1)

# Acceleration range
ACC_RANGE_2 = const(0b00)
ACC_RANGE_4 = const(0b01)
ACC_RANGE_8 = const(0b10)
ACC_RANGE_16 = const(0b11)
acc_range_values = (ACC_RANGE_2, ACC_RANGE_4, ACC_RANGE_8, ACC_RANGE_16)
acc_range_factor = {ACC_RANGE_2: 2, ACC_RANGE_4: 4, ACC_RANGE_8: 8, ACC_RANGE_16: 16}


class KX132:
    """Driver for the KX132 Sensor connected over I2C.

    :param ~busio.I2C i2c_bus: The I2C bus the KX132 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x1F`

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
        kx = kx132.KX132(i2c)

    Now you have access to the attributes

    .. code-block:: python

        accx, accy, accz = kx.acceleration

    """

    _device_id = ROUnaryStruct(_REG_WHOAMI, "B")
    _control_register1 = UnaryStruct(_CNTL1, "B")

    _operating_mode = RWBit(_CNTL1, 7)
    _acc_range = RWBits(2, _CNTL1, 3)

    _acceleration_data = Struct(_ACC, "hhh")

    def __init__(self, i2c_bus: I2C, address: int = 0x1F) -> None:
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != 0x3D:
            raise RuntimeError("Failed to find KX132")

        self._operating_mode = NORMAL_MODE
        self.acc_range = ACC_RANGE_2

    @property
    def acc_range(self) -> str:
        """

        +---------------------------------+------------------+
        | Mode                            | Value            |
        +=================================+==================+
        | :py:const:`kx132.ACC_RANGE_2`   | :py:const:`0b00` |
        +---------------------------------+------------------+
        | :py:const:`kx132.ACC_RANGE_4`   | :py:const:`0b01` |
        +---------------------------------+------------------+
        | :py:const:`kx132.ACC_RANGE_8`   | :py:const:`0b10` |
        +---------------------------------+------------------+
        | :py:const:`kx132.ACC_RANGE_16`  | :py:const:`0b11` |
        +---------------------------------+------------------+
        """
        values = (
            "ACC_RANGE_2",
            "ACC_RANGE_4",
            "ACC_RANGE_8",
            "ACC_RANGE_16",
        )
        return values[self._acc_range_mem]

    @acc_range.setter
    def acc_range(self, value: int) -> None:
        if value not in acc_range_values:
            raise ValueError("Value must be a valid acc_range setting")
        self._acc_range = value
        self._acc_range_mem = value

    @property
    def acceleration(self) -> Tuple[float, float, float]:
        """
        Acceleration
        :return: acceleration
        """
        bufx, bufy, bufz = self._acceleration_data

        factor = acc_range_factor[self._acc_range_mem]

        return (
            bufx / 2**15 * factor,
            bufy / 2**15 * factor,
            bufz / 2**15 * factor,
        )
