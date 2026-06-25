from django.shortcuts import render, redirect, get_object_or_404
from .modelos import Autor, Livro

# --- DESENVOLVIDO POR PEDRO DAVI E THIAGO DE LIMA ---

def criar_autor(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        nacionalidade = request.POST.get("nacionalidade")
        
        # validação para o teste de rejeitar campos inválidos
        if not nome or not nacionalidade:
            return render(request, "biblioteca/formulario_autor.html", {"erro": "Campos obrigatórios!"}, status=200)
            
        Autor.objects.create(nome=nome, nacionalidade=nacionalidade)
        return redirect("listar_livros") # redireciona após salvar o autor no banco
    return render(request, "biblioteca/formulario_autor.html")

def listar_livros(request):
    livros = Livro.objects.all()
    return render(request, "biblioteca/lista_livros.html", {"livros": livros})

def criar_livro(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        ano = request.POST.get("ano")
        autor_id = request.POST.get("autor")
        
        # garante que os dados do formulário foram preenchidos
        if not titulo or not ano or not autor_id:
            return render(request, "biblioteca/formulario_livro.html", {"erro": "Dados inválidos"}, status=200)
            
        autor = get_object_or_404(Autor, id=autor_id)
        # cria o livro com os dados informados
        Livro.objects.create(titulo=titulo, ano=ano, autor=autor)
        return redirect("listar_livros")
    
    autores = Autor.objects.all() # busca autores cadastrados para exibir na seleção do formulário
    return render(request, "biblioteca/formulario_livro.html", {"autores": autores})

def cortar_emprestimo(request, livro_id):
    pass

def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    # inverte a disponibilidade do livro correspondente
    livro.disponivel = not livro.disponivel
    livro.save()
    return redirect("listar_livros")
