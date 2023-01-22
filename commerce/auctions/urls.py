from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("<int:listings_id>", views.show_listing, name="listing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("close", views.close_listing, name="close"),
    path("comments", views.make_comments, name="comments"),
    path("categories", views.categories, name="categories"),
    path("<str:category>", views.category_view, name="category")
]
