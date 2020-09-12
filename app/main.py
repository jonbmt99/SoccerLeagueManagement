from flask import render_template, request, url_for, session, flash
from flask_login import login_user
from app import app, login, dao
from app.forms import extractAndPersistUserDataFromForm, is_valid, getLoginUserDetails, getProductDetails, \
    extractAndPersistKartDetailsUsingSubquery, isUserLoggedIn, getusercartdetails, removeProductFromCart, \
    extractOrderdetails
from app.models import *
import hashlib

@app.route("/")
def index():
    logged_in, username, productCountinCartForGivenUser = getLoginUserDetails()
    return render_template(
        "index.html",
        loggedIn=logged_in,
        username=username,
        productCountinCartForGivenUser = productCountinCartForGivenUser
    )

@app.route("/team")
def teams():
    return render_template("team.html", teamList=dao.read_team())

@app.route("/player")
def players():
    return render_template("player.html", playerList=dao.read_player())

@app.route("/payment")
def payment():
    return render_template("payment.html", resss=dao.payment_momo())


@app.route("/registerationForm")
def registration_form():
    return render_template("register.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        msg = extractAndPersistUserDataFromForm(request)
        return render_template("login.html", error=msg)

@app.route("/login", methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect('/')
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/signIn")
def loginForm():
    if 'email' in session:
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error='')


@app.route("/displayProduct")
def displayProduct():
    product_list = Product.query.all()
    return render_template('displayProduct.html', productList=product_list)



@app.route("/productDescription")
def productDescription():
    productid = request.args.get('productId')
    productDetailsByProductId = getProductDetails(productid)
    return render_template("productDescription.html", data=productDetailsByProductId)


@app.route("/addToCart")
def addToCart():
    if isUserLoggedIn():
        productId = int(request.args.get('productId'))

        # Using Flask-SQLAlchmy SubQuery
        extractAndPersistKartDetailsUsingSubquery(productId)

        # Using Flask-SQLAlchmy normal query
        # extractAndPersistKartDetailsUsingkwargs(productId)
        flash('Item successfully added to cart !!', 'success')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('loginForm'))

@app.route("/shopcart")
def shopcart():
    if isUserLoggedIn():
        loggedIn, firstName, total_productincart = getLoginUserDetails()
        productsincart, totalsum= getusercartdetails();
        return render_template("shopcart.html", productsincart=productsincart , totalsum = totalsum)
    else:
        return redirect(url_for('index'))

@app.route("/removeFromCart")
def removeFromCart():
    if isUserLoggedIn():
        productId = int(request.args.get('productId'))
        removeProductFromCart(productId)
        return redirect(url_for('shopcart'))
    else:
        return redirect(url_for('loginForm'))


@app.route("/checkoutPage")
def checkoutForm():
    if isUserLoggedIn():
        productsincart, totalsum = getusercartdetails()
        return render_template("checkoutPage.html", productsincart=productsincart, totalsum=totalsum)
    else:
        return redirect(url_for('loginForm'))



@app.route("/login-admin", methods = ['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.email == email, User.password == password, User.isAdmin).first()
        if user:
            login_user(user=user)
            return redirect("/admin")


@app.route("/createOrder", methods=['GET', 'POST'])
def createOrder():
    totalsum = request.args.get('total')
    orderid = extractOrderdetails(totalsum)
    print(orderid)
    return render_template("OrderPage.html",orderid=orderid)




@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
