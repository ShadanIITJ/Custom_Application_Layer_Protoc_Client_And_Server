import sqlite3
from sqlite3 import Error

def connect():
    db = None
    try:
        db = sqlite3.connect("database.db")
        return db
    except Error as e:
        print(e)

    return db

def create_table(db):
    try:
        c = db.cursor()
        c.execute('CREATE TABLE info(Email text PRIMARY KEY, Name text NOT NULL, Address text NOT NULL, Profession text NOT NULL, Phone_Number int NOT NULL)')
    except Error as e:
        print(e)

def insert(db, data):  # data = [email,name,address,profession,phoennumber]
    try:
        sql_query = ''' INSERT INTO info(Email,Name,Address,Profession,Phone_Number)
                VALUES(?,?,?,?,?) '''
        c = db.cursor()
        c.execute(sql_query, data)
        db.commit()
        return f"{data[1]} was added sucessfully"
    except Error as e:
        return "DataBase Error:"

def delete(db, email, flag = True):
    c = db.cursor()
    c.execute("SELECT * FROM info WHERE Email=?", (email,))
    data = c.fetchall()
    if len(data) == 0:
        return "Can't delete as it doesn't exist"
    else:
        if flag:
            sql_query = 'DELETE FROM info WHERE Email=?'
            c.execute(sql_query, (email,))
            db.commit()
            return "entry deleted"
        else:
            return "You cancelled the process"

def clear_database(db, flag = True):
    if flag:
        sql_query = 'DELETE FROM info'
        c = db.cursor()
        c.execute(sql_query)
        db.commit()
        print("database cleared")
    else:
        print("You cancelled the process")

def get_all(db):
    c = db.cursor()
    c.execute("SELECT * FROM info")
    rows = c.fetchall()
    #print(type(rows[0]))
    if len(rows) == 0:
        return None
    else:
        return rows


def get_by_email(db, email):
    c = db.cursor()
    c.execute("SELECT * FROM info WHERE Email=?", (email,))
    data = c.fetchall()
    if len(data) == 0:
        return None
    else:
        return data[0]



def update(db,email,data):   # data = [name,address,profession,phoennumber]
    c = db.cursor()
    c.execute("SELECT * FROM info WHERE Email=?", (email,))
    row = c.fetchall()
    if len(row) == 0:
        return None
    else:
        data.append(email)   
        sql_query = ''' UPDATE info SET Name = ? , Address = ? , Profession = ?, Phone_Number = ? WHERE Email = ?'''
        c.execute(sql_query, data)
        db.commit()
        return f"{data[0]} was added sucessfully"




