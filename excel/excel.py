import pandas as pd


def read_sheet(path: str) -> pd.DataFrame:
    return pd.read_excel(path)
