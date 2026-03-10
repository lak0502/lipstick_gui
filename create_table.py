sql = '''
  create table lipstick (
    id integer primary key,
    color text not null,
    texture text not null,
    price integer not null
  );
'''

from db_connect import db, cursor
cursor.execute(sql)
db.commit()
