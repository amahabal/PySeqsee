import colorsys

def HSVToColorString(h, s, v):
  rgb = ('%02x' % (255.0 * x) for x in colorsys.hsv_to_rgb(h, s, v))
  return '#' + ''.join(rgb)
