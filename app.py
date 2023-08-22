from flask import Flask ,render_template
import sqlite3

app = Flask(__name__)

# SQLite veritabanı bağlantısını oluştur
db = 'mydb.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()

# Örnek bir tablo oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL
    )
''')

# Veritabanı değişikliklerini kaydet ve bağlantıyı kapat
conn.commit()
conn.close()

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/getCar')
def getCar():
    print(1)


@app.route('/askCommentOpenAI')
def askCommentOpenAI():
    print(2)


@app.route('/askMarkettingDetails')
def askMarkettingDetails():
    print(3)


@app.route('/createProduct')
def createProduct():
    print(4)


@app.route('/deleteCar')
def deleteCar():
    print(5)
