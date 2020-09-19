"""
24toCodeHackathon

Copyright © 2020 Joy Cross, Kaitlyn Frickensmith, Brenna Levenick, Brandan Naef

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os

# External Packages
try:
    import PySimpleGUI as sg
except ImportError:
    os.system("python -m pip install pysimplegui")
    import PySimpleGUI as sg


def guiWindow():
    layout = [[sg.Text('Select Folder'), sg.Input(disabled=True), sg.FolderBrowse(key='chosen_folder')],
              [sg.Text('')], [sg.Text('                                                                                              '), sg.Button(' Continue -> ', key='Continue')]]
    return sg.Window(title="Select Folder to Upload to the Cloud", layout=layout, size=(500, 100))
