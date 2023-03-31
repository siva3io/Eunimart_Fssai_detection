import pandas as pd
import re
import os
import pickle
import easyocr
import requests
import aiohttp
import asyncio
import tensorflow as tf
import urllib.request
import numpy as np
from PIL import Image
from urllib.request import urlopen
from PIL import Image
from PIL import Image
from io import BytesIO
import cv2
import glob
import easyocr
import pandas as pd
import PIL
from PIL import ImageDraw
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'])


Base_Dir=""

Main_file='bb_beverages.csv'

temp_file=Main_file[:-4]

data = pd.read_csv(Base_Dir+Main_file)



df1 = data[~data['fssai_number'].notna()]
df1.head()
df1.shape
# print(df1)


async def GetFssai2(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                content=await response.read()
                img = Image.open(BytesIO(content))
                results = reader.readtext(img, detail=0, paragraph=False,allowlist='fsaiLcno. 0123456789')
                listToStr = ' '.join([str(i) for i in results])
        #         print(listToStr)
                Fssai_Regex = re.compile(r'\w{3}. \w{2}.\d{14}|\w{3}. \w{2}. \d{14}|\w{3} \w{2} \d{14}|\w{3} \w{2}. \d{14}|w{3}. \w{2} \d{14}|\d{14}')
                Fssai = (Fssai_Regex.findall(listToStr))
        #         print(Fssai)
                if len(Fssai) == 0:
                    print('image doesnot contain fssai number')
                else:
                    return Fssai
                    
            except:
                print('Image Error',url)
    return ''



def GetFssai1(url):
    urllib.request.urlretrieve(url,"exam2.png")
    # img_number = 1 
    reader = easyocr.Reader(['en'])
    im = PIL.Image.open("fsai_1.jpg")
    im = np.array(im)
    results = reader.readtext(im, detail=0, paragraph=False,)
    img_hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    v = cv2.equalizeHist(v)
    hsv_merge = cv2.merge((h,s,v))
    bgr_enh = cv2.cvtColor(hsv_merge, cv2.COLOR_HLS2BGR)
    Image.fromarray(bgr_enh)
    img_hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    clahe = cv2.createCLAHE(clipLimit = 5)
    v = clahe.apply(v)
    # v = cv2.equalizeHist(v)
    hsv_merge = cv2.merge((h,s,v))
    bgr_enh = cv2.cvtColor(hsv_merge, cv2.COLOR_HLS2BGR)
    results = reader.readtext(im, detail=0, paragraph=False,  allowlist='fsaiLcno. 0123456789')

    for i in results:
        if len(i)>10:
            return i
    return ''


# # 

temp_file_urls=temp_file+'CompletedURLS.pickle'
temp_file_rows=temp_file+'CompletedRows.pickle'

if temp_file_urls in os.listdir():
    try:

        with open(temp_file_urls, 'rb') as file:
            # read the list from the file
            completed = pickle.load(file)
        print('Resuming')
        with open(temp_file_rows, 'rb') as file:
            # read the list from the file
            completed_rows = set(pickle.load(file))
        print('Resuming')
        df=pd.read_csv('Updated_'+Main_file)
    except:
        print('Starting')
        completed={}
        completed_rows=set()
        df = pd.DataFrame()
else:
    print('Starting')
    completed={}
    completed_rows=set()
    df = pd.DataFrame()
print(completed,completed_rows)


async def start(df):

    for row in range(len(df1)):

        prod_number = []
        img_url = []
        if row not in completed_rows:
            for urls in df1['image'].iloc[row].strip('[]'):
                fssai_list = []
                if urls not in completed.keys():
                    for url in urls.split(', '):
                        url=url.replace("'",'')
                        print(url)
                        fssai=GetFssai1(url)
                        if fssai=='':
                            fssai=asyncio.run(GetFssai2(url))
                            if fssai!='':
                                fssai_list.append(fssai)
                else:
                    fssai_list=completed[urls]
                completed[urls]=fssai_list
            completed_rows.add(row)

                    
            fssai_list = [item for sublist in fssai_list for item in sublist]
            fssai_list=list(set(fssai_list))
            print(fssai_list)
            prod_number = df1['Sno'].iloc[row]
            df = df.append(pd.DataFrame({'Prod_number(created)': prod_number,'image_url': urls, 'detected_fssai_number': [fssai_list]}), ignore_index=True)
        else:
            print(row,'Record Already Processed')
        with open(temp_file_urls, 'wb') as file:
            # write the list to the file
            pickle.dump(completed, file)
        with open(temp_file_rows, 'wb') as file:
            # write the list to the file
            pickle.dump(list(completed_rows), file)
        
        df.to_csv('Updated_'+Main_file)

asyncio.run(start(df))