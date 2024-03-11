from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages 
from flask_mysqldb import MySQL
import sys
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password32!'
app.config['MYSQL_DB'] = 'dalakristall'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.secret_key = "secret"



@app.route('/')
def index(): 
    if 'role' in session:
        role = session["role"]
        print("Role:", role)
        loggedin = True
        if role == 'customer':
            return render_template('customer.html', title="start", loggedin=loggedin)
        elif role == 'admin':
            return render_template('admin.html', title="admin", loggedin=loggedin)
        elif role == 'owner':
            return render_template('owner.html', title="owner", loggedin=loggedin)
        else:
            # Handle other roles or default case
            return render_template('start.html', title="start", loggedin=loggedin)
    return render_template('start.html', title = "start")

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        
        cur = mysql.connection.cursor()

        try:
            # Insert the new account
            cur.execute("INSERT INTO accounts (email, password, name, role) VALUES (%s, %s, %s, %s)", (email, password, name, 'customer'))
            mysql.connection.commit()

            # Set session information
            session['name'] = request.form['email']
            cur.execute("SELECT role FROM accounts WHERE email = %s", (session['name'],))
            role = cur.fetchall()
            session['role'] = role


            # Create a basket for the user
            cur.execute("INSERT INTO basket (email) VALUES (%s)", (email,))
            mysql.connection.commit()

            cur.close()

            flash("Signup successful!", 'success')
            return render_template('login.html', title="start")

        except mysql.connection.IntegrityError as e:
            # Handle the case where the email is already in use
            cur.close()
            flash("Signup Failed, Email already in use. Please try again", 'error')
            return render_template('signup.html')
    return render_template('login.html', title = "start" )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT EXISTS(SELECT * FROM accounts WHERE email = %s AND password = %s)", (email, password))
        loginStatus = cur.fetchall()
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT EXISTS(SELECT role FROM accounts WHERE email = %s AND password = %s)", (email, password))
        role = cur.fetchall()


        if loginStatus:
            session['logg'] = request.form['email']
            cur.execute("SELECT role FROM accounts WHERE email = %s", (session['logg'],))
            role_result = cur.fetchone()
            if role_result:
                session['role'] = role_result['role']
            else:
                # Handle the case where the role is not found or set a default role
                session['role'] = 'default'

            cur.close()
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'role' in session:
        session.pop('role', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['product_name']
        info = request.form['product_info']
        spec1 = request.form['product_spec1']
        spec2 = request.form['product_spec2']
        price = request.form['product_price']
        stock = request.form['product_stock']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO products (name, product_info, spec1, spec2, price, stock) VALUES (%s, %s, %s, %s, %s, %s)', (name, info, spec1, spec2, price, stock))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/editproduct<id>', methods=['POST'])
def editproduct(id):
    if request.method == 'POST':
        name = request.form['product_name']
        info = request.form['product_info']
        spec1 = request.form['product_spec1']
        spec2 = request.form['product_spec2']
        price = request.form['product_price']
        stock = request.form['product_stock']
        print(id)
        cur = mysql.connection.cursor()
        cur.execute('UPDATE products SET name = %s, product_info = %s, spec1 = %s, spec2 = %s, price = %s, stock = %s WHERE product_id = %s', (name, info, spec1, spec2, price, stock, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/updateinfo', methods=['POST'])
def updateinfo():
    if request.method == 'POST':
        content = request.form['content']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE geninfo SET content = %s', (content,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/admin.html')
def admin():
    return render_template('admin.html')

@app.route('/reklamera.html/<role>', methods=['GET', 'POST'])
def reklamera(role):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reklamera')
    reklamera = cur.fetchall()
    cur.close()
    print(role)
    return render_template('reklamera.html', title = "reklamerat", reklamera=reklamera, role = role )

@app.route('/addreklamera', methods=['POST'])
def addreklamera():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO reklamera (title, content) VALUES (%s, %s)", (title, content))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/review.html/<role>')
def review(role):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM review')
    review = cur.fetchall()
    cur.close()
    return render_template('review.html', title = "review", review=review, role=role)

@app.route('/addreview', methods=['POST'])
def addreview():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        prodname = request.form['name']
        
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO review (title, content, prod_name) VALUES (%s, %s, %s)", (title, content, prodname))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/allinfo.html/<role>')
def generalinfo(role):
    cur = mysql.connection.cursor()
    cur.execute('SELECT content FROM geninfo')
    info = cur.fetchall()
    cur.close()
    return render_template('allinfo.html', title = "allinfo", role = role, info = info )

@app.route('/faq.html', methods=['GET'])
def faq():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM info')
    info = cur.fetchall()
    cur.close()
    return render_template('faq.html', title = "faq", info=info )

@app.route('/productlist.html/<role>', methods=['GET'])
def productlist(role):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    cur.close()
    print(role)
    return render_template('productlist.html', title = "productlist", products=products, role = role )


@app.route("/enter", methods=["GET", "POST"])
def enterbasket():
    if "productID" in request.form:
        product_id = request.form["productID"]

        # Check if user is logged in
        if 'name' not in session:
            flash("Please log in to add items to your basket.", "error")
            return redirect(url_for("index"))

        email = session['name']

        # Get the basket ID associated with the user's email
        cur = mysql.connection.cursor()
        cur.execute("SELECT basket_id FROM basket WHERE email = %s", (email,))
        basket_id = cur.fetchone()


        basket_id = basket_id['basket_id']

        cur.execute("SELECT order_id, quantity FROM orders WHERE basket_id = %s AND product_id = %s", (basket_id, product_id))
        existing_order = cur.fetchone()

        if existing_order:
            print("Existing debug")
            # If the product exists, update the quantity
            order_id = existing_order['order_id']
            quantity = existing_order['quantity'] + 1
            cur.execute("UPDATE orders SET quantity = %s WHERE order_id = %s", (quantity, order_id))
            mysql.connection.commit()
        else:
            # If the product doesn't exist, insert a new order
            cur.execute("INSERT INTO orders (basket_id, product_id, quantity) VALUES (%s, %s, %s)", (basket_id, product_id, 1))
            mysql.connection.commit()

        cur.close()

        flash("Item added to basket!", "success")
        return redirect(url_for("basket", basket_id = basket_id, product_id = product_id))
    else:
        return redirect(url_for('index'))

@app.route('/basket.html/<basket_id><product_id>', methods=['GET'])
def basket(basket_id, product_id):
    cur = mysql.connection.cursor()
    if product_id == 'NULL':
        # Handle the case where no specific product ID is provided
        cur.execute('SELECT products.name, products.price, orders.quantity FROM products JOIN orders ON products.product_id = orders.product_id WHERE orders.basket_id = %s', (basket_id,))
        products = cur.fetchall()
        cur.close()
        total_price = sum(product['price'] * product['quantity'] for product in products)
        #cur.execute('SELECT * FROM orders WHERE basket_id = %s', (ID))
        #cur.execute('SELECT products.name, products.price, orders.quantity FROM products JOIN orders ON products.product_id = orders.product_id WHERE orders.basket_id = %s', (ID,))
    else:
        cur.execute('SELECT products.product_id, products.name, products.price, orders.quantity FROM products JOIN orders ON products.product_id = orders.product_id WHERE orders.basket_id = %s', (basket_id,))
        products = cur.fetchall()
        cur.close()
        total_price = sum(product['price'] * product['quantity'] for product in products)
        print("Total Price:", total_price)
        print(basket_id)
        print(product_id)
    
    return render_template('basket.html', title = 'basket', products=products, total_price = total_price, basket_id = basket_id)

@app.route('/placeorder/<ID>', methods=['POST'])
def placeorder(ID):
    cur = mysql.connection.cursor()

    # Get products in the basket
    cur.execute('SELECT product_id, quantity FROM orders WHERE basket_id = %s', (ID,))
    products_in_basket = cur.fetchall()

    # Check if there's enough stock for each product
    for product in products_in_basket:
        product_id = product['product_id']
        quantity = product['quantity']

        # Check if the stock is sufficient
        cur.execute("SELECT stock FROM products WHERE product_id = %s", (product_id,))
        current_stock = cur.fetchone()['stock']

        if current_stock < quantity:
            return redirect(url_for('index', data = "Failed to place the order"))

    # Update product stock and create order records
    for product in products_in_basket:
        product_id = product['product_id']
        quantity = product['quantity']

        # Update product stock
        cur.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))

        # Create order record (you may need additional fields in your 'orders' table)
        # cur.execute("INSERT INTO order_history (product_id, quantity, basket_id) VALUES (%s, %s, %s)", (product_id, quantity, ID))

    # Clear the basket after placing the order
    cur.execute("DELETE FROM orders WHERE basket_id = %s", (ID,))

    mysql.connection.commit()
    cur.close()

    flash("Order placed successfully!", "success")
    return redirect(url_for('gratz'))

@app.route('/gratz.html')
def gratz():
    messages = get_flashed_messages()
    return render_template('gratz.html', messages=messages)


@app.route('/accmanage.html')
def accmanage():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM accounts')
    accounts = cur.fetchall()
    cur.close()
    return render_template('accmanage.html', title = "Account Manage", accounts=accounts )

@app.route('/removeacc/<ID>', methods=['POST'])
def removeacc(ID):
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        cur.execute("DELETE FROM accounts WHERE email = %s", (ID,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/removeitem', methods=['POST'])
def removeitem():
    if request.method == 'POST':
        basket_id = request.form.get('basket_id')
        product_id = request.form.get('product_id')

        if basket_id and product_id:
            cur = mysql.connection.cursor()

            # Get the current quantity
            cur.execute("SELECT quantity FROM orders WHERE product_id = %s AND basket_id = %s", (product_id, basket_id))
            current_quantity = cur.fetchone()['quantity']

            if current_quantity > 1:
                # If quantity is more than 1, decrement it
                cur.execute("UPDATE orders SET quantity = %s WHERE product_id = %s AND basket_id = %s", (current_quantity - 1, product_id, basket_id))
            else:
                # If quantity is 1, remove the item
                cur.execute("DELETE FROM orders WHERE product_id = %s AND basket_id = %s", (product_id, basket_id))

            mysql.connection.commit()
            cur.close()

            flash("Item quantity decreased in the basket!", "success")
            return redirect(url_for('basket', basket_id = basket_id, product_id=product_id))

    flash("Failed to update item quantity in the basket. Please try again.", "error")
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
