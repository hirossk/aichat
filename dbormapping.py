from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLiteデータベースに接続する
# echo=TrueでデータベースアクセスのSQL文がエコーバックされる
engine = create_engine('sqlite:///example.db', echo=True)

# データベースのテーブルは、このクラスを継承して作成する
Base = declarative_base()

# モデルクラスを作成する
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

# データベースのテーブルを作成する
Base.metadata.create_all(engine)

# データ処理するためにデータベースセッションを作成する
DbSession = sessionmaker(bind=engine)
db_session = DbSession()

# Userの新しいインスタンスを作成する
user = User(name='John', address='Japan')
# セッションを使ってデータを追加する
db_session.add(user)
# データベースへの変更を確定する
db_session.commit()

# データを取得するには、 query() メソッドを使用する
users = db_session.query(User).all()
# データを表示する
for user in users:
    print(user.id, user.name, user.address)

# データを更新するには、 query() メソッドでオブジェクトを取得しプロパティ変更後commitする
user = db_session.query(User).filter_by(name='John').first()
user.address = 'Sapporo Japan'
# データベースへの変更を確定する
db_session.commit()

# データを削除するには、 query() メソッドでオブジェクトを取得しdeleteメソッドを呼び出す
user = db_session.query(User).filter_by(name='John').first()
db_session.delete(user)
# データベースへの変更を確定する
db_session.commit()
