#burada kameradan aldığımız görüntü içersinde göz var mı diye kontrol yapıyoruz
#gözü bulduktan sonra içinde siyah nokta aratacağız

#Video kütüphanelerini yüklüyoruz
from imutils.video import VideoStream
from imutils.video import FPS
import imutils

import time 
from datetime import datetime
import pyautogui 

#argparse kütüphanesi, uygulamaya parametre geçmek için kullanılır
#argparse kütüphanesini debug modda çalışırken kullanmayacağız.
#İlerde uygulamayı exe olarak çalıştırdığımızda gerekebilr
import argparse

#uygulamayı duraksatmak, yavaşlatmak için kullanacağız
import threading
import time

#opencv görüntü işleme kütüphanesi
import cv2

ap = argparse.ArgumentParser()
args = vars(ap.parse_args())
pyautogui.FAILSAFE=False

def moveMouse(x, y, dur):
    pyautogui.moveTo(x,y,duration=dur)

#obje tanıma işleminde, objeyi bilgisayara tanıtmak için bazı hazır şablon dosyalarından yararlanacağız

#bizim projemizde, kamera yüzümüze zaten çok yakın konumda bulunacağından dolayı, yüzün çerçevesini algılamaya gerek yok
#face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #yüz tanıma şablonu

#öncelikle gözü tespit edersek, göz içerisinde göz bebeğini tespit etmek daha kolay olur
#arayacağımız alanı daraltırız, daha kesin netice alırız
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")


#istersek uygulamamızı video üzerinden de çalıştırabiliriz
#videopath="firdevs_goz.mov"
videopath=""

#hangi kameradan çalışmak istersek onun numarasını veriyoruz.
#genellikle dahili kamera 0 numaradır. USB'den bağlanan kameralar 1,2,3... şeklinde sıralanır
camNo=1

#resmi iki boyuta indirgerken kullanacağımız eşik değer. 0 ile 255 arasında bir değer olabilir.
#ortam ışığı, görüntü kalitesi, göz rengi gibi ortam koşullarına göre ayarlanması gerek
#projenin ileri aşamalarında kalibrasyon eklenmesi, mümkünse uygulamanın en uygun değeri otomatik bularak bu değeri belirlemesi hedefleniyor
thresholdValue=3

yatay=1280
dikey=800

#bu değişkeni boş bırakırsak uygulama kameradan çalışır
if videopath!="":
    vs = cv2.VideoCapture(videopath)

else:
    print("[DIKKAT] kameradan görüntü algilama baslatiliyor...")
    vs = VideoStream(src=camNo).start()
    time.sleep(1.0)

fps = None

#uygulamamız biz kapatmadığımız sürece sürekli çalışacak.
#bu nedenle sonsuz bir while döngüsü içine alıyoruz

myCounter=0
xxCounter=0
yyCounter=0
wwCounter=0
hhCounter=0
rowsCounter=0
colsCounter=0

averageX=0
averageY=0
averageW=0
averageH=0

averageRows=0
averageCols=0
eyeDetected=0

while True:

    #video modu
    if videopath!="":
        ret, frame = vs.read()
        if ret is False:
            break

        roi = frame[0: 500, 0: 1400] #dikkate alınacak resmin çerçeve alanı
        rows, cols, ret = roi.shape
        gray_roi = cv2.cvtColor(roi, 6)
        gray_roi = cv2.GaussianBlur(gray_roi, (1, 1), 0)

    #kamera modu
    else:
        frame = vs.read()
        frame=frame[0: int(dikey/2), 0: int(yatay/2)]
        frame = cv2.flip(frame,0) #burası kameradan alınan görüntüyü ters çevirmek için.
        frame = frame[1] if args.get("video", False) else frame
        #resmi siyah beyaz moduna dönüştürüyoruz. yani siyah beyaz sinema filmi gibi.
        #bizim siyah dışında bir renkle işimiz olmadığından performans açısından avantajlı
        gray_roi = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #gözü tespit ediyoruz.
    eyes = eye_cascade.detectMultiScale(gray_roi, 1.3, 3)

    cv2.line(frame,(int(yatay/4),0),(int(yatay/4),1000),(0, 100, 0),2) #dikey koyu çizgi
    cv2.line(frame,(0,int(dikey/4)),(1000,int(dikey/4)),(0, 100, 0),2) #yatay koyu çizgi

    cv2.line(frame, (averageX + int(averageW/2), 0), (averageX + int(averageW/2), averageRows*4), (0, 255, 0), 2) #dikey açık çizgi
    cv2.line(frame, (0, averageY + int(averageH/2)), (averageCols*4, averageY + int(averageH/2)), (0, 255, 0), 2) #yatay açık çizgi

    #pyautogui.FAILSAFE=False
    #pyautogui.moveTo(1280, 0, duration = 5)  


    #mouse göze göre hareket edecek
    #hem mouse hareketi hem algılama aynı anda olmuyor. multitask yapmak gerekebilir

    if eyeDetected==1:

        posX=(int(averageX - int(yatay/2))*2)+yatay
        posY=(int(averageY - int(dikey/2))*2)+dikey

        print("göz x "+str(averageX)+" Y "+str(averageY))
        print("posx "+str(posX)+" posY "+str(posY))

        #hem mouse hareketini hem de uygulamanın gözü takibini aynı anda yapabilmek için
        #multitask şekilde çalıştırıyoruz.
        #mouse hareketini ayrı bir task yapıyor
        x = threading.Thread(target=moveMouse,args=(posX,posY,0.1,))
        x.start()


    eyeDetected=0

    for (x,y,w,h) in eyes:
     eyeDetected=1
     #gözü çerçeve içine alıyoruz
     #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
     #gözü siyah beyaz yapıyoruz
     roi_gray = gray_roi[y:y+h, x:x+w]
     roi_color = frame[y:y+h, x:x+w]


     rows, cols, ret = roi_color.shape
     #iki renge düşürme işi burada yapılıyor. Optimum değeri bulmak gerek
     ret, threshold = cv2.threshold(roi_gray, thresholdValue, 255, cv2.THRESH_BINARY_INV) 
 
     #iki renge düşürülmüş göz içerisinde siyah (aslında tersten olduğu için beyaz) bölgeyi tespit ediyoruz
     #bu bölge göz bebeğidir. bazen çerçeve içine kaş, kirpik vs karışıp yanıltabiliyor.
     contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    
     for cnt in contours:
         myCounter=myCounter+1
         #ileriki aşamada fare imlecini kontrol etmek için bu koordinatları kullanacağız
         (xx, yy, ww, hh) = cv2.boundingRect(cnt)

         #print("xx "+str(xx)+" yy "+ str(yy)+ " ww "+ str(ww)+" hh "+str(hh)+ "  "+ str(datetime.now()))

         #pyautogui.dragRel(xx, yy, duration = 1) 
 
         #sunum kolaylığı için bir kaç izleme çerçevesi oluşturalım
         #cv2.rectangle(roi_gray, (xx, yy), (xx + ww, yy + hh), (255, 0, 0), 2)
         #göz bebeğini yatay ve dikey çizgiyle işaretleyelim
         #cv2.line(roi_gray, (xx + int(ww/2), 0), (xx + int(ww/2), rows), (0, 255, 0), 2)
         #cv2.line(roi_gray, (0, yy + int(hh/2)), (cols, yy + int(hh/2)), (0, 255, 0), 2)

         #ana pencerede de göz ve göz bebeğini işaretleyelim

         xxCounter=xxCounter+xx
         yyCounter=yyCounter+yy
         wwCounter=wwCounter+ww
         hhCounter=hhCounter+hh
         rowsCounter=rowsCounter+rows
         colsCounter=colsCounter+cols
         if myCounter==30:
            averageX=int(xxCounter/myCounter)+x
            averageY=int(yyCounter/myCounter)+y
            averageW=int(wwCounter/myCounter)
            averageH=int(hhCounter/myCounter)
            averageRows=int(rowsCounter/myCounter)
            averageCols=int(colsCounter/myCounter)
         #cv2.line(frame, (int(xCounter/myCounter)+x + int(ww/2), 0), (int(xCounter/myCounter)+x + int(ww/2), rows*4), (0, 255, 0), 2)
         #cv2.line(frame, (0, int(yCounter/myCounter)+y + int(hh/2)), (cols*4, int(yCounter/myCounter)+y + int(hh/2)), (0, 255, 0), 2)
            myCounter=0
            xxCounter=0
            yyCounter=0
            wwCounter=0
            hhCounter=0
            rowsCounter=0
            colsCounter=0
            break
 
     #iki renkli göz bebeği görüntüsünü ekrana veriyoruz
     #cv2.imshow("Threshold", threshold)
     #siyah beyaz (film gibi) göz bebeği görüntüsünü ekrana veriyoruz
     #cv2.imshow("roi_gray", roi_gray)

    #ana görüntü çerçevesini ekrana veriyoruz
    cv2.imshow("frame",frame)

    #uygulamayı kapatmak için herhangi bir ESC tuşuna basıyoruz
    key = cv2.waitKey(30)
    if key == 27:
        break

#tüm pencereleri kapatıp uygulamayı kapatıyoruz
cv2.destroyAllWindows()
