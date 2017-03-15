import unittest
import usb
from mock import patch, Mock, call
from pylamp.color import Color
from pylamp.controller import Controller


class ControllerTest(unittest.TestCase):
    pylamp = None

    def setUp(self):
        self.controller = Controller()

    def test_init(self):
        self.assertEqual(0x1d34, self.controller.VENDOR_ID)
        self.assertEqual(0x0004, self.controller.PRODUCT_ID)
        self.assertEqual(
            (0x1F, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x03),
            self.controller.INIT_PACKET1
        )
        self.assertEqual(
            (0x00, 0x01, 0x29, 0x00, 0xB8, 0x54, 0x2C, 0x04),
            self.controller.INIT_PACKET2
        )
        self.assertIsNone(self.controller.device)

    def test_open_without_pylamp(self):
        with patch('usb.core.find', return_value=None) as find_patch:
            self.assertFalse(self.controller.open())
            self.assertFalse(self.controller.is_connected())
            find_patch.assert_called_once_with(
                idVendor=self.controller.VENDOR_ID,
                idProduct=self.controller.PRODUCT_ID
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
                idVendor=self.controller.VENDOR_ID,
                idProduct=self.controller.PRODUCT_ID
            )
            device.is_kernel_driver_active.assert_called_once_with(0)
            device.detach_kernel_driver.assert_called_once_with(0)
            device.set_configuration.assert_called_once_with()
            self.assertIsInstance(self.controller.device, usb.core.Device)
            device.is_kernel_driver_active.return_value = False
            self.assertIsInstance(self.controller.open(), Controller)

    def test_send_with_error(self):
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 1
        self.controller.device = device
        self.assertFalse(self.controller.send('test'))
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
        self.controller.device = device
        self.assertTrue(self.controller.send(111))
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
        self.controller.device = device
        self.controller.prepare()
        assert device.ctrl_transfer.mock_calls == [
            call(
                usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                0x09,
                0x81,
                0x00,
                self.controller.INIT_PACKET1,
                100
            ),
            call(
                usb.TYPE_CLASS + usb.RECIP_INTERFACE,
                0x09,
                0x81,
                0x00,
                self.controller.INIT_PACKET2,
                100
            )
        ]

    def test_set_color_with_error(self):
        self.assertRaises(TypeError, self.controller.set_color, 'test')

    def test_set_color(self):
        color = Color('cyan')
        device = Mock(spec=usb.core.Device)
        device.ctrl_transfer.return_value = 8
        self.controller.device = device
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
        self.controller.device = device
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
        self.controller.device = device
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
        self.controller.device = device
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
