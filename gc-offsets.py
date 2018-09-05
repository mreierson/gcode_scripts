#!/usr/bin/python
#
# Re-cast g-code with new offset and speeds
#
import sys
import re

if __name__ == '__main__':

    f = open(sys.argv[1])

    power = 0
    travel_speed = 3000
    burn_speed = 500

    xoffset = 68
    yoffset = 42
        
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
                    if sline.startswith('G00'):

                        xr = re.search('X(.+?) ', sline)
                        if xr:
                            newx = xoffset + float(xr.group(1))

                        yr = re.search('Y(.+?) ', sline)
                        if yr:
                            newy = yoffset + float(yr.group(1))

                        print 'G0 X' + str(newx) + ' Y' + str(newy) + ' F' + str(travel_speed)                  
                    else:
                        if sline.startswith('G03'):

                            xr = re.search('X(.+?) ', sline)
                            if xr:
                                newx = xoffset + float(xr.group(1))

                            yr = re.search('Y(.+?) ', sline)
                            if yr:
                                newy = yoffset + float(yr.group(1))

                            print 'G03 X' + str(newx) + ' Y' + str(newy) + ' ' + sline[sline.index('I'):]
                        else:
                            print sline

