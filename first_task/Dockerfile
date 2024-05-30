FROM python:3.12

RUN apt-get update && apt-get install -y nginx certbot python3-certbot-nginx

COPY nginx_config /etc/nginx/sites-available/example
RUN ln -s /etc/nginx/sites-available/example /etc/nginx/sites-enabled/

COPY setup_server.py /

CMD ["python", "/setup_server.py"]
