import sqlite3
import logging
import pandas as pd

def float_price(price):
    price = price[2:].replace('.','').replace(',','.')
    return float(price)

def show_selected_products():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * from products")
        data = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error("Database error: %s" % e)
    except Exception as e:
        logging.error("Exception in _query: %s" % e)
    else:
        return  data
    finally:
        if conn:
            conn.close()

def analysis():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        df = pd.read_sql_query("SELECT * from products", conn)
    except sqlite3.Error as e:
        logging.error("Database error: %s" % e)
    except Exception as e:
        logging.error("Exception in _query: %s" % e)
    else:
        print('\nPreços:')
        print(df['price'].describe())
    finally:
        if conn:
            conn.close()

def insert(selected_product):
    print(selected_product['price'])
    selected_product['price'] = float_price(selected_product['price'])
    list_product = [ v for v in selected_product.values() ]
    list_product = tuple(list_product)
    print(list_product)
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        
        cursor.execute("""
                        INSERT INTO products (link, title, price, email)
                        VALUES (?,?,?,?)""", list_product)
    except sqlite3.Error as e:
        logging.error("Database error: %s" % e)
    except Exception as e:
        logging.error("Exception in _query: %s" % e)
    else:
        conn.commit()
        print('sucessfully added')
    finally:
        if conn:
            conn.close()

def clean():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products')
    except sqlite3.Error as e:
        logging.error("Database error: %s" % e)
    except Exception as e:
        logging.error("Exception in _query: %s" % e)
    else:
        conn.commit()
        print('sucessfully cleaned')
    finally:
        if conn:
            conn.close()

def update(product_id, new_price):
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET price = ? WHERE id = ?',(new_price, product_id))
    except sqlite3.Error as e:
        logging.error("Database error: %s" % e)
    except Exception as e:
        logging.error("Exception in _query: %s" % e)
    else:
        conn.commit()
        print('sucessfully updated')
    finally:
        if conn:
            conn.close()