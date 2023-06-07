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
_TILT_POSITION = const(0x14)
_PREVIOUS_TILT_POSITION = const(0x15)
_INS1 = const(0x16)
_INT_REL = const(0x1A)

STANDBY_MODE = const(0b0)
NORMAL_MODE = const(0b1)

# Acceleration range
ACC_RANGE_2 = const(0b00)
ACC_RANGE_4 = const(0b01)
ACC_RANGE_8 = const(0b10)
ACC_RANGE_16 = const(0b11)
acc_range_values = (ACC_RANGE_2, ACC_RANGE_4, ACC_RANGE_8, ACC_RANGE_16)
acc_range_factor = {ACC_RANGE_2: 2, ACC_RANGE_4: 4, ACC_RANGE_8: 8, ACC_RANGE_16: 16}

TILT_DISABLED = const(0b0)
TILT_ENABLED = const(0b1)
tilt_position_enable_values = (TILT_DISABLED, TILT_ENABLED)

# Tap/Double Tap
TDTE_DISABLED = const(0b0)
TDTE_ENABLED = const(0b1)
tap_doubletap_enable_values = (TDTE_DISABLED, TDTE_ENABLED)


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

    _acceleration_data = Struct(_ACC, "hhh")

    _tilt_position = UnaryStruct(_TILT_POSITION, "B")
    _previous_tilt_position = UnaryStruct(_PREVIOUS_TILT_POSITION, "B")

    # Register CNTL1 (0x1B)
    # |PC1|RES|DRDYE|GSEL1|GSEL0|TDTE|----|TPE|
    _operating_mode = RWBit(_CNTL1, 7)
    _acc_range = RWBits(2, _CNTL1, 3)
    _tap_doubletap_enable = RWBit(_CNTL1, 2)
    _tilt_position_enable = RWBit(_CNTL1, 0)

    _interrupt1 = UnaryStruct(_INS1, "B")
    _interrupt_release = UnaryStruct(_INT_REL, "B")

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
        self._operating_mode = STANDBY_MODE
        self._acc_range = value
        self._acc_range_mem = value
        self._operating_mode = NORMAL_MODE

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

    @property
    def tilt_position(self):
        """
        Current Sensor tilt position.
        """
        states = {
            1: "Face-Up State (Z+)",
            2: "Face-Down State (Z-)",
            4: "Up State (Y+)",
            8: "Down State (Y-)",
            16: "Right State (X+)",
            32: "Left State (X-)",
        }
        return states[self._tilt_position]

    @property
    def previous_tilt_position(self):
        """
        Previous Sensor tilt position.
        """
        states = {
            1: "Face-Up State (Z+)",
            2: "Face-Down State (Z-)",
            4: "Up State (Y+)",
            8: "Down State (Y-)",
            16: "Right State (X+)",
            32: "Left State (X-)",
        }
        return states[self._previous_tilt_position]

    @property
    def tilt_position_enable(self) -> str:
        """
        Sensor tilt_position_enable

        +---------------------------------+-----------------+
        | Mode                            | Value           |
        +=================================+=================+
        | :py:const:`kx132.TILT_DISABLED` | :py:const:`0b0` |
        +---------------------------------+-----------------+
        | :py:const:`kx132.TILT_ENABLED`  | :py:const:`0b1` |
        +---------------------------------+-----------------+
        """
        values = (
            "TILT_DISABLED",
            "TILT_ENABLED",
        )
        return values[self._tilt_position_enable]

    @tilt_position_enable.setter
    def tilt_position_enable(self, value: int) -> None:
        if value not in tilt_position_enable_values:
            raise ValueError("Value must be a valid tilt_position_enable setting")
        self._operating_mode = STANDBY_MODE
        self._tilt_position_enable = value
        self._operating_mode = NORMAL_MODE

    @property
    def tap_doubletap_enable(self) -> str:
        """
        Sensor tap_doubletap_enable

        +---------------------------------+-----------------+
        | Mode                            | Value           |
        +=================================+=================+
        | :py:const:`kx132.TDTE_DISABLED` | :py:const:`0b0` |
        +---------------------------------+-----------------+
        | :py:const:`kx132.TDTE_ENABLED`  | :py:const:`0b1` |
        +---------------------------------+-----------------+
        """
        values = ("TDTE_DISABLED", "TDTE_ENABLED")
        return values[self._tap_doubletap_enable]

    @tap_doubletap_enable.setter
    def tap_doubletap_enable(self, value: int) -> None:
        if value not in tap_doubletap_enable_values:
            raise ValueError("Value must be a valid tap_doubletap_enable setting")
        self._operating_mode = STANDBY_MODE
        self._tap_doubletap_enable = value
        self._operating_mode = NORMAL_MODE

    @property
    def tap_doubletap_report(self):
        """
        Tap/Double Tap report
        """
        states = {
            0: "No Tap/Double Tap reported",
            1: "Z Positive (Z+) Reported",
            2: "Z Negative (Z-) Reported",
            4: "Y Positive (Y+) Reported",
            8: "Y Negative (Y-) Reported",
            16: "X Positive (X+) Reported",
            32: "X Negative (X-) Reported",
        }
        return states[self._interrupt1]

    def interrupt_release(self):
        """
        Clear the interrupt register
        """
        _ = self._interrupt_release
