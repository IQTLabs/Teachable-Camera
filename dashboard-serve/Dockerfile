# production environment
FROM nginx:stable-alpine
COPY ./build /usr/share/nginx/html
COPY *.conf /etc/nginx/
COPY vhosts/ /etc/nginx/conf.d/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]