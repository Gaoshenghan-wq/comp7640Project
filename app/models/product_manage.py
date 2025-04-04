from database.db_connection import get_db_connection
from tkinter import messagebox

class ProductManage:
    @staticmethod
    def format_product_list(products):
        # Define fixed column widths
        col_widths = {
            'product_id': 12,
            'name': 20,
            'price': 10,
            'vendor_id': 12
        }

        # Create the header with fixed column widths
        header = (
            f"{'ProductID'.ljust(col_widths['product_id'])} | "
            f"{'Name'.ljust(col_widths['name'])} | "
            f"{'Price'.ljust(col_widths['price'])} | "
            f"{'VendorID'.ljust(col_widths['vendor_id'])}\n"
        )

        # Separator line
        separator = "-" * (sum(col_widths.values()) + 9) + "\n"  # 9 for spaces and pipes

        # Format each product with fixed column widths
        rows = []
        for product in products:
            product_line = (
                f"{str(product['product_id']).ljust(col_widths['product_id'])} | "
                f"{str(product['name']).ljust(col_widths['name'])} | "
                f"{str(product['price']).ljust(col_widths['price'])} | "
                f"{str(product['vendor_id']).ljust(col_widths['vendor_id'])}"
            )
            rows.append(product_line)

        return header + separator + "\n".join(rows)

    @staticmethod
    def GET(vendor_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE vendor_id = %s", (vendor_id,))
                products = cursor.fetchall()
                if not products:
                    return "No products found for this vendor."
                return ProductManage.format_product_list(products)
        finally:
            conn.close()

    @staticmethod
    def ADD(name, price, vendor_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO products (name, price, vendor_id) VALUES (%s, %s, %s)", (name, price, vendor_id))
                conn.commit()
                messagebox.showinfo("Success", "Product added successfully.")
        finally:
            conn.close()

    @staticmethod
    def SEARCH(keyword):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT * FROM products
                WHERE name LIKE %s
                OR product_id IN (
                    SELECT product_id FROM product_tag_relations
                    JOIN product_tags ON product_tag_relations.tag_id = product_tags.tag_id
                    WHERE product_tags.tag_name LIKE %s
                )
                """
                cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
                products = cursor.fetchall()
                if not products:
                    return "No products found matching the keyword."
                return ProductManage.format_product_list(products)
        finally:
            conn.close()

    @staticmethod
    def RECORD_PURCHASE(customer_id, product_id, quantity, price_at_purchase):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO orders (customer_id, order_date, status) VALUES (%s, NOW(), 'Pending')", (customer_id,))
                order_id = cursor.lastrowid
                cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s)",
                               (order_id, product_id, quantity, price_at_purchase))
                conn.commit()
                # messagebox.showinfo("Success", "Purchase recorded successfully.")
        finally:
            conn.close()
