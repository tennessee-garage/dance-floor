from controller import Test
import sys

square = int(sys.argv[1])
red = int(sys.argv[2])
green = int(sys.argv[3])
blue = int(sys.argv[4])

leds = []
for s in range(64):
    if s == square:
        leds.append((red, green, blue))
    else:
        leds.append((0, 0, 0))

test = Test()
test.run(leds)
