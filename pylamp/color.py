class Color:
    '''
    This class define a color by his red, green and blue
    '''
    MAX_VALUE = 0x40
    red = None
    green = None
    blue = None

    def __init__(self, red: int=None, green: int=None, blue: int=None):
        '''
        Initiliaze color
        '''
        self.set(red, green, blue)

    def set(self, red, green: int=None, blue: int=None):
        '''
        Set new color value
        :param mixed red:
        :param int green:
        :param int blue:
        '''
        if isinstance(red, str) and green is None and blue is None:
            if red[0] in ('#', '_'):
                return self.__from_hex(red)
            return self.__from_string(red)

        if red is None:
            red = 0
        if green is None:
            green = 0
        if blue is None:
            blue = 0

        self.red = self.__get_value(red)
        self.green = self.__get_value(green)
        self.blue = self.__get_value(blue)

    def __get_value(self, value: int) -> int:
        '''
        Get value, if value is higher than the max value
        return self.MAX_VALUE, else, if lower than 0,
        return 0.
        '''
        return min(max(0, int(value)), self.MAX_VALUE)

    def __from_hex(self, string: str):
        '''
        Convert hexadecimal string to color
        '''
        string = string.lstrip('#_')

        if len(string) not in (3, 6):
            raise ValueError('Wrong length for hexadecimal string')

        if len(string) == 6:
            return self.set(
                int(string[0:2], 16),
                int(string[2:4], 16),
                int(string[4:6], 16)
            )
        return self.set(
            int(string[0:1]*2, 16),
            int(string[1:2]*2, 16),
            int(string[2:3]*2, 16)
        )

    def __from_string(self, string: str):
        '''
        Convert simple string to color
        Available values:
        - red
        - green
        - blue
        - white
        - magenta
        - cyan
        - yellow
        '''
        if string == 'red':
            return self.set(self.MAX_VALUE, 0, 0)
        elif string == 'green':
            return self.set(0, self.MAX_VALUE, 0)
        elif string == 'blue':
            return self.set(0, 0, self.MAX_VALUE)
        elif string == 'white':
            return self.set(self.MAX_VALUE, self.MAX_VALUE, self.MAX_VALUE)
        elif string == 'magenta':
            return self.set(self.MAX_VALUE, 0, self.MAX_VALUE)
        elif string == 'purple':
            return self.set(
                self.MAX_VALUE / 2,
                self.MAX_VALUE / 2,
                self.MAX_VALUE / 2
            )
        elif string == 'cyan':
            return self.set(0, self.MAX_VALUE, self.MAX_VALUE)
        elif string == 'yellow':
            return self.set(self.MAX_VALUE, self.MAX_VALUE, 0)
        else:
            return self.set(0, 0, 0)
