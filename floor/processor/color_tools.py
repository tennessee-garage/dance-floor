import random

def add_color(color1, color2):
    return (color1[0]+color2[0], color1[1]+color2[1], color1[2]+color2[2])

def scale_color(color, scale):
    return (scale*color[0], scale*color[1], scale*color[2])

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#palettes as hex strings
palettes = {
    'rainbow_bunny': ['f9c80e', 'f86624', 'f86624', 'ea3546', '662e9b', '43bccd'],
    'new_mexico': ['004777', 'a30000', 'ff7700', 'efd28d', '00afb5'],
    'desert': ['ff9f1c', 'ffbf69', 'ffffff', 'cbf3f0', '2ec4b6'],
    'druids': ['483c46', '3c6e71', '70ae6e', 'beee62', 'f4743b'],
    'autumn': ['8ea604', 'f5bb00', 'ec9f05', 'd76a03', 'bf3100'],
    'unicorns': ['dec5e3', 'cdedfd', 'b6dcfe', 'a9f8fb', '81f7e5'],
    'linoleum': ['d33f49', 'd7c0d0', 'eff0d1', '77ba99', '806c89']
}
palette_keys = palettes.keys()
palletes_length = len(palette_keys)

def get_palette(name, max_value):
    hexList = palettes[name]
    return [scale_color(hex_to_rgb(s), max_value/256) for s in hexList]

def get_random_palette(max_value):
    idx = random.randint(0, palletes_length-1)
    name = palette_keys[idx]
    print idx, name
    return get_palette(name, max)
