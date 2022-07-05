from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from .models import Product

# Create your views here.
def logout(request):
    django_logout(request)
    domain = 'dev-j26j40c7.us.auth0.com'
    client_id = '8Tu4SypkrSbhWfazeOyRVuXC4YMfB3fg'
    return_to = 'http://localhost:8000'

    return HttpResponseRedirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')

@login_required
def profile(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id':auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture']
    }

    return render(request, 'secureapp/profile.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })

def index(request):
    products = Product.objects.all()

    # products = [ 
    #     {'title': 'PlayStation', 'price': 300, 'image': 'https://cdn.auth0.com/blog/django-webapp/playstation.png'},
    #     {'title': 'iPhone', 'price': 900, 'image': 'https://cdn.auth0.com/blog/django-webapp/iphone.png'},
    #     {'title': 'Yummy Pizza', 'price': 10, 'image': 'https://cdn.auth0.com/blog/django-webapp/pizza.png'},
    # ] 
    context = { 'products': products, }
    return render(request, 'secureapp/index.html', context)