from django.contrib.auth import login, authenticate
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .models import Inventory, Product, Buy, Cart 
from datetime import datetime
from django.http import HttpResponse


#############################################
    

def register(request):
    if request.method == 'POST':
     data = json.loads(request.body)
     username = data.get('username')
     password = data.get('password')
     first_name = data.get('first_name')
     last_name = data.get('last_name')
     email = data.get('email')

     if not (username and password and first_name and last_name and email):
        return JsonResponse({'error': 'Invalid registration details.'}, status=400)

     if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Username or email already exists.'}, status=400)

     user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
     )
     return JsonResponse({'message': 'Registration successfull !!'},status=200)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    


  
    


   




#######################################################################



    
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()

        if user is not None and user.check_password(password):
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                if auth_user.is_superuser and auth_user.is_staff:
                    return JsonResponse({'login': 'admin', 'message': 'Login successful.'})
                else:
                    response = JsonResponse({'login': 'user', 'message': 'Login successful.'})
                    
                    if request.is_secure():
                       response.set_cookie('sessionid', 'your_session_id', secure=True)
                    return response
    


   



###############################################################################################




def inventory(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        image = request.FILES.get('blob')

        inventory = Inventory.objects.create(category=category, blob=image)
        inventory.save()

        return JsonResponse({'message': 'Category and image uploaded successfully'})

 
    if request.method == 'GET':
        if request.user.is_authenticated:
            categories = Inventory.objects.all()

            category_data = [
                {
                    'id': category.id,
                    'product': category.category,
                    'image_url': request.build_absolute_uri(category.blob.url)  # Construct the image URL
                }
                for category in categories
            ]

            return JsonResponse({'categories': category_data}, status=200)
        else:
            return JsonResponse({'error': 'Authentication required.'}, status=401)



    if request.method == 'PUT':
        category_id = request.POST.get('category_id')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        inventory = Inventory.objects.get(id=category_id)
        inventory.category = category

        if image:
            inventory.blob = image

        inventory.save()


        return JsonResponse({'message': 'Category updated successfully'})



    elif request.method == 'DELETE':
         category_id = request.DELETE.get('category_id')
         inventory = Inventory.objects.filter(id=category_id).first()
         inventory.deletedTime = datetime.now()
         inventory.delete()
         return JsonResponse({'message': 'Category deleted successfully'})


    return JsonResponse({'message': 'Invalid request method.'}, status=400)



    



########################################################################################


def product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('productname')
        price = data.get('price')
        category_id = data.get('categoryid')
        quantity = data.get('quantity')
        image = request.FILES.get('image')
        category = Inventory.objects.filter(id=category_id).first()
        if category:
            category_name = category.category
            product = Product.objects.create(product=product_name, price=price, category=category, blob=image,quantity=quantity)
            product.save()

        return JsonResponse({'message': 'Registered Product successfully'})
    



    if request.method == 'GET':
        if request.user.is_authenticated:
            products = Product.objects.all()

            product_data = [
                {
                    'id': product.id,
                    'product': product.product,
                   # 'image': product.blob,
                }
                for product in products
            ]

            return JsonResponse({'cart': product_data}, status=200)
        else:
            return JsonResponse({'error': 'Authentication required.'}, status=401)
        


    if request.method == 'PUT':
     product_id = request.POST.get('product_id')
     uname = request.POST.get('uname')
     uprice = request.POST.get('uprice')
     uimage = request.FILES.get('image')
     uquantity = request.POST.get('uquantity')

     product = Product.objects.filter(id=product_id).first()
     if not product:
        return JsonResponse({'product_id': product_id, 'message': 'Product does not exist'}, status=404)

     if uname:
        product.product = uname
     if uprice:
        product.price = float(uprice)
     if uquantity:
        product.quantity = int(uquantity)

    # if uimage:
    #     fs = FileSystemStorage()
    #     try:
    #         fs.save(uimage.name, uimage)
    #         product.blob = fs.url(uimage.name)
    #     except ValidationError:
    #         return JsonResponse({'product_id': product_id, 'message': 'Invalid image format'}, status=400)

     product.save()

     return JsonResponse({'product_id': product_id, 'message': 'Updated the product successfully'})


    elif request.method == 'DELETE':
         
         product_id = request.POST.get('product_id')
         product = Product.objects.filter(id=product_id).first()
         if product:
           product.deletedTime = datetime.now()
           product.delete()
     
         return JsonResponse({'message': 'Product deleted successfully'})


    return JsonResponse({'message': 'Invalid request method.'}, status=400)





#####################################################################################




def cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        auth_user = authenticate(request, username=User.username, password=User.password)
        if auth_user is not None:
                login(request, auth_user)
                
        product = Product.objects.filter(id=product_id).first()
        if product.quantity >= quantity:
            cart, created = Cart.objects.get_or_create(user_id=user_id, product=product,totalprice=product.price * quantity)
            cart.quantity = quantity
            cart.save()
            return JsonResponse({'message': 'Product added to cart successfully'})
    


    if request.method == 'GET':
        if request.user.is_authenticated:

            cproducts = Cart.objects.all()

            cart_data = [
                {
                    'quantity': cproduct.quantity,
                    'product': cproduct.product,
                   # 'image': product.blob,
                }
                for cproduct in cproducts
            ]

            return JsonResponse({'products': cart_data}, status=200)
        else:
            return JsonResponse({'error': 'Authentication required.'}, status=401)
        

    if request.method == 'PUT':
      cart_id = data.get('cart_id')
      quantity = data.get('quantity')
      cart = Cart.objects.filter(id=cart_id).first()
      if cart:
        cart.quantity = quantity
        return JsonResponse({'message':'updated cart successfully'})
        

    if request.method == 'DELETE':
         
        data = json.loads(request.body)
        cart_id = data.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first()
        if cart:
                cart.deletedTime = datetime.now()
                cart.save()
     
         
                return JsonResponse({'message': 'Cart Product deleted successfully'})
        else:
                return JsonResponse({'message': 'Cart Product not found'}, status=404)


    return JsonResponse({'message': 'Invalid request method.'}, status=400)





######################################################################################




def buy(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

       
        product = Product.objects.filter(id=product_id).first()

        if product.quantity >= quantity:
            product.quantity -= quantity
            product.save()

            buy = Buy.objects.create(productid=product, quantity=quantity, billtotal=product.price * quantity)

            return JsonResponse({'billtotal':product.price * quantity,'message': 'Purchase successful'})
        else:
            return JsonResponse({'error': 'Insufficient quantity available for purchase.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)





###########################################################################################################





def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        search = data.get('search')  
        pricemax = data.get('pricemax')
        pricemin = data.get('pricemin')
        
        if search is not None:
            products = Product.objects.filter(product=search).values('product', 'price', 'blob')
            return JsonResponse({'message': 'search result', 'products': list(products)}, status=200)
        elif pricemax is not None or pricemin is not None:  # Use 'or' instead of 'and'
            products = Product.objects.filter(price__range=(pricemin, pricemax)).values('product', 'price', 'blob')
            if products:
                return JsonResponse({'message': 'search result', 'products': list(products)}, status=200)
            else:
                return JsonResponse({'message': 'No results found'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid price range and search'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


#################################################################################################3



def inventory_image_upload(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        image = request.FILES.get('blob')

        if category and image:
            inventory = Inventory(category=category, blob=image)
            inventory.save()
            return JsonResponse({"message": "Image uploaded successfully."}, status=201)
        else:
            return JsonResponse({"message": "Missing category or image data."}, status=400)

















# def inventory(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         category = data['category']
        
        

#         register = Register.objects.filter(id=id).first()

#         if register:
#             todo = TodoTask.objects.create(
#                 taskTest=taskTest,
#             #     createdTime=datetime.now(),
#                   #updatedTime=datetime.now(),
#                  # checkedTime=datetime.now(),
#                 #  deletedTime=datetime.now(),
#                 username=register,
#                # serial=0,
#                 status_c=False,
#                 status_d=False
#             )
#             return JsonResponse({'task_id': todo.id,'status':False,'taskText' : taskTest,'message': 'Todo saved successfully'})
          
#         else:
#             return JsonResponse({'message': 'User not logged in'}, status=400)
    





#     if request.method == 'GET':
#         id = request.GET.get('loginid')
#         if not id:
#           return JsonResponse({'message': 'id required'}, status=400)
     

#         if TodoTask.objects.filter(username_id=id).exists():
#           tasks = TodoTask.objects.filter(username_id=id,status_d=0)
#           task_data = []
#           for task in tasks:
#                task_data.append({'task_id': task.id,'status':False,'taskText': task.taskTest})
#           #task_data = list('task_id': task.id,'status':False,'taskText': task.taskTest)
          
        

#           return JsonResponse({'id':id,'task': task_data})
#         else:
#             return JsonResponse({'message':  'No tasks found for the provided login ID'}, status=200)

  



#login-get
    # if request.method == 'GET':
    #     if request.user.is_authenticated:

    #         categories = Inventory.objects.all()

    #         categories_data = [
    #             {
    #                 'id': category.id,
    #                 'category': category.category,
    #                 'image': category.blob,
    #             }
    #             for category in categories
    #         ]

    #         return JsonResponse({'categories': categories_data}, status=200)
    #     else:
    #         return JsonResponse({'error': 'Authentication required.'}, status=401)

    # else:
    #     return JsonResponse({'error': 'Invalid request method.'}, status=400)

     









