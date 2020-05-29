import sqlite3
import logging

try:
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE products (
        id INTENGER NOT NULL PRIMARY KEY,
        link VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        price DOUBLE NOT NULL,
        email VARCHAR NOT NULL
    );
    """)

except sqlite3.Error as e:
    logging.error("Database error: %s" % e)
except Exception as e:
    logging.error("Exception in _query: %s" % e)
else:
    print('Database created')
finally:
    if conn:
        conn.close()
