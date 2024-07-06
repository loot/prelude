#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Read localised message content strings from translations/messages.<lang>.yaml
# files and use them to replace the corresponding strings in prelude.yaml.
import math
import re
import os

import yaml

def get_expected_languages(messages_for_anchor):
    expected_langs = list(messages_for_anchor.keys())

    expected_langs.sort()

    # Move en to be the first language.
    en_index = expected_langs.index('en')
    en = expected_langs.pop(en_index)
    expected_langs.insert(0, en)

    return expected_langs

def get_yaml_string(raw_message_text):
    return yaml.dump(raw_message_text, width=math.inf, allow_unicode=True, default_style="'").strip()

messages_by_lang = {}
for f in os.scandir('translations'):
    match = re.match(r'messages\.([^\.]+)\.yaml', f.name)
    if match:
        lang = match.group(1)
        with open(f.path, encoding='utf8') as input:
            messages_by_lang[lang] = yaml.safe_load(input)

messages = {}
for lang in messages_by_lang:
    for anchor in messages_by_lang[lang]:
        if not anchor in messages:
            messages[anchor] = {}
        messages[anchor][lang] = messages_by_lang[lang][anchor]

lines = []
with open('prelude.yaml', encoding='utf8') as input:
    lines = input.readlines()

    anchor = None
    lang = None
    expected_langs = []
    index = 0
    while index < len(lines):
        match = re.search(r' &([^\s]+)$', lines[index])
        if match != None:
            if expected_langs:
                # Expected more languages than were found in the last anchor,
                # need to go back and append the remaining expected languages.
                print('Expected more languages', anchor, expected_langs)
                exit(1)

            anchor = match.group(1)
            expected_langs = get_expected_languages(messages[anchor])
            print(f'Expecting the following languages for anchor {anchor}: {expected_langs}')
            lang = None

            index += 1
            continue

        match = re.search(r'- lang: ([a-zA-Z_]+)', lines[index])
        if match != None:
            lang = match.group(1)
            expected_lang = expected_langs[0]
            if lang == expected_lang:
                expected_langs.pop(0)
            else:
                print(f'Expected an entry for language {expected_lang}, found entry for language {lang}, inserting the expected language before it')
                match = re.search(r'(\s+)- lang:', lines[index])
                whitespace = match.group(1)

                text = get_yaml_string(messages[anchor][expected_lang])

                new_lang_line = f'{whitespace}- lang: {expected_lang}\n'
                new_text_line = f'{whitespace}  text: {text}\n'

                lines.insert(index, new_text_line)
                lines.insert(index, new_lang_line)

                expected_langs.pop(0)
                expected_langs.pop(0)

                index += 2

            index += 1
            continue

        match = re.search(r' text: \'(.+)\'', lines[index])
        if match != None and anchor and lang:
            # Replace line with a new line for this message
            text = get_yaml_string(messages[anchor][lang])

            lines[index] = re.sub(r' text: \'.+\'', f' text: {text}', lines[index])

        index += 1

with open('prelude.yaml', mode='w', encoding='utf8') as output:
    output.writelines(lines)
