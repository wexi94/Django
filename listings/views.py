from django.shortcuts import  get_object_or_404, render
from . import models
from .models import listing
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator
from listings.choices import bedroom_choices , price_choices , state_choices
def index(request):
    listings = models.listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    return render(request , 'listings/listings.html',
    {'listings': paged_listings}
    )
def search(request):
    queryset_list = listing.objects.order_by('-list_date')
    # Key Words
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
    # BedRooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request , 'listings/search.html' , context)
def Listing(request,listing_id):
    listing1 = get_object_or_404(listing , pk=listing_id)

    return render(request , 'listings/listing.html',{
        'listing':listing1
    })

