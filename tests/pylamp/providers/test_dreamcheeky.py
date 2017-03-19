import unittest
import usb
from mock import Mock, call
from pylamp.color import Color
from pylamp.providers.dreamcheeky import DreamCheeky


class DreamCheekyTest(unittest.TestCase):
    device = None

    def set_device(self, usb_device):
        self.device = DreamCheeky(usb_device)

    def test_init(self):
        self.assertEqual(0x1d34, DreamCheeky.VENDOR_ID)
        self.assertEqual(0x0004, DreamCheeky.PRODUCT_ID)
        self.assertEqual(
            (0x1F, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x03),
            DreamCheeky.INIT_PACKET1
        )
        self.assertEqual(
            (0x00, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x04),
            DreamCheeky.INIT_PACKET2
        )

    def test_send_with_error(self):
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 1
        self.set_device(device)

        self.assertFalse(self.device.send('test'))
        device.ctrl_transfer.assert_called_once_with(
            usb.TYPE_CLASS + usb.RECIP_INTERFACE,
            0x09,
            0x81,
            0x00,
            'test',
            100,
        )

    def test_send(self):
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.set_device(device)

        self.assertTrue(self.device.send(111))
        device.ctrl_transfer.assert_called_once_with(
            usb.TYPE_CLASS + usb.RECIP_INTERFACE,
            0x09,
            0x81,
            0x00,
            111,
            100,
        )

    def test_prepare(self):
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.set_device(device)
        self.device.prepare()
        assert device.ctrl_transfer.mock_calls == [
            call(
                usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                0x09,
                0x81,
                0x00,
                DreamCheeky.INIT_PACKET1,
                100
            ),
            call(
                usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                0x09,
                0x81,
                0x00,
                DreamCheeky.INIT_PACKET2,
                100
            )
        ]

    def test_colorize(self):
        color = Color('cyan')
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.set_device(device)
        self.device.colorize(color)
        device.ctrl_transfer.assert_called_once_with(
            usb.TYPE_CLASS + usb.RECIP_INTERFACE,
            0x09,
            0x81,
            0x00,
            (
                color.red,
                color.green,
                color.blue,
                0x00, 0x00,
                0x00,
                0x00,
                0x05
            ),
            100
        )
