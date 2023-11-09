from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime

from .models.product import Product
from .models.orderfact import OrderFact
from .models.inventory import Inventory
from .models.carts import Cart

from flask import Blueprint, request
bp = Blueprint('index', __name__)


@bp.route('/', methods = ['GET', 'POST'])
def index():

    # determines table size
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    # finds order history, number of rows in order history
    products = Product.get_byoffset(per_page, offset)
        
    # logic for front and back buttons
    if request.method == 'POST':
        if request.form['action'] == 'next':
            page += 1
        elif request.form['action'] == 'prev':
            page -= 1

        return redirect(url_for('index.index', page = page))
        

    products_all = Product.get_all()
    if current_user.is_authenticated:
        purchases = OrderFact.get_orders_given_buyer(current_user.id)
        return render_template('index.html', avail_products=products, 
                                            purchase_history=purchases, 
                                            current_page = page,
                                            page_length = per_page,
                                            total_avail = products_all,
                                            #seller_check=current_user.is_seller(current_user.id), 
                                            cart_check=current_user.has_cart(current_user.id))
    else:
        return render_template('index.html', avail_products=products,
                               current_page = page,
                               page_length = per_page,
                               total_avail = products_all)
    

#@bp.route('/seller')
#def seller():
#    if current_user.is_authenticated:
#        inventory = Inventory.get_products_given_seller(current_user.id)
#        return render_template('seller.html', inventory=inventory)
#    else:
#        return redirect(url_for('index.index'))
    
    
@bp.route('/cart')
def cart():
    if current_user.is_authenticated:
        cart = Cart.users_cart(current_user.id)
        return render_template('cart.html', cart=cart)
    else:
        return redirect(url_for('index.index'))
    