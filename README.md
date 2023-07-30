# Cleaning Service Booking System

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Database Schema](#database-schema)
- [Note](#note)

## Description

This project is a simple cleaning service booking system developed using Python and Tkinter. The application allows users to log in or register as either a customer or a cleaner. Once logged in, the user is redirected to the appropriate screen with specific functionalities.

## Features

- **User Registration**: New users can register as either a customer or a cleaner by providing their name, phone number, and password.

- **User Login**: Existing users can log in using their name and password. The system will validate the login credentials and redirect the user accordingly.

- **Customer Screen**: Customers will have access to the following options:
  - Book a Cleaner: Customers can view available cleaners and book one for their service.
  - View Booking History: Customers can check their booking history, including details like the cleaner's name, phone number, and the date and time of the cleaning service.
  - About Us: Provides information about the cleaning service company.
  - Logout: Allows customers to log out and return to the home screen.

- **Cleaner Screen**: Cleaners will have access to the following options:
  - Check Your Current Bookings: Cleaners can view the current bookings made for their cleaning services. Details displayed include the customer's name, phone number, and the date and time for cleaning.
  - About Us: Provides information about the cleaning service company.
  - Logout: Allows cleaners to log out and return to the home screen.

## Requirements

- Python 3.x
- Tkinter library (usually included with standard Python distributions)
- SQLite3 (for database storage)

## How to Run

1. Clone this repository to your local machine.
2. Install the required dependencies mentioned in the Requirements section.
3. Make sure you have the `book_cleaning_service.db` database file with the necessary tables (Cleaners, Customers, Bookings) set up for storing user and booking data. This file will be auto generated once you run the code
4. Run the main application file `app.py` using Python.
5. The application window will open, allowing you to use the cleaning service booking system.

## Database Schema

The database used for this project contains the following tables:

- Customers: Stores information about registered customers, including their ID, name, and phone number.
- Bookings: Stores the booking details, including the customer ID, cleaner ID, and the date and time of the cleaning service.

## Note

This project is a basic implementation of a cleaning service booking system for demonstration purposes. For production use, consider enhancing security measures, handling edge cases, and implementing additional features to suit your specific requirements.