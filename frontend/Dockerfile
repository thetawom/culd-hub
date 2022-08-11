# Use an official Node runtime as a parent image
FROM node:18-alpine

WORKDIR /app/

# Install dependencies
COPY package.json package-lock.json /app/

RUN npm install

# Add rest of the client code
COPY . /app/

EXPOSE 3000

CMD npm start