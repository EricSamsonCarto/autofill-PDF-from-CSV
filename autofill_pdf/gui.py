import os
import tkinter
import tkinter.filedialog

import eel

from .core import fill_pdfs


def ask(dialog, **kwargs):
    root = tkinter.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    return dialog(**kwargs)


@eel.expose
def btn_csv_click():
    return ask(tkinter.filedialog.askopenfilename, title='Select file', filetypes=(('CSV Files', '*.csv'),))


@eel.expose
def btn_pdf_click():
    return ask(tkinter.filedialog.askopenfilename, title='Select file', filetypes=(('PDF Files', '*.pdf'),))


@eel.expose
def btn_folder_click():
    return ask(tkinter.filedialog.askdirectory)


@eel.expose
def csv_to_pdf(csv, pdf_template, output_loc, output_filename, colkey=None, checkbox_fields=None):
    try:
        fill_pdfs(csv, pdf_template, output_filename, colkey, checkbox_fields, output_loc or None)
        eel.finished()
    except Exception as e:
        eel.error(f'{type(e).__name__}: {e}')


def main():
    eel.init(os.path.join(os.path.dirname(__file__), 'web'))
    eel.start('index.html', size=(600, 700))


if __name__ == '__main__':
    main()
