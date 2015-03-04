# Ticketbuild
Build a large PDF of numbered tickets using a ticket image template. The output is a pdf in order to make it easier when
printing.

The output pdf-pagesize will be 3508x4960(A3 at 300ppi) pixels in size.

## Usage:
The usage is simply straightforward .. 

```
python ticketbuilder.py -h
```

for more details about the options you have to supply to the script.

## Sample-usage
The sample below will output 300 tickets (numbered 0..300) using test_ticket.png (which have a size of 600x300), using a offset
for the numerations of (100,100) (from the left corner of test_ticket.png).

```
python ticketbuild.py -n 300 -w 600 -x 100 -y 100 -t test_ticket.png
```

## Needed to build
You need to have the following libraries:

* PIL (image library for python)
* reportlab (pdf library for python)
