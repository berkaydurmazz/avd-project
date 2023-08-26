from flask import Flask, render_template,request, jsonify
import sqlite3
import openai
import smtplib
from email.mime.text import MIMEText


app = Flask(__name__)
openai.api_key = ''
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
#conn.commit()
#conn.close()


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

@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
    if request.method == 'POST':
        try:
            productName=request.form['productName']
            productPrice=request.form['productPrice']
            productURL=request.form['productURL']

            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO product (productName, productPrice,productURL) VALUES (?, ?,?)",
                           (productName, productPrice, productURL))
            conn.commit()
            conn.close()
            return render_template('index.html')
        except Exception as e:
            print(e)
    else:
        return render_template('addProduct.html')
    
@app.route('/getProduct',methods=['GET'])
def getProduct():
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM product")
                data =cursor.fetchall()
                return render_template('products.html', data=data)
        except Exception as e:
            print(e)
            return e
 

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

# Ürün bilgilerini getiren bir fonksiyon
@app.route('/get-product-info')
def get_product_info(productName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product WHERE productName = ?", (productName,))
            product = cursor.fetchone()
            if product:
                return product
            else:
                return None
    except Exception as e:
        print(e)
        return None
@app.route('/updateProduct/<productName>', methods=['POST','GET'])
def updateProduct(productName):
    """ if request.method == 'GET':
        productName = request.args.get('productName')
        product = get_product_info(productName)
        if product:
            return render_template('editProduct.html', product=product)
        else:
            return "Ürün bulunamadı."
    
    el """
    if request.method == 'POST':
        productName = request.form['productName']
        productPrice = request.form['productPrice']
        productURL=request.form['productURL']
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE product SET productPrice = ? WHERE productName = ?", (productPrice, productName,productURL))
                conn.commit()
                return "Ürün güncellendi."
        except Exception as e:
            print(e)
            return "Ürün güncelleme hatası." 
        
#Düzenleme gerekli
""" @app.route('/updateProduct')
def updateProduct(productPrice, productName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE product SET productPrice = (?) WHERE productName = (?)", (productPrice, productName))
            conn.commit()
            return True
    except Exception as e:
        print(e)
        return False """

#Düzenleme gerekli
@app.route('/deleteProduct/<productName>', methods=['POST'])
def deleteProduct(productName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM product WHERE productName = (?)", (productName,))
            conn.commit()
            #conn.close()
            #return True
            return render_template("products.html")
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "An error occurred while deleting the {productName}"})


@app.route('/getCustomer', methods=['GET'])
def getCustomer():
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customer")
            
            # No need to commit for SELECT statements
            data = cursor.fetchall()
            
            # Return the data to the HTML template
            return render_template('customers.html', data=data)
    except Exception as e:
        print(e)
        return "Can not connect to database"
        

@app.route('/addCustomer' , methods=['GET','POST'])
def addCustomer():
    if request.method == 'POST':
        try:
            customerName=request.form['customerName']
            budget=request.form['budget']
            customerEmail=request.form['customerEmail']

            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO customer (customerName, budget,customerEmail) VALUES (?, ?,?)",
                           (customerName, budget, customerEmail))
            conn.commit()
            conn.close()
            return render_template('index.html')
        except Exception as e:
            print(e)
    else:
        return render_template('addCustomer.html')

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


@app.route('/deleteCustomer/<customerName>', methods=['POST'])
def deleteCustomer(customerName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customer WHERE customerName = ?", (customerName,))
            conn.commit() 
        return render_template("customers.html")
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    app.run(debug=True)
