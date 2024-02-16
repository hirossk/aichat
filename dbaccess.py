import sqlite3

def db_connect():
    # sanple.dbを作成する
    # すでに存在していれば、それにアスセスする。
    dbname = 'sample.db'
    conn = sqlite3.connect(dbname)
    return conn

def db_close(conn):
    # データベースへのコネクションを閉じる。(必須)
    conn.close()

def db_create_table(conn):
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute(
        'CREATE TABLE IF NOT EXISTS persons(name STRING,address STRING)')

    # データベースへコミット。これで変更が反映される。
    conn.commit()

def db_drop_table(conn):
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute(
        'DROP TABLE IF EXISTS persons')

    # データベースへコミット。これで変更が反映される。
    conn.commit()

def db_insert(conn,name,address):
    cur = conn.cursor()

    # personsというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute('INSERT INTO persons(name,address) values(?,?)',(name,address))

    # データベースへコミット。これで変更が反映される。
    conn.commit()

def db_select(conn):
    cur = conn.cursor()
    cur.execute('SELECT name,address FROM persons')
    res_value = cur.fetchall()
    for value in res_value:
        print(value)
    return res_value;

def db_initialize():
    conn = db_connect()
    db_drop_table(conn)
    db_create_table(conn)
    db_close(conn)
