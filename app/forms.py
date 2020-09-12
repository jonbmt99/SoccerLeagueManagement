import hashlib
from datetime import datetime

from flask import session, flash, redirect, url_for

from app import db, dao
from app.models import User, Cart, Product, Order, OrderedProduct


def extractAndPersistUserDataFromForm(request):
    password = request.form['password']
    email = request.form['email']
    username = request.form['username']

    user = User(username=username, email=email, password=hashlib.md5(password.encode()).hexdigest())
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return "Registered Successfully"



def is_valid(email, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User.query.filter(User.email == email, User.password == password).first()
    if user:
        return True
    return False


def isUserLoggedIn():
    if 'email' not in session:
        return False
    else:
        return True


def isUserAdmin():
    if isUserLoggedIn():
        isAdmin = User.query.with_entities(User.isAdmin).filter(User.email == session['email']).first()
        return isAdmin


def getLoginUserDetails():
    productCountinCartForGivenUser = 0
    if 'email' not in session:
        logged_in = False
        username = ''
    else:
        logged_in = True
        user = User.query.filter(User.email == session['email']).first()
        username = user.username
        userid = user.id

        productCountinCart = []

        # for Cart in Cart.query.filter(Cart.userId == userId).distinct(Products.productId):
        for cart in Cart.query.filter(Cart.userid == userid).all():
            productCountinCart.append(cart.productid)
            productCountinCartForGivenUser = len(productCountinCart)

    return logged_in, username, productCountinCartForGivenUser


def getProductDetails(productId):
    productDetailsById = Product.query.filter(Product.id == productId).first()
    return productDetailsById

def extractAndPersistKartDetailsUsingSubquery(productId):
    user = User.query.filter(User.email == session['email']).first()
    userId = user.id

    subqury = Cart.query.filter(Cart.userid == userId).filter(Cart.productid == productId).subquery()
    qry = db.session.query(Cart.quantity).select_entity_from(subqury).all()

    if len(qry) == 0:
        cart = Cart(userid=userId, productid=productId, quantity=1)
    else:
        cart = Cart(userid=userId, productid=productId, quantity=qry[0][0] + 1)

    db.session.merge(cart)
    db.session.flush()
    db.session.commit()

def getusercartdetails():
    user = User.query.filter(User.email == session['email']).first()
    userId = user.id

    productsincart = Product.query.join(Cart, Product.id == Cart.productid) \
        .add_columns(Product.id, Product.product_name, Cart.quantity, Product.regular_price) \
        .add_columns().filter(
        Cart.userid == userId)
    totalsum = 0

    for row in productsincart:
        totalsum += row[4] * row[3]


    return productsincart, totalsum


def removeProductFromCart(productId):
    user = User.query.filter(User.email == session['email']).first()
    userId = user.id
    kwargs = {'userid': userId, 'productid': productId}
    cart = Cart.query.filter_by(**kwargs).first()
    if productId is not None:
        db.session.delete(cart)
        db.session.commit()
        flash("Product has been removed from cart !!")
    else:
        flash("failed to remove Product cart please try again !!")
    return redirect(url_for('shopcart'))



def extractOrderdetails(totalsum):
    orderdate = datetime.utcnow()
    user = User.query.filter(User.email == session['email']).first()
    userId = user.id
    order = Order(order_date=orderdate, total_price=totalsum, userid=userId)
    db.session.add(order)
    db.session.flush()
    db.session.commit()

    order = Order.query.filter(Order.userid == userId).order_by(
        Order.id.desc()).first()
    orderid = order.id

    addOrderedproducts(userId, orderid)

    removeordprodfromcart(userId)

    return orderid

def addOrderedproducts(userId, orderid):
    cart = Cart.query.with_entities(Cart.productid, Cart.quantity).filter(Cart.userid == userId)

    for item in cart:
        orderedproduct = OrderedProduct(orderid=orderid, productid=item.productid, quantity=item.quantity)
        db.session.add(orderedproduct)
        db.session.flush()
        db.session.commit()

def removeordprodfromcart(userId):
    userid = userId
    db.session.query(Cart).filter(Cart.userid == userid).delete()
    db.session.commit()


