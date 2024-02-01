from flask import Flask, render_template 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('start.html', title = "start" )

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
