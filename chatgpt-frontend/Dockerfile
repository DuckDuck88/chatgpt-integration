FROM node:10
COPY ./ /chatgpt-frontend
WORKDIR /chatgpt-frontend
RUN npm install && npm run build

FROM nginx
RUN mkdir -p /data/app/live-vip-web  && mkdir -p /var/log/live_vip_svr
COPY --from=0 /data/app/live-vip-web/dist /data/app/live-vip-web
COPY ../deploy/nginx.conf /etc/nginx/conf.d/chat-frontend.conf
COPY ../deploy/nginx.logrotate.conf /etc/logrotate.d/nginx