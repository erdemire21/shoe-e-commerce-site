from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from utilization_ali import *

app = Flask(__name__)
app.secret_key = '111'


db_config ={
    'host': 'sql11.freemysqlhosting.net',
    'database': 'sql11670983',
    'user': 'sql11670983',
    'password': 'T7p8T65KtN',
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    )
'''
cursor.execute(create_table_query)

email = "'t@t.com'"
userId = 1
product = get_all_shoes()

order = get_orders(email)

@app.route('/')
def browse_items():
    return render_template('listing.html', products=product)



@app.route('/user_page')
def user_page():
    return render_template('user_page.html', orders=order)


from flask import Flask, render_template
import mysql.connector

app = Flask(_name_)

# Assuming you have db_config defined somewhere with your MySQL database configuration

@app.route('/add_item/<int:item_id>/<float:price>/<int:quantity>/<string:name>/<string:email>')
def add_item(item_id, price, quantity, name, email):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    add_query = "INSERT INTO shopping_cart (item_id, Price, Quantity, Name, email) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(add_query, (item_id, price, quantity, name, email))

    connection.commit()

    cursor.close()
    connection.close()
    return render_template('listing.html', products=product)

    
@app.route('/add_to_database', methods=['POST'])
def add_to_database():
    data = request.json
    cart = data.get('cart', [])

    try:
        # Insert items from the cart into the MySQL table
        insert_query = 'INSERT INTO products (name, price) VALUES (%s, %s)'
        for product in cart:
            cursor.execute(insert_query, (product['name'], product['price']))
        # Commit the changes to the database
        connection.commit()

        return jsonify(result='success')

    except Exception as e:
        print(f"Error inserting into database: {e}")
        connection.rollback()
        return jsonify(result='error')

# Your existing routes and other code...

app.run(debug=True)
