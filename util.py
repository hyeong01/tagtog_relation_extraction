import json
import pandas as pd
import warnings
from tqdm import tqdm
from bs4 import BeautifulSoup

# we will make two csv files. One for dataset and the other for mutual check
def file_iterator(file_name, ann_folder_path, html_folder_path, legend):

    with open(f"{html_folder_path}\\{file_name}.txt.plain.html", 'r', encoding="utf-8") as f:
        all = f.read()

    content = all.split('<pre id="s1v1">')[1]
    clean_text = ' '.join(BeautifulSoup(content, "html.parser").stripped_strings)
    len_text = len(clean_text)

    with open(f"{ann_folder_path}//{file_name}.txt.ann.json", encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    relations = json_data['relations']

    # to append to answer check
    temp_answer_check = pd.DataFrame()
    # to append to dataset
    temp_dataset = pd.DataFrame()

    # df for answer check
    ent_s_lst = []
    sub_ent_lst = []
    obj_ent_lst = []
    label_lst = []

    # df for dataset
    clean_s_lst = []
    sub_w_lst = []
    obj_w_lst = []

    for r in relations:
        e1_type = r['entities'][0].split('|')[1]
        e2_type = r['entities'][1].split('|')[1]
        e1_loc_s, e1_loc_e = map(int, r['entities'][0].split('|')[2].split(','))
        e2_loc_s, e2_loc_e = map(int, r['entities'][1].split('|')[2].split(','))
        
        word1 = clean_text[e1_loc_s:e1_loc_e+1]
        word2 = clean_text[e2_loc_s:e2_loc_e+1]
        
        mmax = max(e1_loc_s, e1_loc_e, e2_loc_s, e2_loc_e)
        mmin = min(e1_loc_s, e1_loc_e, e2_loc_s, e2_loc_e)
        start = find_start(mmin, clean_text)
        end = find_end(mmax, len_text, clean_text)

        try:
            origin_s = clean_text[start:end+1]
        except:
            continue

        clean_s = origin_s.lstrip('.').lstrip()
        ent_s = make_ent_sentence(e1_loc_s, e1_loc_e, e2_loc_s, e2_loc_e, e1_type, e2_type, legend, origin_s, start)
        
        #### for dataset
        if origin_s[0:2] == '. ':
            buffer = 2
        elif origin_s[0] == '.' or origin_s[0] == '\n':
            buffer = 1
        else:
            buffer = 0
        
        sub_w, obj_w = create_data(legend, e1_type, e2_type, word1, word2, e1_loc_s, e1_loc_e, e2_loc_s, e2_loc_e, start, buffer)

        #### gather data
        ent_s_lst.append(ent_s)
        sub_ent_lst.append(sub_w['type'])
        obj_ent_lst.append(obj_w['type'])
        label_lst.append(sub_w['type']+':'+legend[e1_type].split('-')[2])
        clean_s_lst.append(clean_s)
        sub_w_lst.append(sub_w)
        obj_w_lst.append(obj_w)

    temp_dataset['sentence'] = clean_s_lst
    temp_dataset['subject_entity'] = sub_w_lst
    temp_dataset['object_entity'] = obj_w_lst
    temp_dataset['label'] = label_lst

    temp_answer_check['sentence'] = ent_s_lst
    temp_answer_check['sub_tag'] = sub_ent_lst
    temp_answer_check['obj_tag'] = obj_ent_lst
    temp_answer_check['label'] = label_lst

    return temp_dataset, temp_answer_check

### helper functions below:
def find_start(idx, clean_text):
    
    for i in range(idx, -1, -1):
        if i == 0:
            return i
        elif clean_text[i] == '.' or clean_text[i] == '\n':
            return i
    
def find_end(idx, len_text, clean_text):

    for i in range(idx, len_text):
        if i == len_text:
            return i
        elif clean_text[i] == '.' or clean_text[i] == '\n':
            return i-1

def make_ent_sentence(e1_loc_s, e1_loc_e, e2_loc_s, e2_loc_e, e1_type, e2_type, legend, origin_s, start):

    if e1_loc_s < e2_loc_s:
        s1, s2 = e1_loc_s, e2_loc_s
        e1, e2 = e1_loc_e, e2_loc_e
        ent1 = legend[e1_type].split('-')[0]
        ent2 = legend[e2_type].split('-')[0]

    else:
        s1, s2 = e2_loc_s, e1_loc_s
        e1, e2 = e2_loc_e, e1_loc_e
        ent1 = legend[e2_type].split('-')[0]
        ent2 = legend[e1_type].split('-')[0]

    result = f'{origin_s[:s1-start]}<{ent1} {origin_s[s1-start:e1-start+1]}>{origin_s[e1+1-start:s2-start]}<{ent2} {origin_s[s2-start:e2-start+1]}>{origin_s[e2-start+1:]}'.lstrip('.').lstrip()

    return result

def create_data(legend, e1_type, e2_type, word1, word2, e1_loc_s, e1_loc_e, e2_loc_s, e2_loc_e, start, buffer):
    ent1 = legend[e1_type].split('-')[0]
    ent2 = legend[e2_type].split('-')[0]
    
    word_dict1 = dict()
    word_dict2 = dict()

    word_dict1['word'] = word1
    word_dict2['word'] = word2

    word_dict1['start_idx'], word_dict1['end_idx'] = e1_loc_s-start-buffer, e1_loc_e-start-buffer
    word_dict2['start_idx'], word_dict2['end_idx'] = e2_loc_s-start-buffer, e2_loc_e-start-buffer

    word_dict1['type'] = legend[e1_type].split('-')[1]
    word_dict2['type'] = legend[e2_type].split('-')[1]

    if ent1 == 'SUBJ' and ent2 == 'OBJ':
        return word_dict1, word_dict2
    elif ent1 == 'OBJ' and ent2 == 'SUBJ':
        return word_dict2, word_dict1
    else:
        warnings.warn('Not a Rightful Enttitiy Marking')