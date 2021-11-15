from collections import defaultdict
import json 
import glob
from os import path
import argparse
import gc
import pandas as pd
import os

def main(files_dir, output_dir):
    all_name_frames = []
    all_last_names_frames = []

    for filepath in glob.glob(path.join(files_dir,'*.csv')):
        if filepath.endswith('.'):
            continue

        country_code = filepath[-6:-4]

        print(f"Processing: {filepath}...")

        csvfile = pd.read_csv(filepath, names=['name', 'surname', 'sex', 'country'])
        
        country_names = csvfile[['name', 'sex']].copy().groupby(['name', 'sex'], as_index=False).size()
        country_surnames = csvfile[['surname']].copy().groupby('surname', as_index=False).size()

        curr_output_dir = path.join(output_dir, country_code)
        os.makedirs(curr_output_dir)
        country_names.to_csv(path.join(curr_output_dir, 'names.csv'), index=False)
        country_surnames.to_csv(path.join(curr_output_dir, 'last_names.csv'), index=False)

        all_name_frames.append(country_names)
        all_last_names_frames.append(country_surnames)

        print(f"Done")
    
    curr_output_dir = path.join(output_dir, 'ALL')
    os.makedirs(curr_output_dir)
    
    all_names_df = pd.concat(all_name_frames, ignore_index=True).groupby(['name', 'sex'], as_index=False).sum().reset_index()
    all_last_names_df = pd.concat(all_last_names_frames, ignore_index=True).groupby('surname', as_index=False).sum().reset_index()

    all_names_df.to_csv(path.join(curr_output_dir, 'names.csv'), index=False)
    all_last_names_df.to_csv(path.join(curr_output_dir, 'last_names.csv'), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyzes database of names')
    # input file, required positional
    parser.add_argument('files_dir', type=str, help='the dir with the names to process')
    parser.add_argument('output_dir', type=str, help='the dir where the output is saved')

    args = parser.parse_args()
    main(args.files_dir, args.output_dir)