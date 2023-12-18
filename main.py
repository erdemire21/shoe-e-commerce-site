from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from utilization import *
import random

app = Flask(__name__)
# Basically resets the cookie every time the server is restarted
key = random.randint(1, 1000000000)
key = str(key)
app.secret_key = key



@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['new-name']
        new_email = request.form['new-email']
        new_password = request.form['new-password']

        result = add_user_to_database(new_username, new_email, new_password)
        return result

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if authenticate_user(email, password):
            session['email'] = email  # Store the email in the session
            return redirect(url_for('browse2'))

        return "Invalid email or password. Please try again."

    return render_template('login.html')

@app.route('/browse2')
def browse2():
    if 'email' in session:
        return render_template('browse2.html', email=session['email'])
    else:
        return redirect(url_for('main_page'))


# Part of İsmail 


def get_items():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch data from the table (replace 'your_table' with your actual table name)
        query = "SELECT * FROM Shopping_cart"             # cart current
        cursor.execute(query)
        items = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return items

    except Exception as e:
        return []

# Route to display items from the MySQL table
@app.route('/')
def display_items():
    items = get_items()
    total_price = sum(item[2] * item[3] for item in items)
    return render_template('cart.html', items=items, total_price=total_price)

# Route to decrease or remove items
@app.route('/decrease_item/<int:item_id>')                     # <int:item_id> değiştirildi string yapıldı
def decrease_item(item_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Decrease quantity for the specified item_id
    update_query = "UPDATE Shopping_cart SET quantity = quantity - 1 WHERE item_id = %s"
    cursor.execute(update_query, (item_id,))
    connection.commit()

    # Check if quantity is zero, then remove the row
    check_quantity_query = "SELECT quantity FROM Shopping_cart WHERE item_id = %s"
    cursor.execute(check_quantity_query, (item_id,))
    quantity = cursor.fetchone()[0]

    if quantity == 0:
        delete_query = "DELETE FROM Shopping_cart WHERE item_id = %s"
        cursor.execute(delete_query, (item_id,))
        connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()

    # Redirect back to the main page after updating the table
    return redirect(url_for('display_items'))


# Route to increase items
@app.route('/increase_item/<int:item_id>')
def increase_item(item_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    # Increase quantity for the specified item_id
    update_query = "UPDATE Shopping_cart SET quantity = quantity + 1 WHERE item_id = %s"
    cursor.execute(update_query, (item_id,))
    connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()

    # Redirect back to the main page after updating the table
    return redirect(url_for('display_items'))

# Route to remove an item
@app.route('/remove_item/<int:item_id>')
def remove_item(item_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    #Remove row for the specified item_id
    remove_query = "DELETE FROM Shopping_cart WHERE item_id = %s"
    cursor.execute(remove_query, (item_id,))
    connection.commit()
    
    # Close the database connection
    cursor.close()
    connection.close()

    # Redirect back to the main page after removing the item
    return redirect(url_for('display_items'))

# Route to proceed to payment
@app.route('/proceed_to_payment')
def proceed_to_payment():
    # Add logic to handle the payment process
    # (you need to implement this part based on your payment flow)
    return render_template('payment_page.html')


# End of the part of İsmail

@app.route('/payment_page', methods=['GET', 'POST'])
def payment_page():
    if request.method == 'POST':
        card_number = request.form.get('card-number')

        
        if is_valid_credit_card(card_number):
            address = request.form['address']
            card_name = request.form['card-name']
            expiration_date = request.form['expiration-date']
            cvv = request.form['cvv']

            insert_private_info(address, card_name, card_number, expiration_date, cvv, session['email'])

            return redirect(url_for('payment_success'))
        else:
            
            return redirect(url_for('payment_fail'))

    # If it's a GET request, render the 'payment_page.html' template
    return render_template('payment_page.html')


@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')


@app.route('/payment_fail')
def payment_fail():
    return render_template('payment_fail.html')



app.run(debug=True)
