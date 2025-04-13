import sys
from PyQt6.QtWidgets import (
   QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
   QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton,
   QCheckBox, QDialog, QFormLayout, QMenu, QCalendarWidget
)
from PyQt6.QtGui import QAction
import mysql.connector
from datetime import date

class SalesDetails(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Sales Details")
        self.setGeometry(150, 150, 800, 600)
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header Layout
        header_layout = QHBoxLayout()
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet("font-size: 18px;")
        self.home_button.clicked.connect(self.go_home)
        header_layout.addWidget(self.home_button)
        
        self.date_picker = QPushButton("Select Date Range")
        self.date_picker.clicked.connect(self.open_calendar)
        header_layout.addWidget(self.date_picker)
        
        main_layout.addLayout(header_layout)

        # Sales Table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(6)  # Adjust this if your table has different columns
        self.sales_table.setHorizontalHeaderLabels(["Date", "UPC", "Description", "AMT", "Qty", "Wgt"])
        main_layout.addWidget(self.sales_table)
        
        self.load_data()

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def load_data(self):
        try:
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            cursor.execute("SELECT Date, Upc, Description, AMT, Qty, Wgt FROM salesdetails")
            records = cursor.fetchall()

            self.sales_table.setRowCount(len(records))

            for row_idx, row_data in enumerate(records):
                for col_idx, value in enumerate(row_data):
                    self.sales_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def go_home(self):
        self.close()
        self.main_window.show()
    
    def open_calendar(self):
        self.calendar = QDialog(self)
        self.calendar.setWindowTitle("Select Date Range")
        layout = QVBoxLayout()

        self.start_calendar = QCalendarWidget()
        self.end_calendar = QCalendarWidget()
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_calendar)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_calendar)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_date_filter)
        layout.addWidget(apply_button)

        self.calendar.setLayout(layout)
        self.calendar.exec()
    
    def apply_date_filter(self):
        start_date = self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_calendar.selectedDate().toString("yyyy-MM-dd")
        print(f"Filtering sales from {start_date} to {end_date}")
        self.filter_sales_by_date(start_date, end_date)
        self.calendar.close()

    def filter_sales_by_date(self, start_date, end_date):
        try:
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            query = """
            SELECT Date, Upc, Description, AMT, Qty, Weight FROM salesdetails 
            WHERE Date BETWEEN %s AND %s 
            ORDER BY Date ASC;
            """
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()

            self.sales_table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.sales_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            connection.close()

class OrderDetails(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Order Details")
        self.setGeometry(150, 150, 800, 600)
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header Layout
        header_layout = QHBoxLayout()
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet("font-size: 18px;")
        self.home_button.clicked.connect(self.go_home)
        header_layout.addWidget(self.home_button)
        
        self.date_picker = QPushButton("Select Date Range")
        self.date_picker.clicked.connect(self.open_calendar)
        header_layout.addWidget(self.date_picker)
        
        main_layout.addLayout(header_layout)

        # Orders Table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["Date", "UPC", "Vendor Code", "Cases"])
        main_layout.addWidget(self.orders_table)
        
        #load data
        self.load_data()

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def load_data(self):
        try:
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            # Fetch data from the "Orders" table
            cursor.execute("SELECT Date, Upc, VendorCode, Cases FROM Orders")
            records = cursor.fetchall()

            # Set row count dynamically
            self.orders_table.setRowCount(len(records))

            # Populate table
            for row_idx, row_data in enumerate(records):
                for col_idx, value in enumerate(row_data):
                    self.orders_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Close database connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            

    def go_home(self):
        self.close()
        self.main_window.show()
    
    def open_calendar(self):
        self.calendar = QDialog(self)
        self.calendar.setWindowTitle("Select Date Range")
        layout = QVBoxLayout()

        self.start_calendar = QCalendarWidget()
        self.end_calendar = QCalendarWidget()
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_calendar)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_calendar)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_date_filter)
        layout.addWidget(apply_button)

        self.calendar.setLayout(layout)
        self.calendar.exec()
    
    def apply_date_filter(self):
        start_date = self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_calendar.selectedDate().toString("yyyy-MM-dd")
        print(f"Filtering orders from {start_date} to {end_date}")
        self.filter_orders_by_date()  # Call the function to execute the SQL query
        self.calendar.close()

    def filter_orders_by_date(self):
        connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
        cursor = connection.cursor()

        # Get user-selected dates
        start_date = self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_calendar.selectedDate().toString("yyyy-MM-dd")

        # SQL Query
        query = """
        SELECT * FROM Orders 
        WHERE Date BETWEEN %s AND %s 
        ORDER BY Date ASC;
        """
        try:
            cursor.execute(query, (start_date, end_date))  # Execute with placeholders
            results = cursor.fetchall()  # Fetch results

            # Print or process results
            for row in results:
                print(row)  # You can update this to display the data in a table widget
        
        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            connection.close()


class DraftOrderDetails(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle(" Draft Order Details")
        self.setGeometry(150, 150, 800, 600)
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header Layout
        header_layout = QHBoxLayout()
        self.home_button = QPushButton("Home")
        self.home_button.setStyleSheet("font-size: 18px;")
        self.home_button.clicked.connect(self.go_home)
        header_layout.addWidget(self.home_button)
        
        self.date_picker = QPushButton("Select Date Range")
        self.date_picker.clicked.connect(self.open_calendar)
        header_layout.addWidget(self.date_picker)
        
        main_layout.addLayout(header_layout)

        # Orders Table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["Date", "UPC", "Vendor Code", "Cases"])
        main_layout.addWidget(self.orders_table)
        
        #load data
        self.load_data()

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_data(self):
        ##get data from mysql workbench database##
        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            # Fetch data from the "Orders" table
            cursor.execute("SELECT Date, Upc, VendorCode, Cases FROM DraftOrders")
            records = cursor.fetchall()

            # Set row count dynamically
            self.orders_table.setRowCount(len(records))

            # Populate table
            for row_idx, row_data in enumerate(records):
                for col_idx, value in enumerate(row_data):
                    self.orders_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Close database connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    def go_home(self):
        self.close()
        self.main_window.show()
    
    def open_calendar(self):
        self.calendar = QDialog(self)
        self.calendar.setWindowTitle("Select Date Range")
        layout = QVBoxLayout()

        self.start_calendar = QCalendarWidget()
        self.end_calendar = QCalendarWidget()
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(self.start_calendar)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(self.end_calendar)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_date_filter)
        layout.addWidget(apply_button)

        self.calendar.setLayout(layout)
        self.calendar.exec()
    
    def apply_date_filter(self):
        start_date = self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_calendar.selectedDate().toString("yyyy-MM-dd")
        print(f"Filtering draft orders from {start_date} to {end_date}")
        self.filter_draft_orders_by_date()  # Call the function to execute the SQL query
        self.calendar.close()

    def filter_draft_orders_by_date(self):
        connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
        cursor = connection.cursor()

        # Get user-selected dates
        start_date = self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_calendar.selectedDate().toString("yyyy-MM-dd")

        # SQL Query
        query = """
        SELECT * FROM DraftOrders 
        WHERE Date BETWEEN %s AND %s 
        ORDER BY Date ASC;
        """
        try:
            cursor.execute(query, (start_date, end_date))  # Execute with placeholders
            results = cursor.fetchall()  # Fetch results

            # Print or process results
            for row in results:
                print(row)  # You can update this to display the data in a table widget
        
        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            connection.close()


class AddItemDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Item")
        self.setGeometry(200, 200, 400, 500)
        
        layout = QFormLayout()
        
        self.fields = {}

        self.labels = ["UPC", "VendorID", "VendorCode", "UOM", "BaseCost", "CaseSize", "Brand",
                    "Quantity", "Description", "Size", "VolWeight", "Measure", "SubDepartment",
                    "Deposit", "Scalable", "Price", "SalePrice", "DateReceived"]
        
        for label in self.labels:
            self.fields[label] = QLineEdit()
            layout.addRow(QLabel(label + ":"), self.fields[label])
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_to_database)
        layout.addWidget(self.save_button)

        self.setLayout(layout)


    def save_to_database(self):
        """Generate SQL INSERT statement dynamically and execute it. If UPC exists, update quantity."""
        filled_fields = {key: self.fields[key].text().strip() for key in self.labels if self.fields[key].text().strip()}

        if not filled_fields:
            print("No data entered!")
            return

        # Extract UPC and quantity values
        upc = filled_fields.get("UPC")
        quantity = int(filled_fields.get("Quantity", 0))

        if not upc or quantity <= 0:
            print("Invalid UPC or quantity!")
            return

        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            # Check if the UPC already exists in the inventory
            cursor.execute(f"SELECT Quantity FROM Inventory WHERE UPC = %s", (upc,))
            existing_row = cursor.fetchone()

            if existing_row:
                # If the UPC exists, update the quantity by adding the new quantity
                existing_quantity = existing_row[0] if existing_row[0] is not None else 0  # Ensure existing_quantity is 0 if None
                new_quantity = existing_quantity + quantity
                cursor.execute(f"UPDATE Inventory SET Quantity = %s WHERE UPC = %s", (new_quantity, upc))
                print(f"Updated UPC {upc} with new quantity: {new_quantity}")
            else:
                # If the UPC does not exist, insert a new record
                columns = ", ".join(filled_fields.keys())
                placeholders = ", ".join(["%s"] * len(filled_fields))
                values = tuple(filled_fields.values())
                sql_query = f"INSERT INTO Inventory ({columns}) VALUES ({placeholders})"
                cursor.execute(sql_query, values)
                print(f"Inserted new item with UPC {upc}")

            connection.commit()  # Commit the changes
            cursor.close()
            connection.close()

            self.accept()  # Close the dialog after successful insert/update

        except mysql.connector.Error as err:
            print(f"Error: {err}")


class NewOrderDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Order")
        self.setGeometry(300, 300, 300, 200)
        
        layout = QFormLayout()
        
        self.upc_field = QLineEdit()
        self.vendor_code_field = QLineEdit()
        self.cases_field = QLineEdit()
        
        layout.addRow(QLabel("UPC:"), self.upc_field)
        layout.addRow(QLabel("Or"))
        layout.addRow(QLabel("Vendor Code:"), self.vendor_code_field)
        layout.addRow(QLabel("Cases:"), self.cases_field)
        
        self.order_button = QPushButton("Order")
        self.order_button.clicked.connect(self.insert_into_order_database)
        layout.addWidget(self.order_button)

        self.draft_order_button = QPushButton("Draft Orders")
        self.draft_order_button.clicked.connect(self.insert_into_draft_order_database)
        layout.addWidget(self.draft_order_button)
        
        self.setLayout(layout)

    def insert_into_order_database(self):
        connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
        cursor = connection.cursor()
        # Get user inputs
        upc = self.upc_field.text()
        vendor_code = self.vendor_code_field.text()
        cases = self.cases_field.text()

        query = "INSERT INTO orders (Date, Upc, VendorCode, Cases) VALUES (%s, %s, %s, %s)"
        values = (date.today(),upc, vendor_code, cases)
        try:
            cursor.execute(query, values)
            connection.commit()  # Save the changes
            print("Data inserted successfully!")
        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            connection.close()

    def insert_into_draft_order_database(self):
        connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
        cursor = connection.cursor()
        # Get user inputs
        upc = self.upc_field.text()
        vendor_code = self.vendor_code_field.text()
        cases = self.cases_field.text()

        query = "INSERT INTO draftorders (Date, Upc, VendorCode, Cases) VALUES (%s, %s, %s, %s)"
        values = (date.today(),upc, vendor_code, cases)
        try:
            cursor.execute(query, values)
            connection.commit()  # Save the changes
            print("Data inserted successfully!")
        except mysql.connector.Error as err:
            print("Error:", err)
        finally:
            cursor.close()
            connection.close()


class InventoryDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jim’s Inventory Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        # Main Layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header Layout
        header_layout = QHBoxLayout()
        title_label = QLabel("Jim’s Inventory Dashboard")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)

        # New Order and Orders Button
        self.new_order_button = QPushButton("New Order")
        self.new_order_button.clicked.connect(self.show_new_order_dialog)
        self.orders_button = QPushButton("Orders")
        self.orders_button.clicked.connect(self.show_order_details)
        self.draft_order_button = QPushButton("Draft Orders")
        self.draft_order_button.clicked.connect(self.show_draft_order_details)

        header_layout.addWidget(self.new_order_button)
        header_layout.addWidget(self.orders_button)
        header_layout.addWidget(self.draft_order_button)
        main_layout.addLayout(header_layout)

        # Search and Filter Section
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by UPC...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_inventory)

        self.add_button = QPushButton("+")
        self.add_button.setStyleSheet("font-size: 18px; width: 30px; height: 30px;")
        self.add_button.clicked.connect(self.show_add_item_dialog)

        self.menu_button = QPushButton("≡")
        self.menu_button.setStyleSheet("font-size: 18px; width: 30px; height: 30px;")
        self.menu_button.clicked.connect(self.toggle_column_menu)

        search_layout.addWidget(self.menu_button)
        search_layout.addWidget(self.add_button)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        main_layout.addLayout(search_layout)

        # Inventory Table
        self.columns = [
            "UPC", "VendorID", "VendorCode", "UOM", "BaseCost", "CaseSize", "Brand",
            "Quantity", "Description", "Size", "VolWeight", "Measure", "SubDepartment",
            "Deposit", "Scalable", "Price", "SalePrice", "DateReceived"
        ]
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(len(self.columns))
        self.inventory_table.setHorizontalHeaderLabels(self.columns)
        main_layout.addWidget(self.inventory_table)

        # Load data from MySQL
        self.load_inventory_data()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Column Selection Menu
        self.column_menu = QMenu(self)
        self.column_actions = {}
        for column in self.columns:
            action = QAction(column, self, checkable=True)
            action.setChecked(True)
            action.triggered.connect(self.update_columns)
            self.column_menu.addAction(action)
            self.column_actions[column] = action

        # Additional Sections
        sections_layout = QHBoxLayout()
        self.sales_table = self.create_sales_section()
        self.running_low_table = self.create_running_low_section()
        sections_layout.addWidget(self.running_low_table)
        sections_layout.addWidget(self.sales_table)
        main_layout.addLayout(sections_layout)

    def load_inventory_data(self):
        """Fetch inventory data from MySQL and populate the table."""
        try:
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            query = f"SELECT {', '.join(self.columns)} FROM Inventory"
            cursor.execute(query)
            records = cursor.fetchall()

            self.inventory_table.setRowCount(len(records))
            for row_idx, row_data in enumerate(records):
                for col_idx, value in enumerate(row_data):
                    self.inventory_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def toggle_column_menu(self):
        self.column_menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))

    def update_columns(self):
        visible_columns = [col for col, action in self.column_actions.items() if action.isChecked()]
        self.inventory_table.setColumnCount(len(visible_columns))
        self.inventory_table.setHorizontalHeaderLabels(visible_columns)

    def create_section(self, title, columns):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(title)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        table = QTableWidget(5, len(columns))
        table.setHorizontalHeaderLabels(columns)
        layout.addWidget(table)

        widget.setLayout(layout)
        return widget

    def create_sales_section(self):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Sales")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        self.sales_table = QTableWidget()
        layout.addWidget(self.sales_table)

        self.load_sales_data()

        self.more_info_button = QPushButton("More Info")
        self.more_info_button.clicked.connect(self.show_sales_details)
        layout.addWidget(self.more_info_button)

        widget.setLayout(layout)
        return widget

    def load_sales_data(self):
        try:
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            query = "SELECT * FROM sales;"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            self.sales_table.setColumnCount(len(columns))
            self.sales_table.setRowCount(len(rows))
            self.sales_table.setHorizontalHeaderLabels(columns)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.sales_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except mysql.connector.Error as err:
            print("Database error:", err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def create_running_low_section(self):
        widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Running Low")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)

        self.running_low_table = QTableWidget()
        layout.addWidget(self.running_low_table)

        self.load_running_low_data()

        widget.setLayout(layout)
        return widget

    def load_running_low_data(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="73173359",
                database="TestProductManagement"
            )
            cursor = connection.cursor()

            query = "SELECT * FROM runninglow ORDER BY Qty ASC;"
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            self.running_low_table.setColumnCount(len(columns))
            self.running_low_table.setRowCount(len(rows))
            self.running_low_table.setHorizontalHeaderLabels(columns)

            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.running_low_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except mysql.connector.Error as err:
            print("Database error:", err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def search_inventory(self):
        search_term = self.search_bar.text()
        if not search_term:
            return

        try:
            connection = mysql.connector.connect(
                host="INSERTHOSTNAMEHERE", # Replace with your hostname
                user="INSERTUSERHERE", # Replace with your user
                password="INSERTPASSWORDHERE", # Replace with your password
                database="INSERTDATABASEHERE"# Replace with your database
            )
            cursor = connection.cursor()

            query = """
                SELECT * FROM Inventory
                WHERE Upc LIKE %s
            """
            like_pattern = f"%{search_term}%"
            cursor.execute(query, (like_pattern,))
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            self.inventory_table.setRowCount(len(results))
            self.inventory_table.setColumnCount(len(columns))
            self.inventory_table.setHorizontalHeaderLabels(columns)

            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.inventory_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except mysql.connector.Error as err:
            print("Database error:", err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def show_add_item_dialog(self):
        dialog = AddItemDialog()
        if dialog.exec():
            print("New item added:")
            for field, input_box in dialog.fields.items():
                print(f"{field}: {input_box.text()}")

    def show_new_order_dialog(self):
        dialog = NewOrderDialog()
        if dialog.exec():
            print("New order placed:")
            print(f"UPC: {dialog.upc_field.text()}")
            print(f"Vendor Code: {dialog.vendor_code_field.text()}")
            print(f"Cases: {dialog.cases_field.text()}")

    def show_sales_details(self):
        self.sales_details_window = SalesDetails(self)
        self.sales_details_window.show()
        self.hide()

    def show_order_details(self):
        self.order_details_window = OrderDetails(self)
        self.order_details_window.show()
        self.hide()

    def show_draft_order_details(self):
        self.draft_order_details_window = DraftOrderDetails(self)
        self.draft_order_details_window.show()
        self.hide()

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = InventoryDashboard()
   window.show()
   sys.exit(app.exec())
