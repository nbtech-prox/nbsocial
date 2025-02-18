-- Remover banco de dados se existir
DROP DATABASE IF EXISTS nbsocial;

-- Criar banco de dados com suporte a UTF-8
CREATE DATABASE nbsocial CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criar usuário se não existir
CREATE USER IF NOT EXISTS 'nbsocial'@'localhost' IDENTIFIED BY 'nbsocial123';

-- Conceder privilégios
GRANT ALL PRIVILEGES ON nbsocial.* TO 'nbsocial'@'localhost';
FLUSH PRIVILEGES;
