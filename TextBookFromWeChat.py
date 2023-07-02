# -*- coding: utf-8 -*-
import os, sys
import json
import requests
import time,datetime
import re
import codecs
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
 
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
rootUrl = "mp.weixin.qq.com"

header1 = {
    'Host':rootUrl,
    'Connection':'keep-alive',
    'User-Agent':userAgent
}

def __getWebHtml(url):
    if url:
        data = requests.get(url=url, headers = header1)
        return data.text
    return ""
 
def images_to_pdf(img_files, out_pdf):
   #create a list of Image objects
   images = []
   for img_file in img_files:
        img = Image.open(img_file).convert("RGB")
        images.append(img)
   #save the images as a single .pdf file
   if images:
      images[0].save(out_pdf, save_all =True, append_images=images[1:], quality=100)

def write_img2file(file_path,img):
    with open(file_path, 'wb') as fd:
        fd.write(img)

def write_imgFromUrl(imgs_url):
    num = 0
    imgs_file = []
    for idx,img_url in enumerate(imgs_url, 1):
        img = requests.get(img_url).content
        im = Image.open(BytesIO(img))
        #支持竖直的书
        if im.width < im.height:
            num += 1
            file_path = os.path.join('{0:05d}.jpg'.format(num))
            write_img2file(file_path,img)
            imgs_file.append(file_path)
    return imgs_file; 

def GetTextBookFromWeChat(url):
    #1.获得网站内容
    html = __getWebHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all(lambda x:x.has_attr('data-src') and x.name=='img')
    imgs_url = [imgs[i]['data-src'] for i in range(len(imgs))]
    imgs_file = write_imgFromUrl(imgs_url)
    #create one pdf
    pdf_path = os.path.join('1.pdf')
    images_to_pdf(imgs_file, pdf_path)
    #删除图片
    for img_file in imgs_file:
        os.remove(img_file)

if __name__ == "__main__":
    url="https://mp.weixin.qq.com/s/XYftHjVBbfr0DGYK-8TGQw"
    GetTextBookFromWeChat(url)