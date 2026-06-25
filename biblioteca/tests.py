from django.test import TestCase
from django.urls import reverse
from biblioteca.modelos import Autor, Livro

# --- DESENVOLVIDO POR PEDRO DAVI E THIAGO DE LIMA ---

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


    # =========================================================================
    # INÍCIO DOS TESTES DE THIAGO DE LIMA (TESTES 4 E 5)
    # =========================================================================

    # Teste 4: verificar se o empréstimo altera a disponibilidade do livro
    def test_emprestimo_de_livro(self):
        # envia requisição get para alterar a disponibilidade do livro
        response = self.client.get(reverse("emprestar_livro", args=[self.livro.id]), follow=True)
        
        # deve retornar status 200
        self.assertEqual(response.status_code, 200)
        
        # verificar se renderiza a página de listagem
        self.assertTemplateUsed(response, "biblioteca/lista_livros.html")
        
        # atualiza os dados do banco para verificar a alteração
        self.livro.refresh_from_db()
        self.assertFalse(self.livro.disponivel)
        
        # verificar se as informações foram atualizadas na tela
        self.assertContains(response, "Emprestado")
        self.assertContains(response, "Dom Casmurro")

    # Teste 5: rejeitar cadastro de autor com campos vazios
    def test_cadastro_invalido_de_autor_nao_salva(self):
        dados_invalidos = {
            "nome": "",
            "nacionalidade": ""
        }

        # envia requisição post com dados vazios
        response = self.client.post(reverse("criar_autor"), dados_invalidos)
        
        # deve retornar status 200 exibindo o formulário novamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "biblioteca/formulario_autor.html")
        
        # verificar se a mensagem de erro é exibida na tela
        self.assertContains(response, "Campos obrigatórios!")
        
        # a quantidade de autores no banco não pode aumentar
        self.assertEqual(Autor.objects.count(), 1)

    # =========================================================================
    # FIM DOS TESTES DE THIAGO DE LIMA
    # =========================================================================