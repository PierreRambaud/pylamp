import usb
import time
from .color import Color
from .providers import get_providers


class Controller:
    """
    Controller, send packet to the lamp
    """
    device = None
    color = None

    def open(self):
        """
        Open connection to device
        """

        for provider in get_providers():
            usb_device = usb.core.find(
                idVendor=provider.VENDOR_ID,
                idProduct=provider.PRODUCT_ID
            )
            if usb_device is not None:
                break

        if usb_device is None:
            return False

        self.device = provider(usb_device)
        self.device.prepare()
        return self

    def is_connected(self) -> bool:
        """
        Check if device is connected
        """
        return self.device is not None

    def set_color(self, color: Color):
        """
        Change lamp color
        :param Color color:
        """
        if not isinstance(color, Color):
            raise TypeError('Must be an instance of Color')

        self.color = color
        self.device.colorize(color)

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
