import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import re

def is_valid_phone_number(phone_number):
    # Define the regex pattern for a valid phone number
    # This regex pattern allows for 10 digits with optional dashes or spaces
    # Examples of valid phone numbers: "1234567890", "123-456-7890", "123 456 7890"
    pattern = r'^\d{3}[-\s]?\d{3}[-\s]?\d{4}$'

    # Check if the phone number matches the regex pattern
    return re.match(pattern, phone_number)

def is_strong_password(password):

    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not re.search(r'[!@#$%^&*]', password):
        return False

    return True

# SQLite Database Initialization
# Create a database and tables to store user and booking information
conn = sqlite3.connect("book_cleaning_service.db")
cursor = conn.cursor()

# Create a User table to store user information
cursor.execute("""
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    password TEXT NOT NULL,
    user_type TEXT NOT NULL
)
""")

# Create a Booking table to store booking information
cursor.execute("""
CREATE TABLE IF NOT EXISTS Booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    cleaner_id INTEGER NOT NULL,
    date_time TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES User (id),
    FOREIGN KEY (cleaner_id) REFERENCES User (id)
)
""")

conn.commit()

# Tkinter App Initialization
root = tk.Tk()
root.title("Cleaning Service Booking App")

# Function to handle user registration
def register_user():
    clear_screen()
    # Add code to handle user registration and insert user data into the database
    # Function to handle the user registration form submission
    def submit_registration():
        name = entry_name.get()
        phone = entry_phone.get()
        password = entry_password.get()
        user_type = user_type_var.get()
        if len(name)<5:
            messagebox.showerror("Name field Error", "Name should be 5 or more characters long.")
            return
        if not is_valid_phone_number(phone):
            messagebox.showerror("Phone field Error", "Please enter valid phone number")
            return
        if not is_strong_password(password):
            messagebox.showerror('Password field error', '''
    Criteria for a strong password
    At least 8 characters long
    Contains at least one uppercase letter
    Contains at least one lowercase letter
    Contains at least one digit
    Contains at least one special character (e.g., !, @, #, $, %, ^, &, *)''')
            return
            
        # Validate the input (you may add more validation checks as needed)
        if not name or not phone or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Insert user data into the database
        try:
            conn = sqlite3.connect("book_cleaning_service.db")
            cursor = conn.cursor()

            # Check if a user with the same phone number already exists
            cursor.execute("SELECT * FROM User WHERE phone=?", (phone,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "User with this phone number already exists.")
                conn.close()
                return

            # Insert the new user into the User table
            cursor.execute("INSERT INTO User (name, phone, password, user_type) VALUES (?, ?, ?, ?)",
                           (name, phone, password, user_type))  # Assuming the user is registering as a customer
            conn.commit()

            messagebox.showinfo("Success", "Registration successful.")
            # root.destroy()
            login_user()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error while registering: {str(e)}")

        finally:
            conn.close()

    # Create labels and entry fields for the registration form
    label_name = tk.Label(root, text="Name:")
    entry_name = tk.Entry(root)

    label_phone = tk.Label(root, text="Phone:")
    entry_phone = tk.Entry(root)

    label_password = tk.Label(root, text="Password:")
    entry_password = tk.Entry(root, show="*")
    
    user_type_label = tk.Label(root, text="User Type")
    user_type_var = tk.StringVar(root)
    user_type_var.set("Customer")  # Default value
    user_type_options = ["Customer", "Cleaner"]
    user_type_dropdown = tk.OptionMenu(root, user_type_var, *user_type_options)

    btn_register = tk.Button(root, text="Register", command=submit_registration)

    # Grid layout for the widgets
    label_name.grid(row=0, column=0, padx=10, pady=5)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    label_phone.grid(row=1, column=0, padx=10, pady=5)
    entry_phone.grid(row=1, column=1, padx=10, pady=5)

    label_password.grid(row=2, column=0, padx=10, pady=5)
    entry_password.grid(row=2, column=1, padx=10, pady=5)
    
    user_type_label.grid(row=3, column=0, padx=10, pady=5)
    user_type_dropdown.grid(row=3, column=1, padx=10, pady=5)

    btn_register.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Function to handle user login
def login_user():
    clear_screen()
    # Function to handle the user login form submission
    def submit_login():
        global phone
        phone = entry_phone.get()
        password = entry_password.get()

        global user_type
        user_type = user_type_var.get()
        # Validate the input (you may add more validation checks as needed)
        if not phone or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check the login credentials in the database
        try:
            conn = sqlite3.connect("book_cleaning_service.db")
            cursor = conn.cursor()

            # Retrieve user data based on the phone number
            cursor.execute("SELECT * FROM User WHERE phone=?", (phone,))
            user = cursor.fetchone()

            if user is None:
                messagebox.showerror("Error", "User not found.")
                conn.close()
                return

            # Check if the entered password matches the stored password
            if user[3] == password:
                # Redirect the user based on the user_type (customer or cleaner)
                if user_type == user[4]:
                    if user_type == 'Customer':
                        # Redirect to the customer screen
                        show_customer_screen()
                    elif user_type == "Cleaner":
                        # Redirect to the cleaner screen
                        show_cleaner_screen()
                    else:
                        messagebox.showerror("Error", "Invalid user type.")
                else:
                    messagebox.showerror('Error', 'User type mismatch')
            else:
                messagebox.showerror("Error", "Incorrect password.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error while logging in: {str(e)}")

        finally:
            conn.close()

    # Create labels and entry fields for the login form
    label_phone = tk.Label(root, text="Phone:")
    entry_phone = tk.Entry(root)

    label_password = tk.Label(root, text="Password:")
    entry_password = tk.Entry(root, show="*")

    user_type_label = tk.Label(root, text="User Type")
    user_type_var = tk.StringVar(root)
    user_type_var.set("Customer")  # Default value
    user_type_options = ["Customer", "Cleaner"]
    user_type_dropdown = tk.OptionMenu(root, user_type_var, *user_type_options)

    btn_login = tk.Button(root, text="Login", command=submit_login)

    # Grid layout for the widgets
    label_phone.grid(row=0, column=0, padx=10, pady=5)
    entry_phone.grid(row=0, column=1, padx=10, pady=5)

    label_password.grid(row=1, column=0, padx=10, pady=5)
    entry_password.grid(row=1, column=1, padx=10, pady=5)
    
    user_type_label.grid(row=2, column=0, padx=10, pady=5)
    user_type_dropdown.grid(row=2, column=1, padx=10, pady=5)

    btn_login.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Function to handle booking a cleaner
def book_cleaner():
    clear_screen()
    # Function to handle the selection of a cleaner
    def on_select_cleaner(event):
        # Clear any previous booking date and time selection
        date_entry.delete(0, tk.END)

        # Get the selected item (cleaner) from the treeview
        selected_item = cleaners_tree.selection()
        if selected_item:
            cleaner_name = cleaners_tree.item(selected_item, "values")[0]
            cleaner_phone = cleaners_tree.item(selected_item, "values")[1]
            selected_cleaner_label.config(text=f"Selected Cleaner: {cleaner_name} - {cleaner_phone}")

    # Function to handle the booking form submission
    def submit_booking():
        # Get the selected cleaner's name and phone
        selected_item = cleaners_tree.selection()
        if selected_item:
            cleaner_name = cleaners_tree.item(selected_item, "values")[0]
            cleaner_phone = cleaners_tree.item(selected_item, "values")[1]

            # Get the selected date and time for booking
            selected_date_time = date_entry.get()

            # You can now process the booking details and save to the database
            boolean_value = save_booking(cleaner_phone, selected_date_time)

            if boolean_value==True:
                tk.messagebox.showinfo("Booking Successful", f"Booking for {cleaner_name} - {cleaner_phone} on {selected_date_time} is successful!")
            if user_type=='Customer':
                show_customer_screen()
            else:
                show_cleaner_screen()

    # Function to save booking details to the database
    def save_booking(cleaner_phone, booking_date_time):
        try:
            conn = sqlite3.connect("book_cleaning_service.db")
            cursor = conn.cursor()

            # Fetch the cleaner ID from the database
            cursor.execute("SELECT id FROM User WHERE phone=?", (cleaner_phone,))
            cleaner_id = cursor.fetchone()[0]
            
            cursor.execute('SELECT id FROM User WHERE phone=?', (phone,))
            customer_id = cursor.fetchone()[0]

            # Insert the booking details into the database
            cursor.execute("INSERT INTO Booking (customer_id, cleaner_id, date_time) VALUES (?, ?, ?)", (customer_id, cleaner_id, booking_date_time))
            conn.commit()
            return True

        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Error while saving booking: {str(e)}")
            print("Error", f"Error while saving booking: {str(e)}")

        finally:
            conn.close()
            
    root.title("Book a Cleaner")

    # Fetch the list of cleaners from the database
    cleaners_list = []
    try:
        conn = sqlite3.connect("book_cleaning_service.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name, phone FROM User WHERE user_type=?", ('Cleaner',))
        cleaners_list = cursor.fetchall()

    except sqlite3.Error as e:
        tk.messagebox.showerror("Error", f"Error while fetching cleaners: {str(e)}")

    finally:
        conn.close()

    # Create a treeview to display the cleaners' details
    cleaners_tree = ttk.Treeview(root, columns=("Name", "Phone"), show="headings")
    cleaners_tree.heading("Name", text="Name")
    cleaners_tree.heading("Phone", text="Phone")

    # Add the cleaners' details to the treeview
    for cleaner in cleaners_list:
        cleaners_tree.insert("", tk.END, values=cleaner)

    # Bind the selection event of the treeview to the on_select_cleaner function
    cleaners_tree.bind("<<TreeviewSelect>>", on_select_cleaner)

    # Create a label to show the selected cleaner's details
    selected_cleaner_label = tk.Label(root, text="Selected Cleaner: None")

    # Create a date picker for booking date
    date_entry = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2)

    # Create a button to submit the booking
    btn_book = tk.Button(root, text="Book", command=submit_booking)

    # Grid layout for the widgets
    cleaners_tree.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    selected_cleaner_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    date_entry.grid(row=2, column=0, padx=10, pady=5)
    btn_book.grid(row=2, column=1, padx=10, pady=5)
    
# Function to handle viewing booking history
# Function to handle viewing booking history
def view_booking_history():
    clear_screen()
    # Create the booking history window
    root.title("Your Booking History")

    # Get the customer's phone number (you can set this variable when the customer logs in)
    customer_phone = phone

    # Retrieve the customer's user ID based on their phone number
    try:
        conn = sqlite3.connect("book_cleaning_service.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM User WHERE phone=?", (customer_phone,))
        customer_id = cursor.fetchone()[0]

        # Fetch the booking history for the customer from the Booking table
        # cursor.execute("SELECT * FROM Booking WHERE customer_id=?", (customer_id,))
        cursor.execute("SELECT b.date_time, u.name, u.phone FROM Booking b JOIN User u ON b.cleaner_id = u.id WHERE b.customer_id=?", (customer_id,))
        booking_history = cursor.fetchall()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error while fetching booking history: {str(e)}")
        booking_history = []

    finally:
        conn.close()

    # Check if any bookings were found in the database
    if not booking_history:
        messagebox.showinfo("No Bookings", "No booking history available.")
        return

    # Create a listbox to display the booking history
    root.geometry('500x300')
    listbox_booking_history = tk.Listbox(root, width=150)
    for i in booking_history:
        print(i)
    # Add the booking history data to the listbox
    for booking in booking_history:
        date_time, cleaner_name, cleaner_phone = booking
        listbox_booking_history.insert(tk.END, f"Date and Time: {date_time} - Cleaner Name: {cleaner_name} - Cleaner Phone: {cleaner_phone}")

    # Grid layout for the listbox
    listbox_booking_history.pack(padx=10, pady=10)
    if user_type=='Customer':
        btn_to_home = tk.Button(root, text="Go to Home", command=show_customer_screen)
    else:
        btn_to_home = tk.Button(root, text='Go to Home', command=show_cleaner_screen)

    # Grid layout for the label
    btn_to_home.pack(padx=10, pady=10)

# Function to handle checking current bookings
def check_current_bookings():
    clear_screen()
    root.geometry('500x300')
    root.title("Current Bookings")

    # Retrieve the cleaner's user ID based on their phone number
    try:
        conn = sqlite3.connect("book_cleaning_service.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM User WHERE phone=?", (phone,))
        cleaner_id = cursor.fetchone()[0]

        # Fetch the current bookings for the cleaner from the Booking table
        cursor.execute("SELECT b.date_time, u.name, u.phone FROM Booking b JOIN User u ON b.customer_id = u.id WHERE b.cleaner_id=?", (cleaner_id,))
        current_bookings = cursor.fetchall()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error while fetching current bookings: {str(e)}")
        current_bookings = []

    finally:
        conn.close()

    # Check if any current bookings were found in the database
    if not current_bookings:
        messagebox.showinfo("No Current Bookings", "No current bookings found.\nReturning to Home page")
        if user_type=='Customer':
            show_customer_screen()
        else:
            show_cleaner_screen()
        return

    # Create a listbox to display the current bookings
    listbox_current_bookings = tk.Listbox(root, width=150)

    # Add the current bookings data to the listbox
    for booking in current_bookings:
        date_time, customer_name, customer_phone = booking
        listbox_current_bookings.insert(tk.END, f"Date and Time: {date_time} - Customer Name: {customer_name} - Customer Phone: {customer_phone}")

    if user_type=='Customer':
        btn_to_home = tk.Button(root, text="Go to Home", command=show_customer_screen)
    else:
        btn_to_home = tk.Button(root, text='Go to Home', command=show_cleaner_screen)
    # Grid layout for the listbox
    listbox_current_bookings.pack(padx=10, pady=10)
    btn_to_home.pack(padx=10, pady=10)

# Function to show the "About Us" screen
# Function to show the "About Us" screen
def show_about_us():
    clear_screen()
    root.geometry("600x300")

    # Define the "About Us" information (you can replace this with your actual information)
    about_us_info = """Welcome to our Cleaning Service Company!
    
                       Our mission is to provide top-quality cleaning services to our customers at affordable prices. With a team of skilled and reliable cleaners, we are dedicated to making your home or office a clean and pleasant environment.
                       
                       Contact us today to book a cleaner and experience the difference our cleaning service can make in your life."""

    # Create a label to display the "About Us" information
    label_about_us = tk.Label(root, text=about_us_info, wraplength=400, justify=tk.LEFT)
    
    if user_type=='Customer':
        btn_to_home = tk.Button(root, text="Go to Home", command=show_customer_screen)
    else:
        btn_to_home = tk.Button(root, text='Go to Home', command=show_cleaner_screen)

    # Grid layout for the label
    label_about_us.pack(padx=10, pady=10)
    btn_to_home.pack(padx=10, pady=10)

# Function to show the home screen
def show_home_screen():
    clear_screen()

    # Create labels and buttons for login and registration
    label_title = tk.Label(root, text="Welcome to Cleaning Service")
    btn_login = tk.Button(root, text="Login", command=login_user)
    btn_register = tk.Button(root, text="Register", command=register_user)
    btn_close = tk.Button(root, text="Close App", command=close_app)

    # Grid layout for the widgets
    label_title.pack(pady=20)
    btn_login.pack(pady=10)
    btn_register.pack(pady=10)
    btn_close.pack(pady=10)
    
# Function to show the customer screen
def show_customer_screen():
    clear_screen()

    # Create buttons for customer options
    btn_book_cleaner = tk.Button(root, text="Book a Cleaner", command=book_cleaner)
    btn_view_booking_history = tk.Button(root, text="View Booking History", command=view_booking_history)
    btn_about_us = tk.Button(root, text="About Us", command=show_about_us)
    btn_logout = tk.Button(root, text="Logout", command=show_home_screen)
    btn_close = tk.Button(root, text="Close App", command=close_app)

    # Grid layout for the buttons
    btn_book_cleaner.pack(pady=10)
    btn_view_booking_history.pack(pady=10)
    btn_about_us.pack(pady=10)
    btn_logout.pack(pady=10)
    btn_close.pack(pady=10)
    
# Function to show the cleaner screen
def show_cleaner_screen():
    clear_screen()

    # Create buttons for cleaner options
    btn_check_current_bookings = tk.Button(root, text="Check Current Bookings", command=check_current_bookings)
    btn_about_us = tk.Button(root, text="About Us", command=show_about_us)
    btn_logout = tk.Button(root, text="Logout", command=show_home_screen)
    btn_close = tk.Button(root, text="Close App", command=close_app)

    # Grid layout for the buttons
    btn_check_current_bookings.pack(pady=10)
    btn_about_us.pack(pady=10)
    btn_logout.pack(pady=10)
    btn_close.pack(pady=10)

# Function to clear the screen
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
def close_app():
    root.destroy()    
# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cleaning Service booking App")
    root.geometry("400x300")
    show_home_screen()
    root.mainloop()