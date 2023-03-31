import os
import aiohttp
from PIL import Image
from io import BytesIO
import re
import asyncio
import easyocr
import pandas as pd




reader = easyocr.Reader(['en'])


async def GetMyntra(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                content = await response.read()
                img = Image.open(BytesIO(content))
                results = reader.readtext(img, detail=0, paragraph=False, allowlist='myntraMYNTRA')
                listToStr = ' '.join([str(i) for i in results])
                Myntra_Regex = re.compile(r'myntra', re.IGNORECASE)
                matches = Myntra_Regex.findall(listToStr)
                if len(matches) == 0:
                    return False
                else:
                    print('Image contain Myntra')
                    return True
            except:
                print('Image Error',url)
    return False



files=os.listdir()

files=[file for file in files if '.' in file]


for file in files:
    temp_name=file.split('.')[0]
    df=pd.read_csv(file)
    image_cols = df.filter(like="Image")
    df2=pd.DataFrame()
    for column in image_cols:
        for i in range(len(df)):
            resp=asyncio.run(df.loc[column,i])
            if resp:
                df2.appeend({"Image Link":df.loc[column,i]})
    df2.to_csv(temp_name+'links.csv')











reader = easyocr.Reader(['en'])


async def GetMyntra(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                content = await response.read()
                img = Image.open(BytesIO(content))
                results = reader.readtext(img, detail=0, paragraph=False, allowlist='myntraMYNTRA')
                listToStr = ' '.join([str(i) for i in results])
                Myntra_Regex = re.compile(r'myntra', re.IGNORECASE)
                matches = Myntra_Regex.findall(listToStr)
                if len(matches) == 0:
                    return False
                else:
                    print('Image contain Myntra')
                    return True
            except:
                print('Image Error',url)
    return False


files=os.listdir()

files=[file for file in files if '.' in file]


asyncio.run(GetMyntra('https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/11081560/2022/1/27/8a23edc3-6b81-4ad3-909f-32f47a7410c01643280037607MamaearthSustainableUbtanFaceWashwithTurmericSaffronforTanRe5.jpg'))
