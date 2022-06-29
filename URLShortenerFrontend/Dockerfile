### Stage 1: build ###

FROM node:16.15.1-alpine as builder

# Set working directory.
RUN mkdir /app
WORKDIR /app

# Copy app dependencies.
COPY package.json package-lock.json /app/

# Install app dependencies.
RUN npm install --prefix .
RUN npm update

# Copy app files.
COPY . .

# Build app
RUN npm run build --prefix .


### Stage 2: delivery ###

FROM nginx:1.15.7-alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy output directory from builder to nginx image.
COPY --from=builder /app/dist/out /usr/share/nginx/html
RUN ls -la /usr/share/nginx/html/*
# SSL
COPY cert/ /etc/nginx/cert/

# RUN ls -la /etc/nginx/*


# Copy nginx configuration file.
COPY nginx.conf /etc/nginx/conf.d/default.conf

