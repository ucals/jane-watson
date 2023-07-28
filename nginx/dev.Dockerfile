FROM nginx:1.21-alpine

COPY development.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
