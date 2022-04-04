from turtle import heading
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
# from firebase_admin import db
import pyrebase

#Your web app's Firebase configuration
#For Firebase JS SDK v7.20.0 and later, measurementId is optional
firebaseConfig = {
  "apiKey": "AIzaSyBDUx18WYWkbf4v6Xq3oFwZ5FW_p3bC0e4",
  "authDomain": "sales-n-inventory-system-ssvk.firebaseapp.com",
  "databaseURL": "https://sales-n-inventory-system-ssvk-default-rtdb.firebaseio.com",
  "projectId": "sales-n-inventory-system-ssvk",
  "storageBucket": "sales-n-inventory-system-ssvk.appspot.com",
  "messagingSenderId": "370292214222",
  "appId": "1:370292214222:web:4e0427bfc135c92bfc039f",
  "measurementId": "G-5ZSB4CBB0W"
}

# Use a service account (path of file inside _init_ folder)
cred = credentials.Certificate('C:/Users/SK/Documents/GitHub/Final-Year-Project/sales_n_inventory_web/_init_sdk/sales-n-inventory-system-ssvk-firebase-adminsdk-ndio1-b8dd43f87f.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
#---------------ends here->

# Create your views here.

#--------------------------------------------------------->
# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()

def index(request):
    return render(request,"Index.html",{'user':authe.current_user})
 
def signIn(request):
    if authe.current_user==None:
      return render(request,"Login.html",{'user':authe.current_user})
    else:
      return render(request,"Home.html",{'user':authe.current_user})
 
def postsignIn(request):
    if authe.current_user==None:
      email=request.POST.get('email')
      pasw=request.POST.get('pass')
      try:
          # if there is no error then signin the user with given email and password
          user=authe.sign_in_with_email_and_password(email,pasw)
      except:
          message="Invalid Credentials! Please Check your email or password."
          return render(request,"Login.html",{"message":message, 'user':authe.current_user})
      session_id=user['idToken']
      request.session['uid']=str(session_id)
      return render(request,"Home.html",{"email":email, 'user':authe.current_user})
    else:
      return render(request,"Home.html",{'user':authe.current_user})
 
def logout(request):
    try:
        del request.session['uid']
        authe.current_user=None
        print("logged out success")
    except:
        pass
    return render(request,"Login.html",{'user':authe.current_user})
 
def signUp(request):
    return render(request,"Registration.html",{'user':authe.current_user})
 
def postsignUp(request):
     email = request.POST.get('email')
     passs = request.POST.get('pass')
     name = request.POST.get('name')
     try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
     except:
        return render(request, "Registration.html",{'user':authe.current_user})
     return render(request,"Login.html",{'user':authe.current_user})

def reset(request):
	return render(request, "Reset.html",{'user':authe.current_user})

def postReset(request):
	email = request.POST.get('email')
	try:
		authe.send_password_reset_email(email)
		message = "An email to reset password is successfully sent to your registered email."
		return render(request, "Reset.html", {"msg":message, 'user':authe.current_user})
	except:
		message = "Something went wrong, Please check the email you provided is registered or not."
		return render(request, "Reset.html", {"msg":message, 'user':authe.current_user})

def aboutUs(request):
  return render(request, "aboutUs.html", {'user':authe.current_user})


# Sales Dashboard ---------------------------------------->

def newBill(request):
  if authe.current_user==None:
    return render(request,"Login.html",{'user':authe.current_user})
  else:
    data=getInStock()
    l=len(data)
    return render(request,"newBill.html",{'user':authe.current_user, 'data':data,'length':l})

def in_Stock(request):
  if authe.current_user==None:
    return render(request,"Login.html",{'user':authe.current_user})
  else:
    data=getInStock()
    l=len(data)
    return render(request,"in_stock.html",{'user':authe.current_user, 'data':data,'length':l})


# Firebase FireStore Related ----------------------------->
def getInStock():
  collections = db.collection('inventory_db').document(authe.current_user['email']).collection('products').stream()
  data=[]
  for doc in collections:
    d=doc.to_dict()
    if d['quantity']>0:
      data.append(dict(d))
  return(data)
