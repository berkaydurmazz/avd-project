from flask import Flask, render_template
import sqlite3
import openai
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)
openai.api_key = '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'
# SQLite veritabanı bağlantısını oluştur
db = 'mydb.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        productName TEXT PRIMARY KEY,
        productPrice INTEGER NOT NULL,
        productURL TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer (
        customerName TEXT PRIMARY KEY,
        budget INTEGER NOT NULL,        
        customerEmail TEXT NOT NULL

    )
''')

# Veritabanı değişikliklerini kaydet ve bağlantıyı kapat
conn.commit()
conn.close()


def sendMail(message, name, email):
    try:
        msg = MIMEText(message)
        msg['Subject'] = 'Budget Changed'
        msg['To'] = email
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login('your_outlook_email@example.com', 'your_password')
        server.sendmail(msg['From'], email, name)
        server.quit()
    except Exception as e:
        print(e)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/askCommentOpenAI')
def askCommentOpenAI(productName):
    productPromt = "Imagine you are a art collector, I will give you a product name and i except a commment from you. I will expect 100 characters reponses. Product name : "
    openaiPromt = productPromt + productName
    message = [{"role": "system", "content": "You are a art collector"}, {
        "role": "user", "content": openaiPromt}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message)
    reply = chat.choices[0].message['content']
    return reply


@app.route('/askMarkettingDetails')
def askMarkettingDetails(productName):
    marketAdviser = "Imagine you are a marketting professonal, I will give you a product name and i except a commment from you. I will expect 100 characters reponses. Product name : "
    openaiPromt = marketAdviser + productName
    message = [{"role": "system", "content": "You are a marketting professonal"}, {
        "role": "user", "content": openaiPromt}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message)
    reply = chat.choices[0].message['content']
    return reply


@app.route('/getProduct')
def getProduct(all):
    if all == True:
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM product", ())
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print(e)
            return False


@app.route('/addProduct')
def addProduct(productName, prodcutPrice, productURL):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO product (productName, prodcutPrice,productURL) VALUES (?, ?)",
                           (productName, prodcutPrice, productURL))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(e)
        return False


@app.route('/updateProduct')
def updateProduct(productPrice, productName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE product SET productPrice = (?) WHERE productName = (?)", (productPrice, productName))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(e)
        return False


@app.route('/deleteProduct')
def deleteProduct(productName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM product WHERE productName = (?)", (productName))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(e)
        return False


@app.route('/getCustomer')
def getCustomer(all):
    if all == True:
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM customer", ())
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print(e)
            return False


@app.route('/addCustomer')
def addCustomer(customerName, budget, customerEmail):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customer (customerName, budget,customerEmail) VALUES (?, ?)",
                           (customerName, budget, customerEmail))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(e)
        return False


@app.route('/updateCustomer')
def updateCustomer(budget, customerName, customerEmail):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE customer SET budget = (?) WHERE customerName = (?)", (budget, customerName))
            conn.commit()
            conn.close()
            sendMail("Budget Updated", customerName, customerEmail)
            return True
    except Exception as e:
        print(e)
        return False


@app.route('/deleteCustomer')
def deleteCustomer(customerName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM customer WHERE customerName = (?)", (customerName))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    app.run(debug=True)
