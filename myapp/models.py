from django.db import models

class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class category(models.Model):
    category=models.CharField(max_length=100)

class farmer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    ph_no=models.BigIntegerField()
    place=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    image=models.CharField(max_length=200)
    Login=models.ForeignKey(Login,on_delete=models.CASCADE)


class product(models.Model):
    Farmer=models.ForeignKey(farmer,on_delete=models.CASCADE)
    Category=models.ForeignKey(category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    price=models.CharField(max_length=100)

class stock(models.Model):
    Product=models.ForeignKey(product,on_delete=models.CASCADE)
    # price=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)

class user(models.Model):
    Login=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pin=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    ph_no=models.BigIntegerField()
    status=models.CharField(max_length=100)

class feedback(models.Model):
    User=models.ForeignKey(user,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=300)
    date=models.CharField(max_length=100)

class cart(models.Model):
    User=models.ForeignKey(user,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=100)

class complaint(models.Model):
    User=models.ForeignKey(user,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    complaint=models.CharField(max_length=300)
    reply=models.CharField(max_length=100)
    status=models.CharField(max_length=100)


class order_main(models.Model):
    User=models.ForeignKey(user,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class order_sub(models.Model):
    order_main=models.ForeignKey(order_main,on_delete=models.CASCADE)
    Product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    # status=models.CharField(max_length=100)


class user_payment(models.Model):
    User=models.ForeignKey(user,on_delete=models.CASCADE)
    order_main=models.ForeignKey(order_main,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class purchase_main(models.Model):
     Farmer=models.ForeignKey(farmer,on_delete=models.CASCADE)
     date=models.CharField(max_length=100)
     amount=models.CharField(max_length=100)
     status=models.CharField(max_length=100)

class shopkeeper_payment(models.Model):
    Purchase_main=models.ForeignKey(purchase_main,on_delete=models.CASCADE)
    date=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

class puchase_sub(models.Model):
    purchase_main=models.ForeignKey(purchase_main,on_delete=models.CASCADE)
    Product=models.ForeignKey(product,on_delete=models.CASCADE)
    amount=models.CharField(max_length=100)
    quantity=models.CharField(max_length=100)
    status=models.CharField(max_length=100)


class notification(models.Model):
    notification=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
