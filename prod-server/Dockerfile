# Load React app and build latest staticfiles
FROM node:latest as npm-build-stage

WORKDIR /frontend

ENV NODE_ENV production

COPY frontend/package.json frontend/package-lock.json /frontend/

RUN npm install

COPY frontend /frontend/

RUN npm run build

# Import staticfiles into nginx server and serve
FROM nginx:latest as prod-stage

COPY --from=npm-build-stage /frontend/build /usr/share/nginx/html

# TODO: copy config files over from . (/nginx)

EXPOSE 80 443

# TODO: Tweak this command with any params needed 
CMD ["nginx", "-g", "daemon off;"]
