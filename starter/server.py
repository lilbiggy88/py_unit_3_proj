from flask import Flask, render_template, redirect, flash, request, session
import jinja2
from forms import LoginForm

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined
app.secret_key = 'dev'

@app.route('/')
def homepage():
    return render_template('base.html')

@app.route('/melons')
def melons():
    """ Return a page listing all the melons available for purchase"""

    melon_list = melons.get_all()
    return render_template('melons.html', melon_list=melon_list)

@app.route('/melon/<melon_id>')
def melon_type(melon_id):
    """Return a page showing all info about a melon. Also, provide a button to buy that melon."""

    melon = melons.get_by_id(melon_id)
    return render_template('melon_type.html')

@app.route('/add_to_cart<melon_id>')
def add_to_cart(melon_id):
    """Add a melon to the cart and redirect to the shopping cart page. """

    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']

    cart[melon_id] = cart.get(melon_id, 0) + 1
    session.modified = True
    flash(f"Melon {melon_id} successfully added to cart.")
    print(cart)

    return redirect("/cart")

@app.route('/cart')
def cart():
    """Display contents of shopping cart. """

    order_total = 0
    cart_melons = []

    cart = session.get("cart", {})

    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)

        total_cost = quantity * melon.price
        order_total += total_cost
        melon.quantity = quantity
        melon.total_cost = total_cost

        cart.melons.append(melon)

    return render_template('cart.html', cart_melons=cart_melons, order_total=order_total)

@app.route("/empty-cart")
def empty_cart():
    session["cart"] = {}

    return redirect("/cart")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user into site."""
    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = customers.get_by_username(username)

        if not user or user['password'] != password:
            flash("Invalid username or password")
            return redirect('/login')


    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.env = "development"
    app.run(debug = True, port = 8000, host = 'localhost')

