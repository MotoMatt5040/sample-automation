from ml.machine_learning import stratified_split
import pandas as pd
from wdnc import wdnc

class Tarrance:

    def __init__(self, df, stratify_by: list):
        self.data = df
        self.stratify_columns = stratify_by
        self.landline_df = df
        self.cell_df = df
        self.headers = df.columns.to_list()

        landline_batches, cell_batches = self.batchify()

        for i, batch in enumerate(landline_batches):
            batch['BATCH'] = i + 1

        for i, batch in enumerate(cell_batches):
            batch['BATCH'] = i + 1

        final_landline = pd.concat(landline_batches).reset_index(drop=True)
        final_cell = pd.concat(cell_batches).reset_index(drop=True)

        final_landline.to_csv('landline.csv', index=False)
        final_cell.to_csv('cell.csv', index=False)

    def batchify(self) -> tuple:
        landline_batches = stratified_split(self.landline_df, self.stratify_columns)
        cell_batches = stratified_split(self.cell_df, self.stratify_columns)
        return landline_batches, cell_batches

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, df):
        self._data = df

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers=None):
        self._headers = headers

    @property
    def landline_df(self):
        return self._landline_df

    @landline_df.setter
    def landline_df(self, df):
        df = df.where(df['cell'] == 'N').dropna().reset_index(drop=True)
        df = df.where(~df['phone'].isin(wdnc)).dropna().reset_index(drop=True)
        df.VTYPE = 1
        self._landline_df = df

    @property
    def cell_df(self):
        return self._cell_df

    @cell_df.setter
    def cell_df(self, df):
        df = df.where(df['cell'] == 'Y').dropna().reset_index(drop=True)
        df.VTYPE = 2
        df.MD = 1
        self._cell_df = df

