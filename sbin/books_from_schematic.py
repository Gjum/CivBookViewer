'''
Extracts books from a .schematic file and prints them in JSON format.
Installation: python3 -m pip install nbt
Usage: python3 books_from_schematic.py path/to/my.schematic Server_Name
Output example:
{   "source": "Devoted_3",
    "title": "The Navy Seal",
    "signed": "auxchar",
    "generation": "Original",
    "pages": [
        "What the fuck did you just fucking say about me, you little bitch?",
        "I\u2019ll have you know I graduated top of my class in the Navy Seals, and I\u2019ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills.",
        "I am trained in gorilla warfare and I\u2019m the top sniper in the entire US armed forces. You are nothing to me but just another target.",
        "I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words.",
        "You think you can get away with saying that shit to me over the Internet? Think again, fucker.",
        "As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot.",
        "The storm that wipes out the pathetic little thing you call your life. You\u2019re fucking dead, kid.",
        "I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that\u2019s just with my bare hands.",
        "Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it",
        "to its full extent to wipe your miserable ass off the face of the continent, you little shit.",
        "If only you could have known what unholy retribution your little \u201cclever\u201d comment was about to",
        "bring down upon you, maybe you would have held your fucking tongue. But you couldnt, you didn\u2019t, and now you\u2019re paying the price, you goddamn idiot.",
        "I will shit fury all over you and you will drown in it. You\u2019re fucking dead, kiddo."
    ]
}

Created by Gjum
https://github.com/Gjum
'''

import sys
import json
from nbt import nbt
from collections import namedtuple

unknown_te_ids = set()
unknown_item_ids = set()

novalue = namedtuple('novalue', 'value')(None)

generations = {
    0: 'Original',
    1: 'Copy',
    2: 'Copy of Copy',
    3: 'Tattered',
    None: None,
}


def print_json_books_from_schematic(fpath, source_info):
    f = nbt.NBTFile(fpath)
    for te in f['TileEntities']:
        if 'Items' not in te:
            continue  # no container, or contents unknown
        # te_id = te['id'].value
        # if te_id not in ('minecraft:chest', 'minecraft:trapped_chest') \
        #         and te_id not in unknown_te_ids:
        #     unknown_te_ids.add(te_id)
        #     print('Ignoring unexpected block id:', te_id, file=sys.stderr)
        #     continue
        for stack in te['Items']:
            item_id = stack['id'].value
            if item_id not in ('minecraft:written_book', 'minecraft:writable_book') \
                    and item_id not in unknown_item_ids:
                unknown_item_ids.add(te_id)
                print('Ignoring unexpected item id:', item_id, file=sys.stderr)
                continue

            book = {
                'source': source_info,
                'title': stack['tag'].get('title', novalue).value,
                'signed': stack['tag'].get('author', novalue).value,
                'generation': generations[stack['tag'].get('generation', novalue).value],
                'pages': [cleanup_page(page.value) for page in stack['tag']['pages']],
            }
            print(json.dumps(book, separators=(',', ':')))


# This schematic to json book extraction script was created by Gjum. github.com/Gjum


def cleanup_page(in_str):
    wrap_start, wrap_end = '{\"text\":\"', '\"}'
    if not in_str.startswith(wrap_start) or not in_str.endswith(wrap_end):
        return in_str
    # it's json
    j = json.loads(in_str)
    if len(j) > 1:
        print('Unknown keys in page JSON, keeping as JSON:',
              ' '.join(j.keys()), file=sys.stderr)
        return in_str
    return j['text']


if __name__ == "__main__":
    fpath = sys.argv[1]
    source_info = sys.argv[2] if len(sys.argv) > 2 else None
    print_json_books_from_schematic(fpath, source_info)