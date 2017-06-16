[Testing basics](https://docs.djangoproject.com/en/1.11/intro/tutorial05/#the-django-test-client) 
[Testing examples](https://docs.djangoproject.com/en/1.11/intro/tutorial05/)

* Verify that when a specific product category view (e.g. Bags) is requested, that there are items in the response context
* Verify that when x item is added to a category that view_items view has that item in the response context
* Verify that when a item is created that the Item Detail view has the correct item in the response context
* Verify that when an item is created that the Item Detail view has the title, description, price, brand, category_name, and color are in the response body
* Verify that the Category view for a user has all of their categories in the request context
* Verify that the Single Item view for a user has all of the Item Detaisl in the request context