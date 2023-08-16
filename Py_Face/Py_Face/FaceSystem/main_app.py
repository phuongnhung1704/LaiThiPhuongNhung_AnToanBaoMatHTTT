from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from PIL import ImageTk, Image
from datetime import datetime
import cv2, os
import pyodbc
import numpy as np


def start():
    def face_detec():
        # Face Detection to image
        def detecImg(name):
            # Load the cascade
            face_cascade = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml')
            # Read the input image
            img = cv2.imread(name)
            # Detect faces
            faces = face_cascade.detectMultiScale(img, 1.1, 4)
            # Draw rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #img = cv2.resize(img, (400, 400))
            cv2.imshow("Face Img", img)
            print('Successfully Image')

        # Face Detection to video
        def detecVid(name):
            # Read the input video
            cam = cv2.VideoCapture(name)
            # Load the cascade
            detector = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml')
            while (True):
                ret, img = cam.read()
                new_img = None
                grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Detect faces
                face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
                for x, y, w, h in face:
                    # Draw rectangle around the faces
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
                    cv2.putText(img, "Face Detected ", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                    cv2.imshow("FaceDetection", img)
                if cv2.waitKey(1) & 0xFF == ord('s'):  # Click s to close imshow
                    break

            cam.release()
            cv2.destroyAllWindows()
            print('Successfully Video')

        def OpenVideo():
            filepath = filedialog.askopenfile(initialdir="/", title="Open file", filetypes=(
                                              ("MP4 file", "*.mp4"), ("AOV file", "*.aov"), ("MOV file", "*.mov"),
                                              ("All file", "*.*")))
            name = filepath.name
            print(name)
            detecVid(name)

        def OpenImage():
            filepath = filedialog.askopenfile(initialdir="/", title="Open file", filetypes=(
                                              ("JPG file", "*.jpg"), ("JPEG file", "*.jpeg"), ("PNG file", "*.png"),
                                              ("All file", "*.*")))
            name = filepath.name
            print(name)
            detecImg(name)

        def close():
            add.destroy()
            start()

        add = Tk()
        add.title("Face recognition system")
        add.iconphoto(False, PhotoImage(file='image/img.png'))
        add.geometry("600x300")
        render = PhotoImage(file='image/homepagepic.png')
        img = Label(add, image=render)
        img.image = render
        img.place(x=250, y=0)
        Button(add, text='Open Video', font=10, command=OpenVideo, border=1, bg='yellow', fg='red').place(x=50, y=50)
        Button(add, text='Open Image', font=10, command=OpenImage, border=1, bg='yellow', fg='red').place(x=50, y=125)
        Button(add, text='Exit', font=10, command=close, border=2, bg='white', fg='red').place(x=50, y=200)
        add.mainloop()

    def face_recog():
        add = Tk()
        add.title("Face recognition system")

        l1 = Label(add, text="Id", font=20)
        l1.grid(column=0, row=0)
        t1 = Entry(add, width=50, bd=5)
        t1.grid(column=1, row=0)
        l2 = Label(add, text="Name", font=20)
        l2.grid(column=0, row=1)
        t2 = Entry(add, width=50, bd=5)
        t2.grid(column=1, row=1)
        l3 = Label(add, text="Gender", font=20)
        l3.grid(column=0, row=2)
        t3 = Entry(add, width=50, bd=5)
        t3.grid(column=1, row=2)
        l4 = Label(add, text="Age", font=20)
        l4.grid(column=0, row=3)
        t4 = Entry(add, width=50, bd=5)
        t4.grid(column=1, row=3)

        def OpenVideo():
            filepath = filedialog.askopenfile(initialdir="/",
                                              title="Open file",
                                              filetypes=(
                                              ("MP4 file", "*.mp4"), ("AOV file", "*.aov"), ("MOV file", "*.mov"),
                                              ("All file", "*.*")))
            # file = open(filepath, 'r')
            file = filepath.name
            print(file)
            add_face_vid(file)

        def add_face_web():
            # insert/update data to SQL Server
            def insertOrUpdate(id, name, gender, age):
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 11 for SQL Server}; SERVER=DESKTOP-4IK6CM8; Database=FaceSystem; UID=root; PWD=root;')
                cmd = "select * from ADD_USER where ID=?"
                cursor = conn.cursor()
                cursor.execute(cmd, id)
                isRecordExist = 0
                for row in cursor:
                    isRecordExist = 1
                if (isRecordExist == 1):
                    cmd = "UPDATE ADD_USER SET NAME= ? WHERE ID= ?"
                    conn.execute(cmd, id, name)
                else:
                    cmd = "INSERT INTO ADD_USER(ID, NAME, GENDER, AGE) Values(?, ?, ?, ?)"
                    conn.execute(cmd, id, name, gender, age)
                conn.commit()
                conn.close()

            id = t1.get()
            name = t2.get()
            gender = t3.get()
            age = t4.get()
            insertOrUpdate(id, name, gender, age)
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            detector = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml')
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                new_img = None
                grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
                for x, y, w, h in face:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
                    cv2.putText(img, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                    cv2.putText(img, str(str(sampleNum) + " images captured"), (x, y + h + 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 0, 255))
                    new_img = img[y:y + h, x:x + w]
                cv2.imshow("FaceDetection", img)
                key = cv2.waitKey(1) & 0xFF
                try:
                    cv2.imwrite("data/User." + id + '.' + str(sampleNum) + ".jpg", new_img)
                    # cv2.imwrite(str(path + "/" + str(sampleNum) + name + ".jpg"), new_img)
                    sampleNum += 1
                except:

                    pass
                if cv2.waitKey(1) == 13 or sampleNum == 30:
                    break
            cam.release()
            cv2.destroyAllWindows()
            messagebox.showinfo('Result', 'Add Face 30 picture completed!!!')

        def add_face_vid(file):
            # insert/update data to SQL Server
            def insertOrUpdate(id, name, gender, age):
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 11 for SQL Server}; SERVER=DESKTOP-4IK6CM8; Database=FaceSystem; UID=root; PWD=root;')
                cmd = "select * from ADD_USER where ID=?"
                cursor = conn.cursor()
                cursor.execute(cmd, id)
                isRecordExist = 0
                for row in cursor:
                    isRecordExist = 1
                if (isRecordExist == 1):
                    cmd = "UPDATE ADD_USER SET NAME= ? WHERE ID= ?"
                    conn.execute(cmd, id, name)
                else:
                    cmd = "INSERT INTO ADD_USER(ID, NAME, GENDER, AGE) Values(?, ?, ?, ?)"
                    conn.execute(cmd, id, name, gender, age)
                conn.commit()
                conn.close()

            id = t1.get()
            name = t2.get()
            gender = t3.get()
            age = t4.get()
            insertOrUpdate(id, name, gender, age)
            cam = cv2.VideoCapture(file)
            detector = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml')
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                new_img = None
                grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face = detector.detectMultiScale(image=grayimg, scaleFactor=1.1, minNeighbors=5)
                for x, y, w, h in face:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
                    cv2.putText(img, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                    cv2.putText(img, str(str(sampleNum) + " images captured"), (x, y + h + 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (0, 0, 255))
                    new_img = img[y:y + h, x:x + w]
                cv2.imshow("FaceDetection", img)
                key = cv2.waitKey(1) & 0xFF
                try:
                    cv2.imwrite("data/User." + id + '.' + str(sampleNum) + ".jpg", new_img)
                    # cv2.imwrite(str(path + "/" + str(sampleNum) + name + ".jpg"), new_img)
                    sampleNum += 1
                except:

                    pass
                if cv2.waitKey(1) == 13 or sampleNum == 30:
                    break
            cam.release()
            cv2.destroyAllWindows()
            messagebox.showinfo('Result', 'Add Face 30 picture completed!!!')

        def training():
            train = Tk()
            train.title("Train Data Face")

            def trainer():
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                path = 'data'

                def getImagesAndLabels(path):
                    # get the path of all the files in the folder
                    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
                    faces = []
                    IDs = []
                    for imagePath in imagePaths:
                        faceImg = Image.open(imagePath).convert('L');
                        faceNp = np.array(faceImg, 'uint8')
                        # split to get ID of the image
                        ID = int(os.path.split(imagePath)[-1].split('.')[1])
                        faces.append(faceNp)
                        print(ID)
                        IDs.append(ID)
                        cv2.imshow("traning", faceNp)
                        cv2.waitKey(10)
                    return IDs, faces

                Ids, faces = getImagesAndLabels(path)
                # trainning
                recognizer.train(faces, np.array(Ids))
                recognizer.save('Load_face/trainningData.yml')
                cv2.destroyAllWindows()
                messagebox.showinfo('Result', 'Trainer completed!!!')

            def recog():
                reco = Tk()
                reco.title("Face Recognition")

                def Recognizer():
                    now = datetime.now()  # trả về Hôm nay
                    tString = now.strftime('%H:%M:%S')  # biểu thị string giờ phút giây
                    dString = now.strftime('%d/%m/%Y')  # biểu thị string ngày tháng năm

                    def thamdu(name, tString, dString):
                        with open('Load_face/Face_Rec.csv', 'r+') as f:
                            myDataList = f.readlines()
                            print(myDataList)
                            nameList = []
                            for line in myDataList:
                                entry = line.split(',')  # tách theo dấu ,
                                nameList.append(entry[0])
                            if name not in nameList:
                                f.writelines(f'\n{name},{tString},{dString}')

                    faceDetect = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml')
                    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    rec = cv2.face.LBPHFaceRecognizer_create()
                    rec.read("Load_face\\trainningData.yml")
                    id = 0
                    # set text style
                    fontface = cv2.FONT_HERSHEY_SIMPLEX
                    fontscale = 1
                    fontcolor = (203, 23, 252)

                    # get data from sqlite by ID
                    def getProfile(id):
                        conn = pyodbc.connect(
                            'DRIVER={ODBC Driver 11 for SQL Server}; SERVER=DESKTOP-4IK6CM8; Database=FaceSystem; UID=root; PWD=root;')
                        cmd = "select * from ADD_USER where ID=?"
                        cursor = conn.cursor()
                        cursor.execute(cmd, id)
                        profile = None
                        for row in cursor:
                            profile = row
                        conn.close()
                        return profile

                    while (True):
                        # camera read
                        ret, img = cam.read();
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                        cv2.putText(img, 'Date:' + f'\n{tString},{dString}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1,
                                    (0, 255, 0))
                        for (x, y, w, h) in faces:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            id, conf = rec.predict(gray[y:y + h, x:x + w])
                            confidence = 100 - int(conf)
                            profile = getProfile(id)
                            # set text to window
                            if confidence > 50:
                                # if u want to print confidence level
                                # confidence = 100 - int(confidence)
                                cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale,
                                            fontcolor, 2)
                                cv2.putText(img, "Gender: " + str(profile[2]), (x, y + h + 60), fontface, fontscale,
                                            fontcolor, 2)
                                cv2.putText(img, "Age: " + str(profile[3]), (x, y + h + 90), fontface, fontscale,
                                            fontcolor, 2)
                                thamdu(str(profile[1]), tString, dString)
                            else:
                                cv2.putText(img, "UnknownFace", (x, y - 4), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1,
                                            cv2.LINE_AA)
                        cv2.imshow('Face', img)
                        if cv2.waitKey(1) & 0xFF == ord('s'): #Click s to close imshow
                            break
                    cam.release()
                    cv2.destroyAllWindows()

                def close():
                    reco.destroy()
                    start()

                def cancel():
                    reco.destroy()
                    training()

                c1 = Button(reco, text="Face Recognition", font=20, bg='orange', fg='red', command=Recognizer)
                c1.place(x=40, y=140)
                c2 = Button(reco, text="Cancel Train Face", font=20, bg='green', fg='white', command=cancel)
                c2.place(x=280, y=140)
                c3 = Button(reco, text="Exit", font=20, bg='pink', fg='black', command=close)
                c3.place(x=500, y=140)
                reco.iconphoto(False, PhotoImage(file='image/img.png'))
                reco.geometry("600x300")
                reco.mainloop()

            def nextReco():
                train.destroy()
                recog()

            def cancleAdd():
                train.destroy()
                face_recog()

            b1 = Button(train, text="Train Face", font=20, bg='orange', fg='red', command=trainer)
            b1.place(x=20, y=140)
            b2 = Button(train, text="Next Face Reacognition", font=20, bg='green', fg='white', command=nextReco)
            b2.place(x=150, y=140)
            b3 = Button(train, text="Cancel Add Face", font=20, bg='pink', fg='black', command=cancleAdd)
            b3.place(x=410, y=140)
            train.iconphoto(False, PhotoImage(file='image/img.png'))
            train.geometry("600x300")
            train.mainloop()

        def close():
            add.destroy()
            start()

        def nextTrain():
            add.destroy()
            training()

        a1 = Button(add, text="Add Face Webcam", font=20, bg='orange', fg='red', command=add_face_web)
        a1.grid(column=0, row=5)
        b1 = Button(add, text="Add Face Video", font=20, bg='orange', fg='red', command=OpenVideo)
        b1.grid(column=0, row=7)
        a2 = Button(add, text="Next Train Face", font=20, bg='green', fg='white', command=nextTrain)
        a2.grid(column=1, row=5)
        a3 = Button(add, text="Eixt", font=20, bg='pink', fg='black', command=close)
        a3.grid(column=2, row=5)
        add.iconphoto(False, PhotoImage(file='image/img.png'))
        add.geometry("600x300")
        add.mainloop()

    def show_recog():
        def recogImg(file):
            faceDetect = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml');
            img = cv2.imread(file)
            rec = cv2.face.LBPHFaceRecognizer_create()
            rec.read("Load_face\\trainningData.yml")
            id = 0
            # set text style
            fontface = cv2.FONT_HERSHEY_SIMPLEX
            fontscale = 1
            fontcolor = (203, 23, 252)

            # get data from sqlite by ID
            def getProfile(id):
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 11 for SQL Server}; SERVER=DESKTOP-4IK6CM8; Database=FaceSystem; UID=root; PWD=root;')
                cmd = "select * from ADD_USER where ID=?"
                cursor = conn.cursor()
                cursor.execute(cmd, id)
                profile = None
                for row in cursor:
                    profile = row
                conn.close()
                return profile

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5);
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                id, conf = rec.predict(gray[y:y + h, x:x + w])
                confidence = 100 - int(conf)
                profile = getProfile(id)
                # set text to window
                if confidence > 50:
                    # if u want to print confidence level
                    # confidence = 100 - int(confidence)
                    cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale,
                                    fontcolor, 2)
                    cv2.putText(img, "Gender: " + str(profile[2]), (x, y + h + 60), fontface, fontscale,
                                    fontcolor,
                                    2)
                    cv2.putText(img, "Age: " + str(profile[3]), (x, y + h + 90), fontface, fontscale,
                                    fontcolor,
                                    2)
                else:
                    cv2.putText(img, "UnknownFace", (x, y - 4), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1,
                                    cv2.LINE_AA)
            cv2.imshow('Face', img)
            # if cv2.waitKey(1) & 0xFF == ord('s'):  # Click s to close imshow
            #     break

        def reocgVid(file):
            faceDetect = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml');
            cam = cv2.VideoCapture(file)
            rec = cv2.face.LBPHFaceRecognizer_create()
            rec.read("Load_face\\trainningData.yml")
            id = 0
            # set text style
            fontface = cv2.FONT_HERSHEY_SIMPLEX
            fontscale = 1
            fontcolor = (203, 23, 252)

            # get data from sqlite by ID
            def getProfile(id):
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 11 for SQL Server}; SERVER=DESKTOP-4IK6CM8; Database=FaceSystem; UID=root; PWD=root;')
                cmd = "select * from ADD_USER where ID=?"
                cursor = conn.cursor()
                cursor.execute(cmd, id)
                profile = None
                for row in cursor:
                    profile = row
                conn.close()
                return profile
            now = datetime.now()  # trả về Hôm nay
            tString = now.strftime('%H:%M:%S')  # biểu thị string giờ phút giây
            dString = now.strftime('%d/%m/%Y')  # biểu thị string ngày tháng năm
            while (True):
                # camera read
                ret, img = cam.read();
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5);
                cv2.putText(img, 'Date:' + f'\n{tString},{dString}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 255, 0))
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    id, conf = rec.predict(gray[y:y + h, x:x + w])
                    confidence = 100 - int(conf)
                    profile = getProfile(id)
                    # set text to window
                    if confidence > 50:
                        # if u want to print confidence level
                        # confidence = 100 - int(confidence)
                        cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
                        cv2.putText(img, "Gender: " + str(profile[2]), (x, y + h + 60), fontface, fontscale, fontcolor, 2)
                        cv2.putText(img, "Age: " + str(profile[3]), (x, y + h + 90), fontface, fontscale, fontcolor, 2)
                    else:
                        cv2.putText(img, "UnknownFace", (x, y - 4), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1,cv2.LINE_AA)
                cv2.imshow('Face', img)
                if cv2.waitKey(30) & 0xFF == ord('s'):  # Click s to close imshow
                    break
            cam.release()
            cv2.destroyAllWindows()

        def recogWeb():
            now = datetime.now()  # trả về Hôm nay
            tString = now.strftime('%H:%M:%S')  # biểu thị string giờ phút giây
            dString = now.strftime('%d/%m/%Y')  # biểu thị string ngày tháng năm

            def thamdu(name, tString, dString):
                with open('Load_face/Face_Rec.csv', 'r+') as f:
                    myDataList = f.readlines()
                    print(myDataList)
                    nameList = []
                    for line in myDataList:
                        entry = line.split(',')  # tách theo dấu ,
                        nameList.append(entry[0])
                    if name not in nameList:
                        f.writelines(f'\n{name},{tString},{dString}')

            faceDetect = cv2.CascadeClassifier('E:\Py\Py_Bt\haarcascades\haarcascade_frontalface_default.xml');
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW);
            rec = cv2.face.LBPHFaceRecognizer_create();
            rec.read("Load_face\\trainningData.yml")
            id = 0
            # set text style
            fontface = cv2.FONT_HERSHEY_SIMPLEX
            fontscale = 1
            fontcolor = (203, 23, 252)
            def getProfile(id):
                conn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server}; SERVER=DESKTOP-4IK6CM8; Database=FaceSystem; UID=root; PWD=root;')
                cmd = "select * from ADD_USER where ID=?"
                cursor = conn.cursor()
                cursor.execute(cmd, id)
                profile = None
                for row in cursor:
                    profile = row
                conn.close()
                return profile
            while (True):
                # camera read
                ret, img = cam.read();
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5);
                cv2.putText(img, 'Date:' + f'\n{tString},{dString}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 1,(0, 255, 0))
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    id, conf = rec.predict(gray[y:y + h, x:x + w])
                    confidence = 100 - int(conf)
                    profile = getProfile(id)
                    # set text to window
                    if confidence > 50:
                        # if u want to print confidence level
                        # confidence = 100 - int(confidence)
                        cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale,fontcolor, 2)
                        cv2.putText(img, "Gender: " + str(profile[2]), (x, y + h + 60), fontface, fontscale,fontcolor,2)
                        cv2.putText(img, "Age: " + str(profile[3]), (x, y + h + 90), fontface, fontscale,fontcolor,2)
                        thamdu(str(profile[1]), tString, dString)
                    else:
                        cv2.putText(img, "UnknownFace", (x, y - 4), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1,cv2.LINE_AA)
                cv2.imshow('Face', img)
                if cv2.waitKey(30) & 0xFF == ord('s'):  # Click s to close imshow
                    break
            cam.release()
            cv2.destroyAllWindows()

        def OpenVideo():
            filepath = filedialog.askopenfile(initialdir="/",title="Open file",
                                              filetypes=(("MP4 file", "*.mp4"), ("AOV file", "*.aov"), ("MOV file", "*.mov"),
                                              ("All file", "*.*")))
            # file = open(filepath, 'r')
            file = filepath.name
            print(file)
            reocgVid(file)

        def OpenImage():
            filepath = filedialog.askopenfile(initialdir="/",title="Open file",
                                              filetypes=(("JPG file", "*.jpg"), ("JPEG file", "*.jpeg"), ("PNG file", "*.png"),
                                              ("All file", "*.*")))
            file = filepath.name
            print(file)
            recogImg(file)

        def close():
            add.destroy()
            start()

        add = Tk()
        add.title("Show Recognizer")
        add.iconphoto(False, PhotoImage(file='image/img.png'))
        add.geometry("600x300")
        render = PhotoImage(file='image/homepagepic.png')
        img = Label(add, image=render)
        img.image = render
        img.place(x=280, y=0)
        Button(add, text='Open Image', font=10, command=OpenImage, border=1, bg='yellow', fg='red').place(x=63, y=40)
        Button(add, text='Open Video', font=10, command=OpenVideo, border=1, bg='yellow', fg='red').place(x=65, y=100)
        Button(add, text='Open Webcam', font=10, command=recogWeb, border=1, bg='yellow', fg='red').place(x=50, y=160)
        Button(add, text='Exit', font=10, command=close, border=2, bg='white', fg='red').place(x=90, y=220)
        add.mainloop()

    w = Tk()
    w.geometry('800x500')
    w.configure(bg='white')
    w.resizable(0, 0)
    w.title('Face System')
    w.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
    l1 = Label(w, text="Welcome to Face System!!", font=('times', 20, 'bold')).place(x=250, y=40)
    render = PhotoImage(file='image/homepagepic.png')
    img = Label(w, image=render)
    img.image = render
    img.place(x=270, y=100)

    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure?"):
            w.destroy()
    def OpenDete():
        w.destroy()
        face_detec()
    def OpenReco():
        w.destroy()
        face_recog()
    def OpenShowR():
        w.destroy()
        show_recog()
    def menu():
        f1 = Frame(w, width=250, height=500, bg='gray')
        f1.place(x=0, y=0)
        # buttons
        def bttn(x, y, text, bcolor, fcolor, cmd):
            def on_entera(e):
                myButton1['background'] = bcolor
                myButton1['foreground'] = '#262626'
            def on_leavea(e):
                myButton1['background'] = fcolor
                myButton1['foreground'] = '#262626'
            myButton1 = Button(f1, text=text, width=35, height=2, fg='#262626', border=0, bg=fcolor,
                               activeforeground='#262626', activebackground=bcolor, command=cmd)
            myButton1.bind("<Enter>", on_entera)
            myButton1.bind("<Leave>", on_leavea)
            myButton1.place(x=x, y=y)
        bttn(0, 80, 'Face Detection', '#0f9d9a', '#12c4c0', OpenDete)
        bttn(0, 117, 'Add Face Recognition', '#0f9d9a', '#12c4c0', OpenReco)
        bttn(0, 154, 'Show Recognizer', '#0f9d9a', '#12c4c0', OpenShowR)
        bttn(0, 191, 'Exit System', '#0f9d9a', '#12c4c0', on_closing)
        def dele():
            f1.destroy()
        global img2
        img2 = ImageTk.PhotoImage(Image.open("image/close.png"))
        Button(f1, image=img2, border=0, command=dele, bg='#12c4c0', activebackground='#12c4c0').place(x=5, y=10)

    img1 = ImageTk.PhotoImage(Image.open("image/open.png"))
    Button(w, image=img1, command=menu, border=0, bg='#262626', activebackground='#262626').place(x=5, y=10)
    w.iconphoto(False, PhotoImage(file='image/img.png'))
    w.mainloop()

app = start()
