#!/usr/bin/env python
###############################################################################
# This script takes one argument: the name of a file organized in csv format:

# ara, ?, grey
# aze, alman, yellow
# bel, nyametski, blue
# bos, njemacki, blue
# ...

# which is a list of languages, list of words, and corresponding color.
# It will look for the template map 'resources/europe_template.svg'
# and replace the names and colors with the csv's info.
# The colors can be given as hexadecimal (#ff00cc) or common English colour names.
###############################################################################

import os
import sys
import csv
from etymapDicts import basemap_lang_col, colorNames

# If argument not given, load default
try:
    filename = sys.argv[1]
except IndexError:
    print('No user input given')

try:
    svg_file_path = os.path.join(os.path.dirname(__file__),'resources/europe_template.svg')
    with open(svg_file_path, 'r') as theMap:
        with open(filename, "r", encoding='utf8') as theDictionary:

            # Reading files
            theMapSource = theMap.read()
            reader = csv.reader(theDictionary, delimiter=',')

            # Check if the input file has the correct format and columns
            header = next(reader)
            print(header)
            if len(header) != 3:
                print('Invalid input file format. Expected columns: language, word, color')
                sys.exit(1)

            for line in reader:
                # Grabbing language, word, colour
                lang = line[0]
                try:
                    word = line[1].replace('?', '')
                except IndexError:
                    word = ''
                try:
                    color = line[2]
                except IndexError:
                    color = 'grey'

                # Convert English col names to hex
                if color in colorNames:
                    color = colorNames[color]

                # Original map colour to replace (all distinct)
                col = basemap_lang_col[lang]

                # Replace each tag in .svg ($eng etc.) with the word/colour
                theMapSource = theMapSource.replace('${}'.format(lang), word)
                theMapSource = theMapSource.replace('#{}'.format(col), color)

            # Write output map
            outputMap = filename.split('/')[-1]
            outputMap = outputMap.replace('dictionary', 'map').replace('.txt', '.svg')

            with open(outputMap, 'w', encoding='utf8') as theNewMap:
                theNewMap.write(theMapSource)

            print('Output map generated successfully:', outputMap)

except FileNotFoundError:
    print('Input file or SVG template file not found')
except Exception as e:
    print('An error occurred:', str(e))

