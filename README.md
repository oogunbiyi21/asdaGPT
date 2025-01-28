---

# ASDA Scraper

## Overview

ASDA Scraper is a web application built with Flask that helps users find the best product recommendations for a given recipe's ingredients from the ASDA online store. The application leverages OpenAI's GPT-3.5 to generate recipes and ingredient lists and scrapes the ASDA website to find the most suitable products for these ingredients.

## Features

- Generate recipes and ingredient lists using OpenAI's GPT-3.5.
- Scrape ASDA's website for the best product matches for given ingredients.
- Display product recommendations with product names and links.
- Health check endpoint to ensure the application is running correctly.

## Getting Started

### Prerequisites

- Docker (for containerized setup)
- Python 3.8+ and `venv` (for local setup)

### Installation

#### Docker Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/asda-scraper.git
   cd asda-scraper
   ```

2. Set up the environment variables. Create a `.env` file in the project root directory and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Run the `docker_setup.sh` script to build and start the Docker containers:

   ```bash
   chmod +x docker_setup.sh
   ./docker_setup.sh
   ```

#### Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/asda-scraper.git
   cd asda-scraper
   ```

2. Set up the environment variables. Create a `.env` file in the project root directory and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Run the `local_setup.sh` script to set up the virtual environment and install dependencies:

   ```bash
   chmod +x local_setup.sh
   ./local_setup.sh
   ```

4. Run the Flask application:

   ```bash
   python main.py
   ```

## Usage

### Web Interface

1. Open your web browser and navigate to `http://localhost` (or the appropriate URL for your Docker setup).
2. Enter a recipe query to get a recipe and ingredient list.
3. View the best product recommendations for each ingredient from the ASDA store.

### Endpoints

- `/`: Home page.
- `/test_html`: Sample instructions and product recommendations.
- `/test_gpt_response`: Test GPT-3.5 response with sample data.
- `/scrape`: Scrape ASDA using a provided query.
- `/.well-known/ai-plugin.json`: Serve AI plugin configuration.
- `/swagger.yaml`: Serve OpenAPI specification.
- `/health`: Health check endpoint.
- `/selenium-check`: Check Selenium setup.
- `/asda-check`: Check ASDA scraping functionality.
- `/envir-check`: Environment variable check.

## Files

### `main.py`

This is the main Flask application file. It sets up the routes and handles the logic for generating recipes, scraping ASDA for product data, and displaying the results.

### `asda_scraper_multithread.py`

Contains the functions for scraping ASDA's website and selecting the best product based on the provided ingredients.

### `docker_setup.sh`

A script to set up and run the Docker environment for the ASDA Scraper application.

```bash
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
docker build --no-cache -t asda_scraper_app .

# Step 4: Run the asda_scraper_app container
docker run -d --name asda_scraper_app \
    --network my-selenium-network \
    -p 80:80 \
    --privileged \
    asda_scraper_app

# Step 5: Verify container statuses
echo "Selenium Grid container status:"
docker ps -a | grep my-selenium-grid-driver

echo "asda_scraper_app container status:"
docker ps -a | grep asda_scraper_app
```

### `local_setup.sh`

A script to set up a virtual environment and install dependencies for local development.

```bash
#!/bin/bash

python -m venv asda_scraper
source asda_scraper/bin/activate
pip install -r requirements.txt
```

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
