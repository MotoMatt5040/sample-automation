from machine_learning import stratified_split
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
        # plot_batches(landline_batches, stratify_by, source='landline_')
        # plot_batches(cell_batches, stratify_by, source='cell_')

        for i, batch in enumerate(landline_batches):
            batch['BATCH'] = i + 1

        for i, batch in enumerate(cell_batches):
            batch['BATCH'] = i + 1

        self._final_landline = pd.concat(landline_batches).reset_index(drop=True)
        self._final_cell = pd.concat(cell_batches).reset_index(drop=True)

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
        df = df.where(df['CELL'] == 'N').dropna().reset_index(drop=True)
        df = df.where(~df['PHONE'].isin(wdnc)).dropna().reset_index(drop=True)
        df.VTYPE = 1
        self._landline_df = df

    @property
    def cell_df(self):
        return self._cell_df

    @cell_df.setter
    def cell_df(self, df):
        df = df.where(df['CELL'] == 'Y').dropna().reset_index(drop=True)
        df.VTYPE = 2
        df.MD = 1
        self._cell_df = df

    @property
    def final_landline(self):
        return self._final_landline

    @property
    def final_cell(self):
        return self._final_cell


class Baselice:

    def __init__(self, df, stratify_by: list):
        self.data = df
        self.stratify_columns = stratify_by
        self.landline_df = df
        self.cell_df = df
        self.headers = df.columns.to_list()

        landline_batches, cell_batches = self.batchify()
        # plot_batches(landline_batches, stratify_by, source='landline_')
        # plot_batches(cell_batches, stratify_by, source='cell_')

        for i, batch in enumerate(landline_batches):
            batch['BATCH'] = i + 1

        for i, batch in enumerate(cell_batches):
            batch['BATCH'] = i + 1

        self._final_landline = pd.concat(landline_batches).reset_index(drop=True)
        self._final_cell = pd.concat(cell_batches).reset_index(drop=True)

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
        df = df.where(df['STYPE'] == 1).dropna().reset_index(drop=True)
        df = df.where(~df['TELL'].isin(wdnc)).dropna().reset_index(drop=True)
        df.VTYPE = 1
        self._landline_df = df

    @property
    def cell_df(self):
        return self._cell_df

    @cell_df.setter
    def cell_df(self, df):
        df = df.where(df['STYPE'] == 2).dropna().reset_index(drop=True)
        df.VTYPE = 2
        df.MD = 1
        self._cell_df = df

    @property
    def final_landline(self):
        return self._final_landline

    @property
    def final_cell(self):
        return self._final_cell




