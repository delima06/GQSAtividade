from django.db import models

# --- DESENVOLVIDO POR PEDRO DAVI E THIAGO DE LIMA ---

class Autor(models.Model):
    # representa o autor de um livro no sistema
    nome = models.CharField(max_length=200)
    nacionalidade = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        # retorna o nome do autor
        return self.nome


class Livro(models.Model):
    # representa o livro cadastrado na biblioteca
    titulo = models.CharField(max_length=250)
    ano = models.IntegerField()
    disponivel = models.BooleanField(default=True)
    
    # chave estrangeira vinculando o livro ao autor correspondente
    autor = models.ForeignKey(
        Autor, 
        on_delete=models.CASCADE, 
        related_name="livros"
    )

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        ordering = ['titulo']

    def __str__(self):
        # retorna o titulo e ano do livro
        return f"{self.titulo} ({self.ano})"
