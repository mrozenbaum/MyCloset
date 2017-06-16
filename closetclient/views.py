from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .forms import UserForm, ProfileForm, ItemForm
from django.template import RequestContext
from .models import User, Profile, Category, Item
from django.contrib.auth.decorators import login_required


# Create your views here.



def index(request):
    if request.method == 'GET':
        template_name = 'index.html'

        try:
            welcome_user = Profile.objects.filter(closet_name=request.user)
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
    purpose:
    arg:
    author:

    '''
    if request.method == 'GET':
        item_form = ItemForm()
        template_name = 'add_item.html'
        return render(request, template_name, {'item_form': item_form})

    # if POST, gather form data and save, then redirect to details of that item
    elif request.method == 'POST':
        form_data = request.POST
        file_data = request.FILES
        print(file_data)


        def create_item(item_image):
            i = Item(
                user=request.user,
                category_name=form_data['category_name'],
                description=form_data['description'],
                title=form_data['title'],
                brand=form_data['brand'],
                price=form_data['price'],
                color=form_data['color'],
                image_path=item_image,

                # create instance of category of where category = the users choice
                item_category=Category.objects.get(category_name=form_data['name']))
            i.save()
            return i

        item_image = None

        #if trying to upload an image:
        if 'image_path' in request.FILES:
            item_image = request.FILES['image_path']
        else:
            item_image = None

            item = create_item(item_image)
        
        return HttpResponseRedirect('item_details/{}'.format(item.title, item.description, item.brand, item.image_path, item.color, item.category_name))






def item_details(request, item_id):

    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'GET':
        template_name = 'item_details.html'
        try:
            if request.user.is_authenticated():
                item = Item.objects.get(item=item, user=request.user)
            else:
                item = None
        except ObjectDoesNotExist:
            item = None

    elif request.method == 'POST:        


        return render(request, template_name, {
            'item': item,
            })

    







                   

















# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    if request.user.profile().is_valid():
        logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
        return HttpResponseRedirect('/')  



