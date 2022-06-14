from itertools import product
from operator import itemgetter
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) 
                                     # Related to the User imported
                                     # OneToOneField to mean a user can only have one customer and vice versa
                                     # blank=True  meaning the field will not be required in the forms
                                     # blank=False  meaning the field cannot be blank in the forms

	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name  # The value that will show up in our admin panel and when we create the model.



class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True, blank=True)
                   # BooleanField for digital bcos its either a product is ordered online or physical
                   # default=False bcos by default all ordered items should be physical unless otherwise. 
    image = models.ImageField(null=True, blank=True)
  
    def __str__(self):
        return self.name # Returns the product name in the database.


        # model for order placed by the client
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
                        # Related the order to a customer
                        # Has a relationship of many to One rshp with...
                                        #.....customer..meaning one singular customer can have many orders. 
                       # on_delete=models.SET_NULL.....so that if a customer gets deleted, we dont delete the order.
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
                        # default=False.....meaning the cart will remain open and we will keep adding items as long as its false.
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)   # Return the ID of the order. Its the only way we can identify the order.
                              # Bcos the ID is an integer, we have to add str to change it to a string value.
	
		#To get the total value of the order
	@property # We use the @property decorator so we can access these like attributes.
	def get_cart_total(self):
		orderitems = self.orderitem_set.all() #To get the items ordered into that order
		total = sum([item.get_total for item in orderitems]) # To get the total value using orderitems created above
		return total

			#To get the total number of items of the order
	@property # We use the @property decorator so we can access these like attributes.
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems]) # To get how many items are in a cart/in an overall order
		return total

# model for the items that need to be added to the Order
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
                       # on_delete=models.SET_NULL...so that if a customer gets deleted, we dont delete the order.
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
                        # default=0......so that we will increment from 0 on the dashboard as a user.
	date_added = models.DateTimeField(auto_now_add=True)


			# To get the total value for each ORDERED ITEM and the number of items ordered. 
			# That's why we put this function in the model OrderItem
	@property # We use the @property decorator so we can access these like attributes.
	def get_total(self):
		total = self.product.price * self.quantity
		return total # We then render this in the cart.html

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
