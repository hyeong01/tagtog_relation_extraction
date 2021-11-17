# tagtog_relation_extraction
- for making Tagtog annotation into csv dataset

## How to Use
### On Tagtog
**1. Go to Project > Downloads** </br>
**2. Download all documents, using the button below**
![Image](https://i.imgur.com/dmruuVo.png)
### On Local
**1. Place folders and files according to the structure specified below:**
```
tagtog_relation_extraction
├──main.py
├──util.py
├──.gitignore
├──README.md
├──requirements.txt
└──Your_download_file_Name
   ├──annotations-legend.json
   ├──ann.json
   |  └──master
   |     └──pool/
   ├──plain.html
   |  └──pool/
   ├──guidelines.md
   └──README.md
```
**2. Install other required packages**
  - tqdm==4.62.3
  - pandas==1.1.5
  - beautifulsoup4==4.10.0

```
$ pip install -r $ROOT/tagtog_relation_extraction/requirements.txt
```
**3. Run**
```
$ python main.py --path Your_download_file_Name
```

### Result

**1. Dataset file (dataset.csv)
- csv file with row
```
sentence: '가장 가능성이 높은 새 대안은 플랑크 상수를 통해 질량을 정의하는 방안이다.질량의 단위는 킬로그램 외에도 여러가지가 있는데, 그중 대표적인 단위가 바로 원자질량단위이다'
sub_tag: "{'word': '원자질량단위', 'start_idx': 85, 'end_idx': 90, 'type': 'POH'}"
obj_tag: "{'word': '플랑크 상수', 'start_idx': 17, 'end_idx': 22, 'type': 'POH'}"
label: 'POH:no_relation'
```

**2. File for checking answers (answer_check.csv)


