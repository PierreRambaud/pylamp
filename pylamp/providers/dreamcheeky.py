import usb
from pylamp.color import Color
from .base import Base


class DreamCheeky(Base):
    '''
    Dream cheeky lamp
    '''

    VENDOR_ID = 0x1d34
    PRODUCT_ID = 0x0004
    INIT_PACKET1 = (0x1F, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x03)
    INIT_PACKET2 = (0x00, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x04)

    def prepare_packets(self) -> list:
        """
        Return the list of needed packets
        to initialize lamp
        """
        return (
            self.INIT_PACKET1,
            self.INIT_PACKET2,
        )

    def send(self, data: list) -> bool:
        '''
        Send data to usb controller
        :param list data:
        :return bool:
        '''
        request_type = usb.TYPE_CLASS + usb.RECIP_INTERFACE
        request = 0x09
        value = 0x81
        index = 0x00
        timeout = 100
        return self.usb_device.ctrl_transfer(
            request_type,
            request,
            value,
            index,
            data,
            timeout
        ) == 8

    def colorize(self, color: Color):
        '''
        Change lamp color
        :param Color color:
        '''
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
        return self.send(data)
