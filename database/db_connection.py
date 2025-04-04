import pymysql

# 本地或者云数据库
def get_db_connection():
    try:
        connection = pymysql.connect(
            host='mysql.sqlpub.com',
            port=3306,
            user='comp7640project',
            password='fBAkzuQ5ddnsAYVc',
            database='comp7640db233',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Database connection error: {e}")
        return None
    
