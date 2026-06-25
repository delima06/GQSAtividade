from django.urls import path
from . import views

# --- DESENVOLVIDO POR PEDRO DAVI E THIAGO DE LIMA ---

# rotas do sistema da biblioteca
urlpatterns = [
    path('autores/novo/', views.criar_autor, name='criar_autor'),
    path('livros/', views.listar_livros, name='listar_livros'),
    path('livros/novo/', views.criar_livro, name='criar_livro'),
    path('livros/emprestar/<int:livro_id>/', views.emprestar_livro, name='emprestar_livro'),
]
