from etymapDicts import countryCodes
import json
import os.path
import sys
import urllib.request
import re

try:
    word = sys.argv[1]

    # Throw word into Wiktionary Json API and hope for the best
    userUrl = f'https://en.wiktionary.org/w/api.php?action=query&titles={word}&prop=revisions&rvprop=content&rvgeneratejson=&format=json'

    with urllib.request.urlopen(userUrl) as url:
        data = str(json.loads(url.read().decode())['query']['pages'])

        words = {}
        for key, code in countryCodes.items():
            teststr = f'{{t+|{code}'
            strPos = (data.find(teststr))

            if strPos != -1:
                # TODO: swap with for loop

                filteredStr = data[strPos:strPos + 20] \
                                  .replace(teststr, '') \
                                  .replace('}', '') \
                                  .replace('|m}', '') \
                                  .replace('|f}', '') \
                                  .replace('|', '') \
                                  .replace('\n', '') \
                                  .replace('*', '') \
                                  .replace(' S', '') \
                                  .replace('{{', '') \
                                  .replace(',', '') \
                                  .replace('\\', '') \
                                  .removesuffix(' ')[:-1]

                words[key] = filteredStr

            # Add ? for words not found
            if key not in words:
                words[key] = '?'

    # Create and or write to new dictionary txt file
    cond = 'r+' if os.path.isfile(f'generated/dictionary_{word}.txt') is True else 'x'
    with open(f'generated/dictionary_{word}.txt', cond) as f:
        # TODO: Swap with for loop
        f.write(str(words).removeprefix('{').removesuffix('}').replace('\'', '').replace(': ', ',').replace(', ', ',grey\n') + ',grey')

except IndexError:
    print("Please enter a word.")
