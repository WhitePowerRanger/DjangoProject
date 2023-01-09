from django.urls import path, include
from . import views

urlpatterns = [
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("", views.get_main, name="home"),
    path("order/", views.order, name="order"),
    path(
        "create/",
        include(
            [
                path("", views.get_all_city),
                path("<str:city_name>/", views.get_all_restaurants_for_specified_city),
                path("<str:city_name>/<str:restaurant_name>/", views.create_form),
            ]
        ),
    ),
    path(
        "order/<str:restaurant>", views.get_menu_for_given_restaurant
    )

]
