import unittest
import usb
from mock import patch, Mock, call
from pylamp.color import Color
from pylamp.controller import Controller
from pylamp.providers import DreamCheeky


class ControllerTest(unittest.TestCase):
    pylamp = None

    def setUp(self):
        self.controller = Controller()

    def test_init(self):
        self.assertIsNone(self.controller.device)

    def test_open_without_pylamp(self):
        with patch('usb.core.find', return_value=None) as find_patch:
            self.assertFalse(self.controller.open())
            self.assertFalse(self.controller.is_connected())
            find_patch.assert_called_once_with(
                idVendor=DreamCheeky.VENDOR_ID,
                idProduct=DreamCheeky.PRODUCT_ID
            )
            self.assertIsNone(self.controller.device)

    def test_open_with_device(self):
        device = Mock(spec=usb.core.Device)
        device.is_kernel_driver_active.return_value = True
        device.detach_kernel_driver.return_value = None
        device.set_configuration.return_value = None

        with patch('usb.core.find', return_value=device) as find_patch:
            self.assertIsInstance(self.controller.open(), Controller)
            self.assertTrue(self.controller.is_connected())
            find_patch.assert_called_once_with(
                idVendor=DreamCheeky.VENDOR_ID,
                idProduct=DreamCheeky.PRODUCT_ID
            )
            device.is_kernel_driver_active.assert_called_once_with(0)
            device.detach_kernel_driver.assert_called_once_with(0)
            device.set_configuration.assert_called_once_with()
            self.assertIsInstance(self.controller.device, DreamCheeky)
            device.is_kernel_driver_active.return_value = False
            self.assertIsInstance(self.controller.open(), Controller)

    def test_set_color_with_error(self):
        self.assertRaises(TypeError, self.controller.set_color, 'test')

    def test_set_color(self):
        color = Color('cyan')
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.controller.device = DreamCheeky(device)
        self.controller.set_color(color)
        self.assertEqual(color, self.controller.color)
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

    def test_switch_off(self):
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.controller.device = DreamCheeky(device)
        self.controller.switch_off()
        device.ctrl_transfer.assert_called_once_with(
            usb.TYPE_CLASS + usb.RECIP_INTERFACE,
            0x09,
            0x81,
            0x00,
            (0, 0, 0, 0x00, 0x00, 0x00, 0x00, 0x05),
            100
        )

    def test_blink(self):
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.controller.device = DreamCheeky(device)
        with patch('time.sleep', return_value=None) as sleep_patch:
            self.controller.blink(2, Color('blue'))
            self.assertEqual(
                sleep_patch.call_count,
                4
            )

            assert device.ctrl_transfer.mock_calls == [
                call(
                    usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                    0x09,
                    0x81,
                    0x00,
                    (0, 0, 64, 0x00, 0x00, 0x00, 0x00, 0x05),
                    100
                ),
                call(
                    usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                    0x09,
                    0x81,
                    0x00,
                    (0, 0, 0, 0x00, 0x00, 0x00, 0x00, 0x05),
                    100
                ),
                call(
                    usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                    0x09,
                    0x81,
                    0x00,
                    (0, 0, 64, 0x00, 0x00, 0x00, 0x00, 0x05),
                    100
                ),
                call(
                    usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                    0x09,
                    0x81,
                    0x00,
                    (0, 0, 0, 0x00, 0x00, 0x00, 0x00, 0x05),
                    100
                )
            ]

    def test_fade_in(self):
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.controller.device = DreamCheeky(device)
        self.controller.switch_off()
        with patch('time.sleep', return_value=None) as sleep_patch:
            self.controller.fade_in(1, Color('blue'))
            self.assertEqual(
                sleep_patch.call_count,
                64
            )
            self.assertEqual(
                device.ctrl_transfer.call_count,
                65
            )
            device.ctrl_transfer.assert_any_call(
                usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                0x09,
                0x81,
                0x00,
                (0, 0, 0, 0x00, 0x00, 0x00, 0x00, 0x05),
                100
            )
