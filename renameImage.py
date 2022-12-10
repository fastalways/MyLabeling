import os
import glob

## -------------- CONFIG HERE ---------------------
DIR = "E:/eieie/"
ALLOW_IMAGE_TYPE = ['png','TXt']
## ------------------------------------------------


filenames = []
imagenames = []
for IMAGE_TYPE in ALLOW_IMAGE_TYPE:
    filenames.append(glob.glob(DIR+"*."+IMAGE_TYPE))
    print(IMAGE_TYPE)
    print(len(filenames[len(filenames)-1]))
for names in filenames :
    for name in names:
        imagenames.append(name) 
print(f"ALL Image = {len(imagenames)}")
imagenames.sort()
if(len(imagenames)>0):
    imgpath = os.path.split(imagenames[0])[0]
    split_path=imgpath.split('/')
    if(len(split_path)==1):
        split_path=imgpath.split('\\')
    if(len(split_path)==1):
        split_path=imgpath.split("//")
    folderName = split_path[len(split_path)-1]
    print(f"Rename to -> {folderName}")
for count,imagename in enumerate(imagenames):
    imgpath = os.path.split(imagename)[0]
    imgname = os.path.split(imagename)[1]
    file_extension = os.path.splitext(imgname)[1]
    newname = folderName + "_" + str(count+1).zfill(5) + file_extension
    print(imgpath+"/"+newname)