from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'secret123'

# DB Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Menu categorized with 6 categories and 7 items each
menu = {
    # Hot Beverages
    'Full Tea': 20,
    'Half Tea': 10,
    'Espresso': 30,
    'Americano': 35,
    'Filter Coffee': 25,
    'Green Tea': 20,
    'Masala Chai': 25,

    # Cold Beverages
    'Cold Coffee': 50,
    'Lemon Tea': 25,
    'Hot Chocolate': 40,
    'Oreo Shake': 60,
    'KitKat Shake': 65,
    'Milkshake - Vanilla': 50,
    'Milkshake - Chocolate': 55,

    # Sandwiches
    'Veg Sandwich': 40,
    'Cheese Sandwich': 50,
    'Paneer Sandwich': 55,
    'Club Sandwich': 60,
    'Grilled Sandwich': 50,
    'Corn Cheese Sandwich': 55,
    'Spicy Veg Sandwich': 45,

    # Snacks & Sides
    'Veg Puff': 20,
    'Paneer Puff': 25,
    'French Fries': 30,
    'Peri Peri Fries': 35,
    'Garlic Bread': 40,
    'Cheesy Garlic Bread': 45,
    'Spring Rolls': 35,

    # Burgers
    'Veg Burger': 50,
    'Cheese Burger': 55,
    'Paneer Burger': 60,
    'Tandoori Burger': 65,
    'Double Patty Burger': 70,
    'Crispy Veg Burger': 55,
    'Spicy Paneer Burger': 60,

    # Desserts
    'Chocolate Muffin': 30,
    'Blueberry Muffin': 35,
    'Choco Lava Cake': 40,
    'Vanilla Ice Cream': 25,
    'Brownie': 30,
    'Strawberry Cupcake': 35,
    'Donut': 30,
}


# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50))
    items_json = db.Column(db.Text)
    total = db.Column(db.Float)

    def get_items(self):
        return json.loads(self.items_json)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def show_menu():
    return render_template('menu.html', menu=menu)

@app.route('/order', methods=['GET', 'POST'])
def take_order():
    if request.method == 'POST':
        order = {}
        for item in menu:
            qty = request.form.get(item)
            if qty and qty.isdigit() and int(qty) > 0:
                order[item] = int(qty)

        if order:
            item_totals = {}
            total = 0
            for item, qty in order.items():
                item_total = qty * menu[item]
                item_totals[item] = item_total
                total += item_total

            tax = total * 0.10
            grand_total = total + tax

            order_record = Order(
                time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                items_json=json.dumps(order),
                total=grand_total
            )
            db.session.add(order_record)
            db.session.commit()

            return render_template(
                'bill.html',
                order=order,
                item_totals=item_totals,
                total=total,
                tax=tax,
                grand_total=grand_total,
                menu=menu
            )
        else:
            return redirect(url_for('take_order'))

    return render_template('order.html', menu=menu)

@app.route('/history')
def view_history():
    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template('history.html', history=orders)

if __name__ == '__main__':
    app.run(debug=True)
