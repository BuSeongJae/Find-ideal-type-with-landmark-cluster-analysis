import numpy as np
import dlib
import cv2
import pandas as pd


def landmark(image):
    # 이미지에 보여질 점의 숫자 변수 선언
    RIGHT_EYE = list(range(36, 42)) # 보여지는 점 번호 : 37~42 번
    LEFT_EYE = list(range(42, 48)) #보여지는 점 번호 :  43 ~ 48
    MOUTH = list(range(48, 68)) #보여지는 점 번호 :  49~ 68
    NOSE = list(range(27, 36)) #보여지는 점 번호 :  28~36
    EYEBROWS = list(range(17, 27)) #보여지는 점 번호 :  18~27
    JAWLINE = list(range(0, 17)) #보여지는 점 번호 :  1~17
    ALL = list(range(0, 68)) #보여지는 점 번호 :  1~68
    EYES = list(range(36, 48)) #보여지는 점 번호 :  37~ 48


    # 눈,코, 입 등 부분별 좌표값 변수 선언
    global right_eye_coordinate, left_eye_coordinate,mouth_coordinate, nose_coordinate,\
        eyebrows_coordinate, jawline_coordinate, eyes_coordinate, all_coordinate




    #detect한 사각형 너비, 높이 변수 선언
    detect_width = 0
    detect_height = 0
    #학습된 모델
    predictor_file = './model/shape_predictor_68_face_landmarks_GTX.dat'

    # predictor_file = './model/shape_predictor_68_face_landmarks.dat'



    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_file) # 모델을 통해 68개의 점 가져옴

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #rects : 인식한 얼굴들
    rects = detector(gray, 1) # 1: upscale 한번이면 큰 이미지에서 인식
    # print("Number of faces detected: {}".format(len(rects)))

    # 특징추출 변수선언


    #인식한 얼굴들에서 각 얼굴들에 대한 좌표추출 for문
    for (i, rect) in enumerate(rects):

        points = np.matrix([[p.x, p.y] for p in predictor(gray, rect).parts()])
        #이미지에 보여줄 점 번호: All 전체
        show_parts = points[ALL]

        #비율로 계산하기 위해 너비, 높이 구해놓기
        detect_width = rect.right() - rect.left()
        detect_height = rect.bottom() - rect.top()

        # 각 부분의 좌표값 저장
        right_eye_coordinate = points[RIGHT_EYE]
        left_eye_coordinate = points[LEFT_EYE]
        mouth_coordinate = points[MOUTH]
        nose_coordinate = points[NOSE]
        eyebrows_coordinate = points[EYEBROWS]
        jawline_coordinate = points[JAWLINE]
        eyes_coordinate = points[ALL]
        all_coordinate = points[EYES]

        #눈 너비 40-37
        eye_width = points[39] - points[36]
        eye_width = eye_width[0:, 0]/detect_width

        #눈 높이 41-39
        eye_height = points[40] - points[38]
        eye_height = eye_height[0:, 1]/detect_height

        #코 수직길이 34-28
        nose_height = points[33] - points[27]
        nose_height = nose_height[0:, 1]/detect_height

        #코 너비 36-32
        nose_width = points[35] - points[31]
        nose_width = (nose_width[0:, 0]/detect_width)

        # 코 높이(인중에서 콧볼) 34-31
        nose_high = points[33] - points[30]
        nose_high = nose_high[0:, 1]/detect_height

        #입 너비 55-49
        mouth_width = points[54] - points[48]
        mouth_width = mouth_width[0:, 0]/detect_width

        #입 높이 58 -51
        mouth_height = points[57] - points[50]
        mouth_height = mouth_height[0:, 1]/detect_height

        #눈썹 너비 22-18
        eyebrow_width = points[21] -points[17]
        eyebrow_width = eyebrow_width[0:, 0]/detect_width

        #눈과 눈썹사이 거리 38-20
        eye_to_eyebrow = points[37] -points[19]
        eye_to_eyebrow = eye_to_eyebrow[0:, 1]/detect_height

        #눈과 눈 사이 거리 43-40
        eye_to_eye = points[42] -points[39]
        eye_to_eye = eye_to_eye[0:, 0]/detect_width

        #눈과 관자놀이 사이 거리 37-1
        eye_to_temple = points[36] -points[0]
        eye_to_temple = eye_to_temple[0:, 0]/detect_width

        #코와 입 사이 거리 52-34
        nose_to_mouth = points[51] -points[33]
        nose_to_mouth = nose_to_mouth[0:,1]/detect_height

        #입과 턱 사이 거리 9-59
        mouth_to_jaw = points[8] -points[58]
        mouth_to_jaw = mouth_to_jaw[0:,1]/detect_height

        #얼굴 너비 17-1
        face_width = points[16] -points[0]
        face_width = face_width[0:, 0]/detect_width

        #눈썹부터 턱 9 -25
        face_height = points[8] -points[24]
        face_height = face_height[0:,1]/detect_height

        # dataframe 전체컬럼 나오게 설정
        # pd.set_option('display.max_columns', None)
        data_list = [np.ravel(eye_width)[0], np.ravel(eye_height)[0], np.ravel(nose_height)[0], np.ravel(nose_width)[0], np.ravel(nose_high)[0], np.ravel(mouth_width)[0],
                     np.ravel(mouth_height)[0], np.ravel(eyebrow_width)[0], np.ravel(eye_to_eyebrow)[0], np.ravel(eye_to_eye)[0], np.ravel(eye_to_temple)[0],
                     np.ravel(nose_to_mouth)[0], np.ravel(mouth_to_jaw)[0], np.ravel(face_width)[0], np.ravel(face_height)[0]]





        cv2.rectangle(image, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0, 0, 255), 2)



        for (i, point) in enumerate(show_parts):
            x = point[0,0]
            y = point[0,1]
            cv2.circle(image, (x, y), 1, (0, 255, 255), -1)
            cv2.putText(image, "{}".format(i + 1), (x, y - 2),
            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    #
    # cv2.imshow("Face Landmark", image)
    # cv2.waitKey(0)
    return data_list





