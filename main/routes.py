"""
This module defines the Flask application routes, utility functions, and views for the core functionality.
It includes user authentication, rendering templates, handling user actions like buying/selling units, and
managing transaction history. This module integrates Flask, Flask-Login, SQLAlchemy, and forms for a complete web experience.
"""

import datetime  # Used for timestamping transactions
from typing import List  # Type hint for a list return type

from flask import flash, redirect, render_template, url_for, request  # Flask utilities for routing and responses
from flask_login import login_required, login_user, current_user, logout_user  # Session management
from sqlalchemy import or_  # SQLAlchemy operator for OR conditions

from main import app, bcrypt, db  # Flask app instance, bcrypt for hashing, and database
from main.forms import LoginForm, PurchaseForm, RegistrationForm, SellOrderForm  # WTForms for handling forms
from main.models import SellOrder, TransactionHistory, User, get_sellers  # Database models and utility function

# Static dashboard information for demonstration
dashboard_info = {"balance": "50"}

@app.route('/layout')
def layout():
    """
    Render the base layout template for testing purposes.
    """
    return render_template("layout.html")


@app.route('/')
@app.route('/home')
def home():
    """
    Render the home page. Redirects to login if the user is not authenticated.
    Displays user's current unit usage and dashboard information.
    """
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    current = current_user.units
    units = units_used(current)
    return render_template("index.html", user_data=dashboard_info, units_used=units)


def units_used(current, total: int = 35):
    """
    Calculate the percentage of units used by the user.

    Args:
        current (int): Current units of the user.
        total (int): Total units available. Defaults to 35.

    Returns:
        int: Percentage of units used.
    """
    proportion = current / total
    return int(proportion * 100)


@app.route('/transactions')
def transactions():
    """
    Render the transactions page, showing the transaction history for the current user.
    Redirects to login if the user is not authenticated.
    """
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("transaction.html", history=get_transaction_history(current_user.id))


@app.route('/about')
def about():
    """
    Render the about page with static information about the application.
    """
    return render_template("about.html")


@app.route('/account')
def account():
    """
    Render the account page to display user-specific details.
    """
    return render_template("account.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Handle user registration. Redirects authenticated users to the home page.
    On successful registration, hashes the password and stores the new user in the database.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        with app.app_context():
            user = User(username=form.username.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handle user login. Redirects authenticated users to the home page.
    Validates user credentials and starts a session on successful login.
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/seller_page", methods=['GET', 'POST'])
@login_required
def seller_page():
    """
    Display and handle actions on the seller page. Allows users to create sell orders.
    """
    form = SellOrderForm()
    if form.validate_on_submit():
        units, price = form.unit.data, form.price.data
        if current_user.units >= units:
            with app.app_context():
                order = SellOrder(user_id=current_user.id, units=units, price=price)
                db.session.add(order)
                db.session.commit()
        else:
            flash('Units not Available!', 'error')

    sell_orders = get_user_sell_orders()
    return render_template("seller_page.html", title="Page", sell_orders=sell_orders, form=form)


@app.route("/buyer_page", methods=['GET', 'POST'])
@login_required
def buyer_page():
    """
    Display the buyer page with available sell orders from other users.
    """
    sell_orders = get_sell_orders()
    return render_template("buyer_page.html", title="Buy Units", sell_orders=sell_orders)


@app.route("/cancel_sell_order", methods=["GET", "POST"])
@login_required
def cancel_sell_order():
    """
    Cancel an existing sell order for the current user.
    """
    order_id = request.args.get("order_id")
    if order_id is None:
        return redirect(url_for("home"))

    with app.app_context():
        order: SellOrder = SellOrder.query.filter_by(id=order_id).first()
        db.session.delete(order)
        db.session.commit()
        flash(f"Order: {order.id} Closed")
    return redirect(url_for('seller_page'))


@app.route("/checkout_page", methods=["GET", "POST"])
@login_required
def checkout_page():
    """
    Handle the checkout process when a user purchases units from a seller.
    """
    order_id = request.args.get("order_id")
    if order_id is None:
        return redirect(url_for("home"))

    order: SellOrder = SellOrder.query.filter_by(id=order_id).first()
    seller: User = User.query.filter_by(id=order.user_id).first()
    form = PurchaseForm()
    if form.validate_on_submit():
        if form.units.data <= order.units:
            total_price = order.price * form.units.data
            with app.app_context():
                buyer: User = User.query.filter_by(id=current_user.id).first()
                units = form.units.data
                if seller.units >= units:
                    if buyer.units + form.units.data <= 35:
                        buyer.units += units
                        order.units -= units
                        seller.units -= units
                        if order.units == 0:
                            db.session.delete(order)
                        history = TransactionHistory(seller_id=seller.id, seller_username=seller.username, buyer_id=buyer.id,
                                                     units=units, price=total_price, date=datetime.datetime.now())
                        db.session.add(history)

                        db.session.commit()
                        flash(f"Purchase successful for {form.units.data} units at total {total_price}!")
                        return redirect(url_for('home'))
                    else:
                        flash(f"Purchase unsuccessful for {form.units.data} units. Your Battery is Full!")
                else:
                    flash(f"Purchase unsuccessful for {form.units.data} units. Seller Does Not have these Units!")
        else:
            flash('Units exceeded!', 'error')
    return render_template("checkout_page.html", title="Checkout", order=order, seller=seller, form=form)


def get_user_sell_orders():
    """
    Retrieve all sell orders created by the current user.

    Returns:
        List[SellOrder]: List of sell orders belonging to the current user.
    """
    with app.app_context():
        qry = SellOrder.query.filter_by(user_id=current_user.id)
        return qry


def get_transaction_history(user_id):
    """
    Retrieve the transaction history for a given user.

    Args:
        user_id (int): ID of the user.

    Returns:
        List[dict]: List of transactions with type (CREDIT/DEBIT) and details.
    """
    with app.app_context():
        history = []
        transacts = TransactionHistory.query.filter(or_(
            TransactionHistory.buyer_id == user_id,
            TransactionHistory.seller_id == user_id
        )).order_by(TransactionHistory.date.desc())
        for transact in transacts:
            history.append({
                'row': transact,
                'type': "CREDIT" if transact.buyer_id == user_id else "DEBIT"
            })
        return history


def get_sell_orders():
    """
    Retrieve all active sell orders from the database along with their sellers.

    Returns:
        List[dict]: List of orders and their respective seller details.
    """
    with app.app_context():
        sell_orders = SellOrder.query.all()
        orders_with_seller = []
        for order in sell_orders:
            seller = User.query.filter_by(id=order.user_id).first()
            if seller.id == current_user.id:
                continue
            orders_with_seller.append({
                'order': order,
                'seller': seller,
                'status': int(order.units > seller.units)
            })
        return orders_with_seller


@app.route("/logout")
def logout():
    """
    Log the user out and redirect to the about page.
    """
    logout_user()
    return redirect(url_for("about"))
