from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=200)
    nacionalidade = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=250)
    ano = models.IntegerField()
    disponivel = models.BooleanField(default=True)

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
        return f"{self.titulo} ({self.ano})"
