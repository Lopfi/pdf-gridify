from PyPDF2 import PdfReader, PdfWriter, PaperSize, PageObject, Transformation
from PyPDF2.generic import AnnotationBuilder
import math

print("Welcome to the PDF combiner!")
print("This program will combine all the Pages of a PDF into less pages, so you can print them on a single page.")
print("The PDF should be formatted in a way that the pages are in the correct order, and the pages should be the same size.")
input_file = input("Enter the path to your file: ")
lines = input("Do you want the pages to be separated by lines? (y/n): ")

A4_w = PaperSize.A4.width
A4_h = PaperSize.A4.height

reader = PdfReader(open(input_file, 'rb'))
output = [PageObject.create_blank_page(width=A4_w, height=A4_h)]

x = 0
y = 0

dx = math.ceil(reader.pages[0].mediabox.width)
dy = math.ceil(reader.pages[0].mediabox.height)

for i, page in enumerate(reader.pages):
    progress = (i+1/len(reader.pages))/100
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress * 100 + 1), end="", flush=True)
    page.cropbox.upper_right = (A4_w, A4_h)
    page.add_transformation(Transformation().translate(x, y))
    output[-1].merge_page(page)

    x = x + dx
    if x + dx >= output[-1].mediabox.width:
        y = y + dy
        x = 0
        if y + dy >= output[-1].mediabox.height:
            output.append(PageObject.create_blank_page(width=A4_w, height=A4_h))
            y = 0


writer = PdfWriter()
for page in output:
    writer.add_page(page)

    if lines == "n":
        continue
    # draw divider lines
    for x in range(0, round(A4_w), dx):
        writer.add_annotation(len(writer.pages) - 1, AnnotationBuilder().rectangle(
            rect=(x, 0, dx, round(A4_h)),
        ))

    for y in range(0, round(A4_h), dy):
        writer.add_annotation(len(writer.pages) - 1, AnnotationBuilder().rectangle(
            rect=(0, y, round(A4_w), dy),
        ))

with open('out.pdf', 'wb') as f:
    writer.write(f)

print("\n\nDone! Saved to out.pdf")
