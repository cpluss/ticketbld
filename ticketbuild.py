#/usr/bin/sh python

import sys
import optparse
import os

from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.platypus import Image

# Easy as pie
class PDFDocument:
    def __init__(self, filename, fontsize, imagesize):
        self.width, self.height = (3508, 4960)
        self.canvas = canvas.Canvas(filename, (3508, 4960))
        self.fontsize = fontsize
        self.canvas.setFont('Helvetica', fontsize)
        self.imagesize = imagesize

    def text(self, x, y, s):
        (_,h) = self.imagesize
        self.canvas.drawString(x, self.height - y - h, s)

    def image(self, x, y, filename):
        (_,h) = self.imagesize
        self.canvas.drawImage(filename, x, self.height - y - h)

    def pagebreak(self):
        self.canvas.showPage()
        self.canvas.setFont('Helvetica', self.fontsize)

    def save(self):
        self.canvas.save()


def init_parser(argv):
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("-o", "--output", dest="output", default="out.pdf", help="the output pdf filename")
    parser.add_option("-t", "--ticket", dest="ticket", default="ticket.png", help="the ticket filename")
    parser.add_option("-x", "--xoffset", dest="x_offset", default="0", help="the x-offset where the number should be put on the ticket")
    parser.add_option("-y", "--yoffset", dest="y_offset", default="0", help="the y-offset where the number should be put on the ticket")
    parser.add_option("-w", "--width", dest="width", default="0", help="the width of the ticket image (in pixels)")
    parser.add_option("-u", "--height", dest="height", default="0", help="the height of the ticket image (in pixels)")
    parser.add_option("-z", "--font_size", dest="font_size", default="42", help="the font size of the numbers")
    parser.add_option("-n", "--number", dest="num", default="300", help="the amount of tickets that should be produced on the pdf")
    parser.add_option("-q", "--quiet", dest="verbose", default=True, action="store_false", help="verbose output on or off (default on)")
    return parser.parse_args(argv)


def main():
    opts, rest = init_parser(sys.argv[1:])

    if opts.width == "0" or opts.height == "0":
        print "You need to set the width and height of the ticket"
        return
    
    # Lets assemble the pdf!
    pdf = PDFDocument(opts.output, fontsize=int(opts.font_size), 
                      imagesize=(int(opts.width), int(opts.height)))

    # Beginning offsets for the images
    x_offset = 0
    y_offset = 0
    i = 0
    end = False

    while i <= int(opts.num) and not end:
        while ((y_offset + int(opts.height)) < pdf.height) and not end:
            while ((x_offset + int(opts.width)) < pdf.width) and not end:
                pdf.image(x_offset, y_offset, opts.ticket)
                pdf.text(x_offset + int(opts.x_offset), y_offset - int(opts.y_offset), str(i))
                x_offset += int(opts.width)
                i += 1
                if i > int(opts.num):
                    end = True

            x_offset = 0
            y_offset += int(opts.height)

        if not end:
            pdf.pagebreak()
        x_offset = 0
        y_offset = 0


    print "Done generating %s tickets, saving to '%s' ..." % (opts.num, opts.output)
    pdf.save()


if __name__=='__main__':
    main()
