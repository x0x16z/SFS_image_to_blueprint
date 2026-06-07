from tkinter.messagebox import showinfo
from PIL import Image

bp_start = """
{
  "center": 10.0,
  "parts": [
    """
bp_end = """
  ],
  "stages": [],
  "rotation": 0.0,
  "offset": {
    "x": 0.0,
    "y": 0.0
  },
  "interiorView": true
}
"""


def pixel(x, y, black, scale, L):
    # 0.015625 = 1/64, 减轻了图案质量
    return """{
      "n": "Fuel Tank",
      "p": {
        "x": """ + str((x + 32) * scale) + """,
        "y": """ + str(y * scale) + """
      },
      "o": {
        "x": """ + str(scale * 64) + """,
        "y": """ + str(scale * 64 * L) + """,
        "z": 0.0
      },
      "t": "-Infinity",
      "N": {
        "width_original": 0.015625,
        "width_a": 0.015625,
        "width_b": 0.015625,
        "height": 0.015625,
        "fuel_percent": 0.0
      },
      "T": {
        "color_tex": """ + black + """,
        "shape_tex": "Flat"
      }
    },"""


def colorOf(rgb):
    if rgb[0] * rgb[1] * rgb[2] < 512000:
        return "\"Color_Black\""
    if rgb[0] * rgb[1] * rgb[2] < 4096000:
        return "\"Color_Gray\""
    return "\"_\""


def makeFile(from_, to_, SCALE):
    try:
        image = Image.open(from_)
        pixels = image.load()
        width, height = image.size
        finalResult = ""
        oldRGB = colorOf(pixels[0, 0])  # Oh no python没有强制类型, 编辑器觉得这里的类型是None就警告了
        count = 0

        for x0 in range(width):
            for y0 in range(height):
                rgb = colorOf(pixels[x0, y0])  # Again!

                if y0 == height - 1 or rgb != oldRGB:
                    finalResult += pixel(x0, height - y0 - 1, oldRGB, SCALE, count)
                    oldRGB = rgb
                    count = 0

                if rgb == oldRGB:
                    count += 1
            count = 0

        with open(to_, "w") as f:
            f.write(bp_start + finalResult[:-1] + bp_end)
            showinfo("", "Succeed!")
    except Exception as e:
        showinfo("", "Error: " + str(e))


if __name__ == '__main__':
    # 图像会缩放为原来的几分之一
    SCALE_ = 10

    makeFile("image.png", "Blueprint.txt", 1 / SCALE_)
