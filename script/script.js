const defaultCourses = [
    // --- MUNDO 1: PROGRAMAÇÃO & FULLSTACK ---
    {
        id: "1",
        title: "Fase 1: Desenvolvimento Web Fullstack",
        instructor: "Prof. Alexandre Moreira",
        category: "Programação",
        level: "Intermediário",
        link: "https://www.youtube.com/watch?v=Ejkb_YpuHWs&list=PLHz_AreHm4dlAnJ_jJtV29RFxnPHDuk9o",
        description: "Domine HTML5, CSS3, Tailwind, JavaScript e boas práticas de construção de aplicações web modernas.",
        rating: 4.9,
        image: "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "2",
        title: "Fase 2: Estruturas de Dados e Algoritmos",
        instructor: "Prof. Alexandre Moreira da Silva",
        category: "Programação",
        level: "Intermediário",
        link: "https://www.youtube.com/watch?v=8hly31xKli0&list=PLHz_AreHm4dk_nZHmxx_J0jVqikqM7rde",
        description: "Estudo aprofundado de listas encadeadas, pilhas, filas, árvores e complexidade de algoritmos.",
        rating: 5.0,
        image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "3",
        title: "Fase 3: Desenvolvimento Mobile com Flutter",
        instructor: "Prof. Alexandre Moreira",
        category: "Programação",
        level: "Intermediário",
        link: "https://www.youtube.com/watch?v=-_I5XhYhD28&list=PLlsmIu8uEx2MXMfY5O0jScl2xr8sXvYAQ",
        description: "Construção de aplicativos móveis nativos para Android e iOS utilizando o framework Flutter.",
        rating: 4.9,
        image: "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "4",
        title: "Fase 4: APIs RESTful com Node.js",
        instructor: "Prof. Marcos Vinícius",
        category: "Programação",
        level: "Intermediário",
        link: "https://www.youtube.com/watch?v=xks0s4Y2k58&list=PLHz_AreHm4dn1JHgN9XbOUsZ5AQxigLui",
        description: "Desenvolvimento de APIs robustas e escaláveis, autenticação JWT e documentação com Swagger.",
        rating: 4.8,
        image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "5",
        title: "Fase Bônus: Testes TDD",
        instructor: "Prof. Alexandre Moreira da Silva",
        category: "Programação",
        level: "Intermediário",
        link: "https://www.youtube.com/watch?v=u6g2s7t6A28&list=PLHz_AreHm4dlL2T9d5k_1tV2X9Q1Z2v7",
        description: "Garantia de qualidade de código através de Test-Driven Development (TDD) e testes unitários.",
        rating: 4.7,
        image: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80"
    },

    // --- MUNDO 2: BANCOS DE DADOS & TECNOLOGIA ---
    {
        id: "6",
        title: "Mundo 2-1: Banco de Dados e SQL Avançado",
        instructor: "Coordenação ADS - UNIFIP",
        category: "Tecnologia",
        level: "Intermediário",
        link: "https://www.youtube.com/watch?v=Ki8p_2aE5G8&list=PLHz_AreHm4dn1JHgN9XbOUsZ5AQxigLui",
        description: "Modelagem de dados, normalização, consultas complexas (JOINs, Subqueries) com PostgreSQL.",
        rating: 4.9,
        image: "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "7",
        title: "Mundo 2-2: Fundamentos de Cibersegurança",
        instructor: "Equipe Hackers do Bem",
        category: "Tecnologia",
        level: "Iniciante",
        link: "https://www.youtube.com/watch?v=Xn831i3hV8Y&list=PLf-VEOxXqH_H1tF8Wq7lK0yU9O1s5wQzR",
        description: "Conceitos essenciais de segurança da informação, redes de computadores e defesa contra vulnerabilidades.",
        rating: 4.8,
        image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "8",
        title: "Mundo 2-3: NoSQL e MongoDB",
        instructor: "Coordenação de Dados",
        category: "Tecnologia",
        level: "Intermediário",
        link: "https://www.youtube.com/watch?v=J6m1s2Q3r4Y&list=PLHz_AreHm4dm6wY620XvXn7V2X9Q1Z2v7",
        description: "Modelagem de documentos, agregação de dados e alta disponibilidade em bancos orientados a documentos.",
        rating: 4.6,
        image: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "9",
        title: "Mundo 2-4: DevOps, CI/CD e AWS",
        instructor: "Equipe Cloud Tech",
        category: "Tecnologia",
        level: "Avançado",
        link: "https://www.youtube.com/watch?v=ZXgWz9nGYto&list=PLf-VEOxXqH_H1tF8Wq7lK0yU9O1s5wQzR",
        description: "Automação de pipelines de entrega contínua, servidores Linux, Docker, Kubernetes na AWS.",
        rating: 4.8,
        image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "10",
        title: "Mundo 2-Chefe: Inteligência Artificial & ML",
        instructor: "Dra. Juliana Mendes",
        category: "Tecnologia",
        level: "Avançado",
        link: "https://www.youtube.com/watch?v=KNAWp2S3w94&list=PLHz_AreHm4dm6wY620XvXn7V2X9Q1Z2v7",
        description: "Introdução ao aprendizado de máquina com Python, Scikit-Learn e TensorFlow.",
        rating: 5.0,
        image: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80"
    },

    // --- MUNDO 3: DESIGN, GESTÃO & REDES ---
    {
        id: "11",
        title: "Zona 3-1: UI/UX Design com Figma",
        instructor: "Profa. Beatriz Lima",
        category: "Design",
        level: "Iniciante",
        link: "https://www.youtube.com/watch?v=g9z4s3x2W1Y&list=PLHz_AreHm4dn1JHgN9XbOUsZ5AQxigLui",
        description: "Fundamentos de experiência do usuário, criação de wireframes e protótipos navegáveis.",
        rating: 4.9,
        image: "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "12",
        title: "Zona 3-2: Gestão Ágil com Scrum e Kanban",
        instructor: "Prof. Roberto Alencar",
        category: "Outros",
        level: "Iniciante",
        link: "https://www.youtube.com/watch?v=9Xk1s2Q3r4Y&list=PLWKjhJtqVAbnSmfWJ8a46Rj8gQGz22V7t",
        description: "Dinâmicas de equipes ágeis, papéis no Scrum e uso de ferramentas como Jira e Trello.",
        rating: 4.7,
        image: "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "13",
        title: "Zona 3-3: Arquitetura de Microsserviços",
        instructor: "Prof. Carlos Eduardo",
        category: "Programação",
        level: "Avançado",
        link: "https://www.youtube.com/watch?v=1Xk0XlJ1l4Y&list=PL8iIphqZsQZz2K7Z2v7Q1Z2v7Q1Z2v7Q1",
        description: "Construção de sistemas distribuídos, conteinerização de aplicações e API Gateways.",
        rating: 4.9,
        image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "14",
        title: "Zona 3-4: Engenharia de Software Avançada",
        instructor: "Prof. Convidado FIAP",
        category: "Tecnologia",
        level: "Avançado",
        link: "https://www.youtube.com/watch?v=tAuTwn7HqmY&list=PLWKjhJtqVAbnSmfWJ8a46Rj8gQGz22V7t",
        description: "Metodologias ágeis, Clean Architecture e Design Patterns essenciais para sistemas escaláveis.",
        rating: 4.8,
        image: "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80"
    },
    {
        id: "15",
        title: "Zona Final: Segurança Web & OWASP Top 10",
        instructor: "Equipe Hackers do Bem",
        category: "Tecnologia",
        level: "Avançado",
        link: "https://www.youtube.com/watch?v=7Xk1s2Q3r4Y&list=PLf-VEOxXqH_H1tF8Wq7lK0yU9O1s5wQzR",
        description: "Análise profunda das 10 principais vulnerabilidades web (Injection, XSS, CSRF).",
        rating: 5.0,
        image: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80"
    }
];

const defaultUsers = [
    { name: "Prof. Alexandre", email: "professor@educaplus.com", password: "123", role: "professor" },
    { name: "Aluno Teste", email: "aluno@educaplus.com", password: "123", role: "aluno" }
];

function getStoredCourses() {
    const stored = localStorage.getItem('educa_plus_courses_v12');
    if (!stored) {
        localStorage.setItem('educa_plus_courses_v11', JSON.stringify(defaultCourses));
        return defaultCourses;
    }
    return JSON.parse(stored);
}

function saveCourses(courses) {
    localStorage.setItem('educa_plus_courses_v11', JSON.stringify(courses));
}

function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const icon = document.getElementById('mobileMenuIcon');
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-xmark');
    } else {
        menu.classList.add('hidden');
        icon.classList.remove('fa-xmark');
        icon.classList.add('fa-bars');
    }
}

function getRegisteredUsers() {
    const users = localStorage.getItem('educa_plus_users');
    if (!users) {
        localStorage.setItem('educa_plus_users', JSON.stringify(defaultUsers));
        return defaultUsers;
    }
    return JSON.parse(users);
}

function getCurrentUser() {
    const user = localStorage.getItem('educa_plus_current_user');
    return user ? JSON.parse(user) : null;
}

function updateAuthUI() {
    const currentUser = getCurrentUser();
    const authSection = document.getElementById('authSection');
    const userProfileSection = document.getElementById('userProfileSection');
    const mobileAuthSection = document.getElementById('mobileAuthSection');
    const mobileUserProfile = document.getElementById('mobileUserProfile');

    if (!authSection || !userProfileSection) return;

    if (currentUser) {
        authSection.classList.add('hidden');
        userProfileSection.classList.remove('hidden');
        userProfileSection.classList.add('flex');
        document.getElementById('userNameDisplay').textContent = currentUser.name;
        document.getElementById('userRoleDisplay').textContent = currentUser.role === 'professor' ? 'Professor' : 'Aluno';
        document.getElementById('userInitial').textContent = currentUser.name.charAt(0).toUpperCase();

        if (mobileAuthSection && mobileUserProfile) {
            mobileAuthSection.classList.add('hidden');
            mobileUserProfile.classList.remove('hidden');
            mobileUserProfile.classList.add('flex');
            document.getElementById('mobileUserNameDisplay').textContent = currentUser.name;
            document.getElementById('mobileUserRoleDisplay').textContent = currentUser.role === 'professor' ? 'Professor' : 'Aluno';
            document.getElementById('mobileUserInitial').textContent = currentUser.name.charAt(0).toUpperCase();
        }
    } else {
        authSection.classList.remove('hidden');
        userProfileSection.classList.remove('flex');
        userProfileSection.classList.add('hidden');

        if (mobileAuthSection && mobileUserProfile) {
            mobileAuthSection.classList.remove('hidden');
            mobileUserProfile.classList.remove('flex');
            mobileUserProfile.classList.add('hidden');
        }
    }
}

function openAuthModal(type) {
    const modal = document.getElementById('authModal');
    const body = document.getElementById('authModalBody');

    if (type === 'login') {
        body.innerHTML = `
            <h3 class="text-2xl font-black uppercase text-yellow-400 mb-1">Entrar na Partida</h3>
            <p class="text-xs text-blue-200 mb-4">Acesse seu painel no Educa+ Arcade</p>
            
            <div class="bg-blue-900 border-2 border-yellow-400 p-3 rounded-2xl mb-4 text-xs text-blue-100 space-y-1">
                <p class="font-bold text-yellow-300"><i class="fa-solid fa-gamepad mr-1"></i> Contas de acesso rápido:</p>
                <p><strong>Prof:</strong> professor@educaplus.com / 123</p>
                <p><strong>Aluno:</strong> aluno@educaplus.com / 123</p>
            </div>

            <form onsubmit="handleLogin(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-black uppercase text-yellow-400 mb-1">E-mail</label>
                    <input type="email" id="loginEmail" required placeholder="seu@email.com" class="w-full bg-blue-900 border-2 border-blue-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400">
                </div>
                <div>
                    <label class="block text-xs font-black uppercase text-yellow-400 mb-1">Senha</label>
                    <input type="password" id="loginPassword" required placeholder="••••••••" class="w-full bg-blue-900 border-2 border-blue-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400">
                </div>
                <button type="submit" class="w-full bg-yellow-400 hover:bg-yellow-500 text-blue-950 font-black py-3.5 rounded-xl shadow uppercase tracking-wider transition">Start Game / Entrar</button>
            </form>
            <p class="text-center text-xs text-blue-300 mt-4">Novo jogador? <button onclick="openAuthModal('register')" class="text-yellow-400 font-bold hover:underline">Cadastre-se</button></p>
        `;
    } else {
        body.innerHTML = `
            <h3 class="text-2xl font-black uppercase text-yellow-400 mb-1">Novo Jogador</h3>
            <p class="text-xs text-blue-200 mb-6">Junte-se ao Arcade do Educa+</p>
            <form onsubmit="handleRegister(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-black uppercase text-yellow-400 mb-1">Nome Completo</label>
                    <input type="text" id="regName" required placeholder="Ex: Alexandre Moreira" class="w-full bg-blue-900 border-2 border-blue-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400">
                </div>
                <div>
                    <label class="block text-xs font-black uppercase text-yellow-400 mb-1">E-mail</label>
                    <input type="email" id="regEmail" required placeholder="seu@email.com" class="w-full bg-blue-900 border-2 border-blue-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400">
                </div>
                <div>
                    <label class="block text-xs font-black uppercase text-yellow-400 mb-1">Senha</label>
                    <input type="password" id="regPassword" required placeholder="••••••••" class="w-full bg-blue-900 border-2 border-blue-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400">
                </div>
                <div>
                    <label class="block text-xs font-black uppercase text-yellow-400 mb-1">Perfil de Uso</label>
                    <select id="regRole" class="w-full bg-blue-900 border-2 border-blue-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-yellow-400">
                        <option value="aluno">Aluno (Estudante)</option>
                        <option value="professor">Professor / Gestor</option>
                    </select>
                </div>
                <button type="submit" class="w-full bg-yellow-400 hover:bg-yellow-500 text-blue-950 font-black py-3.5 rounded-xl shadow uppercase tracking-wider transition">Criar Conta</button>
            </form>
            <p class="text-center text-xs text-blue-300 mt-4">Já tem conta? <button onclick="openAuthModal('login')" class="text-yellow-400 font-bold hover:underline">Entrar</button></p>
        `;
    }

    modal.classList.remove('hidden');
}

function closeAuthModal() {
    document.getElementById('authModal').classList.add('hidden');
}

function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const role = document.getElementById('regRole').value;

    let users = getRegisteredUsers();
    if (users.some(u => u.email === email)) {
        alert('Este e-mail já está cadastrado!');
        return;
    }

    const newUser = { name, email, password, role };
    users.push(newUser);
    localStorage.setItem('educa_plus_users', JSON.stringify(users));
    localStorage.setItem('educa_plus_current_user', JSON.stringify(newUser));

    closeAuthModal();
    updateAuthUI();
    if (document.getElementById('coursesGrid')) renderStudentCourses();
    alert(`Conta criada com sucesso! Bem-vindo(a), ${name}.`);
    
    if (role === 'professor') {
        window.location.href = 'professor.html';
    } else {
        window.location.href = 'index.html';
    }
}

function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const users = getRegisteredUsers();
    const user = users.find(u => u.email === email && u.password === password);

    if (!user) {
        alert('E-mail ou senha incorretos!');
        return;
    }

    localStorage.setItem('educa_plus_current_user', JSON.stringify(user));
    closeAuthModal();
    updateAuthUI();
    if (document.getElementById('coursesGrid')) renderStudentCourses();
    alert(`Login efetuado com sucesso! Olá, ${user.name}.`);

    if (user.role === 'professor') {
        window.location.href = 'professor.html';
    } else {
        window.location.href = 'index.html';
    }
}

function logoutUser() {
    localStorage.removeItem('educa_plus_current_user');
    updateAuthUI();
    if (document.getElementById('coursesGrid')) renderStudentCourses();
    alert('Você saiu da sua conta.');
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    getRegisteredUsers();
    updateAuthUI();
    saveFavorites(getFavorites());

    if (document.getElementById('coursesGrid')) {
        renderStudentCourses();
        document.getElementById('searchInput').addEventListener('input', renderStudentCourses);
        document.getElementById('categoryFilter').addEventListener('change', renderStudentCourses);
        document.getElementById('levelFilter').addEventListener('change', renderStudentCourses);
    }
});

function getFavorites() {
    const stored = localStorage.getItem('educa_plus_favorites');
    return stored ? JSON.parse(stored) : [];
}

function saveFavorites(favorites) {
    localStorage.setItem('educa_plus_favorites', JSON.stringify(favorites));
    const badge = document.getElementById('favBadge');
    const mobileBadge = document.getElementById('mobileFavBadge');
    if (badge) badge.textContent = favorites.length;
    if (mobileBadge) mobileBadge.textContent = favorites.length;
}

function renderStudentCourses() {
    const grid = document.getElementById('coursesGrid');
    const emptyState = document.getElementById('emptyState');
    const courseCount = document.getElementById('courseCount');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const selectedCategory = document.getElementById('categoryFilter').value;
    const selectedLevel = document.getElementById('levelFilter').value;

    const courses = getStoredCourses();
    const favorites = getFavorites();

    const filtered = courses.filter(course => {
        const matchesSearch = course.title.toLowerCase().includes(searchTerm) || course.description.toLowerCase().includes(searchTerm);
        const matchesCategory = selectedCategory === "" || course.category === selectedCategory;
        const matchesLevel = selectedLevel === "" || course.level === selectedLevel;
        return matchesSearch && matchesCategory && matchesLevel;
    });

    courseCount.textContent = `${filtered.length} curso${filtered.length !== 1 ? 's' : ''}`;

    if (filtered.length === 0) {
        grid.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }

    emptyState.classList.add('hidden');
    grid.innerHTML = filtered.map(course => {
        const isFav = favorites.includes(course.id);
        const courseImg = course.image || "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80";
        return `
            <div class="bg-blue-900 rounded-3xl shadow-xl hover:shadow-2xl transition-all border-2 border-blue-600 flex flex-col justify-between overflow-hidden group">
                <div class="relative h-48 w-full overflow-hidden bg-slate-900 border-b-2 border-blue-600">
                    <img src="${courseImg}" alt="${course.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500 opacity-90">
                    <div class="absolute inset-0 bg-gradient-to-t from-blue-950/80 via-transparent to-transparent"></div>
                    <div class="absolute top-3 left-3">
                        <span class="text-[10px] font-black uppercase tracking-wider bg-yellow-400 text-blue-950 px-3 py-1 rounded-full shadow">${course.category}</span>
                    </div>
                    <div class="absolute top-3 right-3">
                        <button onclick="toggleFavorite('${course.id}')" title="Salvar nos favoritos" class="bg-blue-950/90 backdrop-blur-sm w-9 h-9 rounded-full flex items-center justify-center text-yellow-400 hover:text-white transition shadow border border-yellow-400 ${isFav ? 'bg-yellow-400 text-blue-950' : ''}"><i class="fa-solid fa-bookmark"></i></button>
                    </div>
                </div>
                <div class="p-6 flex-grow flex flex-col justify-between">
                    <div>
                        <div class="flex items-center space-x-2 text-xs text-blue-200 mb-2 font-bold">
                            <span class="bg-blue-950 px-2.5 py-0.5 rounded-full border border-blue-700">${course.level}</span>
                            <span>&bull;</span>
                            <span><i class="fa-solid fa-star text-yellow-400 mr-0.5"></i> ${course.rating || '4.8'}</span>
                        </div>
                        <h3 class="text-lg font-black text-white mb-2 group-hover:text-yellow-400 transition leading-snug">${course.title}</h3>
                        <p class="text-blue-100 text-sm line-clamp-2 mb-4 font-medium">${course.description}</p>
                    </div>
                    <div>
                        <p class="text-xs text-blue-300 mb-4 font-semibold"><i class="fa-solid fa-chalkboard-user mr-1 text-yellow-400"></i> ${course.instructor}</p>
                        <button onclick="openCourseModal('${course.id}')" class="w-full bg-yellow-400 hover:bg-yellow-500 text-blue-950 font-black py-3 rounded-2xl transition flex items-center justify-center space-x-2 text-sm shadow uppercase tracking-wider">
                            <i class="fa-solid fa-play text-xs"></i>
                            <span>Play / Ver Direção</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function toggleFavorite(courseId) {
    const currentUser = getCurrentUser();
    
    if (!currentUser) {
        alert('Você precisa estar logado para adicionar missões aos favoritos!');
        openAuthModal('login');
        return;
    }

    let favorites = getFavorites();
    if (favorites.includes(courseId)) {
        favorites = favorites.filter(id => id !== courseId);
    } else {
        favorites.push(courseId);
    }
    saveFavorites(favorites);
    renderStudentCourses();
}

function toggleFavoritosModal() {
    const currentUser = getCurrentUser();

    if (!currentUser) {
        alert('Você precisa estar logado para ver suas missões favoritas!');
        openAuthModal('login');
        return;
    }

    const modal = document.getElementById('favoritosModal');
    const list = document.getElementById('favoritosList');
    const favorites = getFavorites();
    const courses = getStoredCourses();
    const favCourses = courses.filter(c => favorites.includes(c.id));

    if (favCourses.length === 0) {
        list.innerHTML = `<p class="text-center text-blue-300 py-8 text-sm font-medium">Nenhuma missão salva nos favoritos.</p>`;
    } else {
        list.innerHTML = favCourses.map(course => `
            <div class="bg-blue-900 border-2 border-blue-700 p-4 rounded-2xl flex justify-between items-center">
                <div>
                    <span class="text-[10px] font-black uppercase bg-yellow-400 text-blue-950 px-2 py-0.5 rounded">${course.category}</span>
                    <h4 class="font-black text-white text-sm mt-1">${course.title}</h4>
                    <p class="text-xs text-blue-300">${course.instructor}</p>
                </div>
                <div class="flex space-x-2">
                    <a href="${course.link}" target="_blank" class="bg-yellow-400 text-blue-950 px-3 py-1.5 rounded-xl text-xs font-black uppercase shadow">Play</a>
                    <button onclick="toggleFavorite('${course.id}'); toggleFavoritosModal();" class="text-rose-400 p-1.5 hover:text-rose-300"><i class="fa-solid fa-trash text-xs"></i></button>
                </div>
            </div>
        `).join('');
    }
    modal.classList.toggle('hidden');
}

function openCourseModal(courseId) {
    const courses = getStoredCourses();
    const course = courses.find(c => c.id === courseId);
    if (!course) return;

    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = `
        <div class="h-40 -mx-6 -mt-6 sm:-mx-8 sm:-mt-8 mb-4 overflow-hidden relative rounded-t-3xl border-b-2 border-yellow-400">
            <img src="${course.image || 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80'}" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-blue-950/60"></div>
            <span class="absolute bottom-3 left-4 text-xs font-black uppercase tracking-wider bg-yellow-400 text-blue-950 px-3 py-1 rounded-full shadow">${course.category}</span>
        </div>
        <h2 class="text-2xl font-black text-white uppercase mb-1">${course.title}</h2>
        <p class="text-xs text-yellow-300 mb-4 flex items-center font-bold"><i class="fa-solid fa-chalkboard-user mr-1.5"></i> ${course.instructor}</p>
        <div class="bg-blue-900 p-4 rounded-2xl border-2 border-blue-700 mb-6">
            <p class="text-sm text-blue-100 font-medium">${course.description}</p>
        </div>
        <div class="space-y-3">
            <a href="${course.link}" target="_blank" class="w-full bg-yellow-400 hover:bg-yellow-500 text-blue-950 font-black py-3.5 rounded-2xl shadow uppercase tracking-wider transition flex items-center justify-center space-x-2 text-sm">
                <i class="fa-solid fa-play"></i>
                <span>Acessar Aulas no YouTube</span>
            </a>
            <button onclick="closeModal()" class="w-full bg-blue-900 hover:bg-blue-800 text-white font-bold py-3 rounded-2xl transition text-sm uppercase tracking-wider border border-blue-700">Voltar para o Mapa</button>
        </div>
    `;
    document.getElementById('courseModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('courseModal').classList.add('hidden');
}