FROM node:latest

WORKDIR /frontend

ENV REACT_APP_FASTAPI_URL=http://127.0.0.1:8000

COPY package.json package-lock.json /frontend/

RUN npm install

COPY . /frontend

RUN npm run build

CMD ["npm", "start"]
