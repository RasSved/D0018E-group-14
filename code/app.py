from flask import Flask, render_template, request, redirect, url_for, session 
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
        return render_template('start.html', title = "start")

@app.route('/loggedin')
def loggedin(): 
        userID = session['userID']
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

        cur.execute("INSERT INTO customer (email, password, name) VALUES (%s, %s, %s)", (email, password, name))
        mysql.connection.commit()

        session['name'] = request.form['email']

        cur.execute("SELECT customer_id FROM customer WHERE email = %s", (session['name'],))
        userID = cur.fetchall()
        session['userID'] = userID
        cur.close()
    return render_template('start.html', title = "start" )



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT EXISTS(SELECT * FROM customer WHERE email = %s AND password = %s)", (email, password))
        loginStatus = cur.fetchall()
        
        if loginStatus:
            session['logg'] = request.form['email']

            loggedin = True

            cur.execute("SELECT customer_id FROM customer WHERE email = %s", (session['logg'],))
            userID = cur.fetchall()
            session['userID'] = userID

            cur.close()
            return redirect(url_for('loggedin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'logg' in session:
        session.pop('logg', None)
    return redirect('/')

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO products (name) VALUES (%s)', (product_name,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/customer.html')
def customer():
    return render_template('customer.html')


@app.route('/admin.html')
def admin():
    return render_template('admin.html')

@app.route('/reklamera.html')
def reklamera():
    return render_template('reklamera.html', title = "reklamera" )

@app.route('/review.html')
def review():
    return render_template('review.html', title = "review" )

@app.route('/allinfo.html')
def generalinfo():
    return render_template('allinfo.html', title = "allinfo" )

@app.route('/faq.html')
def faq():
    return render_template('faq.html', title = "faq" )

@app.route('/productlist.html', methods=['GET'])
def productlist():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    cur.close()
    return render_template('productlist.html', title = "productlist", products=products )

@app.route("/enter", methods = ["GET", "POST"])
def enterbasket():
    print(request.form, file=sys.stderr)
    if "productID" in request.form:
        productID = request.form["productID"]

        session["productID"] = productID
        return redirect(url_for("basket"))
    else:
        return redirect(url_for('productlist'))

@app.route('/product.html')
def product():
    return render_template('product.html', title = "product" )

@app.route('/spec.html')
def spec():
    return render_template('spec.html', title = "spec" )

@app.route('/basket.html')
def basket():
    if "productID" in session:
        productID = session["productID"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = 'productID'")
        products = cur.fetchall()
        cur.close()  

        return render_template("basket.html", title = "basket", products=products)
    else:
        return redirect(url_for('productlist'))

@app.route('/delivery.html')
def delivery():
    return render_template('delivery.html', title = "delivery" )

@app.route('/payment.html')
def payment():
    return render_template('payment.html', title = "payment" )

@app.route('/gratz.html')
def gratz():
    return render_template('gratz.html', title = "gratz" )


if __name__ == '__main__':
    app.run(debug=True)
