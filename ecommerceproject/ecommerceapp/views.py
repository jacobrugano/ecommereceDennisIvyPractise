from wsgiref.util import request_uri
from django.shortcuts import render
from .models import Product, Customer, Order, OrderItem, ShippingAddress


def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'ecommerceapp/store.html', context)


def cart(request):
    if request.user.is_authenticated: #We first check of the user is authenticated.
        customer = request.user.customer #If authenticated, get the customer details.
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # To create the entire order
                                                # Then get or create the order using get_or_create() method
                                                # customer=customer...been order for the customer we just queried. 
                                                # complete=False.....to make it automatically an open cart.

        items = order.orderitem_set.all() # To get the items attached to that order we just queried in above line.
                                        # Now that we have the customer and the order, we now query the cart........ 
                                                    #..........items using the order.orderitem_set.all() method.
                                        # Here we are able to  query the child items by setting the parent value order and then 
                                            ###...the child object all orderitem in lower case values and then _set.all()
    
    else: # We create an empty cart / list for the none logged in users
        items = []  
        order = {'get_cart_total':0, 'get_cart_items':0} # Create an order for users who are not logged in

    context = {'items':items, 'order':order}
    return render(request, 'ecommerceapp/cart.html', context)


def checkout(request):
        if request.user.is_authenticated: #We first check of the user is authenticated.
            customer = request.user.customer #If authenticated, get the customer details.
            order, created = Order.objects.get_or_create(customer=customer, complete=False) # To create the entire order
                                                    # Then get or create the order using get_or_create() method
                                                    # customer=customer...been order for the customer we just queried. 
                                                    # complete=False.....to make it automatically an open cart.

            items = order.orderitem_set.all() # To get the items attached to that order we just queried in above line.
                                        # Now that we have the customer and the order, we now query the cart........ 
                                                    #..........items using the order.orderitem_set.all() method.
                                        # Here we are able to  query the child items by setting the parent value order and then 
                                            ###...the child object all orderitem in lower case values and then _set.all()
        
        else: # We create an empty cart / list for the none logged in users
            items = []  
            order = {'get_cart_total':0, 'get_cart_items':0} # Create an order for users who are not logged in

        context = {'items':items, 'order':order}
        return render(request, 'ecommerceapp/checkout.html', context)

