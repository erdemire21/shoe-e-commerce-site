from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from util_ismail import *

app = Flask(__name__)
app.secret_key = "'111'"


db_config ={
    'host': 'sql11.freemysqlhosting.net',
    'database': 'sql11670983',
    'user': 'sql11670983',
    'password': 'T7p8T65KtN',
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

current_email = "t@t.com"
userId = 1
product = get_all_shoes()

order_type = request.form.get('order')                  #new sorting
if order_type=descent:
    product = descent_get_shoe() 
if order_type=ascent:
    product = ascent_get_shoe()                   #new sorting

order = get_orders(current_email)

@app.route('/')
def browse_items():
    return render_template('deneme.html', products=product, mail=current_email)




@app.route('/user_page')
def user_page():
    return render_template('user_page.html', orders=order, email=current_email)


# Assuming you have db_config defined somewhere with your MySQL database configuration

@app.route('/add_item', methods=['POST'])
def add_item():
    item_id = request.form.get('item_id')
    price = request.form.get('price')
    price = float(str(price[1:]))
    quantity = 1
    email = current_email
    brand = request.form.get('brand')
    model = request.form.get('model')

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Check if the item with the given item_id already exists
    
    select_query = "SELECT quantity FROM shopping_cart WHERE item_id = %s"
    cursor.execute(select_query, (item_id,))
    quan = cursor.fetchone()
    

    if quan:
        # If the item exists, update the quantity
        update_query = "UPDATE shopping_cart SET Quantity = Quantity + 1 WHERE item_id = %s;"
        cursor.execute(update_query, (item_id,))
        connection.commit()
    else:
        # If the item does not exist, insert a new row
        add_query = "INSERT INTO shopping_cart (item_id, Price, Quantity, email, brand, model) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(add_query, (item_id, price, quantity, email, brand, model,))
        connection.commit()

    cursor.close()
    connection.close()
    return render_template('deneme.html', products=product, mail=current_email)  

    
@app.route('/login')
def login():
    return render_template('login.html')
app.run(debug=True)
