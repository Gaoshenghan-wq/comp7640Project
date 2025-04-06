from database.db_connection import get_db_connection
from tkinter import messagebox

class VendorManage:
    @staticmethod
    def format_vendor_list(vendors):
        # 定义固定列宽
        col_widths = {
            'vendor_id': 12,
            'business_name': 20,
            'customer_feedback_score': 20,
            'geographical_presence': 20
        }

        # 创建表头
        header = (
            f"{'VendorID'.ljust(col_widths['vendor_id'])} | "
            f"{'BusinessName'.ljust(col_widths['business_name'])} | "
            f"{'FeedbackScore'.ljust(col_widths['customer_feedback_score'])} | "
            f"{'GeographicalPresence'.ljust(col_widths['geographical_presence'])}\n"
        )

        # 分隔线
        separator = "-" * (sum(col_widths.values()) + 9) + "\n"  # 9 为空格和竖线

        # 格式化每个供应商信息
        rows = []
        for vendor in vendors:
            vendor_line = (
                f"{str(vendor['vendor_id']).ljust(col_widths['vendor_id'])} | "
                f"{str(vendor['business_name']).ljust(col_widths['business_name'])} | "
                f"{str(vendor['customer_feedback_score']).ljust(col_widths['customer_feedback_score'])} | "
                f"{str(vendor['geographical_presence']).ljust(col_widths['geographical_presence'])}"
            )
            rows.append(vendor_line)

        return header + separator + "\n".join(rows)

    @staticmethod
    def GET():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM vendors")
                vendors = cursor.fetchall()
                if not vendors:
                    return "No vendors found."
                return VendorManage.format_vendor_list(vendors)
        finally:
            conn.close()

    @staticmethod
    def ADD(business_name, customer_feedback_score, geographical_presence):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO vendors (business_name, customer_feedback_score, geographical_presence) VALUES (%s, %s, %s)",
                               (business_name, customer_feedback_score, geographical_presence))
                conn.commit()
                messagebox.showinfo("Success", "Vendor added successfully.")
        finally:
            conn.close()