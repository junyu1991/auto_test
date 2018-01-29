#!encoding:utf-8

import os
import datetime

import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def save_img(url):
    r=requests.get(url,stream=True)
    file_name=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    dirs=os.path.join(os.curdir,"temp")
    if not os.path.exists(dirs):
        print("Make dirs:%s" % dirs)
        os.makedirs(dirs)

    file_name=os.path.join(dirs,file_name)
    print("Saving img to:%s" % file_name)

    with open(file_name,'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            f.write(chunk)

    return file_name

def save_img(url,connection):
    '''
    Save img to the disk,use requests.session() to connect url to get data.
    '''
    r=connection.get(url,stream=True)
    file_name=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    dirs=os.path.join(os.curdir,"temp")
    if not os.path.exists(dirs):
        print("Make dirs:%s" % dirs)
        os.makedirs(dirs)

    file_name=os.path.join(dirs,file_name)
    print("Saving img to:%s" % file_name)

    with open(file_name,'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            f.write(chunk)

    return file_name

def show_img(img_path):
    if os.path.exists(img_path):
        lena=mpimg.imread(img_path)
        lean.shape
        plt.imshow(lena)
        plt.axis('off')
        plt.show()
    else:
        print("Img not exists!!")
        

def show_rand_img(img_url):
    rand_img=save_img(img_url)
    show_img(img_path)
    #del img on the disk
