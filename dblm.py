import sqlite3

def db_connect():
    # misc.dbを作成する
    # すでに存在していれば、それにアスセスする。
    dbname = 'lm.db'
    conn = sqlite3.connect(dbname)
    return conn

def db_close(conn):
    # データベースへのコネクションを閉じる。(必須)
    conn.close()

def db_create_table(conn):
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    # cur.execute(
    #     'CREATE TABLE IF NOT EXISTS persons(name STRING,passwd STRING)')

    # データベースへコミット。これで変更が反映される。
    conn.commit()

def db_drop_table(conn):
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    # cur.execute(
    #     'DROP TABLE IF EXISTS persons')

    # データベースへコミット。これで変更が反映される。
    conn.commit()

def db_insert(conn,name,password):
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    # cur.execute('INSERT INTO persons(name,passwd) values(?,?)',(name,password))

    # データベースへコミット。これで変更が反映される。
    conn.commit()

def db_select(conn):
    cur = conn.cursor()
    # cur.execute('SELECT name, passwd FROM persons')
    res_value = cur.fetchall()
    for value in res_value:
        print(value)
    return res_value;

def db_initialize():
    conn = db_connect()
    db_drop_table(conn)
    db_create_table(conn)
    # db_insert(conn,'user1','pass1')
    # db_insert(conn,'user2','pass2')
    db_close(conn)

# def db_check_login(conn,name,passwd):
#     cur = conn.cursor()
#     cur.execute('SELECT name, passwd FROM persons WHERE name = ? and passwd = ?',(name,passwd))
#     res_value = cur.fetchall()
#     if (len(res_value) == 0):
#         return False
#     else:
#         return True
