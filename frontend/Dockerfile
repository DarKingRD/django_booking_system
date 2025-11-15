# frontend/Dockerfile

FROM nginx:alpine

# Удаляем стандартный конфиг
RUN rm -rf /etc/nginx/conf.d/default.conf

# Копируем кастомный конфиг Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем фронтенд-файлы в контейнер
COPY ./ /usr/share/nginx/html

# Открываем порт (для ясности)
EXPOSE 80

# Nginx запускается по умолчанию
CMD ["nginx", "-g", "daemon off;"]
