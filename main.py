import pandas as pd
import json
from tqdm import tqdm
from util import file_iterator
import argparse
import os
import glob

def get_args_parser():
    parser = argparse.ArgumentParser('Data Annotation', add_help=False)

    # choose model version
    parser.add_argument('--path', default=0, type=str)

    return parser

def main(args):
    # we will make two csv files. One for dataset and the other for mutual check
    answer_check = pd.DataFrame()
    dataset = pd.DataFrame()

    # append names of all files under plain and ann folder
    ann_folder_path = os.path.join(args.path, 'ann.json\\master\\pool')
    html_folder_path = os.path.join(args.path, 'plain.html\\pool')
    legend_path = os.path.join(args.path, 'annotations-legend.json')
    file_names = glob.glob(ann_folder_path + '\\*.json')
    for i in range(len(file_names)):
        file_names[i] = file_names[i].split('.txt')[0].split('\\')[-1]

    # get legend
    with open(legend_path, encoding='utf-8') as json_file:
        legend = json.load(json_file)

    for file_name in tqdm(file_names):
        temp_dataset, temp_answer_check = file_iterator(file_name, ann_folder_path, html_folder_path, legend)
        answer_check = pd.concat([answer_check, temp_answer_check], axis=0)
        dataset = pd.concat([dataset, temp_dataset], axis=0)

    answer_check.to_csv('answer_check.csv',encoding='utf-8-sig')
    dataset.to_csv('dataset.csv',encoding='utf-8-sig')

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Annotation', parents=[get_args_parser()])
    args = parser.parse_args()
    main(args)