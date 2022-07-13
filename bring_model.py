# DB_Helper.py
import oracle_db as odb

class Face:
    __eye_width = ''
    __eye_height = ''
    __nose_height = ''
    __nose_width = ''
    __nose_high = ''
    __mouth_width = ''
    __mouth_height = ''
    __eyebrow_width = ''
    __eye_to_eyebrow = ''
    __eye_to_eye = ''
    __eye_to_temple = ''
    __nose_to_mouth = ''
    __mouth_to_jaw = ''
    __face_width = ''
    __face_height = ''

    def __init__(self, face_dict):
        self.__eye_width = face_dict['eye_width']
        self.__eye_height = face_dict['eye_height']
        self.__nose_height = face_dict['nose_height']
        self.__nose_width = face_dict['nose_width']
        self.__nose_high = face_dict['nose_high']
        self.__mouth_width = face_dict['mouth_width']
        self.__mouth_height = face_dict['mouth_height']
        self.__eyebrow_width = face_dict['eyebrow_width']
        self.__eye_to_eyebrow = face_dict['eye_to_eyebrow']
        self.__eye_to_eye = face_dict['eye_to_eye']
        self.__eye_to_temple = face_dict['eye_to_temple']
        self.__nose_to_mouth = face_dict['nose_to_mouth']
        self.__mouth_to_jaw = face_dict['mouth_to_jaw']
        self.__face_width = face_dict['face_width']
        self.__face_height = face_dict['face_height']

    def __del__(self):
        print(self, '인스턴스 소멸됨.')
    def set_eye_width(self, eye_width):
        self.__eye_width = eye_width
    def set_eye_height(self, eye_height):
        self.__eye_height = eye_height
    def set_nose_height(self, nose_height):
        self.__nose_height = nose_height
    def set_nose_width(self, nose_width):
        self.__nose_width = nose_width
    def set_nose_high(self, nose_high):
        self.__nose_high =nose_high
    def set_mouth_width(self, mouth_width):
        self.__mouth_width = mouth_width
    def set_mouth_height(self, mouth_height):
        self.__mouth_height = mouth_height
    def set_eyebrow_width(self, eyebrow_width):
        self.__eyebrow_width = eyebrow_width
    def set_eye_to_eyebrow(self, eye_to_eyebrow):
        self.__eye_to_eyebrow = eye_to_eyebrow
    def set_eye_to_eye(self, eye_to_eye):
        self.__eye_to_eye = eye_to_eye
    def set_eye_to_temple(self, eye_to_temple):
        self.__eye_to_temple = eye_to_temple
    def set_nose_to_mouth(self, nose_to_mouth):
        self.__nose_to_mouth = nose_to_mouth
    def set_mouth_to_jaw(self, mouth_to_jaw):
        self.__mouth_to_jaw = mouth_to_jaw
    def set_face_width(self, face_width):
        self.__face_width = face_width
    def set_face_height(self, face_height):
        self.__face_height = face_height


    def info_list(self):
        return [self.__eye_width, self.__eye_height, self.__nose_height, self.__nose_width, self.__nose_high, self.__mouth_width, self.__mouth_height, self.__eyebrow_width, self.__eye_to_eyebrow, self.__eye_to_eye, self.__eye_to_temple, self.__nose_to_mouth, self.__mouth_to_jaw, self.__face_width, self.__face_height]