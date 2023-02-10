FROM node:19
COPY ./chatgpt-frontend /data/app/chatgpt-frontend
WORKDIR /data/app/chatgpt-frontend
RUN npm install --legacy-peer-deps && npm run build



FROM python:3.9
COPY ./chatgpt-backend /data/app/chatgpt-backend
WORKDIR /data/app/chatgpt-backend
## 先跑 run，否则 文件内容变动会导致构建时重新 pip install 依赖  速度较慢
#COPY ./chatgpt-backend/requirements.txt /data/app/chatgpt-backend/requirements.txt
RUN pip3 install -r requirements.txt     && rm -rf ~/.pip/cache


CMD ["gunicorn", "-c", "gunicorn.py", "app:server"]

FROM nginx
RUN mkdir -p /data/app/chatgpt-frontend  && mkdir -p /var/log/chatgpt-frontend && rm /etc/nginx/conf.d/default.conf
COPY --from=0 /data/app/chatgpt-frontend/dist /data/app/chatgpt-frontend
COPY deploy/nginx.conf /etc/nginx/conf.d/chatgpt-frontend.conf