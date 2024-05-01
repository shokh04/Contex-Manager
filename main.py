from typing import List

import psycopg2

db_params = {
    'host': 'localhost',
    'database': 'project',
    'user': 'postgres',
    'password': '1',
    'port': 5432
}


class DbConnect:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = psycopg2.connect(**self.db_params)

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()



class Person:
    def __init__(self,
                 id: int | None = None,
                 fullname: str | None = None,
                 age: int | None = None,
                 email: str | None = None):
        self.id = id
        self.fullname = fullname
        self.age = age
        self.email = email

    def get_person(self):
        with DbConnect(db_params) as cur:
            select_query = 'select * from person;'
            cur.execute(select_query)
            person: List[Person] = []
            for row in cur.fetchall():
                person.append(Person(id=row[0], fullname=row[1], age=row[2], email=row[3]))
            return person

    def save(self):
        with DbConnect(db_params) as cur:
            insert_query = 'insert into person (fullname, age, email) values (%s, %s, %s);'
            insert_params = (self.fullname, self.age, self.email)
            cur.execute(insert_query, insert_params)
            print('INSERT 0 1')

    def __repr__(self):
        return f'Book({self.id} => {self.fullname} => {self.age}, {self.email})'


person = Person(fullname='Shuhrat', age=20, email='shuhratsattorov2004@gmail.com')
person.save()
print(Person().get_person())