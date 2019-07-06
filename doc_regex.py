#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re


def doc_regex(document_input):
    '''
    Uses regular expressions to match key data in order to later build MARC
    record.
    '''

    # Matches the document number / date / title / issued date.
    re_1 = r'(\w+\s+\w+)\s(\d+)/(\d+)\s+([^.]+)Issued\s+((\d+\s+)?(\w+)\s(\d+))'
    re_1 = re.compile(re_1)
    re_1 = re_1.search(document_input)

    # If matches found, assign to variables, else assign placeholder string.
    if re_1 is not None:
        doc_num = re_1.group(2)
        doc_year = re_1.group(3)

        doc_title = re_1.group(4)
        doc_title = doc_title[0].upper() + doc_title[1:].lower().rstrip()

        # Lists of words to either capitalize or title.
        terms_to_cap = ['uk', 'r&d', 'hmrc', ]
        terms_to_title = ['january', 'february', 'march', 'april', 'may',
                          'june', 'july', 'august', 'september', 'october',
                          'november', 'december']

        # Apply capitalization or titling based on lists above.
        formatted_title = []
        for item in doc_title.split():
            if item.lower() in terms_to_cap:
                formatted_title.append(item.upper())
            elif item.lower() in terms_to_title:
                formatted_title.append(item.title())
            else:
                formatted_title.append(item)

        doc_title = ' '.join(formatted_title) + '.'

        # Assigns a non-filing indicator value.
        if doc_title.startswith('The '):
            non_filing = 4
        elif doc_title.startswith('A '):
            non_filing = 2
        elif doc_title.startswith('An '):
            non_filing = 3
        else:
            non_filing = 0

        doc_iss_day = re_1.group(6)
        doc_iss_month = re_1.group(7)
        doc_iss_year = re_1.group(8)

    else:
        doc_num = ' DNF! '
        doc_year = ' DNF! '
        doc_title = ' DNF! '
        doc_iss_day = ' DNF! '
        doc_iss_month = ' DNF! '
        doc_iss_year = ' DNF! '
        non_filing = ' DNF! '

    # =========================================================================
    # Matches 'welcomes the...'.
    re_2 = r'wel[^.]*(on|to)(the)?\s([^.]*)pub\w+([^.]*)(by([^.]*))?(on|in)\s+(\d+\s)?(\w+)\s+(\d{4})'
    re_2 = re.compile(re_2)
    re_2 = re_2.search(document_input)

    # If matches found, assign to variables, else assign placeholder string.
    if re_2 is not None:
        welcomes = re_2.group()
    else:
        welcomes = ' DNF! '

    # =========================================================================
    # Matches 'this response of...'.
    re_3 = r'\w+\sres\w+\s+\w+\s+(\d+)\s(\w+)\s+(\d{4})\s[^.]*\.'
    re_3 = re.compile(re_3)
    re_3 = re_3.search(document_input)

    # If matches found, assign to variables, else assign placeholder string.
    if re_3 is not None:
        this_res = re_3.group()

        # Uses the above regular expression to assign value to field_710.
        if 'x1' in this_res:
            field_710 = 'AUTHOR 1'
        elif 'x2' in this_res:
            field_710 = 'AUTHOR 2'
        elif 'x3' in this_res:
            field_710 = 'AUTHOR 3'
        elif 'x4' in this_res:
            field_710 = 'AUTHOR 4'
        elif 'x5' in this_res:
            field_710 = 'AUTHOR 5'
        elif 'x6' in this_res:
            field_710 = 'AUTHOR 6'
        else:
            field_710 = ' DNF! '

    else:
        this_res = ' DNF! '
        field_710 = ' DNF! '

    # Time data.
    now = datetime.datetime.now()
    date_field_008 = now.strftime("%d%m%y")
    time_field_590 = now.strftime("%Y%m%d")
    time_field_856 = now.strftime("%B %Y")

    return (doc_num, doc_year, doc_title, non_filing, doc_iss_day,
            doc_iss_month, doc_iss_year, welcomes, this_res, field_710,
            date_field_008, time_field_590, time_field_856)
