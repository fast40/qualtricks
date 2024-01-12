FROM nginx:1.25-bookworm as base

RUN rm /etc/nginx/conf.d/*

FROM base as dev
COPY dev.conf /etc/nginx/conf.d

FROM base as prod
COPY prod.conf /etc/nginx/conf.d

FROM base as ssl-setup
COPY ssl-setup.conf /etc/nginx/conf.d
