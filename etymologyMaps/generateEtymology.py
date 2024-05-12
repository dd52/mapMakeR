from etymapDicts import countryCodes
import json
import os.path
import sys
import requests
import urllib
from bs4 import BeautifulSoup

def filter_dict(data, strPos):
    '''Filter the wiktionary data'''
    word = data[strPos:strPos + 20]
    characters_to_replace = [
        "\\n*",
        " F",
        "}}",
        "}",
        "\\n",
        "\\",
        "{{",
        "{{t"
    ]

    for char in characters_to_replace:
        word = word.replace(char, "")

    return word.split("|")[2]

def get_wiktionary_data(word):
    '''Get data from Wiktionary API'''
    encoded_word = urllib.parse.quote(word)
    userUrl = f"https://en.wiktionary.org/w/api.php?action=query&titles={word}" \
              f"&prop=revisions&rvprop=content&rvslots=main&format=json"

    with urllib.request.urlopen(userUrl) as url:
        data = json.loads(url.read().decode())
        return str(data["query"]["pages"])

def create_dictionary_file(word, words):
    '''Create or write to a new dictionary txt file'''
    cond = "r+" if os.path.isfile(f"generated/dictionary_{word}.txt") else "x"
    with open(f"generated/dictionary_{word}.txt", cond) as f:
        for key, value in words.items():
            if key != "ukr":
                f.write(f"{key}, {value},grey\n")
            else:
                f.write(f"{key}, {value},grey")

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Please enter a word.")
            sys.exit()

        word = sys.argv[1].lower()
        pages = get_wiktionary_data(word)

        words = {}
        for key, code in countryCodes.items():
            teststr = f"{{t+|{code}"
            strPos = pages.find(teststr)

            if strPos != -1:
                filteredStr = filter_dict(pages, strPos)
                words[key] = filteredStr

            teststr2 = f"{{t|{code}|"
            strPos2 = pages.find(teststr2)

            if strPos2!= -1:
                filteredStr2 = filter_dict(pages, strPos2)
                words[key] = filteredStr2

            if key not in words:
                words[key] = "?"

        create_dictionary_file(word, words)

    except urllib.error.URLError:
        print("Error: Failed to connect to the Wiktionary API.")
    except json.JSONDecodeError:
        print("Error: Failed to parse the JSON response from the Wiktionary API.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
