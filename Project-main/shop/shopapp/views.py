from django.shortcuts import render
from .models import *

# Create your views here.
class ProductData:
	def __init__(self, id, amount):
		self.id = id
		self.amount = amount

def catalog(request):
	context = {
		"product_list": Product.objects.all()
    }
	
	response = render(request, 'shopapp/main.html', context = context)
	
	if 'productId' in request.POST:
		IdproductList = list(request.POST['productId'])
		AmountproductList = list(request.POST['productAmount'])

		id_product = ''
		amount_product = ''

		for number in IdproductList:
			id_product += number
		for number in AmountproductList:
			amount_product += number
			
		if 'productId' in request.COOKIES:
			old_cookies = request.COOKIES['productId']
			cookie_list = old_cookies.split(' ')

			for cookie in cookie_list:
				if id_product in cookie:
					cookie_list.remove(cookie)

					old_cookies = ' '.join(cookie_list)


			if old_cookies != '':
				old_cookies += ' ' + id_product + '*' + amount_product
			else:
				old_cookies += id_product + '*' + amount_product
				

			response.set_cookie('productId', old_cookies)
		else:
			response.set_cookie('productId', id_product + '*' + amount_product)

	return response

def basket(request):
	products_list = []
	list_of_id = []
	list_of_amount = []

	if 'productId' in request.COOKIES:
		cookies = request.COOKIES['productId']
		cookies_list = cookies.split(' ')
		id = ''
		for el in cookies_list:
			cookie = el.split('*')
			for i in cookie[0]:
				if i != '!':
					id += i

			products_list.append(ProductData(id, cookie[1]))
			id = ''

		for element in products_list:
			list_of_id.append(element.id)
			list_of_amount.append(element.amount)

		sorted_id = sorted(list_of_id)
		sorted_amounts = []

		for id in sorted_id:
			for element in products_list:
				if id == element.id:
					sorted_amounts.append(element.amount)

		


		context = {
			'products': Product.objects.filter(pk__in = list_of_id),
			'amounts': sorted_amounts
		}

	else:
		context = {}

	response = render(request, 'shopapp/basket.html', context)


	if 'productId' in request.POST:
		productIdList = list(request.POST['productId'])
		
		productId = ''

		for i in productIdList:
			productId += i

		old_cookies = request.COOKIES['productId']

		cookies_list = old_cookies.split(' ')

		for cookie in cookies_list:
			if productId in cookie:
				cookies_list.remove(cookie)
				old_cookies = ' '.join(cookies_list)

		if old_cookies != '':
			response.set_cookie('productId', old_cookies)
		else:
			response.delete_cookie('productId')

	return response