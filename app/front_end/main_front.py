import tkinter as tk
from tkinter import simpledialog
from app.models.product_manage import ProductManage

def create_product_management_gui():
    root = tk.Tk()
    root.title("Product Management")

    # 显示产品
    def show_products():
        vendor_id = simpledialog.askinteger("Input", "Enter Vendor ID:")
        if vendor_id is not None:
            result = ProductManage.GET(vendor_id)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result)

    # 添加产品
    def add_product():
        name = simpledialog.askstring("Input", "Enter Product Name:")
        price = simpledialog.askfloat("Input", "Enter Product Price:")
        vendor_id = simpledialog.askinteger("Input", "Enter Vendor ID:")
        if name and price is not None and vendor_id is not None:
            ProductManage.ADD(name, price, vendor_id)

    # 搜索产品
    def search_product():
        keyword = simpledialog.askstring("Input", "Enter Search Keyword:")
        if keyword:
            result = ProductManage.SEARCH(keyword)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result)

    # 记录购买
    def record_purchase():
        customer_id = simpledialog.askinteger("Input", "Enter Customer ID:")
        product_id = simpledialog.askinteger("Input", "Enter Product ID:")
        quantity = simpledialog.askinteger("Input", "Enter Quantity:")
        price_at_purchase = simpledialog.askfloat("Input", "Enter Price at Purchase:")
        if customer_id is not None and product_id is not None and quantity is not None and price_at_purchase is not None:
            ProductManage.RECORD_PURCHASE(customer_id, product_id, quantity, price_at_purchase)

    # 创建按钮
    tk.Button(root, text="Show Products", command=show_products).pack()
    tk.Button(root, text="Add Product", command=add_product).pack()
    tk.Button(root, text="Search Product", command=search_product).pack()
    tk.Button(root, text="Record Purchase", command=record_purchase).pack()

    # 输出文本框
    output_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
    output_text.pack()

    root.mainloop()

if __name__ == "__main__":
    create_product_management_gui()