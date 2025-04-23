"""
Helper functions to make color manipulations easier
"""

from __future__ import division

import math
import random
from builtins import range

from floor.processor.constants import BLACK, COLOR_MAXIMUM, WHITE


def remap(x, oldmin, oldmax, newmin, newmax):
    """
    Remap the float x from the range oldmin-oldmax to the range newmin-newmax

    Does not clamp values that exceed min or max.
    For example, to make a sine wave that goes between 0 and 256:
        remap(math.sin(time.time()), -1, 1, 0, 256)

    """
    zero_to_one = (x - oldmin) / (oldmax - oldmin)
    return zero_to_one * (newmax - newmin) + newmin


def clamp(x, minn, maxx):
    """
    Restrict the float x to the range minn-maxx."""
    return max(minn, min(maxx, x))


def cos(x, offset=0, period=1, minn=0, maxx=1):
    """
    A cosine curve scaled to fit in a 0-1 range and 0-1 domain by default.

    offset: how much to slide the curve across the domain (should be 0-1)
    period: the length of one wave
    minn, maxx: the output range

    """
    value = math.cos((x / period - offset) * math.pi * 2) / 2 + 0.5
    return value * (maxx - minn) + minn


def contrast(color, center, mult):
    """
    Expand the color values by a factor of mult around the pivot value of center.

    color: an (r, g, b) tuple
    center: a float -- the fixed point
    mult: a float -- expand or contract the values around the center point

    """
    r, g, b = color
    r = (r - center) * mult + center
    g = (g - center) * mult + center
    b = (b - center) * mult + center
    return r, g, b


def clip_black_by_luminance(color, threshold):
    """
    If the color's luminance is less than threshold, replace it with black.

    color: an (r, g, b) tuple
    threshold: a float

    """
    r, g, b = color
    if r + g + b < threshold * 3:
        return 0, 0, 0
    return r, g, b


def clip_black_by_channels(color, threshold):
    """
    Replace any individual r, g, or b value less than threshold with 0.

    color: an (r, g, b) tuple
    threshold: a float

    """
    r, g, b = color
    if r < threshold:
        r = 0
    if g < threshold:
        g = 0
    if b < threshold:
        b = 0
    return r, g, b


def mod_dist(a, b, n):
    """
    Return the distance between floats a and b, modulo n.

    The result is always non-negative.
    For example, thinking of a clock:
    mod_dist(11, 1, 12) == 2 because you can "wrap around".

    """
    return min((a - b) % n, (b - a) % n)


def gamma(color, gamma_val):
    """
    Apply a gamma curve to the color.  The color values should be in the range 0-1.
    """
    r, g, b = color
    return max(r, 0) ** gamma_val, max(g, 0) ** gamma_val, max(b, 0) ** gamma_val


def add_color(color1, color2):
    return color1[0] + color2[0], color1[1] + color2[1], color1[2] + color2[2]


def scale_color(color, scale):
    return scale * color[0], scale * color[1], scale * color[2]


def hex_to_rgb(value):
    """Given an RGB hex value, returns a 3-tuple scaled to COLOR_MAXIMUM."""
    value = value.lstrip("#")
    lv = len(value)
    hex_values = (value[i : i + lv // 3] for i in range(0, lv, lv // 3))
    raw_color = tuple(int(v, 16) for v in hex_values)
    return scale_color(raw_color, COLOR_MAXIMUM / 255.0)


# palettes as hex strings
palettes = {
    "rainbow_bunny": ["31cb00", "f9c80e", "f86624", "f86624", "ea3546", "662e9b", "43bccd"],
    "new_mexico": ["004777", "a30000", "ff7700", "efd28d", "00afb5"],
    "desert": ["ff9f1c", "ffbf69", "ffffff", "cbf3f0", "2ec4b6"],
    "druids": ["483c46", "3c6e71", "70ae6e", "beee62", "f4743b"],
    "autumn": ["8ea604", "f5bb00", "ec9f05", "d76a03", "bf3100"],
    "unicorns": ["dec5e3", "cdedfd", "b6dcfe", "a9f8fb", "81f7e5"],
    "linoleum": ["d33f49", "d7c0d0", "eff0d1", "77ba99", "806c89"],
    "wedding1": ["f8aeaa", "abaab2", "f5927b"],
    "rygw": ["ff0000", "ffff00", "00ff00", "ffffff"],
}
palette_keys = list(palettes.keys())
palettes_length = len(palette_keys)


def get_palette(name):
    return [hex_to_rgb(c) for c in palettes[name]]


def get_random_palette():
    idx = random.randint(0, palettes_length - 1)
    name = palette_keys[idx]
    return get_palette(name)


def normalize_pixel(pixel):
    r, g, b = pixel[:3]
    if len(pixel) == 4:
        alpha = pixel[3]
    else:
        alpha = 1.0
    return (
        max(0, min(int(r), COLOR_MAXIMUM)),
        max(0, min(int(g), COLOR_MAXIMUM)),
        max(0, min(int(b), COLOR_MAXIMUM)),
        alpha,
    )


def set_brightness(pixel, brightness):
    if brightness == 1.0:
        return pixel
    return tuple(map(lambda x: x * brightness, pixel))


def tint(color, percent):
    """Lighten `color` to white by `percent`"""
    return alpha_blend(WHITE, color, percent)


def shade(color, percent):
    """Lighten `color` to black by `percent`"""
    return alpha_blend(BLACK, color, percent, black_is_transparent=False)


def alpha_blend(pixel_above, pixel_below, alpha, black_is_transparent=True):
    """Blends `pixel_above` onto `pixel_below` with given alpha."""
    pixel_alpha = 1.0
    if len(pixel_above) == 4:
        pixel_alpha = pixel_above[3]
    alpha = alpha * pixel_alpha
    if pixel_above[:3] == (0, 0, 0) and black_is_transparent:
        # We treat black pixels as fully transparent.
        return pixel_below
    elif alpha == 1.0:
        return pixel_above
    elif alpha == 0.0:
        return pixel_below
    else:
        rAbove, gAbove, bAbove = pixel_above[:3]
        rBelow, gBelow, bBelow = pixel_below[:3]

        rOut = alpha * rAbove + (1 - alpha) * rBelow
        gOut = alpha * gAbove + (1 - alpha) * gBelow
        bOut = alpha * bAbove + (1 - alpha) * bBelow

        return normalize_pixel((rOut, gOut, bOut))[:3]
