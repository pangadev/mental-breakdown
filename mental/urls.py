"""mental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crm.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('contacts/', ContactList.as_view()),
    path('contacts/sort/<str:sort>', ContactListSort.as_view()),
    path('contact/create', ContactCreate.as_view()),
    path('contact/view/<int:id>', ContactView.as_view()),
    path('contact/edit/<int:id>', ContactEdit.as_view()),
    path('contact/delete/<int:id>', ContactDelete.as_view()),
    path('relationships/', RelationshipTypeCreate.as_view()),
    path('contact/<int:id>/relationship/add', ContactRelationshipCreate.as_view()),
    path('contact/<int:id>/relationship/delete/<str:type>/<int:id2>/<int:id3>/', ContactRelationshipDelete.as_view()),
    path('contact/<int:id>/activity/<int:activity_id>/edit/', ActivityEdit.as_view()),
    path('contact/<int:id>/activity/<int:activity_id>/delete/', ActivityDelete.as_view()),
    path('search/', SearchResult.as_view()),
    path('accounts/login/', UserLogin.as_view(), name='usercreate'),
    path('logout/', UserLogout.as_view(), name='userlogout'),
    path('add_user/', CreateUser.as_view(), name='createuser'),
    path('reset_pass/', ForgottenPassword.as_view(), name='forgottenpassword'),

    path('render/pdf/<int:id>', RenderPDF.as_view(), name='pdf'),

    # path('relationships/edit/<int:id>', RelationshipTypeEdit.as_view()),
    # path('relationships/delete/<int:id>', RelationshipTypeDelete.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
