from django.shortcuts import render,redirect
from .models import Account
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
import random

# Create your views here.
def index(request):
    return render(request,"index.html")

def createaccount(request):
    if request.method=="POST":
        name=request.POST["name"]
        dob=request.POST["dob"]
        aadhar=request.POST["aadhar"]
        mobile=request.POST["mobile"]
        email=request.POST["email"]
        adress=request.POST["textarea"]
        # print(name,dob,aadhar,mobile,email,adress)
        Account.objects.create(name=name,Aadhar=aadhar,DOB=dob,mobile=mobile,email=email,address=adress)    
        # print("data sucessfully added")
        send_mail( 
                    f"Hello {name}, thank you for creating an account in our bank.",  # subject
                    "FBH - Fraud Bank of Hyderabad,\nWelcome to the family!\nWe are happy to have you.\n\nRegards,\nManager (DJD-E1)\nThank you ****!",
                    settings.EMAIL_HOST_USER,  # from_email
                    [email],                   # recipient_list (must be a list!)
                    fail_silently=False
                    )

        return HttpResponse("sent mail")
        # print("sent sucessfully")
    return render(request,'create.html')

def pingenerate(request):
    if request.method=="POST":
        accountnumber=request.POST["accountnumber"]
        otp=random.randint(100000,999999)
        data=Account.objects.get(acc=accountnumber)
        email=data.email
        send_mail( 
                    f"Hello {data.name}, thank you for creating an account in our bank.",  # subject
                    f"FBH - Fraud Bank of Hyderabad,\nWelcome to the family! your otp is {otp}\nWe are happy to have you.\n\nRegards,\nManager (DJD-E1)\nThank you ****!",
                    settings.EMAIL_HOST_USER,  
                    [email],                   
                    fail_silently=False
                    )
        print("sucessfully sent ")
        data.otp=otp
        data.save()
        print(otp)
        return redirect("otpvalidation")

    return render(request,"pingeneration.html")

def otpvalidation(request):
    if request.method=="POST":
        accountnumber=request.POST["accnumber"]
        Otp=request.POST["Otp"]
        pin1=request.POST["pin1"]
        pin2=request.POST["pin2"]
        if pin1==pin2:
            data=Account.objects.get(acc=accountnumber)
            if data.otp==int(Otp):
                data.pin=pin1
                print(data.otp)
                print(Otp)
                data.save()
                send_mail( 
                    f"Hello {data.name}, thank you for creating an account in our bank.",  # subject
                    f"FBH - Fraud Bank of Hyderabad,\nWelcome to the family! your pin generation has been  sucessful \nWe are happy to have you.\n\nRegards,\nManager (DJD-E1)\nThank you ****!",
                    settings.EMAIL_HOST_USER,  
                    [data.email],                   
                    fail_silently=False
                    )
            else:
                return HttpResponse("otp is mismatched....")
        else:
            return HttpResponse("pin is mismatched......")
    return render(request,"otpvalidation.html")

def balence(request):
    data=None
    msg = ""
    bal=0
    f=False
    if request.method=="POST":
        acc=request.POST["acc"]
        pin=request.POST["pin"]
        try:
            data=Account.objects.get(acc=int(acc))
        except:
            pass
        if data is not  None:
            if data.pin==int(pin):
                bal=data.bal
                f= True
            else:
                msg="please enter the valid pin"
        else:
            msg="please enter the valid account number"
            # print(msg)
    context={
        'bal':bal,
        'var':f,
        'msg': msg
        
    }


    return render(request,"bal.html",context)


def withdrawal(request):
    if request.method=="POST":
        acc=request.POST["acc"]
        pin=request.POST["pin"]
        amt=int(request.POST["amt"])
        print(acc,pin,amt)
        try:
            data=Account.objects.get(acc=int(acc))
        except:
            print("enter the valid account number")
        if data.pin==int(pin):
            if data.bal>=amt and amt>0:
                data.bal-=amt
                data.save()
                send_mail( 
                        f"Hello {data.name}, thank you for creating an account in our bank.",  # subject
                        f"FBH - Fraud Bank of Hyderabad,\nWelcome to the family!{amt}withdrawal  has been  sucessful from ur{data.acc} available balence is the {data.bal}\nWe are happy to have you.\n\nRegards,\nManager (DJD-E1)\nThank you ****!",
                        settings.EMAIL_HOST_USER,  
                        [data.email],                   
                        fail_silently=False
                        )
            else:
                print("enter the valid amount")
        else:
            print("please enter the valid pin")
            
        return redirect("home")

    return render(request,"withdrawal.html")

def deposit(request):
    if request.method=="POST":
        acc=request.POST["acc"]
        pin=request.POST["pin"]
        amt=int(request.POST["amt"])
        print(acc,pin,amt)
        try:
            data=Account.objects.get(acc=int(acc))
        except:
            print("enter the valid account number")
        if data.pin==int(pin):
            if amt>=100 and amt<=100000:
                data.bal+=amt
                data.save()
                send_mail( 
                        f"Hello {data.name}, thank you for creating an account in our bank.",  # subject
                        f"FBH - Fraud Bank of Hyderabad,\nWelcome to the family!{amt}your deposite has been sucessful to ur accnt {data.acc} available balence is the {data.bal}\nWe are happy to have you.\n\nRegards,\nManager (DJD-E1)\nThank you ****!",
                        settings.EMAIL_HOST_USER,  
                        [data.email],                   
                        fail_silently=False
                        )
            else:
                print("enter the valid amount")
        else:
            print("please enter the valid pin")
            
        return redirect("home")
    return render(request,"deposit.html")

def transfer(request):
    msg=""
    if request.method=="POST":
        f_acc=request.POST.get('f_acc')
        t_acc=request.POST.get('t_acc')
        pin=request.POST.get('pin')
        amt=request.POST.get('amt')
        try:
            from_acc=Account.objects.get(acc=f_acc)
        except:
            msg="sender account is not valid "
        try:
            to_acc=Account.objects.get(acc=t_acc)
        except:
            msg="reciver account is not valid "
        if from_acc.pin==int(pin):
            if int(amt)>100 and int(amt)<=100000 and int(amt)<=from_acc.bal:
                from_acc.bal-=int(amt)
                from_acc.save()
                send_mail( 
                        f"Hello {from_acc.name}, thank you for creating an account in our bank.",  # subject
                        f"FBH - Fraud Bank of Hyderabad,\nWelcome to the family!{amt}your deposite has been sucessful to ur accnt {to_acc.acc} available balence is the {from_acc.bal}\nWe are happy to have you.\n\nRegards,\nManager (DJD-E1)\nThank you ****!",
                        settings.EMAIL_HOST_USER,  
                        [from_acc.email],                   
                        fail_silently=False
                        )
                print("sent sucessfully")
                to_acc.bal+=int(amt)
                to_acc.save()
                send_mail( 
                        f"Hello {from_acc.name}, thank you for creating an account in our bank.",  # subject
                        f"FBH - Fraud Bank of Hyderabad,\nWelcome to the family!{amt}your deposite{to_acc.name} has been sucessful to ur accnt {to_acc.acc} available balence is the {to_acc.bal}\nWe are happy to have you.\n\nRegards,\nManager (DJD-E1)\nThank you ****!",
                        settings.EMAIL_HOST_USER,  
                        [to_acc.email],                   
                        fail_silently=False
                        )
                print("sent sucesfully")
            else:
                msg="enter the valid amount"
        else:
            msg="incorrect pin"

                
    return render(request,"transfer.html",{'msg':msg})