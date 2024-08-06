from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings as conf_settings
from django.core.mail import send_mail
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from serviceProvider.models import Services
from serviceProvider.models import Business_details
from bookings.models import Bookings
import razorpay
from django.db.models import Q
from users.models import Address

# Create your views here.

def home(request):
 
   return render(request, "users/home.html")

def user_registration(request):
 data={}
 is_staff = False
 if(request.method=="POST"):
    username=request.POST.get('username')
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    email=request.POST.get('email')
    password=request.POST.get('password')
    utype = request.POST.get('type')
    print(username, first_name,last_name ,email, password, utype)

    if(utype == "Seller"):
       is_staff = True

    if(username=="" or first_name == "" or last_name =="" or email=="" or password==""):
      data['message'] = f"Fileds can't be empty"
      return render(request, "users/register.html", context=data)
    elif(User.objects.filter(username=username).exists()):
      data['message'] = username+" already exists"
      return render(request, 'users/register.html', context=data)
    elif(User.objects.filter(email=email).exists()):
      data['message'] = "email already exists"
      return render(request, 'users/register.html', context=data)
    else:
        date_joined = datetime.datetime.now()
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, date_joined=date_joined, is_staff=is_staff)
        user.set_password(password)
        user.save()


        subject = 'Welcome to CarGo!'
        if(is_staff==True):
           
         message = f'''Hi {user.username}, You are registered as a Servive provider thank you for signing up and joining our community of car enthusiasts. 
        
We are thrilled to have you on board! At CarGo, we aim to make your life easier by bringing top-notch car wash services right to your doorstep. No more waiting in long lines or dealing with inconvenient car wash trips—simply book your service online and let us take care of the rest.
        
        
To get started, simply log in to your account and explore our services. We recommend booking your first car wash today to experience the convenience and quality of CarGo firsthand.

Best regards,

The CarGo Team
        '''
         email_from = conf_settings.EMAIL_HOST_USER
         recipient_list = [user.email, ]
         send_mail( subject, message, email_from, recipient_list )
        else:
              
         message = f'''Hi {user.username}, thank you for signing up and joining our community of car enthusiasts. 
        
We are thrilled to have you on board! At CarGo, we aim to make your life easier by bringing top-notch car wash services right to your doorstep. No more waiting in long lines or dealing with inconvenient car wash trips—simply book your service online and let us take care of the rest.
        
        
To get started, simply log in to your account and explore our services. We recommend booking your first car wash today to experience the convenience and quality of CarGo firsthand.

Best regards,

The CarGo Team
           
'''
         email_from = conf_settings.EMAIL_HOST_USER
         recipient_list = [user.email, ]
         send_mail( subject, message, email_from, recipient_list )


        return redirect("/login")



   
    
 return render(request, "users/register.html")


def user_login(request):
    data={}
    if(request.method=='POST'):
       username = request.POST.get('username')
       password = request.POST.get('password')
       print(f"Username: {username}, Password: {password}")

       if(username=="" or password==""):
          data['message'] = "field's can't be empty 🥲"
          return render(request, "users/login.html", context=data)
       elif(not User.objects.filter(username=username).exists()):
         data['message'] =  "Username does not exists"
         return render(request,'users/login.html',context=data)
       else:
           user=authenticate(username=username, password=password)
           if user is None:
               data['message']="Wrong password"
               return render(request, "users/login.html", context=data)
           else:
              login(request, user)
              if(user.is_staff==True):
                 messages.success(request, "Logged as Service provider")
                 return redirect("/provider/home")
              else:
               #   messages.success(request, "Logged in sucessful")
                 return redirect("/services")
    
    return render(request, "users/login.html")


def user_logout(request):
   logout(request)
   messages.error(request, "Logged out")
   return redirect("/")

def services(request):
      data={}
      
      if(request.user.is_authenticated):
         show_business = Business_details.objects.all()
         data['services'] = show_business


        
         return render(request, "users/services.html", context=data)
      else:
         return redirect("/")

def view_services(request, sid):
   global filtered_price
   data={}
   service_provider = Services.objects.filter(sid=sid)
   filtered_price = service_provider.order_by("price")
   data['services']=filtered_price

   return render(request, "users/view_services.html", context=data)

def bookService(request, id):
    data1 = {}
    book_service = get_object_or_404(Services, id=id)
    show_business = get_object_or_404(Business_details, sid=book_service.sid)
    total_price = int(book_service.price * 100)  # Convert price to paise
    
    data1['order'] = book_service
    data1['details'] = show_business
    
    try:
        user_details = get_object_or_404(Address, user_id=request.user.id)
    except:
        return redirect("/add-address/")
    
    data1['users'] = user_details
    data1['total_price'] = total_price

    # Payment gateway setup
    client = razorpay.Client(auth=("rzp_test_XRjX6qJ69ajxxs", "s56837vKNGmoW2BiQkQbC3sH"))
    data = {"amount": total_price, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = client.order.create(data=data)
    data1['payment'] = payment

    if request.method == "POST":
        x = datetime.datetime.now()
        booking = Bookings.objects.create(booking_date=x, service=book_service, user=request.user, status='Pending')
        booking.save()
        
        # Prepare email content
        subject = 'Your Booking Confirmation - CarGo Service'
        message = f'''Hi {request.user.username},

Thank you for booking a service with CarGo! We're excited to confirm that your car wash appointment has been successfully scheduled.

Booking Summary:
Service Provider: {show_business.carwash_name}
Service: {book_service.name}
Date: {x.strftime('%Y-%m-%d %H:%M:%S')}
Price: ₹{book_service.price}
Address: {user_details.address}

To make the most of your booking, please ensure that your car is ready for the scheduled service time. If you need to reschedule or have any questions, feel free to contact us at prabuddhachunchekar@gmail.com or call us at +91-900-440-8906.

We look forward to serving you!

Best regards,
The CarGo Team
'''
        email_from = conf_settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        send_mail(subject, message, email_from, recipient_list)

        return redirect("/your-bookings")

    return render(request, "users/booknow.html", context=data1)
def booking_summary(request):
   data={}
   user_id = request.user.id
   bookings = Bookings.objects.filter(user_id=user_id)
   data['mybooking'] = bookings
   return render(request, "users/your_bookings.html", context=data)



def add_address(request):
    get_user = request.user.id
    if Address.objects.filter(user_id=get_user).exists():
       return render(request, "users/update_address.html")
    else:
      if request.method == "POST":
         address = request.POST['address']
         phone = request.POST['phone']
         user_id = request.user
         save_details = Address.objects.create(address=address, phone=phone, user_id=user_id)
         save_details.save()
            
   
    return render(request, "users/address.html")
        

def update_details(request):
   if request.method == "POST":
         address = request.POST['address']
         phone = request.POST['phone']
         user_id = request.user
         save_details = Address.objects.update(address=address, phone=phone)
         return redirect("/services")
 
   return render(request, "users/update_address.html")


def filter_by_price(request, flag):
   global filtered_price
   data={}
   if(flag=='asc'):
      sorted_price = filtered_price.order_by("-price")
      
   else:
      sorted_price = filtered_price.order_by("price")
      
   data['services'] = sorted_price
   return render(request, 'users/view_services.html', context=data)

def search_services(request):
    data={}
    if(request.method=="POST"):
      address = request.POST['address']
      print(address)
      get_business = Business_details.objects.all()
      searched_business = get_business.filter(Q(address__icontains=address))
      # if(not searched_business):
      #    data['error_msg'] = "No entries found"
      #    return render(request, 'show_entry.html', context=data)
      data['services']=searched_business
      return render(request, "users/services.html", context=data)  
    return render(request, "users/services.html", context=data)