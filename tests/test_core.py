import os

import pandas as pd
from pypdf import PdfReader

from autofill_pdf import fill_pdfs

TEMPLATE = os.path.join(os.path.dirname(__file__), 'fixtures', 'form.pdf')


def read_fields(path):
    return {k: v.get('/V') for k, v in PdfReader(path).get_fields().items()}


def test_fills_one_pdf_per_row(tmp_path):
    csv = tmp_path / 'data.csv'
    csv.write_text('Name,Zip,Completed,age\nAda,02134,Yes,36\nBob,,Off,\n')

    out = fill_pdfs(str(csv), TEMPLATE, 'Out.v2', colkey='Name',
                    checkbox_fields='Completed, Language', output_loc=str(tmp_path))

    ada = read_fields(os.path.join(out, 'Out_Ada.pdf'))
    assert ada == {'Name': 'Ada', 'Zip': '02134', 'Completed': '/Yes'}
    bob = read_fields(os.path.join(out, 'Out_Bob.pdf'))
    assert bob['Name'] == 'Bob' and bob['Completed'] == '/Off' and not bob['Zip']


def test_dataframe_input_and_blank_colkey_falls_back_to_row_number(tmp_path):
    df = pd.DataFrame({'Name': [None, 'a/b'], 'Zip': ['1', '2']})

    out = fill_pdfs(df, TEMPLATE, 'Out', colkey='Name', output_loc=str(tmp_path))

    assert sorted(os.listdir(out)) == ['Out_1.pdf', 'Out_a_b.pdf']
    # undeclared checkbox is never touched
    assert read_fields(os.path.join(out, 'Out_1.pdf'))['Completed'] == read_fields(TEMPLATE)['Completed']
