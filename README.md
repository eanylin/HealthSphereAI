# FHIR Chatbot Project

This project implements a chatbot that can answer questions about FHIR (Fast Healthcare Interoperability Resources) data stored in a Neo4j graph database. It uses the Llama 3.1 language model hosted locally with Ollama for natural language processing.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up a Neo4j database and update the connection details in `src/ingest_data.py`, `src/chatbot.py`, and `src/app.py`.

3. Install and set up Ollama with the Llama 3.1 model:
   - Follow the instructions at https://github.com/jmorganca/ollama to install Ollama
   - Pull the Llama 3.1 model: `ollama pull llama2:3.1`

4. Place your FHIR JSON files in the `data/` directory.

5. Place your logo files (fhir_logo.png and openshift_logo.png) in the `static/` directory.

## Usage

1. Ingest FHIR data into Neo4j:
   ```
   python src/ingest_data.py
   ```

2. Ensure Ollama is running:
   ```
   ollama run llama2:3.1
   ```

3. Run the web application:
   ```
   python src/app.py
   ```

   Then open a web browser and navigate to `http://localhost:5000`.

## Project Structure

- `data/`: Directory for FHIR JSON files
- `static/`: Directory for static files (logos)
- `src/`: Source code
  - `ingest_data.py`: Script to ingest FHIR data into Neo4j
  - `chatbot.py`: Chatbot logic using Ollama-hosted Llama 3.1 and Neo4j
  - `app.py`: Flask web application
- `templates/`: HTML templates for the web interface
- `requirements.txt`: Python dependencies
- `README.md`: This file
