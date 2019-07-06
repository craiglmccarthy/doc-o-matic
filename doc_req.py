#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk

import PyPDF2
import requests


def document_request(url_entry, output_text):
    '''
    Requests document, downloads, reads, and parses using regular expressions.
    '''
    try:
        req = requests.get(url_entry)
        req.raise_for_status()

        # Write pdf to file.
        pdf_file = open(r'.\assets\temp.pdf', 'wb')
        for chunk in req.iter_content(100000):
            pdf_file.write(chunk)
        pdf_file.close()

        # Output to text field.
        output_text.delete(1.0, tk.END)
        output_text.insert(
            tk.INSERT, 'Reading...\n' + url_entry + '\n')

        # Open pdf from file to parse.
        pdfFileObj = open(r'.\assets\temp.pdf', 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        # Get page numbers.
        num_pages = pdfReader.numPages

        # Open 1st page.
        pageObj = pdfReader.getPage(0)
        document_output = pageObj.extractText().replace('\n', '')
        pdfFileObj.close()

        return (num_pages, document_output)

    except:
        # Output to text.
        output_text.delete(1.0, tk.END)
        output_text.insert(
            tk.INSERT, 'There was a problem reading the URL.')

        return False
