import usb
import time
from .color import Color


class Controller:
    """
    Controller, send packet to the lamp
    """
    VENDOR_ID = 0x1d34
    PRODUCT_ID = 0x0004
    INIT_PACKET1 = (0x1F, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x03)
    INIT_PACKET2 = (0x00, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x04)

    device = None
    color = None

    def open(self):
        """
        Open connection to device
        """
        device = usb.core.find(
            idVendor=self.VENDOR_ID,
            idProduct=self.PRODUCT_ID
        )

        if device is None:
            return False

        self.device = device
        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)
        self.device.set_configuration()

        return self

    def is_connected(self) -> bool:
        """
        Check if device is connected
        """
        return self.device is not None

    def prepare(self):
        """
        Prepare controller to receive some data
        """
        self.send(self.INIT_PACKET1)
        self.send(self.INIT_PACKET2)

        return self

    def send(self, data: list) -> bool:
        """
        Send data to usb controller
        :param list data:
        :return bool:
        """
        request_type = usb.TYPE_CLASS + usb.RECIP_INTERFACE
        request = 0x09
        value = 0x81
        index = 0x00
        timeout = 100
        return self.device.ctrl_transfer(
            request_type,
            request,
            value,
            index,
            data,
            timeout
        ) == 8

    def set_color(self, color: Color):
        """
        Change lamp color
        :param Color color:
        """
        if not isinstance(color, Color):
            raise TypeError('Must be an instance of Color')

        self.color = color
        data = (
            color.red,
            color.green,
            color.blue,
            0x00,
            0x00,
            0x00,
            0x00,
            0x05
        )
        self.send(data)

    def switch_off(self):
        """
        Switch off
        """
        self.set_color(Color('black'))

    def blink(self, times: int, new_color: Color):
        """
        Blink effect
        :param int times:
        :param Color new_color:
        """
        for i in range(int(times)):
            self.set_color(new_color)
            time.sleep(0.5)
            self.switch_off()
            time.sleep(0.5)

    def fade_in(self, delay: int, new_color: Color):
        """
        Fade in effect
        :param int delay:
        :param Color new_color:
        """
        delay = int(delay)
        c = Color()
        max_value = max(new_color.red, new_color.green, new_color.blue)
        for i in range(max_value):
            time.sleep((delay * 1000 / max_value + 1) / 1000)
            c.red = self.__transition(
                i,
                self.color.red,
                new_color.red,
                max_value
            )
            c.green = self.__transition(
                i,
                self.color.green,
                new_color.green,
                max_value
            )
            c.blue = self.__transition(
                i,
                self.color.blue,
                new_color.blue,
                max_value
            )
            self.set_color(c)

    def __transition(
            self,
            index: int,
            start_point: int,
            end_point: int,
            maximum: int
    ) -> int:
        """
        Calculate transition
        :param int index:
        :param int start_point:
        :param int end_point:
        :param int maximum:
        :return int:
        """
        return int(
            (
                (start_point + (end_point - start_point)) * (index + 1)
            ) / maximum
        )
