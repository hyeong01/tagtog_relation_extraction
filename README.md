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
main.py
util.py
.gitignore
README.md

Your_download_file_name
├──ann.json
|  └──master
|     └──pool/
|  └──plain.html
|     └──pool/
├──guidelines.md
└──README.md
```
**2. Install other required packages**
  - torch==1.7.1
  - torchvision==0.8.2
  - tensorboard==2.4.1
  - pandas==1.1.5
  - opencv-python==4.5.1.48
  - scikit-learn~=0.24.1
  - matplotlib==3.2.1
  - albumentations==1.0.3

```
$ pip install -r $ROOT/image-classification-level1-30/requirements.txt
```
