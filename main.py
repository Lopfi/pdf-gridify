from PyPDF2 import PdfReader, PdfWriter, PaperSize, PageObject, Transformation
import fitz
import math

from util import generate_lines

print("Welcome to the PDF combiner!")
print("This program will combine all the Pages of a PDF into less pages, so you can print them on a single page.")
print(
    "The PDF should be formatted in a way that the pages are in the correct order, and the pages should be the same size.")
input_file = input("Enter the path to your file: ")
lines = input("Do you want the pages to be separated by lines? (y/n): ")

A4_w = PaperSize.A4.width
A4_h = PaperSize.A4.height

w = round(A4_w)
h = round(A4_h)

safe = 0
useSafe = input("Do you want to use the safe area? (y/n): ")
if useSafe == "y":
    w = w - 30
    h = h - 30
    safe = 15

reader = PdfReader(open(input_file, 'rb'))
output = [PageObject.create_blank_page(width=A4_w, height=A4_h)]

x = safe
y = safe

dx = math.ceil(reader.pages[0].mediabox.width)
dy = math.ceil(reader.pages[0].mediabox.height)

generate_lines(w, h, dx, dy, safe)

for i, page in enumerate(reader.pages):
    progress = (i + 1 / len(reader.pages)) / 100
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress * 100 + 1), end="", flush=True)
    page.cropbox.upper_right = (A4_w, A4_h)
    page.add_transformation(Transformation().translate(x, y))
    output[-1].merge_page(page)

    x = x + dx
    if x + dx >= output[-1].mediabox.width - safe:
        y = y + dy
        x = safe
        if y + dy >= output[-1].mediabox.height - safe:
            output.append(PageObject.create_blank_page(width=A4_w, height=A4_h))
            y = safe

writer = PdfWriter()
for page in output:
    writer.add_page(page)

with open('out.pdf', 'wb') as f:
    writer.write(f)

if lines == "y":
    generate_lines(w, h, dx, dy, safe)
    # define the position (upper-right corner)
    image_rectangle = fitz.Rect(0, 0, w, h)
    file_handle = fitz.open('out.pdf')
    for page in file_handle:
        page.insert_image(image_rectangle, filename='lines.png')

    file_handle.save('out_lines.pdf')

print("\n\nDone! Saved to out.pdf and out_lines.pdf")
