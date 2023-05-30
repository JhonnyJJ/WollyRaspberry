import cv2

cap = cv2.VideoCapture(0)

# cascade classifier for face tracking
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()

    # gray scaling for easier detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # face detection for each frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))
    print("Found " + str(len(faces)) + " face(s)")

    # create a green rectangle around the found faces
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

        break

    gray = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    gray = cv2.resize(gray, (1020,700))
    gray = cv2.flip(gray,1)
    cv2.imshow('Input', gray)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()