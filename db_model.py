# DB_Helper.py
import oracle_db as odb
import cx_Oracle

class DBHelper:
    # 멤버변수(field)
    conn = ''
    # 생성자(constructor)
    def __init__(self):
        odb.oracle_init()
        self.conn = odb.connect()

        # 소멸자(destructor) 프로그램 종료되면 자동 삭제 용도
        def __del__(self):
            if self.conn:
                odb.close(self.conn)


    # 멤버함수(method)
    def db_insertLandmarkData(self, T):
        cursor = self.conn.cursor()
        with self.conn.cursor() as cursor: # cursor 자동 close 됨됨
            query = "insert into USERFACE values (SEQ_FID.nextval, :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16)"
            cursor.execute(query, T)
        odb.commit(self.conn)


