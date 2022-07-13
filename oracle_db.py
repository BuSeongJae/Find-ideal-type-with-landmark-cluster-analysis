# oracle_db.py
# common 패키지에 oracle_db 모듈로 정의함

import cx_Oracle

# 사용자 정의 변수
dbURL = "localhost:1521/xe"
dbUSER = "c##student2"
dbPASSWD = "student2"

def oracle_init():  # 애플리케이션 구동시 딱 한번 실행되어야 함
    cx_Oracle.init_oracle_client(lib_dir="C:\instantclient_21_3")

def connect():
    try:
        return cx_Oracle.connect(dbUSER, dbPASSWD, dbURL)
    except Exception as msg:
        print('오라클 연동 관련 에러 발생 : ', msg)

def close(conn):
    try:
        if conn: # conn이 None이 아니면(True 이면)
            conn.close()
    except Exception as msg:
        print("오라클 연동 해제 에러 발생 : ", msg)

def commit(conn):
    try:
        if conn:  # conn이 None이 아니면(True 이면)
            conn.commit()
    except Exception as msg:
        print("오라클 트랜잭션 커밋 에러 발생 : ", msg)

def rollback(conn):
    try:
        if conn:  # conn이 None이 아니면(True 이면)
            conn.rollback()
    except Exception as msg:
        print("오라클 트랜잭션 롤백 에러 발생 : ", msg)