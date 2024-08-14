import traceback
import pandas as pd

from machine_learning import stratified_split, plot_batches
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

    def get_area_codes(self):
        return self.data['PHONE'].str[:3].value_counts().head(5)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, df):
        df['REGN'] = df['REGN'].astype(str).str.pad(2, fillchar='0')
        df['$N'] = df['PHONE']
        df['SD'] = df['SD'].astype(str).str.pad(2, fillchar='0')
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
        landline_batches = stratified_split(self.landline_df, self.stratify_columns)
        cell_batches = stratified_split(self.cell_df, self.stratify_columns)
        return landline_batches, cell_batches

    def get_area_codes(self):
        return self.data['TEL'].str[:3].value_counts().head(5)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, df):
        if df.get('REGN'):
            if df['REGN'].value_counts().shape[0] > 9:
                df['REGN'] = df['REGN'].astype(str).str.pad(2, fillchar='0')
        df['$N'] = df['TEL']
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

        self.source = source
        self._df = self.initialize_df(df)
        '''
        
        IF 2 or more rows have the same UID (REGARDLESS OF OTHER DATA) -> Delete all except 1 row
        
        AGE <- youngest age first
        FNAME
        LNAME
        PHONE
        GENDER
        PRTY
        
        
        [
            [FNAME, LNAME, GEND, PRTY, IAGE], <- Youngest
            [FNME2, LNME2, GEND2, PRTY2, IAGE2],
            [FNME3, LNME3, GEND3, PRTY3, IAGE3], 
            [FNME4, LNME4, GEND4, PRTY4, IAGE4] <- Oldest
        ]
        
        '''

        if self.source == 'LANDLINE':
            self.household()

        self.stratify_columns = stratify_by
        # self.set_df(df, source)
        self.headers = df.columns.to_list()

        batches = self.batchify()

        for i, batch in enumerate(batches):
            batch['BATCH'] = i + 1

        self._final_df = pd.concat(batches).reset_index(drop=True)
        plot_batches(batches, stratify_by, source='landline_')


    def batchify(self) -> tuple:
        final_batches = stratified_split(self.df, self.stratify_columns)
        return final_batches

    def household(self):
        household_columns = [
            'FNME2', 'LNME2', 'GEND2', 'PRTY2', 'IAGE2',
            'FNME3', 'LNME3', 'GEND3', 'PRTY3', 'IAGE3',
            'FNME4', 'LNME4', 'GEND4', 'PRTY4', 'IAGE4'
        ]
        groups = {
            '2 dupes': pd.DataFrame(),
            '3 dupes': pd.DataFrame(),
            '4 dupes': pd.DataFrame()
        }

        for col in household_columns:
            self.df[col] = ''

        group2 = []
        group3 = []
        group4 = []

        for phone, group in self.df.groupby('PHONE'):
            if len(group) > 1:

                first_index = group.index[0]
                for i, (fname, lname, gend, prty, iage) in enumerate(
                        zip(group['FNAME'][1:], group['LNAME'][1:], group['GEND'][1:], group['PRTY'][1:],
                            group['IAGE'][1:]), start=2):
                    self.df.at[first_index, f'FNME{i}'] = fname
                    self.df.at[first_index, f'LNME{i}'] = lname
                    self.df.at[first_index, f'GEND{i}'] = gend
                    self.df.at[first_index, f'PRTY{i}'] = prty
                    self.df.at[first_index, f'IAGE{i}'] = iage

                if len(group) == 2:
                    group2.append(group.iloc[1:].copy())
                elif len(group) == 3:
                    group3.append(group.iloc[1:].copy())
                elif len(group) == 4:
                    group4.append(group.iloc[1:].copy())

        if group2:
            groups['2 dupes'] = pd.concat(group2)
        if group3:
            groups['3 dupes'] = pd.concat(group3)
        if group4:
            groups['4 dupes'] = pd.concat(group4)

        self._groups = groups

        # Remove the duplicates based on the 'PHONE' column, keeping the first occurrence
        self.df = self.df.drop_duplicates(subset=['PHONE'])

    def get_area_codes(self):
        return self.df['PHONE'].str[:3].value_counts().head(5)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers=None):
        self._headers = headers

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, df):
        self._df = df

    def initialize_df(self, df):
        df = df.copy()
        df['RDATE'] = pd.to_datetime(df['RDATE'], errors='coerce')
        df['RDATE'] = df['RDATE'].dt.strftime('%Y%m%d')

        df['PHONE'] = df['PHONE'].str.strip()
        df['CELL'] = df['CELL'].str.strip()

        df.loc[(df['PHONE'] != '') & (df['CELL'] == ''), 'SOURCE'] = 1
        df.loc[(df['CELL'] != '') & (df['PHONE'] == ''), 'SOURCE'] = 2
        df.loc[(df['PHONE'] != '') & (df['CELL'] != ''), 'SOURCE'] = 3

        df['IAGE'] = date.today().year - df['DOBY'].astype(int)
        df['IAGE'] = df['IAGE'].fillna(0).astype(int)
        df.loc[df['IAGE'] > 99, 'IAGE'] = 99
        df = df.sort_values(by='IAGE', ascending=True)

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

        df['SD'] = df['SD'].astype(str).str.pad(3, fillchar='0')
        df['GCCD20'] = df['GCCD20'].astype(str).str.pad(2, fillchar='0')
        df['GCSSD20'] = df['GCSSD20'].astype(str).str.pad(3, fillchar='0')
        df['GCSHD20'] = df['GCSHD20'].astype(str).str.pad(3, fillchar='0')
        df['GCD22'] = df['GCD22'].astype(str).str.pad(2, fillchar='0')
        df['GSD22'] = df['GSD22'].astype(str).str.pad(3, fillchar='0')
        df['GHD22'] = df['GHD22'].astype(str).str.pad(3, fillchar='0')

        if self.source == 'LANDLINE':
            df['$N'] = df['PHONE']
            # Make a copy of the filtered DataFrame
            df = df[~df['PHONE'].isin(wdnc)].copy()
            df.loc[:, 'VTYPE'] = 1
        elif self.source == 'CELL':
            df['$N'] = df['CELL']
            df.loc[:, 'VTYPE'] = 2
            df.loc[:, 'MD'] = 1

        # Reset index and store the DataFrame
        df = df.reset_index(drop=True)
        return df

    @property
    def final_df(self):
        return self._final_df

    @property
    def groups(self):
        return self._groups


class Householding:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def check_for_duplicates(self):
        ...

    def split_record(self):
        ...
