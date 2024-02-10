#!/bin/bash

# Step 1: Create a Docker network
docker network create my-selenium-network

# Step 2: Run the Selenium Grid container
docker run -d --name my-selenium-grid-driver \
    --network my-selenium-network \
    -p 4444:4444 \
    -p 7900:7900 \
    --shm-size="2g" \
    --privileged \
    seleniarm/standalone-chromium:latest

# Step 3: Build the asda_scraper_app image
docker build -t asda_scraper_app .

# Step 4: Run the asda_scraper_app container
docker run -d --name asda_scraper_app \
    --network my-selenium-network \
    -p 81:81 \
    --privileged \
    asda_scraper_app

# Step 5: Verify container statuses
echo "Selenium Grid container status:"
docker ps -a | grep my-selenium-grid-driver

echo "asda_scraper_app container status:"
docker ps -a | grep asda_scraper_app
