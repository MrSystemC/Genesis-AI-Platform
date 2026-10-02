#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "=== Genesis-3.0.3 Persistent Data Platform ==="


mkdir -p storage30
mkdir -p database30
mkdir -p backup30


touch storage30/__init__.py
touch database30/__init__.py
touch backup30/__init__.py



echo "[1] SQLite database layer"


printf '%s\n' \
'import sqlite3' \
'' \
'class Database:' \
'' \
'    def __init__(self):' \
'        self.conn=sqlite3.connect("genesis30.db")' \
'        self.create()' \
'' \
'    def create(self):' \
'        cursor=self.conn.cursor()' \
'' \
'        cursor.execute("' \
'        CREATE TABLE IF NOT EXISTS users (' \
'        "id INTEGER PRIMARY KEY,' \
'        "name TEXT)' \
'        ")"' \
'' \
'        cursor.execute("' \
'        CREATE TABLE IF NOT EXISTS universes (' \
'        "id INTEGER PRIMARY KEY,' \
'        "name TEXT,' \
'        "age INTEGER)' \
'        ")"' \
'' \
'        self.conn.commit()' \
'' \
'    def add_user(self,name):' \
'        self.conn.execute(' \
'        "INSERT INTO users(name) VALUES(?)",' \
'        (name,)' \
'        )' \
'        self.conn.commit()' \
'' \
'    def add_universe(self,name,age):' \
'        self.conn.execute(' \
'        "INSERT INTO universes(name,age) VALUES(?,?)",' \
'        (name,age)' \
'        )' \
'        self.conn.commit()' \
'' \
'    def status(self):' \
'        users=self.conn.execute("SELECT * FROM users").fetchall()' \
'        worlds=self.conn.execute("SELECT * FROM universes").fetchall()' \
'        return {' \
'        "users":users,' \
'        "universes":worlds' \
'        }' \
> database30/sqlite.py



echo "[2] Persistent storage"


printf '%s\n' \
'class Storage:' \
'' \
'    def __init__(self):' \
'        self.data={}' \
'' \
'    def save(self,key,value):' \
'        self.data[key]=value' \
'' \
'    def load(self,key):' \
'        return self.data.get(key)' \
'' \
'    def all(self):' \
'        return self.data' \
> storage30/system.py



echo "[3] Backup system"


printf '%s\n' \
'class Backup:' \
'' \
'    def __init__(self):' \
'        self.backups=[]' \
'' \
'    def create(self,data):' \
'        self.backups.append(data)' \
'' \
'    def list(self):' \
'        return self.backups' \
> backup30/system.py



echo "[4] Persistence test"


printf '%s\n' \
'from database30.sqlite import Database' \
'from storage30.system import Storage' \
'from backup30.system import Backup' \
'' \
'db=Database()' \
'storage=Storage()' \
'backup=Backup()' \
'' \
'db.add_user("Founder")' \
'db.add_universe("Genesis Prime",10)' \
'' \
'storage.save("status","running")' \
'' \
'backup.create(' \
'db.status()' \
')' \
'' \
'print("DATABASE")' \
'print(db.status())' \
'' \
'print("STORAGE")' \
'print(storage.all())' \
'' \
'print("BACKUP")' \
'print(backup.list())' \
> persistence_test.py



echo "Checking syntax..."

python -m py_compile \
database30/sqlite.py \
storage30/system.py \
backup30/system.py \
persistence_test.py



echo "Running persistence test..."

python persistence_test.py


echo "=== Genesis-3.0.3 COMPLETE ==="

