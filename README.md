# NBSocial

Uma rede social moderna desenvolvida com Django e Tailwind CSS.

## Requisitos

- Python 3.8+
- MariaDB
- Node.js e npm (para Tailwind CSS)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nbsocial.git
cd nbsocial
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados MariaDB:
```sql
CREATE DATABASE nbsocial CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. Configure as variáveis de ambiente no arquivo .env:
```
DEBUG=True
SECRET_KEY=sua-chave-secreta
DB_NAME=nbsocial
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=3306
```

6. Execute as migrações:
```bash
python manage.py migrate
```

7. Crie um superusuário:
```bash
python manage.py createsuperuser
```

8. Instale e compile o Tailwind CSS:
```bash
python manage.py tailwind install
python manage.py tailwind build
```

9. Execute o servidor de desenvolvimento:
```bash
python manage.py runserver
```

## Funcionalidades

- Sistema de autenticação completo
- Perfis de usuários
- Sistema de posts e comentários
- Sistema de likes e compartilhamentos
- Painel de administração
- Moderação de conteúdo
- Design responsivo com Tailwind CSS

## Estrutura do Projeto

- `core/` - Aplicação principal
- `users/` - Gestão de usuários e perfis
- `posts/` - Sistema de posts e interações
- `templates/` - Templates HTML
- `static/` - Arquivos estáticos
- `media/` - Uploads de usuários

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
