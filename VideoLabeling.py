import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
from os import listdir,mkdir
from os.path import isfile, join, exists
import tkinter as tk
from tkinter import filedialog as fd
import copy
import re
import pathlib
import subprocess


'''==============  Automatically Folders Listing  ================'''
AutomaticallyFoldersListing = False # True = Auto   / False = Manually

'''  Label Listing  '''
label_name_list = [
    'swimming',
    'drowning',
    'not_swimming',
]

'''  Manually Folders Listing  '''
folder_name_list = [
    ''#'training_images'
]

img_index = 0
folder_name = folder_name_list[0]
dataset_path = './DrowningDetectionDataset/'

'''------------------ Open VDO File ------------------'''
filetypes = (
        ('All Media Files', '*.wav;*.aac;*.wma;*.wmv;*.avi;*.mpg;*.mpeg;*.m1v;*.mp2;*.mp3;*.mpa;*.mpe;*.m3u;*.mp4;*.mov;*.3g2;*.3gp2;*.3gp;*.3gpp;*.m4a;*.cda;*.aif;*.aifc;*.aiff;*.mid;*.midi;*.rmi;*.mkv;*.WAV;*.AAC;*.WMA;*.WMV;*.AVI;*.MPG;*.MPEG;*.M1V;*.MP2;*.MP3;*.MPA;*.MPE;*.M3U;*.MP4;*.MOV;*.3G2;*.3GP2;*.3GP;*.3GPP;*.M4A;*.CDA;*.AIF;*.AIFC;*.AIFF;*.MID;*.MIDI;*.RMI;*.MKV'),
        #('All files', '*.*')
    )
root = tk.Tk()
vdo_filename = fd.askopenfilename(title='Open a vdo',
        initialdir=dataset_path,
        filetypes=filetypes)
root.destroy()

cap = cv.VideoCapture(vdo_filename)
if (cap.isOpened()== False): 
    print("Error -> opening video file!!!")
    print("[[ Please recheck the video file and video codec ]]")
    tk.messagebox.showerror(title="Error in opening vdo", message="Error -> opening video file "+vdo_filename+" !!!\n[[ Please recheck the video file and video codec ]]")
    sys.exit()

VDO_NFRAME = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

if(AutomaticallyFoldersListing):
    folder_name_list = []
    folder_name_list = [ folder for folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, folder)) ]
    folder_name_list.sort()

class cvRect:
    def __init__(self, xywh):
        self.x = xywh[0]
        self.y = xywh[1]
        self.w = xywh[2]
        self.h = xywh[3]
        self.xmin = self.x
        self.ymin = self.y
        self.xmax = self.x + self.w
        self.ymax = self.y + self.h
    def area(self):
        return self.w * self.h
    def tl(self):
        return [self.x,self.y]
    def br(self):
        return [self.x+self.w,self.y+self.h]
    def center(self):
        return [self.x+(self.w//2),self.y+(self.h//2)]
    def xywh(self):
        return  [self.x,self.y,self.w,self.h]

# print("[[[[[   Select Directory   ]]]]]")

'''for i,name in enumerate(folder_name_list):
    print(f'{i} : {name} \n',end='')'''
    #if((i+1)%3==0):
    #    print('') # newline

'''select_folder_id = int(input('\nEnter Number :'))

if(select_folder_id<0 or select_folder_id>=len(folder_name_list)):
    sys.exit()'''


folder_name = os.path.dirname(os.path.abspath(vdo_filename))
vdo_onlyname = os.path.basename(vdo_filename)
vdo_onlyname_excluded_type = os.path.splitext(vdo_onlyname)[0]

#tk.messagebox.showinfo(title="Show Path", message=f"{folder_name} * {vdo_onlyname} * {vdo_onlyname_excluded_type}")

#folder_name = folder_name_list[select_folder_id]
print(f'Fetch image in -> {folder_name}')
img_path = folder_name + '/'
#img_crop_path = dataset_crop_path + folder_name + '/'

'''
list_files = []
list_files = [f for f in listdir(img_path) if isfile(join(img_path, f))]
del_lists = []
for i,fname in enumerate(list_files):
    file_ext = pathlib.Path(fname).suffix
    if(file_ext!='.JPG' and file_ext!='.jpg'and file_ext!='.png' and file_ext!='.PNG' and file_ext!='.bmp' and file_ext!='.BMP'and file_ext!='.jpeg' and file_ext!='.JPEG'):
        del_lists.append(fname) # mark as delete
        #print(file_ext)
for val in del_lists:
    list_files.remove(val)
list_files.sort()

if(len(list_files)<=0):
    print(f"No Image in folder -> {img_path}")
    sys.exit()

print(f"File List ext:{list_files}")'''

print("============= How to use =============")
print("Drag Mouse to crop image")
print("Enter/Spacebar to save cropped box")
print("Del to remove specific cropped boxes in the image")
print("k to remove all boxes in the image")
print("p to remove 1st cropped box in the image")
print("n to remove last cropped box in the image")
print("w or / to select label")
print("Esc to cancel (a) cropped box")
print("←/↑ or a goto previous image")
print("→/↓ or d goto next image")
print("q Exit program")
mouseFirstPoint = [0,0]
mouseLastPoint = [9,9]
mouseFinished = False
mouseDragging = False
lockCropping = 'lock'

selectBoxToDelete = -1

'''GUI Select Delete Specify Label'''
class SimpleSelectBoxDeleteLabel():
    def __init__(self):
        global selectBoxToDelete
        selectBoxToDelete = -1
        self.window = tk.Tk()
        self.window.geometry("600x300")
        self.window.title("Select # number of box to delete!")
        labelShow = tk.Label(self.window, text='Please enter # (number of box to delete)')
        labelShow.config(font=('Helvatical bold',18))
        labelShow.place(x=50, y=40, anchor=tk.NW)
        self.textBox = tk.Text(self.window,height=2,width=18);
        self.textBox.place(x=50, y=110, anchor=tk.NW)
        label = tk.Label(self.window, text='OK')
        label.config(font=('Helvatical bold',20))
        label.bind("<Button-1>",lambda event,text='OK':self.hLabelClickOK(event,text))
        label.place(x=100, y=150, anchor=tk.NW)
        self.window.mainloop()
    def hLabelClickOK(self,event,text):
        global selectBoxToDelete
        try:
            inp = self.textBox.get(1.0, "end-1c")
            string_int = int(inp)
            selectBoxToDelete = string_int
        except ValueError:
            selectBoxToDelete = -1
        finally:
            if(selectBoxToDelete<=-1):
                selectBoxToDelete=-1
        self.window.quit()
        self.window.destroy()
  

'''GUI Select Label'''
changedLabel = None
class SimpleSelectLabel():
    def __init__(self,labelList,nCol=6):
        numInRow = nCol
        self.window = tk.Tk()
        self.window.geometry("1800x950")
        i = 0 # row_index
        iLabel = 0 # index of Label
        nLabel = len(labelList)
        while(1):
            self.window.columnconfigure(i, weight=1, minsize=90)
            self.window.rowconfigure(i, weight=1, minsize=50)
            for j in range(0, numInRow):
                frame = tk.Frame(
                    master=self.window,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j, padx=10, pady=10)
                label = tk.Label(master=frame, text=labelList[iLabel])
                label.config(font=('Helvatical bold',18))
                txtLabel = labelList[iLabel]
                label.bind("<Button-1>",lambda event,text=txtLabel:self.hLabelClick(event,text))
                iLabel+=1 # fecth next LabelS
                label.pack(padx=3, pady=3)
                if(iLabel>=nLabel):
                    break
            i+=1 # new row
            if(iLabel>=nLabel):
                break
        self.window.mainloop()
    def hLabelClick(self,event,text):
        global changedLabel
        changedLabel = text
        self.window.quit()
        self.window.destroy()

def mouse_handler(event, x, y, flags, param):
    global mouseFirstPoint,mouseLastPoint,mouseFinished,mouseDragging,lockCropping
    if lockCropping == 'unlock': # if unlocked
        if event == cv.EVENT_LBUTTONDOWN:
            mouseFirstPoint = [x,y]
            mouseDragging = True
            mouseLastPoint = [x+10,y+10]
        elif event == cv.EVENT_LBUTTONUP:
            mouseDragging = False
            mouseLastPoint = [x,y]
            mouseFinished = True
        else :
            if mouseDragging :
                mouseLastPoint  = [x,y]


img_index_changed = True
original_image = []
show_original_image = []
temp_show_original_image = []
cropped_image = []
cropRect = []
imgName = vdo_onlyname
imgExtension = ''
savedMessage = ''
frame = np.zeros((10,10,3), np.uint8)

# Read Number (img_index) from file
if os.path.exists(vdo_filename+'.count'):
    file_count = open(vdo_filename+'.count', 'r')
    line = file_count.readline()
    if not line:
        img_index=0
    else:
        if (line.isnumeric()):
            img_index=int(line)
            #print(f"Read img_index success : {img_index} !!")
        else:
            img_index=0
    file_count.close()

if(img_index > 0 and img_index <= VDO_NFRAME-1):
    cap.set(cv.CAP_PROP_POS_FRAMES, img_index)
    
else:
    img_index = 0
    cap.set(cv.CAP_PROP_POS_FRAMES, img_index)
    

currentLabel = label_name_list[0]
SimpleSelectLabel(label_name_list)
if changedLabel!=None:
    currentLabel = changedLabel
    print(f"selected -> {currentLabel}")
lines = []
xywh_str = []
key = -1

def loadLabelsFromFile():
    global imgName,img_index
    txt_path = img_path+imgName+'_'+str(img_index).zfill(6)+'.anno'
    xywhs = []
    labels = []
    if os.path.exists(txt_path): # เช็คว่า path existed ?
        with open(txt_path) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            xywh_strs = [re.split(r'\t+', line) for line in lines]
            for xywh_str in xywh_strs:
                if(len(xywh_str)==5):
                    (xc,yc,wc,hc) = int(xywh_str[1]),int(xywh_str[2]),int(xywh_str[3]),int(xywh_str[4])
                    labels.append(xywh_str[0])
                    xywhs.append(cvRect([xc,yc,wc,hc]))
    return xywhs,labels

def saveLabelsToFile():
    global imgName,cropRect,img_index
    txt_path = img_path+imgName+'_'+str(img_index).zfill(6)+'.anno'
    croppedPosString = ''
    if os.path.exists(txt_path): # เช็คว่า path existed ?
        croppedPosString = '\n'
    croppedPosString += currentLabel+'\t'
    croppedPosString += str(cropRect.x) + '\t' + str(cropRect.y) +'\t' + str(cropRect.w) + '\t' + str(cropRect.h) # x   y   w   h
    croppedPosFile = open(txt_path, "a+")
    n = croppedPosFile.write(croppedPosString)
    croppedPosFile.close()

cv.waitKey(250)
cv.namedWindow("OriginalShow",cv.WINDOW_NORMAL)
cv.setMouseCallback("OriginalShow", mouse_handler)
#cv.namedWindow("CroppedShow",cv.WINDOW_NORMAL)
refreshLabel = False
lockCropping = 'unlock'
cropRectOK = False

ret, frame = cap.read()
if(not ret):
    print("Error -> opening video file!!!")
    print("[[ Please recheck the video file and video codec ]]")
    tk.messagebox.showerror(title="Error in opening vdo", message="Error -> opening video file "+vdo_filename+" !!!\n[[ Please recheck the video file and video codec ]]")
    sys.exit()

while(True):
    if(img_index_changed): 
        #cropped_image = None
        img_index_changed=False
        mouseFinished = False
        mouseDragging = False
        print(img_path+imgName+'_'+str(img_index).zfill(6)+'.anno')
        #original_image = cv.imread(img_path+list_files[img_index])
        show_original_image = frame.copy()
        #imgName,imgExtension = os.path.splitext(list_files[img_index]) 
        #cropped_image = cv.imread(img_crop_path+imgName+'.png')
        (hImg,wImg) = show_original_image.shape[:2]
        putNamePos = (20,200)
        textSize = wImg/500
        textThickness = wImg//500
        cv.putText(show_original_image, imgName+'_'+str(img_index).zfill(6), putNamePos, cv.FONT_HERSHEY_SIMPLEX, textSize, (0,0,255),textThickness)
        temp_show_original_image = show_original_image.copy()
        marked_cvRects,marked_Label = loadLabelsFromFile()
        marked_Label_count = 0
        marked_Label_count = len(marked_Label)
        putLabel_count = (20,400)
        cv.putText(show_original_image,str(marked_Label_count), putLabel_count, cv.FONT_HERSHEY_SIMPLEX, textSize, (0,0,255),textThickness)
        for idx,marked_cvRect in enumerate(marked_cvRects):
            labelColor = list(np.random.random(size=3) * 256)
            xc,yc,wc,hc = marked_cvRect.xywh()
            cv.rectangle(show_original_image, (xc,yc), (xc+wc,yc+hc), labelColor,4)
            cv.putText(show_original_image,'#'+str(idx)+' '+marked_Label[idx], (xc,yc),cv.FONT_HERSHEY_COMPLEX_SMALL,wImg/500, labelColor,wImg//500)
        #if cropped_image is None:
        #    cv.imshow("CroppedShow",np.zeros((300,300,3),dtype=np.uint8))
    if lockCropping == 'unlock':
        if(mouseDragging):
            show_original_image = temp_show_original_image.copy()
            cv.rectangle(show_original_image, mouseFirstPoint, mouseLastPoint, (128,0,255),wImg//200)
        elif(mouseFinished or refreshLabel):
            show_original_image = temp_show_original_image.copy()
            if mouseFirstPoint[0]>mouseLastPoint[0]: # Swap X
                tmpFPX = mouseFirstPoint[0]
                mouseFirstPoint[0] = mouseLastPoint[0]
                mouseLastPoint[0] = tmpFPX
            if mouseFirstPoint[1]>mouseLastPoint[1]: # Swap Y
                tmpFPY = mouseFirstPoint[1]
                mouseFirstPoint[1] = mouseLastPoint[1]
                mouseLastPoint[1] = tmpFPY
            cropRect = cvRect([mouseFirstPoint[0],mouseFirstPoint[1],abs(mouseLastPoint[0] - mouseFirstPoint[0]),abs(mouseLastPoint[1] - mouseFirstPoint[1])])
            (hImg,wImg) = show_original_image.shape[:2]
            if(cropRect.x<0):
                cropRect.x=0
            if(cropRect.y<0):
                cropRect.y=0
            if ( (cropRect.area() >= 500) and (cropRect.w+cropRect.x <= wImg-1) and (cropRect.h+cropRect.y <= hImg-1) ): ## large_enough & not bigger than the original_image
                cropRectOK = True
                (hImg,wImg) = show_original_image.shape[:2]
                cv.rectangle(show_original_image, cropRect.tl(), cropRect.br(), (255,0,255),wImg//200)
                cv.putText(show_original_image,currentLabel, cropRect.tl(),cv.FONT_HERSHEY_COMPLEX_SMALL,wImg/500, (255,0,255),wImg//500)
            else :
                cropRectOK = False
                img_index_changed=True
                mouseFinished = False
                mouseDragging = False
                mouseFirstPoint = [0,0]
                mouseLastPoint = [9,9]
            refreshLabel = False
            mouseFinished = False


    cv.imshow("OriginalShow",show_original_image)
    #if cropped_image is not None:
    #    cv.imshow("CroppedShow",cropped_image)
    
    if(mouseDragging):
        key = cv.waitKeyEx(40)
    else :
        key = cv.waitKeyEx(200)
    # print(key)
    # key control
    if(key==ord('q') or key==ord('Q')): # 'q' -> exit
        if os.path.exists(vdo_filename+'.count'):
            subprocess.check_call(["attrib","-H",vdo_filename+'.count'])
        with open(vdo_filename+'.count', 'w') as f:
            f.write(str(img_index))
            #print(f"Written img_index : {img_index}")
            subprocess.check_call(["attrib","+H",vdo_filename+'.count'])
        break;
    elif(key==2424832 or key==2490368 or key==ord('a')): # ←/↑ or a goto previous image 
        print("--")
        img_index-=1
        img_index_changed=True
        cropRectOK = False
        mouseFinished = False
        mouseDragging = False
        mouseFirstPoint = [0,0]
        mouseLastPoint = [9,9]
        cap.set(cv.CAP_PROP_POS_FRAMES, img_index)
        if(img_index<0):
            img_index=0
        ret, frame = cap.read()
    elif(key==2555904 or key==2621440 or key==ord('d')): # →/↓ or d goto next image
        print("++")
        img_index+=1
        img_index_changed=True
        cropRectOK = False
        mouseFinished = False
        mouseDragging = False
        mouseFirstPoint = [0,0]
        mouseLastPoint = [9,9]
        if(img_index>=VDO_NFRAME):
            img_index=VDO_NFRAME-1
            cap.set(cv.CAP_PROP_POS_FRAMES, img_index)
        ret, frame = cap.read()
    elif(key==13 or key==32): # Enter or Spacebar -> save cropped
        if cropRectOK :
            #cropped_image = original_image[cropRect.y:cropRect.y+cropRect.h ,cropRect.x:cropRect.x+cropRect.w]
            #cv.imwrite(img_crop_path+imgName+'.png',cropped_image)
            if(not os.path.exists(img_path+imgName+'_'+str(img_index).zfill(6)+'.jpg')):
                cv.imwrite(img_path+imgName+'_'+str(img_index).zfill(6)+'.jpg',frame,[int(cv.IMWRITE_JPEG_QUALITY), 100])
            saveLabelsToFile()
            img_index_changed = True
            cropRectOK = False
            mouseFinished = False
            mouseDragging = False
            mouseFirstPoint = [0,0]
            mouseLastPoint = [9,9]
            print(f"Saved CroppedImage of {imgName}")
    elif(key==ord('k') or key==ord('K')): # k or K -> delete all boxes
        (hImg,wImg) = show_original_image.shape[:2]
        #cv.putText(show_original_image,"Confirm deletion in commandline!", (50,600),cv.FONT_HERSHEY_COMPLEX_SMALL,wImg/500, (0,242,255),wImg//500)
        #cv.imshow("OriginalShow",show_original_image)
        #cv.waitKey(500)
        #confirm_del = input('Do you want to delete all crop in '+imgName+' ?(Y/n)')
        confirm_del='y'
        if(confirm_del=='y' or confirm_del=='Y'):
            try:
                os.remove(img_path+imgName+'_'+str(img_index).zfill(6)+".anno")
                os.remove(img_path+imgName+'_'+str(img_index).zfill(6)+".jpg")
            except:
                print("Cannot find :"+img_path+imgName+'_'+str(img_index).zfill(6)+".anno")
            cropRectOK = False
            img_index_changed=True
            mouseFinished = False
            mouseDragging = False
            mouseFirstPoint = [0,0]
            mouseLastPoint = [9,9]
            print(f"Deleted All Cropped Object")
        img_index_changed=True
    elif(key==3014656):
        (hImg,wImg) = show_original_image.shape[:2]
        # Also disable croppring
        lockCropping = 'lock'
        oldMouseLastPoint = mouseLastPoint
        cv.setMouseCallback("OriginalShow",lambda *args : None)
        SimpleSelectBoxDeleteLabel()
        confirm_del='y'
        if(confirm_del=='y' or confirm_del=='Y'):
            try:
                with open(img_path+imgName+'_'+str(img_index).zfill(6)+".anno", 'r') as fin:
                    data = fin.read().splitlines(True)
                    #clear empty line
                    numData = len(data)
                    idx=0
                    while(True):
                        if(data[idx] in ['\n','\r\n']):
                            data.pop(idx)
                            numData = numData - 1
                        else:
                            idx = idx + 1
                        if(idx>=numData):
                            break
                    if(selectBoxToDelete>=0 and selectBoxToDelete<len(data)):
                        data.pop(selectBoxToDelete)
                        print(f"Deleted #{selectBoxToDelete} cropped box in the image")
                    with open(img_path+imgName+'_'+str(img_index).zfill(6)+".anno", 'w') as fout:
                        fout.writelines(data)
            except:
                print("Cannot find or delete on :"+img_path+imgName+".anno")
            cropRectOK = False
            img_index_changed=True
            mouseFinished = False
            mouseDragging = False
            mouseFirstPoint = [0,0]
            mouseLastPoint = [9,9]
            
        cv.waitKey(250)
        cv.setMouseCallback("OriginalShow", mouse_handler)
        mouseLastPoint = oldMouseLastPoint
        lockCropping = 'unlock'
        img_index_changed=True
    elif(key==ord('p')):
        (hImg,wImg) = show_original_image.shape[:2]
        confirm_del='y'
        if(confirm_del=='y' or confirm_del=='Y'):
            try:
                with open(img_path+imgName+'_'+str(img_index).zfill(6)+".anno", 'r') as fin:
                    data = fin.read().splitlines(True)
                with open(img_path+imgName+'_'+str(img_index).zfill(6)+".anno", 'w') as fout:
                    fout.writelines(data[1:])
            except:
                print("Cannot find :"+img_path+imgName+'_'+str(img_index).zfill(6)+".anno")
            cropRectOK = False
            img_index_changed=True
            mouseFinished = False
            mouseDragging = False
            mouseFirstPoint = [0,0]
            mouseLastPoint = [9,9]
            print(f"Deleted 1st cropped box in the image")
        img_index_changed=True
    elif(key==ord('n')):
        (hImg,wImg) = show_original_image.shape[:2]
        confirm_del='y'
        if(confirm_del=='y' or confirm_del=='Y'):
            try:
                with open(img_path+imgName+'_'+str(img_index).zfill(6)+".anno", 'r') as fin:
                    data = fin.read().splitlines(True)
                with open(img_path+imgName+'_'+str(img_index).zfill(6)+".anno", 'w') as fout:
                    fout.writelines(data[:len(data)-1])
            except:
                print("Cannot find :"+img_path+imgName+".anno")
            cropRectOK = False
            img_index_changed=True
            mouseFinished = False
            mouseDragging = False
            mouseFirstPoint = [0,0]
            mouseLastPoint = [9,9]
            print(f"Deleted last cropped box in the image")
        img_index_changed=True
    elif(key==27): # Enter -> cancel cropped
        cropRectOK = False
        img_index_changed=True
        mouseFinished = False
        mouseDragging = False
        mouseFirstPoint = [0,0]
        mouseLastPoint = [9,9]
        print(f"Cancelled Cropped")
    elif(key==ord('w') or key==ord('W')):
        # Also disable croppring
        lockCropping = 'lock'
        oldMouseLastPoint = mouseLastPoint
        cv.setMouseCallback("OriginalShow",lambda *args : None)
        cv.destroyAllWindows()
        changedLabel = None
        SimpleSelectLabel(label_name_list)
        if changedLabel!=None:
            currentLabel = changedLabel
            print(f"selected -> {currentLabel}") #print(changedLabel)
        cv.waitKey(250)
        cv.namedWindow("OriginalShow",cv.WINDOW_NORMAL)
        cv.setMouseCallback("OriginalShow", mouse_handler)
        mouseLastPoint = oldMouseLastPoint
        lockCropping = 'unlock'
        if(cropRectOK):
            refreshLabel = True
        else :
            img_index_changed = True
        

