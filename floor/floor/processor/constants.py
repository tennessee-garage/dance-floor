from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Maximum value for any component color in a pixel. As currently defined,
# colors have a 10-bit range of `[0, 1023]`
COLOR_MAXIMUM = 1023

WHITE = (COLOR_MAXIMUM, COLOR_MAXIMUM, COLOR_MAXIMUM)
BLACK = (0, 0, 0)

# Maximum value of a ranged input.
RANGED_INPUT_MAX = 127
