import mysql.connector
from mysql.connector import Error

db_config ={
    'host': 'sql11.freemysqlhosting.net',
    'database': 'sql11670983',
    'user': 'sql11670983',
    'password': 'T7p8T65KtN',
}


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




def get_orders(email):
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
