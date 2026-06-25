from django.test import TestCase
from django.urls import reverse
from biblioteca.modelos import Autor, Livro


class TestesBiblioteca(TestCase):
    def setUp(self):
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

    def test_listagem_de_livros(self):
        response = self.client.get(reverse("listar_livros"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "biblioteca/lista_livros.html")
        self.assertContains(response, "Dom Casmurro")
        self.assertContains(response, "1899")
        self.assertContains(response, "Machado de Assis")

    def test_cadastro_de_autor(self):
        dados_autor = {
            "nome": "Clarice Lispector",
            "nacionalidade": "Brasileira"
        }

        response = self.client.post(reverse("criar_autor"), dados_autor)
        self.assertEqual(Autor.objects.count(), 2)
        novo_autor = Autor.objects.get(nome="Clarice Lispector")
        self.assertEqual(novo_autor.nacionalidade, "Brasileira")
        self.assertRedirects(response, reverse("listar_livros"))

    def test_cadastro_de_livro(self):
        dados_livro = {
            "titulo": "Memórias Póstumas de Brás Cubas",
            "ano": 1881,
            "autor": self.autor.id
        }

        response = self.client.post(reverse("criar_livro"), dados_livro)
        self.assertEqual(Livro.objects.count(), 2)
        novo_livro = Livro.objects.get(titulo="Memórias Póstumas de Brás Cubas")
        self.assertEqual(novo_livro.ano, 1881)
        self.assertTrue(novo_livro.disponivel)
        self.assertEqual(novo_livro.autor, self.autor)
        self.assertRedirects(response, reverse("listar_livros"))

    def test_emprestimo_de_livro(self):
        response = self.client.get(reverse("emprestar_livro", args=[self.livro.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "biblioteca/lista_livros.html")
        self.livro.refresh_from_db()
        self.assertFalse(self.livro.disponivel)
        self.assertContains(response, "Emprestado")
        self.assertContains(response, "Dom Casmurro")

    def test_cadastro_invalido_de_autor_nao_salva(self):
        dados_invalidos = {
            "nome": "",
            "nacionalidade": ""
        }

        response = self.client.post(reverse("criar_autor"), dados_invalidos)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "biblioteca/formulario_autor.html")
        self.assertContains(response, "Campos obrigatórios!")
        self.assertEqual(Autor.objects.count(), 1)