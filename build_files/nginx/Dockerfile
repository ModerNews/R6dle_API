FROM node:16.13.1-buster AS build

WORKDIR /app

RUN git clone https://github.com/rafisto/r6dle
RUN rm -rf r6dle/build/

WORKDIR /app/r6dle

ENV PATH /app/r6dle/node_modules/.bin:$PATH

RUN npm ci
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/r6dle/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]