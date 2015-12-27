#/usr/bin/sh python

import sys
import optparse
import os
import math
from pprint import pprint

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
    parser.add_option("-z", "--font_size", dest="font_size", default="72", help="the font size of the numbers")
    parser.add_option("-n", "--number", dest="num", default="450", help="the amount of tickets that should be produced on the pdf")
    parser.add_option("-w", "--width", dest="width", default="1160", help="the width of the ticket image size")
    parser.add_option("-u", "--height", dest="height", default="580", help="the width of the ticket image size")
    parser.add_option("-q", "--quiet", dest="verbose", default=True, action="store_false", help="verbose output on or off (default on)")
    return parser.parse_args(argv)


def main():
    opts, rest = init_parser(sys.argv[1:])
    
    # Ticket dimensions to perfectly fit a A3
    height = int(opts.height)
    width = int(opts.width)

    pdf = PDFDocument(opts.output, fontsize=int(opts.font_size), 
                      imagesize=(width, height))

    # 3 on the width, ~8.5 on the height (8)
    tickets_per_page = 24.0
    pages_needed = math.ceil(float(opts.num) / tickets_per_page)

    print "Tickets per page: %d" % tickets_per_page
    print "Pages needed: %d" % pages_needed

    # Collect and order the numberings correctly (easier to stack)
    nums = dict()
    i = 0
    while i <= int(opts.num):
        for x in xrange(0, int(pages_needed)):
            if nums.has_key(x):
                nums[x].append(i)
            else:
                nums[x] = [i]
            i += 1

    # Plot the tickets
    for k, ns in nums.iteritems():
        # k = page-number
        # ns = numbering on current page
        # n = current-ticket-index
        n = 0
        for y_offset in xrange(0, pdf.height, height):
            if y_offset + height > pdf.height:
                break

            for x_offset in xrange(0, pdf.width, width):
                if x_offset + width > pdf.width:
                    break

                pdf.image(x_offset, y_offset, opts.ticket)
                pdf.text(x_offset + int(opts.x_offset), y_offset - int(opts.y_offset), str(ns[n]))
                n += 1
        
        if k != (pages_needed - 1):
            pdf.pagebreak()


    print "Done generating %s tickets, saving to '%s' ..." % (opts.num, opts.output)
    pdf.save()


if __name__=='__main__':
    main()
