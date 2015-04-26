import Image
import settings


def color_to_hex(rgb):
  return '#%02x%02x%02x' % rgb[:3]


def get_color_palete(path, color_count=10, tolerance=1):
  img = Image.open(settings.IMG_ROOT+'\\'+path)
  historam = get_histogram(img)
  colors = [(color_to_hex(color), count) for color, count in find_dominant_colors(historam, color_count, tolerance)]
  return dict(colors=colors, filename=path, count=color_count, tolerance=tolerance, status="ok")


def get_histogram(img):
  colors = {}
  for pix in list(img.getdata()):
    colors[pix] = colors.get(pix, 0) + 1
  return sorted(colors.items(), key=lambda x: x[1], reverse=True)


def find_dominant_colors(histogram, colors_count=10, tolerance=1):
  colors = []
  for color, count in histogram[:100*colors_count]:
    if _is_color_unique(color, colors, tolerance=tolerance):
      colors.append((color, count))
  return colors[:colors_count]


def _is_color_unique(color, histogram, tolerance=1):
  for c, count in histogram:
    if abs(c[0]+c[1]+c[2] - (color[0]+color[1]+color[2])) <= tolerance:
      return False
  return True
