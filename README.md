# 🍔 SnappFood - Restaurant Management System

A Python-based desktop application for restaurant management and food ordering, developed using Tkinter and Object-Oriented Programming (OOP).

The application provides separate interfaces for customers and restaurant managers, making it possible to manage restaurant menus and place food orders through a graphical user interface.

## ✨ Features

- **User Registration & Login:** Supports customer and restaurant manager accounts.
- **Restaurant Management:** Creates a restaurant when a manager registers.
- **Menu Management:** Managers can add food and beverage items with prices and categories.
- **Restaurant Browsing:** Customers can browse registered restaurants and view their menus.
- **Shopping Cart:** Customers can add available items to their cart.
- **Order Placement:** Calculates the total order price and saves order information.
- **Order Management:** Managers can view orders received by their restaurant.
- **Data Persistence:** Stores application data in a local JSON file.

## 🛠️ Technologies

- Python 3
- Tkinter
- JSON
- Object-Oriented Programming (OOP)

## 📂 Project Structure

```text
SnappFood/
├── SnappFood.py
├── database.json
└── README.md
```

Note: `database.json` is created when the application saves data.

## 🚀 Installation & Usage

### Prerequisites

- Python 3.x
- Tkinter

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/NikanNaseri/Snapp-Food
   ```

2. Navigate to the project directory:

   ```bash
   cd SnappFood
   ```

3. Run the application:

   ```bash
   python SnappFood.py
   ```

Replace the repository URL and filename if your GitHub repository or Python file uses a different name.

## 👤 User Roles

### Restaurant Manager

- Register and create a restaurant.
- Add food and beverage items to the menu.
- View orders associated with the restaurant.

### Customer

- Create an account and log in.
- Browse available restaurants.
- View restaurant menus.
- Add items to the shopping cart.
- Place orders and see the total price.

## 💾 Data Storage

The application uses `database.json` to store users, restaurants, menus, and orders. Data is loaded when the application starts and saved when relevant changes are made.

## 🎯 Project Purpose

This project was created to practice Python programming, object-oriented design, GUI development with Tkinter, and JSON-based data persistence.

## 🔮 Future Improvements

- Password hashing and improved authentication security.
- Input validation and duplicate user ID prevention.
- Customer order history.
- Order status tracking.
- Editing and deleting menu items.
- Improved graphical interface.
- Integration with a real database.
- Online payment gateway integration.

## ⚠️ Disclaimer

This is an educational desktop project. Order placement and price calculation are implemented locally; real online payment processing is not supported.

## 📄 License

No license has been specified. Add a license file if you intend to allow others to use, modify, or distribute this project.
