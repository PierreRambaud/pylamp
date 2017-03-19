import unittest
from pylamp.color import Color


class ColorTest(unittest.TestCase):
    color = None

    def setUp(self):
        self.color = Color()

    def test_init(self):
        self.assertEqual(0x40, self.color.MAX_VALUE)

    def test_set(self):
        self.color.set(10, 11, 12)
        self.assertEqual(10, self.color.red)
        self.assertEqual(11, self.color.green)
        self.assertEqual(12, self.color.blue)

    def test_set_from_hex(self):
        self.color.set('#112233')
        self.assertEqual(17, self.color.red)
        self.assertEqual(34, self.color.green)
        self.assertEqual(51, self.color.blue)
        self.color.set('_112233')
        self.assertEqual(17, self.color.red)
        self.assertEqual(34, self.color.green)
        self.assertEqual(51, self.color.blue)
        self.color.set('#123')
        self.assertEqual(17, self.color.red)
        self.assertEqual(34, self.color.green)
        self.assertEqual(51, self.color.blue)

    def test_set_from_string(self):
        self.color.set('red')
        self.assertEqual(64, self.color.red)
        self.assertEqual(0, self.color.green)
        self.assertEqual(0, self.color.blue)
        self.color.set('green')
        self.assertEqual(0, self.color.red)
        self.assertEqual(64, self.color.green)
        self.assertEqual(0, self.color.blue)
        self.color.set('blue')
        self.assertEqual(0, self.color.red)
        self.assertEqual(0, self.color.green)
        self.assertEqual(64, self.color.blue)
        self.color.set('white')
        self.assertEqual(64, self.color.red)
        self.assertEqual(64, self.color.green)
        self.assertEqual(64, self.color.blue)
        self.color.set('magenta')
        self.assertEqual(64, self.color.red)
        self.assertEqual(0, self.color.green)
        self.assertEqual(64, self.color.blue)
        self.color.set('cyan')
        self.assertEqual(0, self.color.red)
        self.assertEqual(64, self.color.green)
        self.assertEqual(64, self.color.blue)
        self.color.set('yellow')
        self.assertEqual(64, self.color.red)
        self.assertEqual(64, self.color.green)
        self.assertEqual(0, self.color.blue)
        self.color.set('purple')
        self.assertEqual(32, self.color.red)
        self.assertEqual(32, self.color.green)
        self.assertEqual(32, self.color.blue)
        self.color.set('nothing')
        self.assertEqual(0, self.color.red)
        self.assertEqual(0, self.color.green)
        self.assertEqual(0, self.color.blue)

    def test_set_with_errors(self):
        # Wrong length
        self.assertRaises(ValueError, self.color.set, '#FF')
        # Wrong length
        self.assertRaises(ValueError, self.color.set, '#FFFF')
        # Wrong length
        self.assertRaises(ValueError, self.color.set, '#FFFFF')
        # Invalid hexa
        self.assertRaises(ValueError, self.color.set, '#GGG')

    def test_init_with_color(self):
        c = Color(10, 11, 12)
        self.assertEqual(10, c.red)
        self.assertEqual(11, c.green)
        self.assertEqual(12, c.blue)
