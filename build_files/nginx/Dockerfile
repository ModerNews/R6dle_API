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
COPY r6dle.tech /etc/nginx/sites-available/r6dle.tech
COPY api.r6dle.tech /etc/nginx/sites-available/api.r6dle.tech

EXPOSE 80
EXPOSE 443

RUN mkdir -p /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/r6dle.tech /etc/nginx/sites-enabled/r6dle.tech && \
    ln -s /etc/nginx/sites-available/api.r6dle.tech /etc/nginx/sites-enabled/api.r6dle.tech

CMD ["nginx", "-g", "daemon off;"]