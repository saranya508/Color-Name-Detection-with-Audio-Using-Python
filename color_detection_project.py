# -*- coding: utf-8
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import pandas as pd
import cv2
from gtts import gTTS
import os
from playsound import playsound

print("Select Image Source")
print("1.From Web Camera")
print("2.From Specified Path")
c=int(input())
if c==1:
        cam = cv2.VideoCapture(0)
        
        cv2.namedWindow("Display")
        
        img_counter = 0
        
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Display", frame)
        
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
        
        cam.release()
        
        cv2.destroyAllWindows()
elif c==2:
    img_name="C:\\Users\\This PC\\Desktop\\Color detection\\pic1.jpg"
img_path=img_name
csv_path='colors.csv'

index=['color','color_name','hex','R','G','B']
df=pd.read_csv(csv_path,names=index,header=None)
img=cv2.imread(img_path)
img=cv2.resize(img,(800,600))

clicked=False
r=g=b=xpos=ypos=0
def get_color_name(R,G,B):
    minimum=1000
    for i in range(len(df)):
        d=abs(R-int(df.loc[i,'R']))+abs(G-int(df.loc[i,'G']))+abs(B-int(df.loc[i,'B']))
        if d<=minimum:
            minimum=d
            cname=df.loc[i,'color_name']
    return cname

def draw_function(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global clicked,r,g,b,xpos,ypos
        clicked=True
        xpos=x
        ypos=y
        b,g,r=img[y,x]
        b=int(b)
        g=int(g)
        r=int(r)
        
        
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)
while True:
    cv2.imshow('image',img)
    if clicked:
        cv2.rectangle(img,(20,20),(600,60),(b,g,r),-1)
        msg=get_color_name(r,g,b)+' R='+str(r)+' G='+str(g)+' B='+str(b)
        cv2.putText(img,msg,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        if r+g+b>=600:
            cv2.putText(img,msg,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        ccolor="This is"+get_color_name(r,g,b)+'color and RGB values are R value is'+str(r)+" "+' and G value is'+str(g)+' and B value is'+str(b)
        speech=gTTS(text=ccolor)
        speech.save('o.mp3')
        playsound('o.mp3')
        os.remove('o.mp3')
        
    if cv2.waitKey(20) & 0xFF==27:
        break

cv2.destroyAllWindows()