from database.db_connection import get_db_connection
from tkinter import messagebox


class OrderManage:
    @staticmethod
    def format_order_list(orders):
        col_widths = {
            'order_id': 10,
            'customer_id': 10,
            'product_name': 20,
            'quantity': 10,
            'unit_price': 10,
            'status': 10
        }

        header = (
            f"{'OrderID'.ljust(col_widths['order_id'])} | "
            f"{'CustomerID'.ljust(col_widths['customer_id'])} | "
            f"{'ProductName'.ljust(col_widths['product_name'])} | "
            f"{'Quantity'.ljust(col_widths['quantity'])} | "
            f"{'Unit Price'.ljust(col_widths['unit_price'])} | "
            f"{'Status'.ljust(col_widths['status'])}\n"
        )

        separator = "-" * (sum(col_widths.values()) + 15) + "\n"

        rows = []
        for order in orders:
            order_line = (
                f"{str(order['order_id']).ljust(col_widths['order_id'])} | "
                f"{str(order['customer_id']).ljust(col_widths['customer_id'])} | "
                f"{str(order['product_name']).ljust(col_widths['product_name'])} | "
                f"{str(order['quantity']).ljust(col_widths['quantity'])} | "
                f"{str(order['price']).ljust(col_widths['unit_price'])} | "
                f"{str(order['status']).ljust(col_widths['status'])}"
            )
            rows.append(order_line)

        return header + separator + "\n".join(rows)

    @staticmethod
    def CREATE_ORDER(customer_id, product_info):
        if not product_info:
            messagebox.showerror("Error", "You must add at least one product to the order.")
            return
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO orders (customer_id, status) VALUES (%s, 'Pending')", (customer_id,))
                order_id = cursor.lastrowid
                for product_id, quantity in product_info:
                    cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
                    price_result = cursor.fetchone()
                    if price_result:
                        price = price_result['price']
                        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                                       (order_id, product_id, quantity, price))
                conn.commit()
                messagebox.showinfo("Success", "Order created successfully.")
        finally:
            conn.close()

    @staticmethod
    def GET_ORDERS():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT o.order_id, o.customer_id, p.name as product_name, oi.quantity, p.price, o.status
                    FROM orders o
                    JOIN order_items oi ON o.order_id = oi.order_id
                    JOIN products p ON oi.product_id = p.product_id
                """
                cursor.execute(query)
                orders = cursor.fetchall()
                if not orders:
                    return "No orders found."
                return OrderManage.format_order_list(orders)
        finally:
            conn.close()

    @staticmethod
    def REMOVE_PRODUCT_FROM_ORDER(order_id, product_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM order_items WHERE order_id = %s AND product_id = %s", (order_id, product_id))
                conn.commit()
                messagebox.showinfo("Success", "Product removed from order successfully.")
        finally:
            conn.close()

    @staticmethod
    def CANCEL_ORDER(order_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
                cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
                conn.commit()
                messagebox.showinfo("Success", "Order cancelled successfully.")
        finally:
            conn.close()

    @staticmethod
    def CHANGE_ORDER_STATUS(order_id, new_status):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_status, order_id))
                conn.commit()
                messagebox.showinfo("Success", "Order status changed successfully.")
        finally:
            conn.close()

    @staticmethod
    def GET_ORDER_ITEMS_BY_ORDER_ID(order_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT oi.order_item_id, p.name as product_name,p.product_id as product_id, oi.quantity, p.price
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.product_id
                    WHERE oi.order_id = %s
                """
                cursor.execute(query, (order_id,))
                order_items = cursor.fetchall()
                if not order_items:
                    return "No order items found for this order ID."
                col_widths = {
                    'order_item_id': 12,
                    'product_id': 9,
                    'product_name': 20,
                    'quantity': 10,
                    'unit_price': 10
                }
                header = (
                    f"{'OrderItemID'.ljust(col_widths['order_item_id'])} | "
                    f"{'ProductID'.ljust(col_widths['product_id'])} | "
                    f"{'ProductName'.ljust(col_widths['product_name'])} | "
                    f"{'Quantity'.ljust(col_widths['quantity'])} | "
                    f"{'Unit Price'.ljust(col_widths['unit_price'])}\n"
                )
                separator = "-" * (sum(col_widths.values()) + 9) + "\n"
                rows = []
                for item in order_items:
                    item_line = (
                        f"{str(item['order_item_id']).ljust(col_widths['order_item_id'])} | "
                        f"{str(item['product_id']).ljust(col_widths['product_id'])} | "
                        f"{str(item['product_name']).ljust(col_widths['product_name'])} | "
                        f"{str(item['quantity']).ljust(col_widths['quantity'])} | "
                        f"{str(item['price']).ljust(col_widths['unit_price'])}"
                    )
                    rows.append(item_line)
                return header + separator + "\n".join(rows)
        finally:
            conn.close()