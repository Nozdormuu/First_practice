import subprocess

# Установка Nginx
subprocess.run(["apt-get", "update"])
subprocess.run(["apt-get", "install", "-y", "nginx"])

# Настройка базовой конфигурации Nginx для работы с Certbot
nginx_config = """
server {
    listen 80;
    server_name example.com www.example.com;
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""

with open("nginx.conf", "w") as f:
    f.write(nginx_config)

subprocess.run(["ln", "-s", "/etc/nginx/sites-available/example", "/etc/nginx/sites-enabled/"])

# Установка Certbot
subprocess.run(["apt-get", "install", "-y", "certbot", "python3-certbot-nginx"])

# Настройка автоматического получения и обновления SSL-сертификатов
subprocess.run(["certbot", "--nginx", "-d", "example.com", "-d", "www.example.com", "--non-interactive", "--agree-tos", "--email", "your-email@example.com"])

# Перезапуск Nginx
subprocess.run(["systemctl", "restart", "nginx"])
