"""
URL configuration for meuprojeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin # type: ignore
from django.urls import path
from app_leandro import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cliente', views.cliente,name='cliente'),
    path('contato', views.contato, name='contato'),
    path('contatos', views.contatos, name='contatos'),
    path('edit_usuario', views.edit_usuario, name='edit_usuario'),
    path('erro', views.erro, name='erro'),
    path('', views.login, name='login'),
    path('admin/', admin.site.urls),
    path('meus_clientes',views.meus_clientes, name='meus_clientes'),
    path('paginainicial', views.paginainicial, name='paginainicial'),
    path('rotas', views.rotas, name='rotas'),
    path('sobre', views.sobre, name='sobre'),
    path('sucesso', views.sucesso, name='sucesso'),
    path('usuarios', views.usuarios, name='usuarios')
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()