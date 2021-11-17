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
└──Your_download_file_name
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
