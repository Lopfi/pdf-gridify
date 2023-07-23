import os

from PIL import Image, ImageDraw
import fitz


def generate_lines(file):
    file_handle = fitz.open(file)

    w = round(file_handle[0].rect.width)
    h = round(file_handle[0].rect.height)

    # size of image
    canvas = (w, h)

    # init canvas
    img = Image.new('RGBA', canvas, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # draw rectangle
    draw.rectangle([0, 0, w-1, h-1], outline=(0, 0, 0, 255))

    # save image
    img.save('lines.png')

    # define the position (upper-right corner)
    image_rectangle = fitz.Rect(0, 0, w, h)
    for page in file_handle:
        page.insert_image(image_rectangle, filename='lines.png')

    file_handle.save("temp.pdf")
    os.remove("lines.png")

