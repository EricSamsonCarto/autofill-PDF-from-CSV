
<p align="center">
  <h2 align="center">AutoFill PDF From CSV</h2>
  <p align="center">
    An eel python application that auto fills a template pdf's form fields, creating one PDF per row of a csv or pandas dataframe<br>
  </p>
</p>

<!-- ABOUT THE PROJECT -->
## Project layout
```
autofill_pdf/
  core.py      # fill_pdfs(): the PDF filling logic
  gui.py       # desktop app (Eel + tkinter file dialogs)
  web/         # front end files for the app
tests/         # pytest tests and a sample fillable PDF
```

## Install
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
The app needs Python with Tk. On macOS with Homebrew Python: `brew install python-tk`.

## App Usage
```bash
python -m autofill_pdf.gui
```
The below gif illustrates how to use it:

<p>
<img src="https://github.com/EricSamsonCarto/Autofill_PDF_FromCSV/blob/master/example.gif" width="55%"/>
</p>
For easier usage, you can download the latest version of the .exe program from the Releases tab, made with pyinstaller.

## Python Usage
```python
from autofill_pdf import fill_pdfs

fill_pdfs(df_or_csv, pdf_template,
          output_filename, colkey=None,
          checkbox_fields=None, output_loc=None)
```

<b>df_or_csv</b> (dataframe or csv path): input data, a pandas dataframe or path to a csv file. CSV values are read as text, so ZIP codes keep leading zeros.<br>
<b>pdf_template</b> (pdf path): fillable PDF to use as the template. Column names must match its form field names.<br>
<b>output_filename</b> (string): base name of the output files, e.g. "Form" gives "Form_1.pdf", "Form_2.pdf".<br>
<b>colkey</b> (string, optional): column whose values name each file instead of the row number. Values must be unique, otherwise files will be overwritten. Rows with a blank value fall back to the row number.<br>
<b>checkbox_fields</b> (list or comma-separated string, optional): columns that fill checkbox fields. Use the checkbox's state name as the value, usually "Yes" or "Off". Checkboxes not listed are left as they are in the template.<br>
<b>output_loc</b> (directory path, optional): where to create the `<template>_AUTOFILLOUTPUT` folder. Defaults to the template's directory.<br>

Returns the output folder path.

## Tests
```bash
pytest
```

### Built With
* [pypdf](https://github.com/py-pdf/pypdf)
* [Pandas](https://pandas.pydata.org/)
* [Eel](https://github.com/samuelhwilliams/Eel)

Website: [EricSamson.com](https://ericsamson.com) <br>
