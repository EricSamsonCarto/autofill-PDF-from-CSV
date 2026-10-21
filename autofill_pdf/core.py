import os
import re

import pandas as pd
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject


def fill_pdfs(df_or_csv, pdf_template, output_filename, colkey=None, checkbox_fields=None, output_loc=None):
    """Create one filled PDF per row of a DataFrame or CSV.
    Column names must match the form field names in the PDF template.

    Args:
        df_or_csv (DataFrame or path): input data, a pandas DataFrame or a path to a CSV file.
        pdf_template (path): fillable PDF to use as the template.
        output_filename (str): base name of the output files, e.g. "Form" gives "Form_1.pdf".
        colkey (str, optional): column whose values name each file instead of the row number.
            Values must be unique, otherwise files are overwritten.
        checkbox_fields (list or comma-separated str, optional): columns that fill checkbox fields.
            Checkboxes not listed here are left untouched.
        output_loc (path, optional): directory for the output folder. Defaults to the template's directory.

    Returns:
        The folder the PDFs were written to.
    """
    if isinstance(checkbox_fields, str):
        checkbox_fields = [f.strip() for f in checkbox_fields.split(',') if f.strip()]
    checkbox_fields = set(checkbox_fields or [])

    # dtype=str keeps ZIP codes like 02134 and stops ints turning into 12345.0
    df = pd.read_csv(df_or_csv, dtype=str) if isinstance(df_or_csv, (str, os.PathLike)) else df_or_csv

    template_stem = os.path.splitext(os.path.basename(pdf_template))[0]
    output_stem = os.path.splitext(output_filename)[0]
    out_folder = os.path.join(output_loc or os.path.dirname(pdf_template), f'{template_stem}_AUTOFILLOUTPUT')
    os.makedirs(out_folder, exist_ok=True)

    template_fields = PdfReader(pdf_template).get_fields() or {}
    button_fields = {k for k, v in template_fields.items() if v.get('/FT') == '/Btn'}

    for row_number, row in enumerate(df.to_dict('records'), start=1):
        values = {k: str(v) for k, v in row.items() if pd.notnull(v)}
        text_values = {k: v for k, v in values.items() if k not in button_fields and k not in checkbox_fields}
        checkbox_values = {k: v if v.startswith('/') else f'/{v}' for k, v in values.items() if k in checkbox_fields}

        writer = PdfWriter(clone_from=pdf_template)
        writer.set_need_appearances_writer(True)
        for page in writer.pages:
            writer.update_page_form_field_values(page, text_values, auto_regenerate=False)
            set_checkboxes(page, checkbox_values)

        key = values.get(colkey) if colkey else None
        file_id = re.sub(r'[\\/:*?"<>|]', '_', key) if key else str(row_number)
        writer.write(os.path.join(out_folder, f'{output_stem}_{file_id}.pdf'))

    return out_folder


def set_checkboxes(page, values):
    """Set checkbox /V and /AS so the box shows checked (or /Off) in every viewer."""
    for annot in page.get('/Annots') or []:
        annot = annot.get_object()
        name = annot.get('/T') or annot.get('/Parent', {}).get('/T')
        if name in values:
            state = NameObject(values[name])
            annot[NameObject('/V')] = state
            annot[NameObject('/AS')] = state
