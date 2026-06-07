FROM node:20-slim AS build

WORKDIR /app

ARG VITE_API_URL=http://localhost:9000/api
ENV VITE_API_URL=$VITE_API_URL

COPY package.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20-slim

RUN npm install -g serve

WORKDIR /app

COPY --from=build /app/build ./build

WORKDIR /app/build

RUN cp 200.html index.html

EXPOSE 5173

CMD ["serve", "-s", ".", "-l", "5173"]
