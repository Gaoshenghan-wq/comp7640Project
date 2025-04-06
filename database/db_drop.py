import pymysql
from db_connection import get_db_connection


def drop_tables():
    connection = get_db_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 按顺序删除表，避免外键约束问题
                cursor.execute("DROP TABLE IF EXISTS order_items")
                cursor.execute("DROP TABLE IF EXISTS customer_order_history")
                cursor.execute("DROP TABLE IF EXISTS orders")
                cursor.execute("DROP TABLE IF EXISTS product_tag_relations")
                cursor.execute("DROP TABLE IF EXISTS product_tags")
                cursor.execute("DROP TABLE IF EXISTS products")
                cursor.execute("DROP TABLE IF EXISTS customers")
                cursor.execute("DROP TABLE IF EXISTS vendors")
            connection.commit()
            print("Tables dropped successfully.")
        except pymysql.Error as e:
            print(f"Error dropping tables: {e}")
        finally:
            connection.close()


if __name__ == "__main__":
    drop_tables()