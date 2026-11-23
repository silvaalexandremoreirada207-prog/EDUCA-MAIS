
from django.contrib.auth.models import User
from usuarios.models import Perfil, Curso

# ==========================================
# 1. CRIAR PROFESSOR
# ==========================================

professor, criado = User.objects.get_or_create(
    username="professor",
    defaults={
        "first_name": "Alexandre",
        "last_name": "Moreira",
        "email": "professor@educaplus.com"
    }
)

if criado:
    professor.set_password("123")
    professor.save()

Perfil.objects.update_or_create(
    usuario=professor,
    defaults={"tipo": "professor"}
)

print("Professor Alexandre criado/verificado!")

# ==========================================
# 2. LISTA DOS 15 CURSOS ORIGINAIS
# ==========================================

cursos = [
    {
        "titulo": "Fase 1: Desenvolvimento Web Fullstack",
        "instrutor": "Prof. Alexandre Moreira",
        "categoria": "Programação",
        "nivel": "Intermediário",
        "link": "https://www.youtube.com/watch?v=Ejkb_YpuHWs&list=PLHz_AreHm4dlAnJ_jJtV29RFxnPHDuk9o",
        "descricao": "Domine HTML5, CSS3, Tailwind, JavaScript e boas práticas de construção de aplicações web modernas.",
        "avaliacao": 4.9,
        "imagem": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Fase 2: Estruturas de Dados e Algoritmos",
        "instrutor": "Prof. Alexandre Moreira da Silva",
        "categoria": "Programação",
        "nivel": "Intermediário",
        "link": "https://www.youtube.com/watch?v=8hly31xKli0&list=PLHz_AreHm4dk_nZHmxx_J0jVqikqM7rde",
        "descricao": "Estudo aprofundado de listas encadeadas, pilhas, filas, árvores e complexidade de algoritmos.",
        "avaliacao": 5.0,
        "imagem": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Fase 3: Desenvolvimento Mobile com Flutter",
        "instrutor": "Prof. Alexandre Moreira",
        "categoria": "Programação",
        "nivel": "Intermediário",
        "link": "https://www.youtube.com/watch?v=-_I5XhYhD28&list=PLlsmIu8uEx2MXMfY5O0jScl2xr8sXvYAQ",
        "descricao": "Construção de aplicativos móveis nativos para Android e iOS utilizando Flutter.",
        "avaliacao": 4.9,
        "imagem": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Fase 4: APIs RESTful com Node.js",
        "instrutor": "Prof. Marcos Vinícius",
        "categoria": "Programação",
        "nivel": "Intermediário",
        "link": "https://www.youtube.com/watch?v=xks0s4Y2k58&list=PLHz_AreHm4dn1JHgN9XbOUsZ5AQxigLui",
        "descricao": "Desenvolvimento de APIs robustas e escaláveis, autenticação JWT e documentação com Swagger.",
        "avaliacao": 4.8,
        "imagem": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Fase Bônus: Testes TDD",
        "instrutor": "Prof. Alexandre Moreira da Silva",
        "categoria": "Programação",
        "nivel": "Intermediário",
        "link": "https://www.youtube.com/watch?v=u6g2s7t6A28&list=PLHz_AreHm4dlL2T9d5k_1tV2X9Q1Z2v7",
        "descricao": "Garantia de qualidade de código através de Test-Driven Development e testes unitários.",
        "avaliacao": 4.7,
        "imagem": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Mundo 2-1: Banco de Dados e SQL Avançado",
        "instrutor": "Coordenação ADS - UNIFIP",
        "categoria": "Tecnologia",
        "nivel": "Intermediário",
        "link": "https://www.youtube.com/watch?v=Ki8p_2aE5G8&list=PLHz_AreHm4dn1JHgN9XbOUsZ5AQxigLui",
        "descricao": "Modelagem de dados, normalização, consultas complexas com PostgreSQL.",
        "avaliacao": 4.9,
        "imagem": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Mundo 2-2: Fundamentos de Cibersegurança",
        "instrutor": "Equipe Hackers do Bem",
        "categoria": "Tecnologia",
        "nivel": "Iniciante",
        "link": "https://www.youtube.com/watch?v=Xn831i3hV8Y&list=PLf-VEOxXqH_H1tF8Wq7lK0yU9O1s5wQzR",
        "descricao": "Conceitos essenciais de segurança da informação, redes de computadores e defesa contra vulnerabilidades.",
        "avaliacao": 4.8,
        "imagem": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Mundo 2-3: NoSQL e MongoDB",
        "instrutor": "Coordenação de Dados",
        "categoria": "Tecnologia",
        "nivel": "Intermediário",
        "link": "https://www.youtube.com/watch?v=J6m1s2Q3r4Y&list=PLHz_AreHm4dm6wY620XvXn7V2X9Q1Z2v7",
        "descricao": "Modelagem de documentos, agregação de dados e alta disponibilidade em bancos orientados a documentos.",
        "avaliacao": 4.6,
        "imagem": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Mundo 2-4: DevOps, CI/CD e AWS",
        "instrutor": "Equipe Cloud Tech",
        "categoria": "Tecnologia",
        "nivel": "Avançado",
        "link": "https://www.youtube.com/watch?v=ZXgWz9nGYto&list=PLf-VEOxXqH_H1tF8Wq7lK0yU9O1s5wQzR",
        "descricao": "Automação de pipelines de entrega contínua, servidores Linux, Docker, Kubernetes na AWS.",
        "avaliacao": 4.8,
        "imagem": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Mundo 2-Chefe: Inteligência Artificial & ML",
        "instrutor": "Dra. Juliana Mendes",
        "categoria": "Tecnologia",
        "nivel": "Avançado",
        "link": "https://www.youtube.com/watch?v=KNAWp2S3w94&list=PLHz_AreHm4dm6wY620XvXn7V2X9Q1Z2v7",
        "descricao": "Introdução ao aprendizado de máquina com Python, Scikit-Learn e TensorFlow.",
        "avaliacao": 5.0,
        "imagem": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Zona 3-1: UI/UX Design com Figma",
        "instrutor": "Profa. Beatriz Lima",
        "categoria": "Design",
        "nivel": "Iniciante",
        "link": "https://www.youtube.com/watch?v=g9z4s3x2W1Y&list=PLHz_AreHm4dn1JHgN9XbOUsZ5AQxigLui",
        "descricao": "Fundamentos de experiência do usuário, criação de wireframes e protótipos navegáveis.",
        "avaliacao": 4.9,
        "imagem": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Zona 3-2: Gestão Ágil com Scrum e Kanban",
        "instrutor": "Prof. Roberto Alencar",
        "categoria": "Outros",
        "nivel": "Iniciante",
        "link": "https://www.youtube.com/watch?v=9Xk1s2Q3r4Y&list=PLWKjhJtqVAbnSmfWJ8a46Rj8gQGz22V7t",
        "descricao": "Dinâmicas de equipes ágeis, papéis no Scrum e uso de ferramentas como Jira e Trello.",
        "avaliacao": 4.7,
        "imagem": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Zona 3-3: Arquitetura de Microsserviços",
        "instrutor": "Prof. Carlos Eduardo",
        "categoria": "Programação",
        "nivel": "Avançado",
        "link": "https://www.youtube.com/watch?v=1Xk0XlJ1l4Y&list=PL8iIphqZsQZz2K7Z2v7Q1Z2v7Q1Z2v7Q1",
        "descricao": "Construção de sistemas distribuídos, conteinerização de aplicações e API Gateways.",
        "avaliacao": 4.9,
        "imagem": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Zona 3-4: Engenharia de Software Avançada",
        "instrutor": "Prof. Convidado FIAP",
        "categoria": "Tecnologia",
        "nivel": "Avançado",
        "link": "https://www.youtube.com/watch?v=tAuTwn7HqmY&list=PLWKjhJtqVAbnSmfWJ8a46Rj8gQGz22V7t",
        "descricao": "Metodologias ágeis, Clean Architecture e Design Patterns essenciais para sistemas escaláveis.",
        "avaliacao": 4.8,
        "imagem": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80"
    },
    {
        "titulo": "Zona Final: Segurança Web & OWASP Top 10",
        "instrutor": "Equipe Hackers do Bem",
        "categoria": "Tecnologia",
        "nivel": "Avançado",
        "link": "https://www.youtube.com/watch?v=7Xk1s2Q3r4Y&list=PLf-VEOxXqH_H1tF8Wq7lK0yU9O1s5wQzR",
        "descricao": "Análise profunda das 10 principais vulnerabilidades web (Injection, XSS, CSRF).",
        "avaliacao": 5.0,
        "imagem": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80"
    }
]

# ==========================================
# 3. CADASTRAR OS CURSOS NO POSTGRESQL
# ==========================================

for dados in cursos:
    Curso.objects.update_or_create(
        titulo=dados["titulo"],
        defaults={
            **dados,
            "criador": professor,
            "ativo": True
        }
    )

print(f"{len(cursos)} cursos cadastrados/verificados!")
print("Professor: professor")
print("Senha: 123")
