from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://20010615:sumsar1928@127.0.0.1/db20010615' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 
pymysql.connect(db='db20010615', user='20010615', passwd='sumsar1928', host='127.0.0.1', port=3306)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'


@app.route('/')
def testdb():
    try:
        db.session.query(db.text('1')).from_statement(db.text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

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

@app.route('/productlist.html')
def productlist():
    return render_template('productlist.html', title = "productlist" )

@app.route('/product.html')
def product():
    return render_template('product.html', title = "product" )

@app.route('/spec.html')
def spec():
    return render_template('spec.html', title = "spec" )

@app.route('/basket.html')
def basket():
    return render_template('basket.html', title = "basket" )

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
