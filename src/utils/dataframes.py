from io import BytesIO

import pandas as pd

from models import S3File


def dataframes(file: S3File):
    if file and file.content:
        excel_file = pd.ExcelFile(BytesIO(file.content))
        sheets = {}
        for sheet_name in excel_file.sheet_names:
            sheets[sheet_name] = pd.read_excel(
                BytesIO(file.content), sheet_name=sheet_name
            )
        return sheets
    return None
