from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse , Http404, JsonResponse
from django.template import loader
from .models import Item ,Cart, ItemCart
import requests
import json

cartOwner = ''

def index(request):
    return render(request, "ChickenFarmApp/index.html", {
        'itemInPage':Item.objects.all(), 
        # 'CartInPage':Cart.objects.all()[0].item_set.all()
    })                                              #forengkey OneToMany
                                                    #Cart.objects.all()[0].item_set.all()
                                                    #ManyToMany
                                                    #Item.objects.all()[0].carts.all()     (all carts the item is in)
                                                    #Cart.objects.all()[0].item_set.all()  (all items in cart)
                                                    #Cart.objects.get(id=4).item_set.all()
                                                    #https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/



def item(request, item_id):
    specItem = Item.objects.get(pk = item_id)
    if specItem:
        return render(request, 'ChickenFarmApp/item.html', {'itemInPage': specItem}) 
    else: 
        return Http404('This page doesnt exist')
        # Cart.objects.all()[0].item_set.all() #turn into get(pk = item_id)

def deleteItm(request, item_id):
    print("delete what" , item_id)

    if request.COOKIES.get('user'):

        b = Item.objects.get(pk = item_id)
       
        b.delete()
        b.save()
    else:
        print("your kidding me")

    return checkOut(request)

def pay(request):
    print("you got a payer. . .")

    SECRET_KEY = 'sk_test_960bfde0VBrLlpK098e4ffeb53e1'

    response = requests.post(
    'https://online.yoco.com/v1/charges/',
    headers={
        'X-Auth-Secret-Key': SECRET_KEY,
    },
    json={
        'token': request.POST['rslt[id]'],
        'amountInCents': request.POST['mony'],
        'currency': 'ZAR',
    },
    )
    print(request.POST['rslt[id]'])
    print(response.status_code)

    return JsonResponse(response.json()) 

def paypal(request):
    print("you got a paypal payer. . .")
    print( request.POST['bought'])  

    got = Cart.objects.get(user= request.COOKIES.get('user'))

    print("Before break " , got.bought)

    if  got.bought == None:
        got.bought = "break"

    print("After save " , got.bought)

    got.bought = got.bought + request.POST['bought']
    got.save()

    print("After concatination " , got.bought)

    print(request.COOKIES.get('user'))

    return JsonResponse({'state' : 'notfound'}) 


def addUser(request):
    #ADD TO CART
     
     if len(Cart.objects.filter(user= request.POST['usNm'])) < 1 and len(request.POST['usNm']) != 0 :
        Cart.objects.create(user = request.POST['usNm'], passW = request.POST['usPw'] )
        
        print("made")
        print(request.POST['usNm'])
        print(request.POST['usPw'])

        return  cartHelper(request, 1)
     else:
         print("name already there")
         return JsonResponse({'state' : 'notfound'}) 


def add(request, reply_id):
    if request.method == "POST":

        print(reply_id, request.POST['usrName'])

        print(Cart.objects.get(user= request.POST['usrName']))

        crt = Cart.objects.get(user= request.POST['usrName'])
        itm = Item.objects.get(pk = reply_id)

        crt.item_set.add(itm)
        crt.save()

        idOfCount = ItemCart.objects.get(cart = Cart.objects.get(user= request.POST['usrName']), item = Item.objects.get(pk = reply_id)).id

        a = ItemCart.objects.get(pk=idOfCount)
        if a.count:
            a.count = a.count + 1 
            a.save()
        else:
            a.count = 0
            a.count = a.count + 1 
            a.save()

        
        

        print(ItemCart.objects.get(pk=idOfCount), ItemCart.objects.get(pk=idOfCount).count)
        
        print('====================================end========================================')
        return JsonResponse({'state' : 'notfound'}) 



def cartHelper(request, reply_id):
    print("====================================From pyCartHelper, I was called=================================")

    if request.method == "POST":

        match reply_id:
            case 0:  #CHECK, AND RETURN THE ITEMS
            
                print("Check users then return items!")
                if Cart.objects.filter(user= request.POST['usrName']):    # if Cart.objects.filter(user= usrNme, psW) :
                    print("FOUND "+request.POST['usrName'])  

                    itmsArrName = []
                    itemArrQty = []
                    itemArrPrice = []
                    itemArrCount = []
                    itemArrId = []

                    for itms in Cart.objects.get(user= request.POST['usrName']).item_set.all() :
                        itmsArrName.append(itms.itemName)
                        itemArrQty.append(itms.itemQty)
                        itemArrPrice.append(itms.itemPrice)
                        itemArrId.append(itms.id)


                        idOfCount = ItemCart.objects.get(cart = Cart.objects.get(user= request.POST['usrName']), item = Item.objects.get(pk = itms.id)).id
                        a = ItemCart.objects.get(pk=idOfCount)
                        # print(a.count)
                        itemArrCount.append(a.count)

                    return JsonResponse({ 
                    'names': itmsArrName, 
                    'quantity': itemArrQty ,
                    'price': itemArrPrice,
                    'count': itemArrCount,
                    'id': itemArrId
                    })

                else:
                    print(request.POST['usrName'] + " is not on the list") 
                    return JsonResponse({'state' : 'notfound'}) 

            case 1: #INITIAL CHECK, ON SIGNIN PRESS CHECK IF THE USRER IS IN THE DB THEN TELL JS TO MAKE THE CART
                print("check users, make cookie")

                if Cart.objects.filter(user= request.POST['usNm'] , passW = request.POST['usPw']  ):    # if Cart.objects.filter(user= usrNme, psW) :
                    print(Cart.objects.get(user= request.POST['usNm']).id)
                    print("FOUND "+request.POST['usNm'])  

                    itmsArrName = []
                    itemArrQty = []
                    itemArrPrice = []
                    itemArrCount = []
                    itemArrId = []

                    for itms in Cart.objects.get(user= request.POST['usNm']).item_set.all() :
                        itmsArrName.append(itms.itemName)
                        itemArrQty.append(itms.itemQty)
                        itemArrPrice.append(itms.itemPrice)
                        itemArrId.append(itms.id)


                        idOfCount = ItemCart.objects.get(cart = Cart.objects.get(user= request.POST['usNm']), item = Item.objects.get(pk = itms.id)).id
                        a = ItemCart.objects.get(pk=idOfCount)
                        print(a.count)
                        itemArrCount.append(a.count)

                    return JsonResponse({ 
                    'user': Cart.objects.get(user= request.POST['usNm']).user,
                    'names': itmsArrName, 
                    'quantity': itemArrQty ,
                    'price': itemArrPrice,
                    'count': itemArrCount,
                    'id' : itemArrId 
                    })

                else:
                    print(request.POST['usNm'] + " is not on the list") 
                    return JsonResponse({'notfound': 'false'})  


            case 400:
                print("Uh oh. Are you lost?")
            case 500:
                print("Yikes. Something went wrong!")


def checkOut(request):
    # if checklist:
    
    itms = []
    howMuch = []
    total = 0
    if request.COOKIES.get('user'):

        #  itms = Cart.objects.get(user= request.COOKIES.get('user')).item_set.all()


         for i in Cart.objects.get(user= request.COOKIES.get('user')).item_set.all() :
            print('============================================================================')
            idOfCount = ItemCart.objects.get(cart = Cart.objects.get(user= request.COOKIES.get('user')), item = Item.objects.get(pk = i.id)).id
            howMuch.append(ItemCart.objects.get(pk=idOfCount).count) 
            total = total + i.itemPrice * ItemCart.objects.get(pk=idOfCount).count

            itms.append([Item.objects.get(pk = i.id).itemName, Item.objects.get(pk = i.id).itemPrice,  ItemCart.objects.get(pk=idOfCount).count, i.id ])


    else:
        print("your kidding me")
    
    return render(request, 'ChickenFarmApp/checkout.html', { 
        'itemInPage':itms,
        'count' : total,
    })

def aboutUs(request):
    return render(request, 'ChickenFarmApp/aboutus.html', {})