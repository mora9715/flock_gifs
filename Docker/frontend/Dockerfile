ARG BASE_IMAGE='flock_gifs_backend:latest'

# Building frontend:

FROM node:latest as build-stage
WORKDIR /app
COPY ./frontend/package*.json ./
COPY ./frontend ./
RUN npm install
RUN npm run build

# Moving static to nginx-friendly location
FROM ${BASE_IMAGE} as base_image
FROM nginx as production-stage

# Static for backend:
COPY --from=base_image /application/static /usr/share/backend/static/

# Static for frontend:
COPY --from=build-stage /app/dist /usr/share/frontend/static/
COPY ./Docker/frontend/conf/frontend.conf /etc/nginx/conf.d/frontend.conf

COPY ./Docker/frontend/conf/nginx.conf /etc/nginx/nginx.conf


#COPY html/ /usr/share/nginx/html
