from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL configurations
mysql_config = {
    'host': 'sql11.freemysqlhosting.net',
    'user': 'sql11670983',
    'password': 'T7p8T65KtN',
    'database': 'sql11670983',
}

# Establish a MySQL connection
connection = mysql.connector.connect(**mysql_config)
cursor = connection.cursor()

# Create a table if not exists
create_table_query = '''
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    )
'''
cursor.execute(create_table_query)

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

if __name__ == '__main__':
    app.run(debug=True)
