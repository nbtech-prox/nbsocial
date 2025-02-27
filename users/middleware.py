from django.db import connection

class EnsureProfileTableMiddleware:
    """
    Middleware para garantir que a tabela users_profile exista.
    Executa apenas uma vez durante o processamento da primeira requisição.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.table_checked = False
    
    def __call__(self, request):
        # Executa apenas uma vez
        if not self.table_checked and not request.path.startswith('/admin/'):
            self.ensure_profile_table_exists()
            self.table_checked = True
        
        return self.get_response(request)
    
    def ensure_profile_table_exists(self):
        """Verificar se a tabela users_profile existe e criá-la se necessário"""
        try:
            with connection.cursor() as cursor:
                # Verificar se a tabela existe
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_name = 'users_profile'
                """)
                if cursor.fetchone()[0] == 0:
                    # Criar a tabela se não existir
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS `users_profile` (
                      `id` bigint NOT NULL AUTO_INCREMENT,
                      `bio` longtext,
                      `user_id` bigint NOT NULL,
                      PRIMARY KEY (`id`),
                      UNIQUE KEY `user_id` (`user_id`),
                      CONSTRAINT `users_profile_user_id_foreignkey` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                    """)
                    print("[INFO] Tabela users_profile criada com sucesso!")
        except Exception as e:
            print(f"[ERRO] Erro ao verificar/criar tabela Profile: {e}")
