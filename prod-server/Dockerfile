# Load React app and build latest staticfiles
FROM node:latest as npm-build-stage

WORKDIR /frontend

ENV NODE_ENV production

COPY frontend/package.json frontend/package-lock.json /frontend/

RUN npm install

COPY frontend /frontend/

ARG REACT_APP_FASTAPI_URL

ENV REACT_APP_FASTAPI_URL ${REACT_APP_FASTAPI_URL}

RUN npm run build

# Import staticfiles into nginx server and serve
FROM nginx:latest as prod-stage

COPY --from=npm-build-stage /frontend/build /usr/share/nginx/html

COPY prod-server/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443

# TODO: Tweak this command with any params needed 
CMD ["nginx", "-g", "daemon off;"]
