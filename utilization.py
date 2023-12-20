import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'sql11.freemysqlhosting.net',
    'database': 'sql11670983',
    'user': 'sql11670983',
    'password': 'T7p8T65KtN',
    'port': 3306,
}

def add_user_to_database(username, email, password):
    """
    Add a new user to the database.

    Args:
        username (str): The username of the new user.
        email (str): The email of the new user.
        password (str): The password of the new user.

    Returns:
        str: A message indicating the result of the registration process.

    Raises:
        Error: If there is an error during the database operation.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the email is already in use
        check_query = "SELECT * FROM user_info WHERE email = %s"
        cursor.execute(check_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Email is already in use. Choose a different one."

        # Insert the new user into the database
        insert_query = "INSERT INTO user_info (create_time, name, email, password) VALUES (NOW(), %s, %s, %s)"
        cursor.execute(insert_query, (username, email, password))
        connection.commit()

        return "Registration successful!"

    except Error as e:
        return f"Error: {e}"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def authenticate_user(email, password):
    """
    Authenticates a user by checking their email and password against the database.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check user credentials
        query = "SELECT * FROM user_info WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def is_valid_credit_card(card_number):
    """
    Check if a credit card number is valid.
    Example working card numbers: 5555555555554444
    Args:
        card_number (str): The credit card number to be validated.

    Returns:
        bool: True if the credit card number is valid, False otherwise.
    """
    # Remove spaces and reverse the card number
    card_number = card_number.replace(" ", "")[::-1]

    # Ensure the card number is a valid numeric string
    if not card_number.isdigit():
        return False

    total = 0
    alternate = False

    for digit in card_number:
        digit = int(digit)

        if alternate:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit
        alternate = not alternate

    return total % 10 == 0


def insert_private_info(address, card_name, card_number, expiration_date, cvv,email):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_private_info (address, card_name, card_number, expiration_date, cvv, email)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (address, card_name, card_number, expiration_date, cvv, email))

    conn.commit()
    conn.close()


def get_items(email):
    """
    Retrieve items from the Shopping_cart table based on the provided query.

    Args:
        query (str): The SQL query to execute (default is "SELECT * FROM Shopping_cart").

    Returns:
        list: A list of items retrieved from the database.

    """
    query = f"SELECT * FROM shopping_cart_with_product_names WHERE email = '{email}'"
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(query)
        items = cursor.fetchall()

        cursor.close()
        connection.close()

        return items

        # products = [{"name": product[5], "price": product[2]} for product in items]
        # return products
    except Exception as e:
        return {}


def get_items_as_dictionary(email):
    """
    Retrieve items from the Shopping_cart table based on the provided query.

    Args:
        query (str): The SQL query to execute (default is "SELECT * FROM Shopping_cart").

    Returns:
        list: A list of items retrieved from the database.

    """
    query = f"SELECT * FROM shopping_cart_with_product_names WHERE email = '{email}'"
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(query)
        items = cursor.fetchall()

        cursor.close()
        connection.close()

        products = [{"name": product[4], "price": product[1]} for product in items]
        return products
    except Exception as e:
        return {}
    

def delete_items_by_email_from_shopping_cart(email):
    """
    Delete all entries in the Shopping_cart table where the email column has the specified value.

    Args:
        email (str): The email value to match for deletion.

    Returns:
        bool: True if the deletion is successful, False otherwise.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # SQL query to delete entries with a specific email value
        delete_query = f"DELETE FROM Shopping_cart WHERE email = '{email}'"
        
        cursor.execute(delete_query)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def insert_into_orders(table, email, order_id):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Select rows from shopping_cart based on the provided email
        select_query = f"SELECT item_id, quantity, email FROM {table} WHERE email = '{email}'"
        cursor.execute(select_query)
        rows_to_insert = cursor.fetchall()

        # Insert selected rows into the orders table with the specified order_id
        for row in rows_to_insert:
            item_id, quantity, _ = row  # Extract values from the row
            insert_query = f"INSERT INTO orders (order_id, item_id, quantity, email) VALUES ({order_id}, {item_id}, {quantity}, '{email}')"
            cursor.execute(insert_query)

        # Delete the selected rows from the shopping_cart table
        delete_query = f"DELETE FROM {table} WHERE email = '{email}'"
        cursor.execute(delete_query)

        # Commit the changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()

        print(f"Rows inserted into 'orders' table and removed from '{table}' successfully.")
    except Exception as e:
        print(f"Error: {e}")
        

## Previous parts belonged to Emre Hakan Erdemir Now the next part belongs to Alihan Yalcin
##############
##############
def get_orders_for_profile(email):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    

    u_orders = "SELECT item_id, quantity FROM  orders WHERE orders.email=%s;"

    cursor.execute(u_orders, (email,))
    orders = cursor.fetchall()
    #order = order_id, item_id, quantity, mail, price

    
    products=[]
    for order in orders:
        item_id = order[0]
        current_query = "SELECT item_id, Brand, Model, Type, Gender, Size, Color, Material, Price, Image_URL FROM shoe_info WHERE item_id=%s;"
        cursor.execute(current_query, (item_id,))
        product = cursor.fetchall()
        products.append([product, order[1]])
    cursor.close()
    connection.close()
    return products



def descent_get_shoes():
    # Use a context manager for the cursor
    try:
        connection = mysql.connector.connect(**db_config)

        with connection.cursor() as cursor:
            display_all = "SELECT item_id, Brand, Model, Type, Gender, Size, Color, Material, Price, Image_URL FROM shoe_info ORDER BY CAST(SUBSTRING(Price, 2) AS SIGNED) DESC;"
            cursor.execute(display_all)
            shoes = cursor.fetchall()

        # The connection will be closed automatically when exiting the 'with' block

        return shoes

    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return None



def ascent_get_shoes():
    # Use a context manager for the cursor
    try:
        connection = mysql.connector.connect(**db_config)

        with connection.cursor() as cursor:
            display_all = "SELECT item_id, Brand, Model, Type, Gender, Size, Color, Material, Price, Image_URL FROM shoe_info ORDER BY CAST(SUBSTRING(Price, 2) AS SIGNED) ASC;"
            cursor.execute(display_all)
            shoes = cursor.fetchall()

        # The connection will be closed automatically when exiting the 'with' block

        return shoes

    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return None

def get_all_shoes():
    # Use a context manager for the cursor
    try:
        connection = mysql.connector.connect(**db_config)

        with connection.cursor() as cursor:
            display_all = "SELECT item_id, Brand, Model, Type, Gender, Size, Color, Material, Price, Image_URL FROM shoe_info;"
            cursor.execute(display_all)
            shoes = cursor.fetchall()

        # The connection will be closed automatically when exiting the 'with' block

        return shoes

    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return None


def get_men_shoes():
    try:
        connection = mysql.connector.connect(**db_config)

        with connection.cursor() as cursor:
            display_all = "SELECT item_id, Brand, Model, Type, Gender, Size, Color, Material, Price, Image_URL FROM shoe_info WHERE Gender='Men';"
            cursor.execute(display_all)
            shoes = cursor.fetchall()

        # The connection will be closed automatically when exiting the 'with' block

        return shoes

    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return None
    
def get_women_shoes():
    try:
        connection = mysql.connector.connect(**db_config)

        with connection.cursor() as cursor:
            display_all = "SELECT item_id, Brand, Model, Type, Gender, Size, Color, Material, Price, Image_URL FROM shoe_info WHERE Gender='Women';"
            cursor.execute(display_all)
            shoes = cursor.fetchall()

        # The connection will be closed automatically when exiting the 'with' block

        return shoes

    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return None
    
def get_brand_shoes(brand):
    try:
        connection = mysql.connector.connect(**db_config)

        with connection.cursor() as cursor:
            display_all = "SELECT item_id, Brand, Model, Type, Gender, Size, Color, Material, Price, Image_URL FROM shoe_info WHERE Brand=%s;"
            cursor.execute(display_all, (brand,))
            shoes = cursor.fetchall()

        # The connection will be closed automatically when exiting the 'with' block

        return shoes

    except mysql.connector.Error as err:
        # Handle database errors
        print(f"Error: {err}")
        return None