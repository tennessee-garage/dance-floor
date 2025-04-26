import sys
import logging

from floor.controller import Test

def main():
    test = Test()
    leds = []

    bands = [
        (1023, 0, 0),
        (0, 1023, 0),
        (0, 0, 1023),
        (0, 0, 0),
        (1023, 1023, 0),
        (0, 1023, 1023),
        (1023, 0, 1023),
        (1023, 1023, 1023),
    ]

    for x in range(8):
        for y in range(8):
            mult = y / 8.0
            leds.append([mult * val for val in bands[x]])

    test.run(leds)


if __name__ == "__main__":
    main()
