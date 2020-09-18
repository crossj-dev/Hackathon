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
