import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Creation of tables or dropping if they already exist
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

'''Here you can choose to enter a file name
or to proceed using the saved one by pressing start.'''

fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'roster_data.json'

#Example of the roster json file
# list[0] is the name of the user
# list[1] is the name of the class
# list[2] is the type of user (0 is student, 1 is teacher)

# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

#Opening the data
str_data = open(fname).read()
json_data = json.loads(str_data)

'''This for loop takes the information and put them into the previously created DB
First　it puts the data (name) into the User tables
Second it puts the data (course title) into the Course table
Third it puts the data into the Member table, by taking elements from the previous
two tables, creating a many to many relationship.'''

for entry in json_data:

    name = entry[0];
    title = entry[1];
    role = entry[2];

    print name, title, role

    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )

    conn.commit()
