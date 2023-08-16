import cv2, sys, numpy, os

def Add_face(inp):
    haar_file = 'haarcascade_frontalface_default.xml'

    #Tạo thư mục tên Dataset
    dataset = 'Dataset'
    #inp = input('Enter your name: ')

    path = os.path.join(dataset, inp)
    if not os.path.isdir(path):
        os.mkdir(path)
    (width, height) = (128, 128)
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    count = 0
    while (True):
        (_, img) = webcam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 255), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite('%s/%s.png' % (path, count), face_resize)
        count += 1

        cv2.imshow('Add Face', img)
        key = cv2.waitKey(5000)
        if key & 0xFF == ord('s'):
            break
        elif count == 20:
            break

    webcam.release()
    cv2.destroyAllWindows()

def Reco_face():
    size = 4
    haar_file = 'haarcascade_frontalface_default.xml'
    dataset = 'Dataset'

    print('Start Recognitor...')
    (images, labels, name, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(dataset):
        for subdirs in dirs:
            name[id] = subdirs
            subjectpath = os.path.join(dataset, subdirs)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                label = id
                images.append(cv2.imread(path, 0))
                labels.append(int(label))
            id +=1
    (width, height) = (128, 128)
    (images, labels) = [numpy.array(lis) for lis in [images, labels]]

    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, labels)
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    str1 = 'cctv'
    str2 = 'unknown'
    count = 0
    while True:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if prediction[1] < 70:
                cv2.putText(im, '%s - %.0f' % (name[prediction[0]], prediction[1]), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            else:
                cv2.putText(im, 'not recognized', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                cv2.imwrite(str2 + '/' + str(count) + '.jpg', face)
                count = count + 1

        cv2.imshow('OpenCV', im)

        key = cv2.waitKey(10)
        if key & 0xFF == ord('s'):
            break

print("Action Face")
print("1. Add face")
print("2. Recog face")
ac = input("Vui long chon: ")
if int(ac) == 1:
    inp = input('Enter your name: ')
    Add_face(inp)
elif int(ac) == 2:
    Reco_face()
else:
    print("Error, please enter number...!!!")

