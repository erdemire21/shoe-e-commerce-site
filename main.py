from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from utilization import *

app = Flask(__name__)
app.secret_key = '111'


db_config = {
    'host': 'localhost',
    'database': 'login',
    'user': 'root',
    'password': 'E19741453'
}


products = {
    'product1': {
        'name': 'Product 1',
        'price': 10.0,
    },
    'product2': {
        'name': 'Product 2',
        'price': 15.0,
    },
}

@app.route('/')
def browse_items():
    return render_template('index.html', products=products)

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
        return redirect(url_for('login'))



@app.route('/payment_page', methods=['GET', 'POST'])
def payment_page():
    if request.method == 'POST':
        card_number = request.form.get('card-number')

        # Use the is_valid_credit_card function to check if the credit card is valid
        if is_valid_credit_card(card_number):
            # If valid, redirect to payment_success.html
            return redirect(url_for('payment_success'))
        else:
            # If not valid, redirect to payment_fail.html
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