from database.db_connection import get_db_connection
from tkinter import messagebox


class CustomerManage:
    @staticmethod
    def format_customer_list(customers):
        col_widths = {
            'customer_id': 12,
            'contact_number': 20,
            'shipping_details': 30
        }

        header = (
            f"{'CustomerID'.ljust(col_widths['customer_id'])} | "
            f"{'ContactNumber'.ljust(col_widths['contact_number'])} | "
            f"{'ShippingDetails'.ljust(col_widths['shipping_details'])}\n"
        )

        separator = "-" * (sum(col_widths.values()) + 7) + "\n"

        rows = []
        for customer in customers:
            customer_line = (
                f"{str(customer['customer_id']).ljust(col_widths['customer_id'])} | "
                f"{str(customer['contact_number']).ljust(col_widths['contact_number'])} | "
                f"{str(customer['shipping_details']).ljust(col_widths['shipping_details'])}"
            )
            rows.append(customer_line)

        return header + separator + "\n".join(rows)

    @staticmethod
    def GET():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM customers")
                customers = cursor.fetchall()
                if not customers:
                    return "No customers found."
                return CustomerManage.format_customer_list(customers)
        finally:
            conn.close()

    @staticmethod
    def ADD(contact_number, shipping_details):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO customers (contact_number, shipping_details) VALUES (%s, %s)",
                               (contact_number, shipping_details))
                conn.commit()
                messagebox.showinfo("Success", "Customer added successfully.")
        finally:
            conn.close()