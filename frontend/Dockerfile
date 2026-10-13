# ==============================================================================
# Stage 1: Build the React application
# ==============================================================================
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code and build production assets
COPY . .
RUN npm run build

# ==============================================================================
# Stage 2: Serve static assets with Nginx
# ==============================================================================
FROM nginx:alpine

# Copy built React files to Nginx public web folder
COPY --from=build /app/build /usr/share/nginx/html

# Expose web server port
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
