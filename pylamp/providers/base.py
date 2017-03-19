from abc import ABCMeta, abstractmethod
from pylamp.color import Color


class Base(metaclass=ABCMeta):
    usb_device = None

    def __init__(self, usb_device):
        self.usb_device = usb_device

    def prepare(self):
        '''
        Prepare controller to receive some data
        '''
        if self.usb_device.is_kernel_driver_active(0):
            self.usb_device.detach_kernel_driver(0)
        self.usb_device.set_configuration()

        for packets in self.prepare_packets():
            self.send(packets)

        return self

    @abstractmethod
    def prepare_packets(self) -> list:
        pass

    @abstractmethod
    def send(self, data: list) -> bool:
        pass

    @abstractmethod
    def colorize(self, color: Color):
        pass
