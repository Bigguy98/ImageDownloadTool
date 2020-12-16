import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import os
import zipfile
from pathlib import Path
import random
import string
import sys
import shutil


# add user-agent to header
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
header = {
    'User-Agent' : user_agent
}
url = ""


def getHostFromUrl(url):
    _str = url[8:]
    host = ""
    if '/' in _str:
        host = url[:8] + _str[:_str.index('/')]
    else:
        host = url
    return host

def downloadImagesFromUrl(url, folder_name):

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    host = getHostFromUrl(url)
    # get all <img> elements
    imgs = soup('img')
    sources = []
    for img in imgs:
        # get src of image
        src = img.get('src') if img.get('src') != None else (img.get('data-src') if img.get('data-src') != None else img.get('data-original'))
        # preprocess src, remove ?......
        # scr can be none
        if src == None:
            continue
        if '?' in src:
            src = src[:src.index('?')]
        # handle different type of href 
        src = src if "https://" in src else ("https:" + src if src[:2] == "//" else host + src)
        sources.append(src)
    
    # print("Number of images: {}".format(len(imgs)))
    for src in sources:
        # print("Downloading image: " + src)
        # split to get image name
        imageName = src.split('/')[-1]
        fhand = open(folder_name + '/' + imageName, 'wb')
        # read image
        try:
            request = urllib.request.Request(src.encode('ascii', 'ignore').decode('ascii'), headers=header)
            img = urllib.request.urlopen(request).read()
            # write image to folder
            fhand.write(img)
        except urllib.error.URLError as error:
            f = open("logs.txt", "a")
            f.write("Downloading image {} with error {} ".format(imageName.encode('ascii', 'ignore').decode('ascii'), error))
            f.close()
        fhand.close()

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        # print("placeholder {}".format(dirs))
        for file in files:
            ziph.write(os.path.join(root, file))

def get_random_folder_name(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("created random name {}".format(result_str))
    return result_str


if __name__ == "__main__":
    # get arguments
    args = sys.argv
    url = args[1]
    # print("DOWNLOADING IMAGES FROM URL {}".format(url))
    # create folder with random name
    rdName = get_random_folder_name(7)
    Path(rdName).mkdir(parents=True, exist_ok=True)
    # download images from url to folder
    downloadImagesFromUrl(url, rdName)
    # zip images folder
    zipf = zipfile.ZipFile("rars/" + rdName + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(rdName, zipf)
    zipf.close()
    # remove folder after zip
    shutil.rmtree(rdName)
    print(rdName+ ".zip")
