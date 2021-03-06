# Python script to control USB leds

[![Build Status](https://travis-ci.org/PierreRambaud/pylamp.png?branch=master)](https://travis-ci.org/PierreRambaud/pylamp)

## Supported USB leds:

-  WebMail Notifier with python [Dream Cheeky](http://www.dreamcheeky.com/webmail-notifier)

## Supported python version

This tool was test with python `3.2` and higher.

## Installation

From Pypi

```bash
$ pip install pylamp
```

From Github

```bash
$ git clone https://github.com/PierreRambaud/pylamp.git
$ cd pylamp
$ ./pylamp --help
```

## Usage

```bash
$ pylamp -h
usage: pylamp [-h] [-c COLOR] [-r RED] [-g GREEN] [-b BLUE] [-fi FADEIN]
              [-bl BLINK]

Python script to power the Dreamcheeky USB webmail notifier gadget which is
shipped with windows only software. by Pierre Rambaud
<https://github.com/PierreRambaud/pylamp>

optional arguments:
  -h, --help            show this help message and exit
  -c COLOR, --color COLOR
                        Color as hexadecimal or string (#0000FF or 'blue')
  -r RED, --red RED     Red
  -g GREEN, --green GREEN
                        Green
  -b BLUE, --blue BLUE  Blue
  -fi FADEIN, --fadein FADEIN
                        Fade in effect, delay in second
  -bl BLINK, --blink BLINK
                        Blink effect, delay in second
```

## Troubleshooting

Must be run as root unless the necessary udev rules are set.

Create the file `/etc/udev/rules.d/42-pylamp.rules`

And add this content by replacing `USERNAME` by your username:


```bash
SUBSYSTEM !="usb_device", ACTION !="add", GOTO="datalogger_rules_end"
SYSFS{idVendor} =="1d34", SYSFS{idProduct} =="0004", SYMLINK+="datalogger"
MODE="0666", OWNER="USERNAME", GROUP="root"
LABEL="datalogger_rules_end"
```

## Running tests

Install dependencies:

```bash
$ ./setup.py test
```

To run unit tests:

```bash
$ ./setup.py nosetests
$ # or
$ nosetests
```

To check code style:

```bash
$ ./setup.py flake8
$ # or
$ flake8
```

## License

See [LICENSE.md](LICENSE.md) file
