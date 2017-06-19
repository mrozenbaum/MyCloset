from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import UserForm, ProfileForm, ItemForm
from django.template import RequestContext
from .models import User, Profile, Category, Item
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.datastructures import MultiValueDictKeyError



# Create your views here.



def index(request):
    if request.method == 'GET':
        template_name = 'index.html'

        try:
            welcome_user = Profile.objects.filter(account_name=request.user)
            return render(request, template_name, {
                  'welcome_user': welcome_user})
        except TypeError:
            return render(request, template_name, {
                  'welcome_user': list('apple')})    
    

def login_user(request):
    '''
    purpose: Handles the creation of a new user for authentication
    author: steve brownlee
    args: request -- The full HTTP request object
    returns: render index view or error if invalid login
    '''
    # Obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = request.POST['username']
        password = request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)            
            return HttpResponseRedirect('/closetclient')

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'login.html', {}, context)


def register(request):
    """
    purpose: Handles the creation of a new user for authentication
    author: steve brownlee
    args: request -- The full HTTP request object
    returns: render of a registration from or invocation of django's login() method
    """
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()   

            user.profile.closet_name = profile_form.cleaned_data['closet_name'] 
            user.save()            

            # Update our variable to tell the template registration was successful.
            registered = True        

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        profile_form = ProfileForm()
        template_name = 'register.html'
        return render(request, template_name, {
            'user_form': user_form,
            'profile_form': profile_form})


def view_account(request):
    template_name = 'view_account.html'
    if request.method == 'GET':
        return render(request, template_name)

    if request.method == "POST":
        return render(request, template_name)         


def add_item(request):
    '''
    purpose: produce a form for the user to be able to add an item to a category
    author: miriam rozenbaum
    arg: request
    returns: redirect to detail view for item added

    '''
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        item_form = ItemForm()
        template_name = 'create_item.html'
        return render(request, template_name, {'item_form': item_form})      
    elif request.method == 'POST':
        form_data = request.POST
        file_data = request.FILES
        print(file_data)
        return render(request, 'closetclient/create_item.html', {
            'item_form': item_form,
            })
        
        def create_item(item_image):
            i = Item(
                user=request.user,
                title=form_data['title'],
                description=form_data['description'],
                brand=form_data['brand'],
                image_path=item_image,
               # create instance of category of where category_name = the user's choice
                item_category=Category.objects.get(category_name=form_data['item_category']))
            i.save()
            return i

            item_image = None
            
            # if trying to upload an image:
            if 'image_path' in request.FILES:
                item_image = request.FILES['image_path']
            else:
                item_image = None
                item = create_item(item_image)
                return HttpResponseRedirect('closetclient:item_details/{}'.format(item.id))





def item_details(request, item_id):
    """
    purpose: Allows user to view item_detail view, which contains a very specific view
        for a singular item


    author: miriam rozenbaum

    args: item_id: (integer): id of item we are viewing

    returns: (render): a view of the request, template to use, and item object
    """
    
    # If trying to view, render item corresponding to id passed
    item = get_object_or_404(Item, pk=item.id)


    if request.method == 'GET':
        template_name = 'item_details.html'
        user_items = Item.object.filter(user=request.user)
        if user_items:
            number_of_items = dict()
            for item in user_items:
                number_of_items[item.title] = User.objects.filter( user=request.user)

        else:
            user_items = None
       
  
    elif request.method == 'POST':

        print(request.user.is_authenticated())
        try:
            user_items = Item.objects.get(item=item, user=request.user)
            if user_items:
                return HttpResponseRedirect('item_details/{}'.format(item_id))
        except MultipleObjectsReturned:
            return HttpResponseRedirect('item_details/{}'.format(item_id))
        except ObjectDoesNotExist:
            pass

    return render(request, template_name, {
    "item_details": item_details})                    





# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    if request.user.profile().is_valid():
        logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
        return HttpResponseRedirect('/')  



