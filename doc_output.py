#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import tkinter as tk

from pymarc import Field, Record


def output_to_text(output_text, doc_year, doc_num, non_filing, doc_title,
                   doc_iss_year, num_pages, welcomes, this_res, date_field_008,
                   time_field_590, field_710, time_field_856, url_entry):
    '''Outputs bibliographic data in text format to text field.'''
    output_text.insert(
        tk.INSERT, f'''
MARC 21 -

080  |  |  657 {doc_year}{doc_num}
110  |2 |  COMPANY
245  |1{str(non_filing)}|  {doc_title}
260  |  |  London : |bCOMPANY, |c{doc_iss_year}
300  |  |  {str(num_pages)} pages
336  |  |  text |2rdacontent
337  |  |  unmediated |2rdamedia
338  |  |  volume |2rdacarrier
490  |  |  COMPANY ; |v{doc_num}/{doc_year}
500  |  |  {welcomes}... {this_res}
590  |  |  {time_field_590}
650  |  |
650  |  |
710  |2 |  {field_710}
710  |2 |  COMPANY
830  |  |  COMPANY
856  |  |  In {time_field_856} available at : |u{url_entry}''')


def output_to_marc(output_text, doc_year, doc_num, non_filing, doc_title,
                   doc_iss_year, num_pages, welcomes, this_res, date_field_008,
                   time_field_590, field_710, time_field_856, url_entry):
    '''
    Outputs data in MARC format via PyMARC. Field 999 includes a random number
    generator to get around the problem of the LMS needing unique item ids.
    '''
    record = Record()
    record.add_field(
        Field(
            tag='000',
            data='im  0c',
        ))
    record.add_field(
        Field(
            tag='008',
            data=f'{date_field_008}n                      000 0 eng u',
        ))
    record.add_field(
        Field(
            tag='080',
            indicators=[' ', ' '],
            subfields=[
                'a', f'657 {doc_year}{doc_num}',
            ]))
    record.add_field(
        Field(
            tag='110',
            indicators=['2', ' '],
            subfields=[
                'a', 'COMPANY',
            ]))
    record.add_field(
        Field(
            tag='245',
            indicators=['1', f'{str(non_filing)}'],
            subfields=[
                'a', f'{doc_title}',
            ]))
    record.add_field(
        Field(
            tag='260',
            indicators=[' ', ' '],
            subfields=[
                'a', 'London : ',
                'b', 'COMPANY, ',
                'c', f'{doc_iss_year}',
            ]))
    record.add_field(
        Field(
            tag='300',
            indicators=[' ', ' '],
            subfields=[
                'a', f'{str(num_pages)} pages',
            ]))
    record.add_field(
        Field(
            tag='336',
            indicators=[' ', ' '],
            subfields=[
                'a', 'text |2rdacontent',
            ]))
    record.add_field(
        Field(
            tag='337',
            indicators=[' ', ' '],
            subfields=[
                'a', 'unmediated |2rdamedia',
            ]))
    record.add_field(
        Field(
            tag='338',
            indicators=[' ', ' '],
            subfields=[
                'a', 'volume |2rdacarrier',
            ]))
    record.add_field(
        Field(
            tag='490',
            indicators=[' ', ' '],
            subfields=[
                'a', 'COMPANY ; ',
                'v', f'{doc_num}/{doc_year}',
            ]))
    record.add_field(
        Field(
            tag='500',
            indicators=[' ', ' '],
            subfields=[
                'a', f'"{welcomes}... {this_res}"',
            ]))
    record.add_field(
        Field(
            tag='590',
            indicators=[' ', ' '],
            subfields=[
                'a', f'{time_field_590}',
            ]))
    record.add_field(
        Field(
            tag='650',
            indicators=[' ', ' '],
            subfields=[
                'a', '',
            ]))
    record.add_field(
        Field(
            tag='650',
            indicators=[' ', ' '],
            subfields=[
                'a', '',
            ]))
    record.add_field(
        Field(
            tag='710',
            indicators=['2', ' '],
            subfields=[
                'a', f'{field_710}',
            ]))
    record.add_field(
        Field(
            tag='710',
            indicators=['2', ' '],
            subfields=[
                'a', 'COMPANY',
            ]))
    record.add_field(
        Field(
            tag='830',
            indicators=[' ', ' '],
            subfields=[
                'a', 'COMPANY',
            ]))
    record.add_field(
        Field(
            tag='856',
            indicators=[' ', ' '],
            subfields=[
                'a', f'In {time_field_856} available at : ',
                'u', f'{url_entry}',
            ]))
    record.add_field(
        Field(
            tag='999',
            indicators=[' ', ' '],
            subfields=[
                'a', f'087 {doc_year}{doc_num}',
                'w', 'UDC',
                'c', '1',
                'i', f'{random.randint(1000000000,9999999999)}',
                'l', 'STORE',
                'm', 'COMPANY-LIB',
                'r', 'Y',
                's', 'Y',
                't', 'REFERENCE',
            ]))
    record.add_field(
        Field(
            tag='999',
            indicators=[' ', ' '],
            subfields=[
                'a', f'657 {doc_year}{doc_num}',
                'w', 'UDC',
                'c', '1',
                'i', f'{random.randint(1000000000,9999999999)}',
                'l', 'STORE',
                'm', 'COMPANY-LIB',
                'r', 'Y',
                's', 'Y',
                't', 'LENDING',
            ]))

    # Write MARC file to disk.
    with open(f'.\\marc_files\\marc_{doc_year}-{doc_num}.mrc', 'wb') as out:
        out.write(record.as_marc())
