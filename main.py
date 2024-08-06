from tkinter import filedialog
import pandas as pd
import numpy as np
from tarrance.tarrance import Tarrance



def get_file_path():
    file_path = filedialog.askopenfilename(initialdir=r"I:\PROJ\12880\SAMPLE")
    return file_path


def get_data(file_path: str = None) -> pd.DataFrame:
    if not file_path:
        raise ("File path is required")

    file_type = file_path.split(".")[-1]
    match file_type:
        case 'xlsx':
            print('xlsx')
            return pd.read_excel(file_path)
        case 'xls':
            print('xls')
            return pd.read_excel(file_path)
        case 'csv':
            print('csv')
            return pd.read_csv(file_path)
        case 'txt':
            print('txt')
            return pd.read_csv(file_path, delimiter="\t")
        case _:
            raise f"File type not supported"


def add_headers(df, headers=None, append=True):
    if append:
        if not headers:
            raise ValueError("Header is required")

    return df


path = get_file_path()
df = get_data(path)
df['CALLIDL1'] = ''
df['CALLIDL2'] = ''
df['CALLIDC1'] = ''
df['CALLIDC2'] = ''
df['TFLAG'] = 0
df['VEND'] = 5
df['VTYPE'] = ''
df['MD'] = ''
df['BATCH'] = ''
client_selection = None
while not client_selection:
    print("Select a client:\n[T]arrance\n")
    client_selection = input("Selection: ").upper()
    match client_selection:
        case 'T':
            print("Tarrance selected")
            tarrance = Tarrance(df)
        case _:
            continue
# df = add_headers(df=df, headers=[])
# tarrance = Tarrance(df)
