import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse

from .factories import CheeseFactory, UserFactory
from ..models import Cheese
from ..views import (
    CheeseListView,
    CheeseDetailView,
)

@pytest.fixture
def user():
    return UserFactory()

pytestmark = pytest.mark.django_db

def test_good_cheese_list_view_expanded(rf):
    # Determine the URL
    url = reverse("cheeses:list")
    # rf is pytest shortcut to django.test.RequestFactory
    # We generate a request as if from a user accessing
    # the cheese list view
    request = rf.get(url)
    # Call as_view() to make a callable object
    # callable_obj is analogous to a function-based view
    callable_obj = CheeseListView.as_view()
    # Pass in the request into the callable_obj to get an
    # HTTP response served up by Django
    response = callable_obj(request)
    # Test that the HTTP response has 'Cheese List' in the
    # HTML and has a 200 response code
    assertContains(response, 'Cheese List')

def test_good_cheese_list_view(rf):
    # Get the request
    request = rf.get(reverse("cheeses:list"))
    # Use the request to get the response
    response = CheeseListView.as_view()(request)
    # Test that the response is valid
    assertContains(response, 'Cheese List')

def test_good_cheese_detail_view(rf):
    # Order cheese from the factory
    cheese = CheeseFactory()
    # reqeust the new cheese
    url = reverse("cheeses:detail",
        kwargs={'slug': cheese.slug})
    request = rf.get(url)

    # use the request to get the response
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    # test that response is valid
    assertContains(response, cheese.name)

def test_good_cheese_create_view(client, user):
    # force client authentication
    client.force_login(user)
    #specify url of the view
    url = reverse("cheeses:add")
    # Use the client to make the request
    response = client.get(url)
    # Test that the response is valid
    assert response.status_code == 200

    