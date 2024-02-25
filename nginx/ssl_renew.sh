
COMPOSE="/usr/local/bin/docker-compose --no-ansi --no-deps"

cd /etc/my_application/
$COMPOSE up -d certbot && $COMPOSE restart nginx
