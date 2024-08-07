import traceback
import pandas as pd

from machine_learning import stratified_split
from wdnc import wdnc
from datetime import date


class Tarrance:

    def __init__(self, df: pd.DataFrame, stratify_by: list):
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
        df = df[df['CELL'] == 'N']
        df = df[~df['PHONE'].isin(wdnc)]
        df.loc[:, 'VTYPE'] = 1
        df = df.reset_index(drop=True)
        self._landline_df = df

    @property
    def cell_df(self):
        return self._cell_df

    @cell_df.setter
    def cell_df(self, df):
        df = df[df['CELL'] == 'Y']
        df.loc[:, 'VTYPE'] = 2
        df.loc[:, 'MD'] = 1
        df = df.reset_index(drop=True)
        self._cell_df = df

    @property
    def final_landline(self):
        return self._final_landline

    @property
    def final_cell(self):
        return self._final_cell


class Baselice:

    def __init__(self, df: pd.DataFrame, stratify_by: list):
        try:
            # print(df.head().to_string())
            self.data = df
            self.stratify_columns = stratify_by
            self.landline_df = df
            self.cell_df = df
            self.headers = df.columns.to_list()
            # print(self.landline_df.head().to_string())
            # print(self.cell_df.head().to_string())


            landline_batches, cell_batches = self.batchify()
        except Exception as e:
            print(traceback.format_exc(), e)
        # plot_batches(landline_batches, stratify_by, source='landline_')
        # plot_batches(cell_batches, stratify_by, source='cell_')

        for i, batch in enumerate(landline_batches):
            batch['BATCH'] = i + 1

        for i, batch in enumerate(cell_batches):
            batch['BATCH'] = i + 1

        self._final_landline = pd.concat(landline_batches).reset_index(drop=True)
        self._final_cell = pd.concat(cell_batches).reset_index(drop=True)

    def batchify(self) -> tuple:
        landline_batches = stratified_split(self.landline_df, self.stratify_columns, n=20)
        cell_batches = stratified_split(self.cell_df, self.stratify_columns, n=20)
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
        df.to_csv('landline.csv', index=False)
        df = df[df['STYPE'] == '1']
        df = df[~df['TEL'].isin(wdnc)]
        df.loc[:, 'VTYPE'] = 1
        df = df.reset_index(drop=True)
        self._landline_df = df

    @property
    def cell_df(self):
        return self._cell_df

    @cell_df.setter
    def cell_df(self, df):
        df = df[df['STYPE'] == '2']
        df.loc[:, 'VTYPE'] = 2
        df.loc[:, 'MD'] = 1
        df = df.reset_index(drop=True)
        self._cell_df = df

    @property
    def final_landline(self):
        return self._final_landline

    @property
    def final_cell(self):
        return self._final_cell


class I360:

    def __init__(self, df: pd.DataFrame, stratify_by: list, source: str):
        try:
            df['PHONE'] = df['PHONE'].str.strip()
            df['CELL PHONE'] = df['CELL PHONE'].str.strip()

            df.loc[(df['PHONE'] != '') & (df['CELL PHONE'] == ''), 'SOURCE'] = 1
            df.loc[(df['CELL PHONE'] != '') & (df['PHONE'] == ''), 'SOURCE'] = 2
            df.loc[(df['PHONE'] != '') & (df['CELL PHONE'] != ''), 'SOURCE'] = 3

            df['IAGE'] = date.today().year - df['BIRTH YEAR'].astype(int)
            df.loc[df['IAGE'] > 99, 'IAGE'] = 99

            party_mapping = {
                'Republican': 1,
                'R': 1,
                'Democrat': 2,
                'D': 2,
                'Unaffiliated/Non-Partisan': 3,
                'I': 3,
                'Decline to State': 3
            }

            df['PRTY'] = df['PARTY'].map(party_mapping).fillna(4).astype(int)

            # df['REGN'] =

            df.to_csv('i360.csv', index=False)
            self.stratify_columns = stratify_by
            self.set_df(df, source)
            self.headers = df.columns.to_list()

            batches = self.batchify()

            for i, batch in enumerate(batches):
                batch['BATCH'] = i + 1

            self._final_df = pd.concat(batches).reset_index(drop=True)
        except Exception as e:
            print(traceback.format_exc(), e)

    def batchify(self) -> tuple:
        final_batches = stratified_split(self.df, self.stratify_columns, n=5)
        return final_batches

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers=None):
        self._headers = headers

    @property
    def df(self):
        return self._df

    def set_df(self, df, source):
        if source == 'LANDLINE':
            df = df[~df['PHONE'].isin(wdnc)]
            df.loc[:, 'VTYPE'] = 1
        elif source == 'CELL':
            df.loc[:, 'VTYPE'] = 2
            df.loc[:, 'MD'] = 1
        df = df.reset_index(drop=True)
        self._df = df

    @property
    def final_df(self):
        return self._final_df


