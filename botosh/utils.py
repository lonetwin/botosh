#!/usr/bin/python

# _wrap_with() and colors code borrowed from fabric's ( https://github.com/fabric/fabric ) colors.py
# Copyright (c) 2009, Christian Vest Hansen and Jeffrey E. Forcier

def _wrap_with(code):

    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')

error   = red
info    = green
prompt  = cyan
data    = magenta

def print_table(rows):
    """print_table(rows)

    Prints out a table using the data in `rows`, which is assumed to be a
    sequence of sequences with the 0th element being the header.
    """

    # - figure out column widths
    widths = [ len(max(columns, key=len)) for columns in zip(*rows) ]

    # - print the header
    header, data = rows[0], rows[1:]
    print(
        ' | '.join( green(format(title, "%ds" % width)) for width, title in zip(widths, header) )
        )

    # - print the separator
    print( '-+-'.join( '-' * width for width in widths ) )

    # - print the data
    for row in data:
        print(
            " | ".join( format(cdata, "%ds" % width) for width, cdata in zip(widths, row) )
            )
