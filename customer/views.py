from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Category, OrderModel
from django.conf import settings
# Create your views here.

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        
        #getting every item from each category
        Tiffins = MenuItem.objects.filter(category__name__contains='Tiffin')
        Meals = MenuItem.objects.filter(category__name__contains='Meals')
        Drinks = MenuItem.objects.filter(category__name__contains='Drink')
        Fast_Food = MenuItem.objects.filter(category__name__contains='Fast Food')

        #pass into context
        context = {
            'Tiffins': Tiffins,
            'Meals': Meals,
            'Drinks': Drinks,
            'Fast_Food': Fast_Food,
        }

        #render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
    
        order_items = {
            'items' : []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            address=address
        )
        order.items.add(*item_ids)

        
        body = ("Thank you for your order! Your order will be delivered soon!\n"
                f"Your Bill: {price}\n")
        send_mail(
            'Order Confirmed!!',
            body,
            'anandhakrishna2624@gmail.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }
    
        return render(request, 'customer/order_confirmation.html', context)
