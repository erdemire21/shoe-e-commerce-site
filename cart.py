from flask import Flask, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'sql11.freemysqlhosting.net',
    'user': 'sql11670983',
    'password': 'T7p8T65KtN',
    'database': 'sql11670983',
}

# Function to fetch items from the table
def get_items():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch data from the table (replace 'your_table' with your actual table name)
        query = "SELECT * FROM shopping_cart"             # cart current
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
    return redirect(url_for('display_items'))


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
    return redirect(url_for('display_items'))

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
    return redirect(url_for('display_items'))

# Route to proceed to payment
@app.route('/proceed_to_payment')
def proceed_to_payment():
    # Add logic to handle the payment process
    # (you need to implement this part based on your payment flow)
    return render_template('payment_page.html')

if __name__ == '__main__':
    app.run(debug=True)
