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
        msg['From'] = 'productcommenterai@outlook.com'
        msg['To'] = email
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login('', '')
        server.sendmail(msg['From'], email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred:", e)

@app.route('/details/<productName>', methods=['GET'])
def comments(productName):
    product = get_product_info(productName)
    if product:
            comment1 =askCommentOpenAI(productName)
            comment2 =askCommentOpenAI(productName)
            comment3 =askCommentOpenAI(productName)
            comment4 =askCommentOpenAI(productName)
            comment5 =askCommentOpenAI(productName)
            detail=askMarkettingDetails(productName)
            return render_template('comments.html', product=product,comment1=comment1,comment2=comment2,comment3=comment3,comment4=comment4,comment5=comment5,detail=detail)
    else:
            return "Ürün bulunamadı."

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
    productPromt = """Imagine you are a store sales manager, I will give you a product name and i expect good or bad a comment from you.
    Do not specify or enumerate it .I will expect 100 characters reponses. Product name : """
    openaiPromt = productPromt + productName
    message = [{"role": "system", "content": "You are a store sales manager"}, {
        "role": "user", "content": openaiPromt}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.7,  # Adjust the temperature for creativity
    )
    reply = chat.choices[0].message['content']
    print(reply) 
    return reply

@app.route('/askMarkettingDetails')
def askMarkettingDetails(productName):
    marketAdviser = """Imagine you are a marketting  professional, I will give you a product name and I expect an description about the product  in a few sentences from you.
      I will expect 100 characters reponses.Do not write again product name Product name : """
    openaiPromt = marketAdviser + productName
    message = [{"role": "system", "content": "You are a marketting  professional"}, {
        "role": "user", "content": openaiPromt}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.7,)
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
                return False
    except Exception as e:
        print(e)
        return False
    
@app.route('/updateProduct/<productName>', methods=['POST','GET'])
def updateProduct(productName):
     if request.method == 'GET':
        product = get_product_info(productName)
        if product:
            return render_template('editProduct.html', product=product)
        else:
            return "Ürün bulunamadı."
    
     elif request.method == 'POST':
        productName = request.form['productName']
        productPrice = request.form['productPrice']
        productURL=request.form['productURL']
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE product SET productName = ?, productPrice = ?, productURL = ? WHERE productName = ?", (productName, productPrice, productURL, productName))
                conn.commit()
                return render_template("index.html")
        except Exception as e:
            print(e)
            return "Ürün güncelleme hatası." 
        

@app.route('/deleteProduct/<productName>', methods=['POST'])
def deleteProduct(productName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM product WHERE productName = (?)", (productName,))
            conn.commit()
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
            data = cursor.fetchall()
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

@app.route('/get-customer-info')
def get_customer_info(customerName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customer WHERE customerName = ?", (customerName,))
            customer = cursor.fetchone()
            if customer:
                return customer
            else:
                return False
    except Exception as e:
        print(e)
        return False

@app.route('/updateCustomer/<customerName>', methods=['POST','GET'])
def updateCustomer(customerName):
    if request.method == 'GET':
        customer = get_customer_info(customerName)
        if customer:
            return render_template('editCustomer.html', customer=customer)
        else:
            return "Müşteri bulunamadı."
    elif request.method == 'POST':
        customerName = request.form['customerName']
        budget= request.form['budget']
        customerEmail=request.form['customerEmail']
        try:
            with sqlite3.connect(db) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE customer SET customerName = ?, budget = ?, customerEmail = ? WHERE customerName = ?", (customerName, budget, customerEmail, customerName))
                conn.commit()
                sendMail("Budget Updated", customerName, customerEmail)
                return render_template("index.html")
        except Exception as e:
            print(e)
            return "Müşteri güncelleme hatası."


@app.route('/deleteCustomer/<customerName>', methods=['POST'])
def deleteCustomer(customerName):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customer WHERE customerName = ?", (customerName,))
            conn.commit() 
        return render_template("index.html")
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    app.run(debug=True)
