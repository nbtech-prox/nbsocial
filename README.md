# NBSocial 🌐

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.2-green.svg)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4.1-blue.svg)](https://tailwindcss.com/)


[English](#english) | [Português](#português)

---

<a name="english"></a>
# NBSocial - Social Network Platform 🌐

## Overview
NBSocial is a modern social networking platform built with Django, offering a rich set of features for user interaction and content sharing. The platform focuses on providing a seamless user experience with real-time updates and responsive design.

## 🚀 Features
- **User Management**
  - Custom user profiles with avatars
  - Bio and personal information
  - Social media integration (Facebook, Instagram, TikTok, GitHub)
  - Follow/Unfollow system
  
- **Content Sharing**
  - Post creation and management
  - Image uploads
  - Hashtag support
  - Like and comment system
  
- **Real-time Interactions**
  - Live notifications
  - Instant messaging (coming soon)
  - Real-time post updates
  
- **Explore & Discover**
  - Trending hashtags
  - User search
  - Content discovery
  - Popular posts section

## 🛠️ Technology Stack
- **Backend**
  - Django 5.0.2
  - Python 3.11.11
  - MariaDB
  - Django Channels (for WebSocket support)
  
- **Frontend**
  - Tailwind CSS
  - JavaScript
  - HTML5
  
- **Infrastructure**
  - Docker support (coming soon)
  - Redis for caching
  - WebSocket for real-time features

## 📋 Prerequisites
- Python 3.11+
- Node.js and npm
- MariaDB
- Redis (for WebSocket support)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nbsocial.git
cd nbsocial
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate  # Windows
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies:
```bash
npm install
```

5. Set up the database:
```bash
mysql -u root -p < setup_database.sql
python manage.py migrate
```

6. Build Tailwind CSS:
```bash
npm run build
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## 🔐 Environment Variables
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://nbsocial:nbsocial123@localhost:3306/nbsocial
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the [LICENSE](LICENSE) file for details.

This means:
- Commercial use allowed
- Modifications allowed
- Distribution allowed
- Source code must be disclosed
- Same license required
- License and copyright notice required

---

<a name="português"></a>
# NBSocial - Plataforma de Rede Social 🌐

## Visão Geral
NBSocial é uma plataforma moderna de rede social construída com Django, oferecendo um conjunto rico de funcionalidades para interação entre utilizadores e partilha de conteúdo. A plataforma concentra-se em fornecer uma experiência de utilizador fluida com atualizações em tempo real e design responsivo.

## 🚀 Funcionalidades
- **Gestão de Utilizadores**
  - Perfis personalizados com avatares
  - Biografia e informações pessoais
  - Integração com redes sociais (Facebook, Instagram, TikTok, GitHub)
  - Sistema de Seguir/Deixar de Seguir
  
- **Partilha de Conteúdo**
  - Criação e gestão de publicações
  - Carregamento de imagens
  - Suporte a hashtags
  - Sistema de gostos e comentários
  
- **Interações em Tempo Real**
  - Notificações instantâneas
  - Mensagens instantâneas (em breve)
  - Atualizações de publicações em tempo real
  
- **Explorar & Descobrir**
  - Hashtags em tendência
  - Pesquisa de utilizadores
  - Descoberta de conteúdo
  - Secção de publicações populares

## 🛠️ Stack Tecnológica
- **Backend**
  - Django 5.0.2
  - Python 3.11.11
  - MariaDB
  - Django Channels (para suporte WebSocket)
  
- **Frontend**
  - Tailwind CSS
  - JavaScript
  - HTML5
  
- **Infraestrutura**
  - Suporte Docker (em breve)
  - Redis para cache
  - WebSocket para funcionalidades em tempo real

## 📋 Pré-requisitos
- Python 3.11+
- Node.js e npm
- MariaDB
- Redis (para suporte WebSocket)

## 🔧 Instalação

1. Clonar o repositório:
```bash
git clone https://github.com/seuusername/nbsocial.git
cd nbsocial
```

2. Criar e ativar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows
```

3. Instalar dependências Python:
```bash
pip install -r requirements.txt
```

4. Instalar dependências Node.js:
```bash
npm install
```

5. Configurar a base de dados:
```bash
mysql -u root -p < setup_database.sql
python manage.py migrate
```

6. Compilar Tailwind CSS:
```bash
npm run build
```

7. Criar um superutilizador:
```bash
python manage.py createsuperuser
```

8. Executar o servidor de desenvolvimento:
```bash
python manage.py runserver
```

## 🔐 Variáveis de Ambiente
Criar um ficheiro `.env` no diretório raiz com:
```
DEBUG=True
SECRET_KEY=sua-chave-secreta
DATABASE_URL=mysql://nbsocial:nbsocial123@localhost:3306/nbsocial
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🤝 Contribuir
1. Faça fork do repositório
2. Crie a sua branch de funcionalidade (`git checkout -b funcionalidade/RecursoIncrivel`)
3. Commit das suas alterações (`git commit -m 'Adicionar algum RecursoIncrivel'`)
4. Push para a branch (`git push origin funcionalidade/RecursoIncrivel`)
5. Abra um Pull Request

## 📝 Licença
Este projeto está licenciado sob a GNU General Public License v3.0 (GPL-3.0) - veja o ficheiro [LICENSE](LICENSE) para detalhes.

Isto significa:
- Uso comercial permitido
- Modificações permitidas
- Distribuição permitida
- Código fonte deve ser divulgado
- Mesma licença requerida
- Aviso de licença e copyright necessários

---

Made with ❤️ by Nuno Batista - NBTech
