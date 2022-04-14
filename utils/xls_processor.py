# -*- coding: utf-8 -*-
"""Class to process xls/xlsx files."""


__all__ = ['XLSXProcessor']


import os

import pandas as pd


class XLSXProcessor(object):
    """Define the static class to process xls/xlsx files."""
    @staticmethod
    def open(path, index, header):
        file = pd.read_excel(path, index, header=header)
        return file

    @staticmethod
    def fetch_data(path, index=0, header=0):
        if not os.path.exists(path):
            raise FileExistsError(f'{path} does not exists.')
        file = XLSXProcessor.open(path, index, header)
        return file.to_dict('index')

    @staticmethod
    def save(path, dfs, sheet_names=None):
        """Save the dict with keys as the COLUMNs."""
        if not isinstance(dfs, list):
            dfs = [dfs]
        with pd.ExcelWriter(path) as writer:
            for i, df in enumerate(dfs):
                if not isinstance(df, pd.DataFrame):
                    df = pd.DataFrame(df)
                if sheet_names is None:
                    sheet_name = f'Sheet{i+1}'
                else:
                    sheet_name = sheet_names[i]
                df.to_excel(writer, sheet_name=sheet_name)
