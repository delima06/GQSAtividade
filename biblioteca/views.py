from django.shortcuts import render, redirect, get_object_or_404
from .modelos import Autor, Livro

def criar_autor(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        nacionalidade = request.POST.get("nacionalidade")

        if not nome or not nacionalidade:
            return render(request, "biblioteca/formulario_autor.html", {"erro": "Campos obrigatórios!"}, status=200)

        Autor.objects.create(nome=nome, nacionalidade=nacionalidade)
        return redirect("listar_livros")
    return render(request, "biblioteca/formulario_autor.html")

def listar_livros(request):
    livros = Livro.objects.all()
    return render(request, "biblioteca/lista_livros.html", {"livros": livros})

def criar_livro(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        ano = request.POST.get("ano")
        autor_id = request.POST.get("autor")

        if not titulo or not ano or not autor_id:
            return render(request, "biblioteca/formulario_livro.html", {"erro": "Dados inválidos"}, status=200)

        autor = get_object_or_404(Autor, id=autor_id)
        Livro.objects.create(titulo=titulo, ano=ano, autor=autor)
        return redirect("listar_livros")

    # Preenche o select com os autores já cadastrados.
    autores = Autor.objects.all()
    return render(request, "biblioteca/formulario_livro.html", {"autores": autores})

def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    # Alterna entre disponível e emprestado.
    livro.disponivel = not livro.disponivel
    livro.save()
    return redirect("listar_livros")
