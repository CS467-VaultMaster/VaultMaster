FROM node:latest

WORKDIR /frontend

COPY package.json package-lock.json /frontend/

RUN npm install

COPY . /frontend

RUN npm run build

CMD ["npm", "start"]
