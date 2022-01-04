#!/usr/bin/env python
# coding: utf-8

import os
import hashlib
import numpy as np
import pandas as pd

def calculate_md5(fpath, chunk_size=1024 * 1024):
    md5 = hashlib.md5()
    with open(fpath, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def get_deleted_paths(path):
    df_file = pd.DataFrame(columns=['path', 'md5', 'date'])
    
    for root, dirs, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            df_file.loc[len(df_file)] = [file_path, calculate_md5(file_path), os.path.getctime(file_path)]
            
    df_file = df_file.sort_values(by=['date'], axis=0)
    new_df = df_file.drop_duplicates(['md5'])
    delete_df = df_file.loc[~df_file.index.isin(new_df.index), :]
    delete_df = delete_df.reset_index(drop=True)
    
    return delete_df['path'].values

# path need to modify by require
deleted_paths = get_deleted_paths(r'D:\weixin_files\WeChat Files\wxid_7zmt2fls7n8y31\FileStorage\File')
for i in deleted_paths:
    os.remove(i)


