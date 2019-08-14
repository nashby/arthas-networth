FROM node:12.4.0-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install --silent

ADD . /app
WORKDIR /app

CMD ["npm", "run", "build"]
