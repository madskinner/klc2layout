#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      marks
#
# Created:     03/06/2013
# Copyright:   (c) marks 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

ctrl = {\
	0x0000:"nul", \
	0x0001:"soh", \
	0x0002:"stx", \
	0x0003:"etx", \
	0x0004:"eot", \
	0x0005:"enq", \
	0x0006:"ack", \
	0x0007:"bel", \
	0x0008:"bs", \
	0x0009:"ht", \
	0x000a:"lf", \
	0x000b:"vt", \
	0x000c:"ff", \
	0x000d:"cr", \
	0x000e:"so", \
	0x000f:"si", \
	0x0010:"dle", \
	0x0011:"dc1", \
	0x0012:"dc2", \
	0x0013:"dc3", \
	0x0014:"dc4", \
	0x0015:"nak", \
	0x0016:"syn", \
	0x0017:"etb", \
	0x0018:"can", \
	0x0019:"em", \
	0x001a:"sub", \
	0x001b:"esc", \
	0x001c:"fs", \
	0x001d:"gs", \
	0x001e:"rs", \
	0x001f:"us", \
	0x0020:"␣", \
	0x007f:"del", \
	0x00a0:"nbsp", \
	0x2000:"nqsp", \
	0x2001:"mqsp", \
	0x2002:"ensp", \
	0x2003:"emsp", \
	0x2004:"3/msp", \
	0x2005:"4/msp", \
	0x2006:"6/msp", \
	0x2007:"fsp", \
	0x2008:"psp", \
	0x2009:"thsp", \
	0x200a:"hsp", \
	0x200b:"zwsp", \
	0x200c:"zwnj", \
	0x200d:"zwj", \
	0x200e:"lrm", \
	0x200f:"rlm", \
	0x2028:"lsep", \
	0x2029:"psep", \
	0x202a:"lre", \
	0x202b:"rle", \
	0x202c:"pdf", \
	0x202d:"lro", \
	0x202e:"rlo", \
	0x202f:"nnbsp", \
    0x205f:"mmsp", \
    0x2060:"wj", \
    0x206a:"iss", \
    0x206b:"ass", \
    0x206c:"iafs", \
    0x206d:"aafs", \
    0x206e:"nads", \
    0x206f:"nods"}
combiningChars = [range(0x300, 0x36f), \
                    range(0x483, 0x48a), \
                    range(0x591, 0x5c0), range(0x5c1, 0x5c6), range(0x5c7, 0x5c8), \
                    range(0x610, 0x61b), range(0x64b, 0x660), range(0x6d6, 0x6de), range(0x6df, 0x6e9), range(0x6ea, 0x6ee), range(0x8e4, 0x8ff), \
                    range(0x7eb, 0x7f4) ]
                    #start of range,after end range

