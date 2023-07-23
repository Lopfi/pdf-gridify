import os

from PyPDF2 import PdfReader, PdfWriter, PaperSize, PageObject, Transformation
import math
import shutil

from util import generate_lines

print("Welcome to the PDF combiner!")
print("This program will combine all the Pages of a PDF into less pages, so you can print them on a single page.")
print(
    "The PDF should be formatted in a way that the pages are in the correct order, and the pages should be the same size.")
input_file = input("Enter the path to your file: ")
lines = input("Do you want the pages to be separated by lines? (y/n): ")

if lines == "y":
    generate_lines(input_file)
else:
    shutil.copyfile(input_file, 'temp.pdf')

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

reader = PdfReader(open('temp.pdf', 'rb'))
output = [PageObject.create_blank_page(width=A4_w, height=A4_h)]

x = safe
y = safe

dx = round(reader.pages[0].mediabox.width)
dy = round(reader.pages[0].mediabox.height)

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

os.remove("temp.pdf")

print("\n\nDone! Saved to out.pdf and out_lines.pdf")
