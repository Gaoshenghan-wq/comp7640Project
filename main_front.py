import tkinter as tk
from tkinter import simpledialog
from app.models.product_manage import ProductManage
from app.models.vendor_manage import VendorManage
from app.models.customer_manage import CustomerManage
from app.models.order_manage import OrderManage


def create_product_management_gui():
    root = tk.Tk()
    root.title("Product Management")

    def show_products():
        vendor_id = simpledialog.askinteger("Input", "Enter Vendor ID:")
        if vendor_id is not None:
            result = ProductManage.GET(vendor_id)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result)

    def add_product():
        name = simpledialog.askstring("Input", "Enter Product Name:")
        price = simpledialog.askfloat("Input", "Enter Product Price:")
        vendor_id = simpledialog.askinteger("Input", "Enter Vendor ID:")
        tags = simpledialog.askstring("Input", "Enter Product Tags (comma - separated, max 3 tags):")
        if name and price is not None and vendor_id is not None:
            tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
            if len(tag_list) > 3:
                tk.messagebox.showerror("Error", "A product can have at most 3 tags.")
            else:
                ProductManage.ADD(name, price, vendor_id, tag_list)

    def search_product():
        keyword = simpledialog.askstring("Input", "Enter Search Keyword:")
        if keyword:
            result = ProductManage.SEARCH(keyword)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result)

    def show_vendors():
        result = VendorManage.GET()
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)

    def add_vendor():
        business_name = simpledialog.askstring("Input", "Enter Business Name:")
        customer_feedback_score = simpledialog.askfloat("Input", "Enter Customer Feedback Score:")
        geographical_presence = simpledialog.askstring("Input", "Enter Geographical Presence:")
        if business_name and customer_feedback_score is not None and geographical_presence:
            VendorManage.ADD(business_name, customer_feedback_score, geographical_presence)

    def show_customers():
        result = CustomerManage.GET()
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)

    def add_customer():
        contact_number = simpledialog.askstring("Input", "Enter Contact Number:")
        shipping_details = simpledialog.askstring("Input", "Enter Shipping Details:")
        if contact_number:
            CustomerManage.ADD(contact_number, shipping_details)

    def create_order():
        customer_id = simpledialog.askinteger("Input", "Enter Customer ID:")
        product_info = []
        while True:
            product_id = simpledialog.askinteger("Input", "Enter Product ID (or 0 to finish):")
            if product_id == 0:
                break
            quantity = simpledialog.askinteger("Input", "Enter Quantity:")
            if product_id and quantity:
                product_info.append((product_id, quantity))

        if customer_id and product_info:
            OrderManage.CREATE_ORDER(customer_id, product_info)

    def show_all_orders():
        result = OrderManage.GET_ORDERS()
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)

    def show_order():
        order_id = simpledialog.askinteger("Input", "Order ID:")
        if order_id is not None:
            result = OrderManage.GET_ORDER_ITEMS_BY_ORDER_ID(order_id)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result)

    def modify_order():
        order_id = simpledialog.askinteger("Input", "Enter Order ID:")
        if order_id:
            action = simpledialog.askstring("Input", "Enter action (remove_product, cancel_order, change_status):")
            if action == "remove_product":
                product_id = simpledialog.askinteger("Input", "Enter Product ID to remove:")
                OrderManage.REMOVE_PRODUCT_FROM_ORDER(order_id, product_id)
            elif action == "cancel_order":
                OrderManage.CANCEL_ORDER(order_id)
            elif action == "change_status":
                new_status = simpledialog.askstring("Input", "Enter new status ('pending', 'paid', 'shipped', 'completed'):")
                OrderManage.CHANGE_ORDER_STATUS(order_id, new_status)

    # 产品相关按钮
    tk.Button(root, text="Show Products", command=show_products).grid(row=0, column=0)
    tk.Button(root, text="Add Product", command=add_product).grid(row=1, column=0)
    tk.Button(root, text="Search Product", command=search_product).grid(row=2, column=0)

    # 供应商相关按钮
    tk.Button(root, text="Show Vendors", command=show_vendors).grid(row=0, column=1)
    tk.Button(root, text="Add Vendor", command=add_vendor).grid(row=1, column=1)

    # 客户相关按钮
    tk.Button(root, text="Show Customers", command=show_customers).grid(row=0, column=2)
    tk.Button(root, text="Add Customer", command=add_customer).grid(row=1, column=2)
    # tk.Button(root, text="Show All Customers", command=show_customers).grid(row=2, column=2)

    # 订单相关按钮
    tk.Button(root, text="Create Order", command=create_order).grid(row=0, column=3)
    tk.Button(root, text="Show All Orders", command=show_all_orders).grid(row=1, column=3)
    tk.Button(root, text="Show Order", command=show_order).grid(row=2, column=3)
    tk.Button(root, text="Modify Order", command=modify_order).grid(row=3, column=3)

    output_text = tk.Text(root, wrap=tk.WORD, width=120, height=30)
    output_text.grid(row=4, column=0, columnspan=4)

    root.mainloop()


if __name__ == "__main__":
    create_product_management_gui()