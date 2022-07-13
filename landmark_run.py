import face_landmark as land
import cv2
import numpy as np
import pandas as pd

import oracle_db as oradb
from face_alignment import align_image


# userface 에 USER FACE정보 insert
def userfaceland_insert(data):
    conn = oradb.connect()
    print(data)
    query = '''insert into USERFACE values 
    (SEQ_FID.nextval, :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, 'base')'''

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        oradb.commit(conn)
        print("새 회원 face정보 저장완료")

    except Exception as msg:
        oradb.rollback(conn)
        print('user face 정보 저장(userfaceland_insert) 에러 발생 : ', msg)

    finally:
        cursor.close()
        oradb.close(conn)


#새로등록할 face_num 가져오기
def bring_face_num():
    # face_num 가져오기
    sql = """
            select max(face_num)
            from userface
            """
    conn = oradb.connect()
    cursor = conn.cursor()
    num_list = []
    rs = cursor.execute(sql)
    for record in rs:
       num_list.append(record[0])
    num = num_list[0]

    return num


# 1. 웹에서 이미지가 등록되어 image폴더에 이미지가 등록되면 align_image 폴더에 align한 이미지 파일 저장

# face_num 을 이미지이름(db의 face_num 최대값 가져와서)과 동일하게

# DB에서 가장 최근 face_num 값 다음 num으로 이미지 align
face_num = bring_face_num()+1
image_file= './image/{}.jpg'.format(face_num)
align_image(image_file) # face_alignment.py 의 align_image 함수 실행

#align된 이미지 landmark 돌려 userface TABLE 에 insert
align_image_file = './align_image/{}.jpg'.format(face_num)
image = cv2.imread(align_image_file)

userfaceland_insert(land.landmark(image)) #land.landmark(image)가 list형식의 한사람 데이터 가져오고 userfaceland_insert함수가 db에 리스트 1개씩 데이터 저장

# df = pd.DataFrame(columns=['eye_width', 'eye_height', 'nose_height', 'nose_width', 'nose_high', 'mouth_width', 'mouth_height', 'eyebrow_width', 'eye_to_eyebrow', 'eye_to_eye', 'eye_to_temple', 'nose_to_mouth', 'mouth_to_jaw', 'face_width', 'face_height'])
#######

# align: 얼굴 수평 맞추기 => align_image폴더 만들어 놓으면 폴더에 수평맞춰진 사진 저장됨
# for i in range(1,401):
#     image_file= './image/{}.jpg'.format(i)
#     align_image(image_file) # face_alignment.py 의 align_image 함수 실행



#align된 이미지 landmark 돌려서 얼굴비율 추출, DB에 저장
#######
# for i in range(1,401):
#     align_image_file = './align_image/{}.jpg'.format(i)
#     image = cv2.imread(align_image_file)
#
#     userfaceland_insert(land.landmark(image)) #land.landmark(image)가 list형식의 한사람 데이터 가져오고 userfaceland_insert함수가 db에 리스트 1개씩 데이터 저장
#######
#csv에 저장
# df.to_csv('landmark_test.csv', sep= ',')