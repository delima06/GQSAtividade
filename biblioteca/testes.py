from django.test import TestCase
from django.urls import reverse
from .modelos import Autor, Livro

class TestesBiblioteca(TestCase):
    def setUp(self):
        # dados iniciais para rodar os testes
        self.autor = Autor.objects.create(
            nome="Machado de Assis",
            nacionalidade="Brasileira"
        )
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            ano=1899,
            disponivel=True,
            autor=self.autor
        )

    # =========================================================================
    # INÍCIO DOS TESTES DE PEDRO DAVI (TESTES 1, 2 E 3)
    # =========================================================================

    # Teste 1: verificar se a listagem de livros está exibindo os dados de forma correta
    def test_listagem_de_livros(self):
        # requisição get na rota de listagem
        response = self.client.get(reverse("listar_livros"))
        
        # deve retornar status 200 
        self.assertEqual(response.status_code, 200)
        
        # verificar se está usando o template de listagem
        self.assertTemplateUsed(response, "biblioteca/lista_livros.html")
        
        # verificar se o título ano e autor aparecem no html retornado
        self.assertContains(response, "Dom Casmurro")
        self.assertContains(response, "1899")
        self.assertContains(response, "Machado de Assis")

    # Teste 2: cadastrar um novo autor pela interface da aplicação
    def test_cadastro_de_autor(self):
        dados_autor = {
            "nome": "Clarice Lispector",
            "nacionalidade": "Brasileira"
        }
        
        # envia requisição post para cadastrar o autor
        response = self.client.post(reverse("criar_autor"), dados_autor)
        
        # deve conter dois autores cadastrados no banco de dados
        self.assertEqual(Autor.objects.count(), 2)
        
        # verificar se salvou com o nome e nacionalidade correspondentes
        novo_autor = Autor.objects.get(nome="Clarice Lispector")
        self.assertEqual(novo_autor.nacionalidade, "Brasileira")
        
        # deve redirecionar para a tela de listagem
        self.assertRedirects(response, reverse("listar_livros"))

    # Teste 3: cadastrar livro associado a um autor existente
    def test_cadastro_de_livro(self):
        dados_livro = {
            "titulo": "Memórias Póstumas de Brás Cubas",
            "ano": 1881,
            "autor": self.autor.id  # id do autor criado no setup
        }
        
        # envia requisição post para salvar o livro
        response = self.client.post(reverse("criar_livro"), dados_livro)
        
        # deve conter dois livros salvos no banco de dados
        self.assertEqual(Livro.objects.count(), 2)
        
        # verificar se o livro salvo corresponde aos dados informados
        novo_livro = Livro.objects.get(titulo="Memórias Póstumas de Brás Cubas")
        self.assertEqual(novo_livro.ano, 1881)
        self.assertTrue(novo_livro.disponivel) # por padrão deve ser criado como disponível
        
        # verificar se o relacionamento com o autor foi mantido
        self.assertEqual(novo_livro.autor, self.autor)
        
        # deve redirecionar para a listagem de livros também
        self.assertRedirects(response, reverse("listar_livros"))

    # =========================================================================
    # FIM DOS TESTES DE PEDRO DAVI
    # =========================================================================
