# Educa+ Django — interface original preservada

Esta versão usa as páginas HTML originais do Educa+ Arcade e as serve pelo Django. Mantém o visual azul/amarelo, catálogo de 15 cursos, pesquisa e filtros, modal de login/cadastro, favoritos e painel do professor com cadastro/edição/exclusão de cursos.

## Linux Mint / Ubuntu

No terminal, dentro da pasta do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra **http://127.0.0.1:8000/** — não use a porta `5500` do Live Server.

## Contas de demonstração
- Professor: `professor@educaplus.com` / `123`
- Aluno: `aluno@educaplus.com` / `123`

O front-end original usa `localStorage` do navegador para contas, favoritos e cursos cadastrados. Portanto, esses dados ficam neste navegador e não são contas seguras do banco de dados Django. Os modelos Django também estão disponíveis no admin para evolução do projeto.
