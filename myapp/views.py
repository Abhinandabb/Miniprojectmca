from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, request
from django.shortcuts import render

# Create your views here.
from myapp.models import *


def login(request):
    return render(request,"login.html")
def login_post(request):
    name=request.POST['textfield']
    password=request.POST['textfield2']
    lobj=Login.objects.filter(username=name,password=password)

    if lobj.exists():
        lobj1 = Login.objects.get(username=name, password=password)
        request.session['lid']=lobj1.id
        if lobj1.type=='admin':
            return HttpResponse('<script>alert("success");window.location="/myapp/admin_home/"</script>')
        elif lobj1.type=='farmer':
            return HttpResponse('<script>alert("success");window.location="/myapp/farmer_home/"</script>')
        elif lobj1.type=='user':
            return HttpResponse('<script>alert("success");window.location="/myapp/user_home/"</script>')
        else:
            return HttpResponse('<script>alert("not found");window.location="/myapp/login/"</script>')
    else:
        return HttpResponse('<script>alert("not found");window.location="/myapp/login/"</script>')


def admin_home(request):
    return render(request,"admin/Admin_home.html")

def change_password(request):
    return render(request,"admin/change password.html")

def change_password_post(request):
    current=request.POST['textfield']
    newpass=request.POST['textfield2']
    confirmpass=request.POST['textfield3']
    id=request.session['lid']

    obj=Login.objects.get(id=id)
    if obj.password == current:
        if confirmpass == newpass:
            log=Login.objects.filter(id=id).update(password=confirmpass)
            return HttpResponse('''<script>alert("Password updates");window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse('''<scipt>alert("password missing");window.location="/myapp/admin_change_passw/"</script>''')
    else:
        return HttpResponse('''<script>alert("please check your paasword");window.location="/myapp/admin_change_passw/"</script>''')



def admin_add_category(request):
    return render(request,"admin/admin add category.html")

def admin_add_category_post(request):
    name=request.POST['textfield']

    obj=category()
    obj.category=name
    obj.save()
    return HttpResponse('<script>alert("success");window.location="/myapp/admin_add_category/"</script>')




def admin_view_category(request):
    o=category.objects.all()
    return render(request,"admin/view category.html",{"data":o})



def admin_edit_category(request,id):
    res=category.objects.get(id=id)
    return render(request,"admin/admin edit  category.html",{"data":res})


def admin_edit_category_post(request):
    id=request.POST['id']
    name=request.POST['textfield1']
    obj = category.objects.get(id=id)
    obj.category =name
    obj.save()
    return HttpResponse('<script>alert("success");window.location="/myapp/admin_view_category"</script>')


def admin_delete_category(request,id):
    c=category.objects.get(id=id)
    c.delete()
    return HttpResponse('''<script>alert('Delete Successfull');window.location="/myapp/admin_view_category/"</script>''')

def admin_order(request,id):
    return render(request,"admin/admin order.html",{'id':id})

def admin_order_post(request):
    # import razorpay
    # razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    # razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"
    #
    # razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    # amount = 200


    id = request.POST['id']

    i=product.objects.get(id=id)
    qty=request.POST["textfield"]


    quantity = request.POST['textfield']
    ttl = int(quantity) * int(i.price)



    p=product.objects.get(id=id).Farmer.id
    pm=purchase_main()
    pm.Farmer_id=p
    from datetime import datetime
    pm.date=datetime.now().today()
    pm.amount=ttl
    pm.status='pending'
    pm.save()

    ps=puchase_sub()
    ps.purchase_main=pm
    ps.Product_id=id
    ps.amount=ttl
    ps.quantity=quantity
    ps.status='pending'
    ps.save()

    py=shopkeeper_payment()
    py.Purchase_main=pm
    py.date=datetime.today()
    py.price=ttl
    py.status='paid'
    py.save()
    return HttpResponse('<script>alert("success");window.location="/myapp/admin_viewfarmers_products/"</script>')


    # # Create a Razorpay order (you need to implement this based on your logic)
    # order_data = {
    #     'amount': amount,
    #     'currency': 'INR',
    #     'receipt': 'order_rcptid_11',
    #     'payment_capture': '1',  # Auto-capture payment
    # }
    #
    # # Create an order
    # order = razorpay_client.order.create(data=order_data)
    #
    # context = {
    #     'razorpay_api_key': razorpay_api_key,
    #     'amount': order_data['amount'],
    #     'currency': order_data['currency'],
    #     'order_id': order['id'],
    # }
    #
    # obj = shopkeeper_payment()
    # obj.User = user.objects.get(Login_id=request.session['lid'])
    #
    # obj.date = datetime.now().strftime('%Y%m%d')
    # obj.price = amount
    # obj.status = 'paid'
    # obj.save()
    #
    # return render(request, 'user/payment.html', {'razorpay_api_key': razorpay_api_key,
    #                                              'amount': order_data['amount'],
    #                                              'currency': order_data['currency'],
    #                                              'order_id': order['id'], "id": id})

    # quantity=request.POST['textfield']
    # id=request.POST['id']
    #
    # p=product.objects.get(id=id).Farmer.id
    # pm=purchase_main()
    # pm.Farmer_id=p
    # from datetime import datetime
    # pm.date=datetime.now().today()
    # pm.amount="0"
    # pm.status='pending'
    # pm.save()
    #
    # ps=puchase_sub()
    # ps.purchase_main=pm
    # ps.Product_id=id
    # ps.amount='0'
    # ps.quantity=quantity
    # ps.status='pending'
    # ps.save()
    #
    # py=shopkeeper_payment()
    # py.Purchase_main=pm
    # py.date=datetime.today()
    # py.price=amount
    # py.status='paid'
    # py.save()
    # return HttpResponse('<script>alert("success");window.location="/myapp/admin_viewfarmers_products/"</script>')


def admin_purchase_main(request):
    obj = purchase_main.objects.all().order_by('-id')
    return render(request,"admin/admin purchase main.html",{'data':obj})



def admin_view_payment(request):
    obj=user_payment.objects.all()
    return render(request,"admin/view payment.html",{"data":obj})


def admin_purchase_sub(request,id):
    obj = puchase_sub.objects.filter(purchase_main_id=id)
    return render(request,"admin/admin purchase sub.html",{'data':obj})

def admin_viewfarmers_products(request):
    obj=farmer.objects.all()
    return render(request,"admin/admin view farmer&products.html",{"data":obj})

def admin_viewproducts_order(request,id):
    obj=product.objects.filter(Farmer_id=id)
    return render(request,"admin/view prodts & buyadmin.html",{"data":obj})



def admin_viewproducts_order_post(request):
    sc=request.POST['textfield2']
    o=product.objects.filter(name__icontains=sc)
    return render(request,"admin/view prodts & buyadmin.html",{"data":o})



def admin_addstock(request):
    obj=product.objects.all()
    return render(request,"admin/admin update stock.html",{"data":obj})

def admin_add_stock_post(request):
    product=request.POST['pp']
    stocks=request.POST['textfield2']


    obj=stock()
    obj.Product_id=product
    obj.quantity=stocks
    obj.save()

    return HttpResponse('<script>alert("success");window.location="/myapp/admin_home/"</script>')


def admin_viewstock(request):
    o=stock.objects.all()
    return render(request,"admin/view stock.html",{"data":o})

def admin_viewstock_post(request):
    sc=request.POST['textfield2']
    o = stock.objects.filter(Product__name__icontains=sc)
    return render(request, "admin/view stock.html", {"data": o})

def admin_editstock(request,id):
    obj = product.objects.all()
    data2=stock.objects.get(id=id)
    return render(request,"admin/edit stock.html",{'data':obj,'data2':data2})

def admin_editstock_post(request):
    product=request.POST['pp']
    stocks=request.POST['textfield2']
    sid=request.POST['sid']

    obj=stock.objects.get(id=sid)
    obj.Product_id=product
    obj.quantity=stocks
    obj.save()

    return HttpResponse('''<script>alert('updated Successfull');window.location="/myapp/admin_viewstock/"</script>''')


def admin_delete_stock(request,id):
    obj=stock.objects.get(id=id)
    obj.delete()
    return HttpResponse('''<script>alert('Delete Successfull');window.location="/myapp/admin_viewstock/"</script>''')

def admin_send_notification(request):
    return render(request,"admin/admin send notification.html")

def admin_send_notification_post(request):
    noti=request.POST['textfield']

    obj=notification()
    obj.notification=noti

    from datetime import datetime
    obj.date=datetime.now().today()
    obj.save()
    return HttpResponse('''<script>alert('add notification');window.location="/myapp/admin_home/"</script>''')

def admin_view_user_order(request):
    obj=order_main.objects.all()
    return render(request,"admin/Admin view user order.html",{"data":obj})

def admin_order_main(request):
    obj=order_main.objects.all()
    return render(request,"admin/order_main.html",{"data:obj"})

def admin_order_sub(request,id):
    obj=order_sub.objects.filter(order_main_id=id)
    return render(request,"admin/order sub.html",{"data":obj})

def admin_view_complaints(request):
    obj=complaint.objects.all()
    return render(request,"admin/admin view complaints.html",{"data":obj})

def admin_view_complaints_post(request):
    from_date=request.POST['textfield']
    to_date=request.POST['textfield2']
    obj=complaint.objects.filter(date__range=[from_date,to_date])
    return render(request, "admin/admin view complaints.html",{"data":obj})


def admin_send_reply(request,id):
    data=complaint.objects.get(id=id)
    return render(request,"admin/admin send reply.html",{'data':data})

def admin_send_reply_post(request):
    cid=request.POST['cid']
    reply=request.POST['textarea']
    obj=complaint.objects.filter(id=cid).update(reply=reply,status='replied')
    return HttpResponse('''<script>alert('success');window.location="/myapp/admin_view_complaints/"</script>''')


def admin_view_feedback(request):
    obj=feedback.objects.all()
    return render(request,"admin/view feedback.html",{"data":obj})

def admin_view_feedback_post(request):
    from_date=request.POST['textfield']
    to_date=request.POST['textfield2']
    obj=feedback.objects.filter(date__range=[from_date,to_date])
    return render(request, "admin/view feedback.html", {"data": obj})


def raz_pay1(request,amount):
    import razorpay
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    # amount = 200
    amount= float(amount)*100

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order1 = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order1['id'],
    }



    return render(request, 'admin/payment1.html',{ 'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order1['id'],"id":id})


#farmer

def farmer_home(request):
    return render(request,"farmer/farmerhome.html")
def farmer_change_password(request):
    return render(request,"farmer/change password.html")

def farmer_change_password_post(request):
    currentpassw=request.POST['textfield']
    newpassw=request.POST['textfield2']
    confirmpassw=request.POST['textfield3']
    id = request.session['lid']

    obj = Login.objects.get(id=id)
    if obj.password == currentpassw:
        if confirmpassw == newpassw:
            log = Login.objects.filter(id=id).update(password=confirmpassw)
            return HttpResponse('''<script>alert("Password updates");window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse(
                '''<scipt>alert("password missing");window.location="/myapp/farmer_change_password/"</script>''')
    else:
        return HttpResponse(
            '''<script>alert("please check your paasword");window.location="/myapp/farmer_change_password/"</script>''')





def farmer_registration(request):
    return render(request,"farmer/farmer registration.html")

def farmer_registration_post(request):
    name=request.POST['textfield']
    email=request.POST['textfield2']
    ph_no=request.POST['textfield3']
    place=request.POST['textfield4']
    pin=request.POST['textfield5']
    post=request.POST['textfield6']
    photo=request.FILES['fileField']
    password=request.POST['textfield7']
    confirmpassw=request.POST['textfield8']
    fs = FileSystemStorage()
    import datetime
    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    fs.save(date, photo)
    path = fs.url(date)

    if password==confirmpassw:
        l = Login()
        l.username = email
        l.password = password
        l.type = "farmer"
        l.save()

        obj = farmer()
        obj.name = name
        obj.email = email
        obj.ph_no = ph_no
        obj.place = place
        obj.pin = pin
        obj.post = post
        obj.pin = pin
        obj.post = post
        obj.image = path
        obj.Login = l
        obj.save()


        return HttpResponse('<script>alert("success");window.location="/myapp/login/"</script>')


def farmer_view_profile(request):
    obj=farmer.objects.get(Login_id=request.session['lid'])
    return render(request,"farmer/view profile.html",{'data':obj})



def farmer_update_profile(request):
    obj = farmer.objects.get(Login_id=request.session['lid'])
    return render(request,"farmer/update profile.html",{'data':obj})


def farmer_update_profile_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    place = request.POST['textfield4']
    pin = request.POST['textfield5']
    post = request.POST['textfield6']

    obj = farmer.objects.get(Login_id=request.session['lid'])
    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']
        if photo !="":
            fs = FileSystemStorage()
            import datetime
            date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
            fs.save(date, photo)
            path = fs.url(date)
            obj.image = path

    obj.name = name
    obj.email = email
    obj.ph_no = phone
    obj.place = place
    obj.pin = pin
    obj.post = post
    obj.pin = pin
    obj.post = post
    obj.save()

    return HttpResponse('<script>alert("success");window.location="/myapp/farmer_view_profile/"</script>')


def farmer_add_product(request):
    res=category.objects.all().order_by('category')
    return render(request,"farmer/farmer manage product.html",{"data":res})

def farmer_add_product_post(request):
    name=request.POST['textfield']
    type=request.POST['textfield2']
    quantity=request.POST['textfield3']
    description=request.POST['textarea']
    image=request.FILES['fileField']
    price=request.POST['textfield4']
    category=request.POST['select']

    fs=FileSystemStorage()
    import datetime
    date=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+".jpg"
    fs.save(date,image)
    path=fs.url(date)


    obj=product()
    obj.name=name
    obj.type=type
    obj.quantity=quantity
    obj.description=description
    obj.image=path
    obj.price=price
    obj.Category_id=category
    obj.Farmer=farmer.objects.get(Login_id= request.session['lid'])
    obj.save()
    return HttpResponse('<script>alert("success");window.location="/myapp/farmer_add_product/"</script>')



def farmer_view_product(request):
    o=product.objects.all()
    return render(request,"farmer/farmer view product.html",{"data":o})

def farmer_view_product_post(request):
    sc=request.POST['textfield2']
    o=product.objects.filter(name__icontains=sc)
    return render(request,"farmer/farmer view product.html",{"data":o})



def farmer_edit_product(request,id):
    res=product.objects.get(id=id)
    data = category.objects.all()
    return render(request,"farmer/farmer edit product.html",{"data":data,"data2":res})

def farmer_edit_product_post(request):
    id = request.POST['id']
    name = request.POST['textfield']
    type = request.POST['textfield2']
    quantity = request.POST['textfield3']
    description = request.POST['textfield4']

    price = request.POST['textfield5']
    category = request.POST['select']

    if 'fileField' in request.FILES:
        image = request.POST['fileField']
        fs = FileSystemStorage()
        import datetime
        date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
        fs.save(date,image)
        path = fs.url(date)

        obj = product.objects.get(id=id)
        obj.name = name
        obj.type = type
        obj.quantity = quantity
        obj.description = description
        obj.image = path
        obj.price = price
        obj.Category_id = category
        obj.Farmer = farmer.objects.get(Login_id=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('update sucessfull');window.location='/myapp/farmer_view_product'</script>")

    else:
        obj = product.objects.get(id=id)
        obj.name = name
        obj.type = type
        obj.quantity = quantity
        obj.description = description
        obj.price = price
        obj.Category_id = category
        obj.Farmer = farmer.objects.get(Login_id=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('update sucessfull');window.location='/myapp/farmer_view_product'</script>")


def farmer_delete_product(request,id):
    obj=product.objects.get(id=id)
    obj.delete()
    return HttpResponse('''<script>alert('Delete Successfull');window.location="/myapp/farmer_view_product/"</script>''')

def farmer_view_notifications(request):
    obj=notification.objects.all().order_by('-id')
    return render(request,"farmer/view notification.html",{"data":obj})

def farmer_view_payment(request):
    obj=shopkeeper_payment.objects.all().order_by('-id')
    return render(request,"farmer/view payment.html",{"data":obj})

def farmer_view_order(request):
    obj=purchase_main.objects.filter(Farmer__Login_id=request.session['lid'],status='pending').order_by('-id')
    return render(request,"farmer/view order.html",{"data":obj})
def farmer_view_approved_order(request):
    obj=purchase_main.objects.filter(Farmer__Login_id=request.session['lid'],status='approved').order_by('-id')
    return render(request,"farmer/view order accp reje.html",{"data":obj})

def farmer_view_more(request,id):
    obj=puchase_sub.objects.filter(purchase_main_id=id)
    return render(request,"farmer/view more.html",{'data':obj})

def farmer_approve_order(request,id):
    obj=purchase_main.objects.filter(id=id).update(status="approved")
    return HttpResponse('''<script>alert('Approved');window.location="/myapp/farmer_view_order/"</script>''')

def farmer_reject_order(request,id):
    obj=purchase_main.objects.filter(id=id).update(status="rejected")
    return HttpResponse('''<script>alert('Rejected');window.location="/myapp/farmer_view_order/"</script>''')

#user


def userhome(request):
    return render(request,"user/userhome.html")
def user_change_password(request):
    return render(request,"user/change password.html")

def user_change_passw_post(request):
    currentpassw=request.POST['textfield']
    newpassw=request.POST['textfield2']
    confirmpassw=request.POST['textfield3']
    id=request.session['lid']
    obj = Login.objects.get(id=id)
    if obj.password == currentpassw:
        if confirmpassw == newpassw:
            log = Login.objects.filter(id=id).update(password=confirmpassw)
            return HttpResponse('''<script>alert("Password updates");window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse(
                '''<scipt>alert("password missing");window.location="/myapp/user_change_passw/"</script>''')
    else:
        return HttpResponse(
            '''<script>alert("please check your paasword");window.location="/myapp/user_change_passw/"</script>''')


def user_registration(request):
    return render(request,"user/user registration.html")

def user_registration_post(request):
    name=request.POST['textfield']
    age=request.POST['textfield9']
    email=request.POST['textfield2']
    phone=request.POST['textfield3']
    place=request.POST['textfield4']
    pin=request.POST['textfield5']
    post=request.POST['textfield6']
    gender=request.POST['RadioGroup1']
    password=request.POST['textfield7']
    confirmpassw=request.POST['textfield8']

    if password==confirmpassw:
        l = Login()
        l.username = email
        l.password = password
        l.type = "user"
        l.save()

        obj=user()
        obj.name=name
        obj.age=age
        obj.email=email
        obj.ph_no=phone
        obj.place=place
        obj.pin=pin
        obj.post=post
        obj.gender=gender
        obj.Login=l
        obj.save()
    return HttpResponse('<script>alert("success");window.location="/myapp/login/"</script>')


def user_view_profile(request):
    obj = user.objects.get(Login_id=request.session['lid'])
    return render(request,"user/view profile.html",{'data':obj})

def user_view_product(request):
    obj=product.objects.all()
    return render(request,"user/view product.html",{"data":obj})

def user_view_product_post(request):
    sc=request.POST['textfield2']
    obj=product.objects.filter(name__icontains=sc)
    return render(request,"user/view product.html",{"data":obj})

def user_add_productto_cart(request,id):
    data=stock.objects.get(Product_id=id)
    return render(request,"user/add prd to cart.html",{"data":data})

def user_add_productto_cart_post(request):
    quantity=request.POST['quantity']
    pid=request.POST['pid']

    if int(quantity) > int(stock.objects.get(Product_id=pid).quantity):
        print(stock.objects.get(Product_id=pid).quantity)
        return HttpResponse('<script>alert("out of stock");window.location="/myapp/user_view_product/"</script>')
    elif int(quantity) <= int(stock.objects.get(Product_id=pid).quantity):
        re=cart.objects.filter(product_id=pid)

        if re.exists():
            e = cart.objects.get(product_id=pid).quantity
            qu = int(e) + int(quantity)
            cart.objects.filter(product_id=pid).update(quantity=qu)
            return HttpResponse('<script>alert("added to cart successfully");window.location="/myapp/user_view_cart/"</script>')
        else:
            data=cart()
            data.User=user.objects.get(Login_id=request.session['lid'])
            data.product_id=pid
            data.quantity=quantity
            data.save()
            return HttpResponse('<script>alert("added to cart successfully");window.location="/myapp/user_view_cart/"</script>')
    else:
        return HttpResponse('<script>alert("please add valid data");window.location="/myapp/user_view_cart/"</script>')


def user_view_cart(request):
    data=cart.objects.filter(User__Login_id=request.session['lid'])
    l=[]
    total_sum = 0
    for i in data:
        ttl = int(i.quantity) * int(i.product.price)
        total_sum += ttl
    # ttl=int(i.quantity)*int(i.product.price)

        l.append({
            'id':i.id,
            'name':i.product.name,
            'quantity':i.quantity,
            'price':i.product.price,
            'ttl':ttl

        })


    return render(request,"user/view cart.html",{"data":data,"total_sum": total_sum})

def user_remove_cart(request,id):
    obj=cart.objects.get(id=id)
    obj.delete()
    return HttpResponse('''<script>alert('Delete Successfull');window.location="/myapp/user_view_cart/"</script>''')

def user_send_complaints(request):
    return render(request,"user/send complaints.html")

def user_send_complaints_post(request):
    complain=request.POST['textarea']
    obj=complaint()
    obj.date=datetime.now().strftime('%Y-%m-%d')
    obj.complaint=complain
    obj.reply='pending'
    obj.status='pending'
    obj.User=user.objects.get(Login=request.session['lid'])
    obj.save()
    return HttpResponse('<script>alert("complaint sent successfully" );window.location="/myapp/user_view_reply/"</script>')

def user_view_reply(request):
    obj=complaint.objects.filter(User__Login_id=request.session['lid'])
    return render(request,"user/view reply.html",{"data":obj})

def user_send_feedback(request):
    return render(request,"user/feedback user.html")

def user_send_feedback_post(request):
    feedbac=request.POST['textarea']
    obj=feedback()
    obj.date=datetime.now().strftime('%Y-%m-%d')
    obj.feedback=feedbac
    obj.User = user.objects.get(Login=request.session['lid'])
    obj.save()
    return HttpResponse('<script>alert("feedback sent successfully" );window.location="/myapp/user_send_feedback/"</script>')


def raz_pay(request,amount):
    import razorpay
    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    # amount = 200
    amount= float(amount)*100

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    pay=order_main()
    pay.User=user.objects.get(Login_id=request.session['lid'])
    pay.date=datetime.today()
    pay.amount=amount
    pay.status='ordered'
    pay.save()


    c=cart.objects.filter(User__Login_id= request.session['lid'])

    for i in c:





        pay2=order_sub()
        pay2.order_main=pay
        pay2.Product=i.product
        pay2.quantity=i.quantity
        pay2.save()


    obj = user_payment()
    obj.User=user.objects.get(Login_id=request.session['lid'])
    obj.order_main=pay
    obj.date = datetime.now().strftime('%Y%m%d')
    obj.amount = amount
    obj.status='paid'
    obj.save()

    if obj.status == 'paid':
        cart.objects.filter(User__Login_id=request.session['lid']).delete()

    return render(request, 'user/payment.html',{ 'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],"id":id})











