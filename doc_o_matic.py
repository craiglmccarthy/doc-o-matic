#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Doc-o-matic -
Automated production of MARC 21 skeleton records from pdf documents.
"""

import os
import shutil
import tkinter as tk
from tkinter import font

import requests
from PIL import Image, ImageTk

from doc_func import join_marc_records, open_marc_folder, submission
from doc_output import output_to_marc, output_to_text
from doc_regex import doc_regex
from doc_req import document_request

# Create GUI window.
root = tk.Tk()
root.title('DOC-O-MATIC')
root.geometry('900x900')
root.resizable(0, 0)

# Create menu.
menu = tk.Menu(root)
root.config(menu=menu)

# Add submenus to menu.
sub_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=sub_menu)
sub_menu.add_command(label='MARC Records Folder', command=open_marc_folder)
sub_menu.add_command(label='Join MARC records',
                     command=lambda: join_marc_records(output_text))
sub_menu.add_separator()
sub_menu.add_command(label='Close', command=root.quit)

# Uses PIL to convert image to a Tkinter appropriate format.
image = Image.open(r'.\assets\doc_o_matic.png')
photo = ImageTk.PhotoImage(image)

# =============================================================================
# Top frame.
top_frame = tk.Frame(root, bg='#fff')
top_frame.place(relwidth=1, height=150)

# Doc-o-matic logo.
label = tk.Label(top_frame, image=photo, borderwidth=0)
label.image = photo  # keep a reference!
label.place(x=10, y=10)

# Separator.
separator = tk.Frame(root, bg='lightblue')
separator.place(y=110, relwidth=1, height=10)

# =============================================================================
# Middle frame.
entry_frame = tk.Frame(root, bg='#fff')
entry_frame.place(y=120, relwidth=1, height=85)

# Enter URL label.
url = tk.Label(entry_frame, text='Enter the URL of the document:', bg='#fff',
               font=('Courier New', 12))
url.place(x=25, y=10)

# URL entry.
url_entry = tk.Entry(entry_frame, width=80)
url_entry.place(x=25, y=50)
url_entry.bind('<KeyPress-Return>',
               (lambda event: submission(url_entry.get(), output_text,
                                         document_request, output_to_text,
                                         output_to_marc, doc_regex)))

# URL submit button.
submit_button = tk.Button(entry_frame, text='SUBMIT',
                          bg='#fff', font=('Courier New', 10),
                          command=lambda: submission(url_entry.get(),
                                                     output_text,
                                                     document_request,
                                                     output_to_text,
                                                     output_to_marc, doc_regex))
submit_button.place(x=525, y=45)

# =============================================================================
# Bottom frame.
bottom_frame = tk.Frame(root, bg='#fff')
bottom_frame.place(y=205, relwidth=1, relheight=0.8)

# Output label.
output = tk.Label(bottom_frame, text='Output:', bg='#fff',
                  font=('Courier New', 12))
output.place(x=25, y=10)

# Output text field.
output_text = tk.Text(bottom_frame, bg='lightgrey', padx=5)
output_text.place(x=20, y=50, width=860, height=600)

# Main loop of GUI.
root.mainloop()
