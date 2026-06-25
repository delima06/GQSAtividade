# Sistema de Biblioteca - Atividade de GQS

Este é um projeto simples de biblioteca desenvolvido para fins de testes de integração na disciplina de Gestão da Qualidade de Software.

**Desenvolvido por:** Pedro Davi e Thiago de Lima

---

## Como Executar o Projeto

### 1. Instalar dependências
Certifique-se de ter o Python instalado e execute:
```bash
pip install django
```

### 2. Rodar as migrações do banco
```bash
python manage.py migrate
```

### 3. Rodar o servidor
```bash
python manage.py runserver
```
Acesse o sistema em: http://127.0.0.1:8000/

---

## Como Executar os Testes

Para rodar todos os testes de integração do projeto, execute o comando:
```bash
python manage.py test
```
