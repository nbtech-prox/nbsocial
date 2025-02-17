CREATE DATABASE nbsocial CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'nbsocial'@'localhost' IDENTIFIED BY 'nbsocial123';
GRANT ALL PRIVILEGES ON nbsocial.* TO 'nbsocial'@'localhost';
FLUSH PRIVILEGES;
