#!/usr/bin/python
#
# Inlines power settings from single line S command to end of G1
#
import sys
import re

if __name__ == '__main__':

    f = open(sys.argv[1])

    power = 0
    travel_speed = 2400
    burn_speed = 600
    
    for line in f:

        sline = line.strip()
        
        if sline.startswith('M106') or sline.startswith('M3') or sline.startswith('M4'):
            m = re.search('S(.+?)$', sline)
            if m:
                parse_power = float(m.group(1))
                if parse_power < 1.0:
                    parse_power = parse_power * 255
                power = int(parse_power)
        else:
            if sline.startswith('M5'):
                power = 0
            else:
                if sline.startswith('G1'):
                    if (power < 1):
                        print 'G0 ' + sline[3:] + ' F' + str(travel_speed)
                    else:
                        print sline + ' S' + str(power) + ' F' + str(burn_speed)
                else:        
                    print sline + ' F' + str(travel_speed)

