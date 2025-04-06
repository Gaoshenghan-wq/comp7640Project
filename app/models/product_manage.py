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
            'vendor_name': 20,
            'tags': 30
        }

        # Create the header with fixed column widths
        header = (
            f"{'ProductID'.ljust(col_widths['product_id'])} | "
            f"{'Name'.ljust(col_widths['name'])} | "
            f"{'Price'.ljust(col_widths['price'])} | "
            f"{'VendorName'.ljust(col_widths['vendor_name'])} | "
            f"{'Tags'.ljust(col_widths['tags'])}\n"
        )

        # Separator line
        separator = "-" * (sum(col_widths.values()) + 13) + "\n"  # 13 for spaces and pipes

        # Format each product with fixed column widths
        rows = []
        for product in products:
            tag_str = ', '.join(product['tags']) if product['tags'] else 'No tags'
            tag_str = tag_str[:col_widths['tags']].ljust(col_widths['tags'])
            product_line = (
                f"{str(product['product_id']).ljust(col_widths['product_id'])} | "
                f"{str(product['name']).ljust(col_widths['name'])} | "
                f"{str(product['price']).ljust(col_widths['price'])} | "
                f"{str(product['vendor_name']).ljust(col_widths['vendor_name'])} | "
                f"{tag_str}"
            )
            rows.append(product_line)

        return header + separator + "\n".join(rows)

    @staticmethod
    def GET(vendor_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT p.product_id, p.name, p.price, v.business_name as vendor_name, 
                           GROUP_CONCAT(pt.tag_name) as tags
                    FROM products p
                    LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
                    LEFT JOIN product_tag_relations ptr ON p.product_id = ptr.product_id
                    LEFT JOIN product_tags pt ON ptr.tag_id = pt.tag_id
                    WHERE p.vendor_id = %s
                    GROUP BY p.product_id
                """
                cursor.execute(query, (vendor_id,))
                products = cursor.fetchall()
                for product in products:
                    product['tags'] = product['tags'].split(',') if product['tags'] else []
                if not products:
                    return "No products found for this vendor."
                return ProductManage.format_product_list(products)
        finally:
            conn.close()

    @staticmethod
    def ADD(name, price, vendor_id, tags):
        if len(tags) > 3:
            messagebox.showerror("Error", "A product can have at most 3 tags.")
            return
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO products (name, price, vendor_id) VALUES (%s, %s, %s)", (name, price, vendor_id))
                product_id = cursor.lastrowid
                for tag in tags:
                    # 检查标签是否已经存在
                    cursor.execute("SELECT tag_id FROM product_tags WHERE tag_name = %s", (tag,))
                    tag_result = cursor.fetchone()
                    if tag_result:
                        tag_id = tag_result['tag_id']
                    else:
                        # 如果标签不存在，插入新标签
                        cursor.execute("INSERT INTO product_tags (tag_name) VALUES (%s)", (tag,))
                        tag_id = cursor.lastrowid
                    # 插入产品和标签的关联关系
                    cursor.execute("INSERT INTO product_tag_relations (product_id, tag_id) VALUES (%s, %s)",
                                   (product_id, tag_id))
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
                    SELECT p.product_id, p.name, p.price, v.business_name as vendor_name, 
                           GROUP_CONCAT(pt.tag_name) as tags
                    FROM products p
                    LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
                    LEFT JOIN product_tag_relations ptr ON p.product_id = ptr.product_id
                    LEFT JOIN product_tags pt ON ptr.tag_id = pt.tag_id
                    WHERE p.name LIKE %s
                    OR p.product_id IN (
                        SELECT product_id FROM product_tag_relations
                        JOIN product_tags ON product_tag_relations.tag_id = product_tags.tag_id
                        WHERE product_tags.tag_name LIKE %s
                    )
                    GROUP BY p.product_id
                """
                cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
                products = cursor.fetchall()
                for product in products:
                    product['tags'] = product['tags'].split(',') if product['tags'] else []
                if not products:
                    return "No products found matching the keyword."
                return ProductManage.format_product_list(products)
        finally:
            conn.close()