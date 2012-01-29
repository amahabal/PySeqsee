import colorsys

def HSVToColorString(hue, saturation, value):
  rgb = ('%02x' % (255.0 * x) for x in colorsys.hsv_to_rgb(hue, saturation, value))
  return '#' + ''.join(rgb)
