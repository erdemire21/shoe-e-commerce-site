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