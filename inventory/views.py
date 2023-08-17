from django.contrib.auth import login, authenticate
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .models import Inventory, Product, Buy, Cart 
from datetime import datetime
from django.http import HttpResponse
#from django.core.mail import send_mail





###################################-----TESTED REGISTER-------###############################################
    

    
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
        #send_mail(
        #                     'Registration Successful',
        #                     'Your registration for Onestop grocery shopping app is succesfull you can now shop any grocery product from wide range of varities available at Onestop .Happy shopping:) ',
        #                     'srijanomar5840@gmail.com',
        #                     ['omarsrijan3094@gmail.com'],
        #     
     return JsonResponse({'message': 'Registration successfull !!'},status=200)

  
    



#######################################------TESTED LOGIN-------################################################



    
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
                
                    return response
    else:
        return JsonResponse({'message':'Request not valid'})
    


   



#####################################-----TESTED INVENTORY-------###############################################





def inventory(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            category = request.POST.get('category')
            image = request.FILES.get('image')
            uid = request.POST.get(('uid'))
            ucategory = request.POST.get('ucategory')
            uimage = request.FILES.get('uimage')
            
            if category and image:
                inventory = Inventory.objects.create(category=category, blob=image)
                return JsonResponse({'message': 'Category and image uploaded successfully'})
            
            if uid:
                inventory=Inventory.objects.filter(id=uid).first()

                if inventory:
                 inventory.category = ucategory

                if uimage:
                    inventory.blob = uimage

                inventory.save()
                return JsonResponse({'message': 'Category updated successfully'})
            else:
                return JsonResponse({'category_id':uid,'error': 'Inventory item not found'}, status=404)
        else:
            return JsonResponse({'error': 'Authentication required.'}, status=401)


       

    # if request.method == 'GET':
    #         if request.user.is_authenticated and request.user.is_superuser:
    #             categories = Inventory.objects.exclude(deletedTime__isnull=False)

    #             category_data = [
    #                 {
    #                     'id': category.id,
    #                     'product': category.category,
    #                     'image': category.blob if category.blob else None,
    #                 }
    #                 for category in categories
    #             ]

    #             return JsonResponse({'categories': category_data}, status=200)
    #         else:
    #             return JsonResponse({'error': 'Admin Authentication required.'}, status=401)
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
        
            category=list(Inventory.objects.values('id','category','blob'))
            return JsonResponse(category,safe=False)
        if request.user.is_authenticated:
        
            category=list(Inventory.objects.values('id','category','blob'))
            return JsonResponse(category,safe=False)
        else:
            return JsonResponse({'error': 'Admin Authentication required.'}, status=401)     




    if request.method == 'DELETE':
         if request.user.is_authenticated and request.user.is_superuser:
        
            category_id = request.GET.get('category_id')
            
            if category_id is not None:
                inventory = Inventory.objects.filter(id=category_id).first()
                
                if inventory:
                    inventory.deletedTime = datetime.now()
                    inventory.save()
                    return JsonResponse({'message': 'Category deleted successfully'})
                else:
                    return JsonResponse({'message': 'Category not found'}, status=404)
            else:
                return JsonResponse({'message': 'Invalid request data.'}, status=400)
         else:
             return JsonResponse({'error': 'Admin Authentication required.'}, status=401)
             



    return JsonResponse({'message': 'Invalid request method.'}, status=400)



    



#################################--------TESTED PRODUCT------ #########################################################



def product(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            product_name = request.POST.get('productname')
            price = request.POST.get('price')
            category_id = request.POST.get('categoryid')
            quantity = request.POST.get('quantity')
            image = request.FILES.get('image')
            description = request.POST.get('description')
            # uproduct_id = request.POST.get('uproduct_id')
            # uname = request.POST.get('uname')
            # uprice = request.POST.get('uprice')
            # uimage = request.FILES.get('uimage')
            # uquantity = request.POST.get('uquantity')
            # uproduct = request.POST.get('uproduct')

            category = Inventory.objects.filter(id=category_id).first()

            if category:
                new_product = Product.objects.create(
                    product=product_name,
                    price=price,
                    category=category,
                    blob=image,
                    quantity=quantity,
                    description=description
                )
                product = Product.objects.filter(product=product_name,price=price).first()
                return JsonResponse({'productid':product.id,'message': 'Registered Product successfully'})

            # existing_product = Product.objects.filter(id=uproduct_id).first()

            # if not existing_product:
            #     return JsonResponse({'message': 'Product does not exist'}, status=404)

            # if uname:
            #     existing_product.product = uname
            # if uprice:
            #     existing_product.price = float(uprice)
            # if uquantity:
            #     existing_product.quantity = int(uquantity)
            # if uimage:
            #     existing_product.blob = uimage
            # if uproduct:
            #     existing_product.product = uproduct

            # existing_product.save()

            # return JsonResponse({'message': 'Updated the product successfully'})
        else:
            return JsonResponse({'error': 'Admin Authentication required.'}, status=401)




    # if request.method == 'GET':
    #     if request.user.is_authenticated:
    #         products = Product.objects.exclude(deletedTime__isnull=False)

                 
    #         product_data = list(products.values('id', 'product', image=product('blob') if product('blob') else None))
    #         return JsonResponse({'product': product_data}, status=200)

    #     else:
    #         return JsonResponse({'error': 'Authentication required.'}, status=401)
    #     from django.db.models import Case, Value, When, F

    # if request.method == 'GET':
    #     if request.user.is_authenticated:
    #         products = Product.objects.exclude(deletedTime__isnull=False)

    #         product_data = list(
    #             products.annotate(
    #                 image=Case(
    #                     When(blob__isnull=False, then=F('blob')),
    #                     default=Value(None),
    #                     output_field=ImageField(),  # Replace ImageField with your field's actual type
    #                 )
    #             ).values('id', 'product', 'image')
    #         )

    #         return JsonResponse({'product': product_data}, status=200)

    #     else:
    #         return JsonResponse({'error': 'Authentication required.'}, status=401)
    #     def get_category(request):

    if request.method == 'GET':
        category_id = request.GET.get('categoryid') 
         
        if request.user.is_authenticated and request.user.is_superuser:
            products = list(Product.objects.values('id', 'product', 'blob', 'description', 'price', 'quantity'))
            return JsonResponse(products, safe=False)
        elif request.user.is_authenticated:
            if category_id:
                products = list(Product.objects.filter(category_id=category_id).values('id', 'product', 'blob', 'description', 'price'))
                return JsonResponse(products, safe=False)
            else:
                products = list(Product.objects.values('id', 'product', 'blob', 'description', 'price'))
                return JsonResponse(products, safe=False)
        else:
            return JsonResponse({'error': 'Authentication required.'}, status=401)

        
       
    
        # product_data = [
            #     {
            #         'id': product.id,
            #         'product': product.product,
            #         #'image': product.blob.url if product.blob else None,
            #         'image': product.blob, if product.blob else None,
            #     }
            #     for product in products
            # ]

            # return JsonResponse({'product': product_data}, status=200)
#             product_data = [
#     {
#         'id': product.id,
#         'product': product.product,
#         'image': product.blob if product.blob else None,
#     }
#     for product in products
# ] 




    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_superuser:
            product_id = request.GET.get('product_id')
            product = Product.objects.filter(id=product_id).first()
            if product:
             product.deletedTime = datetime.now()
             product.save()
        
            return JsonResponse({'id':product_id,'message': 'Product deleted successfully'})
        else:
            return JsonResponse({'error': ' Authentication required.'}, status=401)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)





#########################################---- CART-----#####################################################



def cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_id = data.get('id')
           # quantity = data.get('quantity')

            user_id = request.user.id
            product = Product.objects.filter(id=product_id).first()
            productimg = Product.objects.filter(id=product_id).values('blob').first()

            if product and productimg and product.quantity >= quantity:
                cart = Cart.objects.create(
                    user_id=user_id,
                    product=product,
                    totalprice=product.price * quantity,
                    quantity=quantity,
                    image=productimg['blob'],
                )
                return JsonResponse({'message': 'Product added to cart successfully'})
            else:
                return JsonResponse({'error': 'Product not found or insufficient quantity'}, status=400)
        else:
            return JsonResponse({'error': 'authentication required'}, status=401)
    




    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.user.id
            cproducts = Cart.objects.filter(id=user_id).first()
            cart_data = [
                {
                    'quantity': cproduct.quantity,
                    'product': cproduct.product,
                    'image': cproduct.image.url if cproduct.image else None,
                    'id' : cproducts.id
                      }
                for cproduct in cproducts]
            return JsonResponse({'products': cart_data}, status=200)
        else:
             return JsonResponse({'error': 'authentication required.'}, status=401)
        






    if request.method == 'PUT':
      if request.user.is_authenticated:
        cart_id = data.get('cart_id')
        quantity = data.get('quantity')
        cart = Cart.objects.filter(id=cart_id).first()
        if cart:
            cart.quantity = quantity
            return JsonResponse({'message':'updated cart successfully'})
      else:
             return JsonResponse({'error': 'authentication required.'}, status=401)
        



    if request.method == 'DELETE':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            cart_id = data.get('cart_id')
            cart = Cart.objects.filter(id=cart_id).first()
            if cart:
                    cart.deletedTime = datetime.now()
                    cart.save()
                    return JsonResponse({'message': 'Cart Product deleted successfully'})
            else:
                return JsonResponse({'message': 'Cart Product not found'}, status=404)
        else:
             return JsonResponse({'error': 'authentication required.'}, status=401)
        

    return JsonResponse({'message': 'Invalid request method.'}, status=400)





################################-----TESTED BUY----######################################################




def buy(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
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
        else:
            return JsonResponse({'error': 'authentication required'}, status=401)


    return JsonResponse({'error': 'Invalid request method.'}, status=400)





#####################################-----TESTED SEARCH-----####################################################################





def search(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            search = data.get('search')  
            pricemax = data.get('pricemax')
            pricemin = data.get('pricemin')
            
            if search is not None:
                products = Product.objects.filter(product=search).values('product', 'price', 'blob')
                return JsonResponse({'message': 'search result', 'products': list(products)}, status=200)
            elif pricemax is not None or pricemin is not None: 
                products = Product.objects.filter(price__range=(pricemin, pricemax)).values('product', 'price', 'blob')
                if products:
                    return JsonResponse({'message': 'search result', 'products': list(products)}, status=200)
                else:
                    return JsonResponse({'message': 'No results found'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid price range and search'}, status=400)
        else:
            return JsonResponse({'error': 'authentication required'}, status=401)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    









#################################################################################################3






###########-----PUT OF PRODUCTS------#######


    # if request.method == 'PUT':
    #     product_id = request.POST.get('product_id')
    #     uname = request.POST.get('uname')
    #     uprice = request.POST.get('uprice')
    #     uimage = request.FILES.get('image')
    #     uquantity = request.POST.get('uquantity')

    #     product = Product.objects.filter(id=product_id).first()
    #     if not product:
    #         return JsonResponse({'product_id': product_id,'uprice': uprice, 'message': 'Product does not exist'}, status=404)

    #     if uname:
    #         product.product = uname
    #     if uprice:
    #         product.price = float(uprice)
    #     if uquantity:
    #         product.quantity = int(uquantity)

    #     if uimage:
    #         product.blob = uimage

    #     product.save()

    #     return JsonResponse({'product_id': product_id, 'message': 'Updated the product successfully'})





#####--PUT OF INVENTORY------####


 # if request.method == 'PUT':
    #     data = json.loads(request.body)
    #     uid = data['ucategory_id']
    #     ucategory = data['ucategory']
    #     uimage = data['uimage']
    #     inventory=Inventory.objects.filter(id=id).first()

    #     if inventory:
    #         inventory.category = category

    #         if image:
    #             inventory.blob = image

    #         inventory.save()
    #         return JsonResponse({'message': 'Category updated successfully'})
    #     else:
    #         return JsonResponse({'category_id':category_id,'error': 'Inventory item not found'}, status=404)



##########################################################


# def inventory_image_upload(request):
#     if request.method == 'POST':
#         category = request.POST.get('category')
#         image = request.FILES.get('blob')

#         if category and image:
#             inventory = Inventory(category=category, blob=image)
#             inventory.save()
#             return JsonResponse({"message": "Image uploaded successfully."}, status=201)
#         else:
#             return JsonResponse({"message": "Missing category or image data."}, status=400)





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

     









