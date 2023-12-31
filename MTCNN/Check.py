import cv2
from sys import argv
from os import listdir
import time
from fer import FER as MTCNN


def get_emotion(img_path: str) -> str:
    try:
        img = cv2.imread(img_path)
        detector = MTCNN()
        emotions = detector.detect_emotions(img)
        # print(emotions)
        weights = emotions[0]["emotions"]
        weights = [(weights[emotion], emotion) for emotion in weights]
        weights.sort()
        return weights[-1][1]
    except:
        return "No face"


def custom_check():
    arg = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_haar_cascade = cv2.CascadeClassifier(arg)

    for image in listdir("Custom/"):
        emotion = get_emotion("Custom/" + image)
        while True:
            test_img = cv2.imread("Custom/" + image)
            gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

            faces_detected = face_haar_cascade.detectMultiScale(
                gray_img, 1.32, 5
            )

            for (x, y, w, h) in faces_detected:
                cv2.rectangle(
                    test_img,
                    (x, y),
                    (x + w, y + h),
                    (255, 0, 0),
                    thickness=7,
                )
                cv2.putText(
                    test_img,
                    emotion,
                    (int(x), int(y)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )

            resized_img = cv2.resize(test_img, (1000, 700))
            cv2.imshow("Facial emotion analysis ", resized_img)

            if cv2.waitKey(10) == ord("q"):
                break

            time.sleep(0.1)

        cv2.destroyAllWindows


custom_check()
