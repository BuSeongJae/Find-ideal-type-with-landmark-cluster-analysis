import bring_model
import face_landmark as land
import cv2
import numpy as np
import pandas as pd

import oracle_db as oradb
from face_alignment import align_image

df = pd.DataFrame(columns=['eye_width', 'eye_height', 'nose_height', 'nose_width', 'nose_high', 'mouth_width', 'mouth_height', 'eyebrow_width', 'eye_to_eyebrow', 'eye_to_eye', 'eye_to_temple', 'nose_to_mouth', 'mouth_to_jaw', 'face_width', 'face_height'])

def select_all_userface():
    conn = oradb.connect()
    query = '''select eye_width, eye_height, nose_height, nose_width, nose_high, mouth_width, mouth_height, eyebrow_width, eye_to_eyebrow, eye_to_eye, eye_to_temple, nose_to_mouth, mouth_to_jaw, face_width, face_height
            from userface'''

    try:
        cursor = conn.cursor()
        result = cursor.execute(query)
        i=1
        face_list = []
        for row in result:
            row_dict = {'eye_width': row[0], 'eye_height': row[1], 'nose_height':row[2], \
            'nose_width': row[3], 'nose_high': row[4], 'mouth_width': row[5], 'mouth_height': row[6], \
            'eyebrow_width': row[7], 'eye_to_eyebrow': row[8], 'eye_to_eye': row[9], 'eye_to_temple': row[10], 'nose_to_mouth': row[11], \
            'mouth_to_jaw': row[12], 'face_width': row[13], 'face_height': row[14]}

            ref = bring_model.Face(row_dict)
            face_list.append(ref)
            # df.loc[i] = face_list
            i += 1


    except Exception as msg:
        print('userface 정보 가져오기 에러 발생 : ', msg)
    finally:
        cursor.close()
        oradb.close(conn)

    return face_list


def get_select_all():
    face_list = select_all_userface()
    i=1
    for face_ref in face_list:
        df.loc[i] = bring_model.Face.info_list(face_ref)
        i += 1
    return df

#userface의 회원 face 정보 df로 저장
userface_df = get_select_all()


def bring_idealface_num():
    # face_num 가져오기
    sql = """
            select max(idealface_num)
            from idealface
            """
    conn = oradb.connect()
    cursor = conn.cursor()
    num_list = []
    rs = cursor.execute(sql)
    for record in rs:
       num_list.append(record[0])
    num = num_list[0]

    return num

idealface_num = bring_idealface_num()+1
image_file= './ideal_image/{}.jpg'.format(idealface_num)
align_image(image_file) # face_alignment.py 의 align_image 함수 실행

#align된 이미지 landmark 돌려 userface TABLE 에 insert
align_image_file = './ideal_align_image/{}.jpg'.format(idealface_num)
image = cv2.imread(align_image_file)

userface_df.loc[len(userface_df)+1] = land.landmark(image)

print(userface_df)

from sklearn.decomposition import PCA

# Instantiating PCA
pca = PCA()

# Fitting and Transforming the DF
df_pca = pca.fit_transform(userface_df)


# Finding the exact number of features that explain at least 99% of the variance in the dataset
total_explained_variance = pca.explained_variance_ratio_.cumsum()
n_over_99 = len(total_explained_variance[total_explained_variance>=.99])
n_to_reach_99 = userface_df.shape[1] - n_over_99

print(f"Number features: {n_to_reach_99}\nTotal Variance Explained: {total_explained_variance[n_to_reach_99]}")


# Reducing the dataset to the number of features determined before
pca = PCA(n_components=n_to_reach_99)

# Fitting and transforming the dataset to the stated number of features
df_pca = pca.fit_transform(userface_df)

# Seeing the variance ratio that still remains after the dataset has been reduced
pca.explained_variance_ratio_.cumsum()[-1]

from sklearn.cluster import AgglomerativeClustering
# Instantiating HAC
hac = AgglomerativeClustering(n_clusters=5)

# Fitting
hac.fit(df_pca)

# Getting cluster assignments
cluster_assignments = hac.labels_

userface_df['Cluster #'] = cluster_assignments
print(userface_df)

cluster = userface_df.loc[len(userface_df)][15]

# Assigning the Cluster Profiles as a new DF
group = userface_df[userface_df['Cluster #']==cluster].drop('Cluster #', axis=1)

# Trasnposing the DF so that we are correlating with the index(users)
corr_group = group.T.corr()
user = len(userface_df)

top_5_sim = corr_group[[user]].sort_values(by=[user],axis=0, ascending=False)[1:6]

top_5 = []
for i in range (5):
    top_5.append(int(top_5_sim.index[i]))

print(top_5)

print("\nThe most similar user to User #", user, "is User #", top_5_sim.index[0])


def idealfaceinfo_insert(data):
    conn = oradb.connect()
    query = '''insert into IDEALFACE values
    (SEQ_IFID.nextval, :1, :2, :3, :4, :5, 'USER_ID')'''

    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        oradb.commit(conn)
        print("새 회원 face정보 저장완료")

    except Exception as msg:
        oradb.rollback(conn)
        print('IDEALface 정보 저장(userfaceland_insert) 에러 발생 : ', msg)

    finally:
        cursor.close()
        oradb.close(conn)



idealfaceinfo_insert(top_5)