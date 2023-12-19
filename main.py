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
            return redirect(url_for('anasayfa_olcak'))

        return "Invalid email or password. Please try again."

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('main_page'))  # Change 'index' to the desired route

@app.route('/anasayfa_olcak')
def anasayfa_olcak():
    return render_template('anasayfa_olcak.html')




@app.route('/user_page')
def user_page():
    if 'email' in session and session['email'] != None:
        return render_template('user_page.html', orders=get_orders_for_profile(session['email']), email=session['email'])
    else:
        return redirect(url_for('main_page'))


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

            ###### New Code ######
            # Get all the items that have email = session['email'] from the shopping_cart table
            # Generate random order Id
            order_id = random.randint(1, 1000000000)

            insert_into_orders(table = 'shopping_cart', email=session['email'],order_id=order_id)

            ###### End New Code ######
            return redirect(url_for('payment_success'))
        else:
            
            return redirect(url_for('payment_fail'))

    items = get_items(email = session['email'])
    total_price = sum(item[1] * item[2] for item in items)
    return render_template('payment_page.html', items = get_items(email = session['email']), total_price = total_price)


@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')


@app.route('/payment_fail')
def payment_fail():
    return render_template('payment_fail.html')


##### New Code #####
@app.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    items = get_items(session['email'])
    total_price = sum(item[1] * item[2] for item in items)
    return render_template('shopping_cart.html', items=items, total_price=total_price)


# Route to decrease or remove items
@app.route('/decrease_item/<int:item_id>')              
def decrease_item(item_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Decrease quantity for the specified item_id
    update_query = "UPDATE shopping_cart SET quantity = quantity - 1 WHERE item_id = %s"
    cursor.execute(update_query, (item_id,))
    connection.commit()

    # Check if quantity is zero, then remove the row
    check_quantity_query = "SELECT quantity FROM shopping_cart WHERE item_id = %s"
    cursor.execute(check_quantity_query, (item_id,))
    quantity = cursor.fetchone()[0]

    if quantity == 0:
        delete_query = "DELETE FROM shopping_cart WHERE item_id = %s"
        cursor.execute(delete_query, (item_id,))
        connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()

    # Redirect back to the main page after updating the table
    return redirect(url_for('shopping_cart'))


# Route to increase items
@app.route('/increase_item/<int:item_id>')
def increase_item(item_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    # Increase quantity for the specified item_id
    update_query = "UPDATE shopping_cart SET quantity = quantity + 1 WHERE item_id = %s"
    cursor.execute(update_query, (item_id,))
    connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()

    # Redirect back to the main page after updating the table
    return redirect(url_for('shopping_cart'))

# Route to remove an item
@app.route('/remove_item/<int:item_id>')
def remove_item(item_id):

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    #Remove row for the specified item_id
    remove_query = "DELETE FROM shopping_cart WHERE item_id = %s"
    cursor.execute(remove_query, (item_id,))
    connection.commit()
    
    # Close the database connection
    cursor.close()
    connection.close()

    # Redirect back to the main page after removing the item
    return redirect(url_for('shopping_cart'))


##### End New Code #####



app.run(debug=True)