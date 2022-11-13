# Technics 1210 Platter Strobe Effect (Pimoroni Interstate 75)

An experimental LED matrix display using the [Pimoroni Interstate 75](https://shop.pimoroni.com/products/interstate-75?variant=39443584417875)
controller and a [64x64 MOD75 LED Matrix Panel](https://www.adafruit.com/product/3649) driven using a custom `asyncio` manager.

## Features

TODO

## Requirements

- [Pimoroni Interstate 75](https://shop.pimoroni.com/products/interstate-75?variant=39443584417875) RGB LED matrix controller
- Any compatible 64x64 pixel MOD75 LED matrix panel, such as [AdaFruit 64x64 Matrix](https://www.adafruit.com/product/3649)
- Micro USB (5v/3A) power supply or powered hub

## Usage

Create a Python `virtualenv` and install the [CircUp](https://github.com/adafruit/circup) library manager:

    python -m venv ./venv
    source ./venv/bin/activate
    pip install circup

Connect the Matrix Portal M4 to device and confirm USB device is connected and automatically mounted (e.g. `/media/${USER}/CIRCUITPY`):

    ls /dev/ttyACM0
    ls /media/${USER}/CIRCUITPY

Install project dependencies and libraries using `circup`:

    circup install -r ./requirements.txt

Copy the contents of the `src` directory to the root of your Matrix Portal M4 filesystem (e.g. `/media/${USER}/CIRCUITPY`):

    rsync -rv ./src/ /media/${USER}/CIRCUITPY/
