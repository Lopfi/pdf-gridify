from PIL import Image, ImageDraw


def generate_lines(w, h, dx, dy):
    # size of image
    canvas = (w, h)

    # rectangles (width, height, left position, top position)
    frames = []
    for x in range(0, w, dx):
        frames.append((1, h, x, 0))

    for y in range(h, 0, -dy):
        frames.append((w, 1, 0, y))

    # init canvas
    img = Image.new('RGBA', canvas, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # draw rectangles
    for frame in frames:
        x1, y1 = frame[2], frame[3]
        x2, y2 = frame[2] + frame[0], frame[3] + frame[1]
        draw.rectangle([x1, y1, x2, y2], outline=(0, 0, 0, 255))

    # save image
    img.save('lines.png')
