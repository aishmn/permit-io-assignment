FROM node:alpine AS build

WORKDIR /app

COPY ./webapp/package*.json ./

RUN npm install --production

COPY ./webapp .

RUN npm run build

FROM node:alpine

WORKDIR /app

COPY --from=build /app/build ./build

EXPOSE 3000

CMD ["npx", "serve", "-s", "build", "-l", "3000"]
