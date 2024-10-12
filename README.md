# HealthSphereAI: Red Hat OpenShiftAI Powered Graph RAG system

## 🏥 Project Overview

This project is an advanced AI-driven healthcare information system that combines natural language processing, graph databases, and vector search capabilities to provide accurate and contextual answers about patient health records and hospital data. It leverages FHIR (Fast Healthcare Interoperability Resources) data stored in a Neo4j graph database and uses AI models for intelligent query processing.

## 🚀 Key Features

- **Natural Language Query Processing**: Ask complex questions in plain English about patient data and medical history.
- **FHIR Data Integration**: Supports standardized healthcare information exchange format.
- **Graph Database**: Utilizes Neo4j for efficient storage and querying of complex healthcare data relationships.
- **Vector Search**: Implements semantic search capabilities using Neo4jVector.
- **AI-Powered Responses**: Leverages large language models (VLLM) for generating human-like, contextually relevant answers.
- **Date-Aware Querying**: Automatically extracts and interprets date information from queries.
- **Multi-Resource Query Capability**: Answers questions about patients, practitioners, organizations, and other healthcare entities.
- **Real-time Data Access**: APIs for retrieving up-to-date patient and hospital information.
- **Flexible Deployment**: Supports both local and OpenShift deployment.
- **S3 Data Ingestion**: Capable of ingesting FHIR data from S3-compatible storage.
- **Automated Vector Indexing**: Creates and updates vector indexes for efficient semantic search.
- **Confidence Scoring**: Provides confidence scores with responses for decision support.

## 🛠️ Tech Stack

- Python
- Flask
- Neo4j
- LangChain
- HuggingFace Embeddings
- VLLM (Large Language Model)
- OpenShift
- S3-compatible storage

## 📋 Prerequisites

- Python 3.8+
- Neo4j Database
- S3-compatible object storage (optional)
- OpenShift cluster (for OpenShift deployment)

## 🚀 Local Deployment

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fhir-ai-chatbot.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables (see `.env`)

4. Run the data ingestion script:
   ```
   python src/ingest_data.py
   ```

5. Start the Flask server:
   ```
   python src/app.py
   ```

## 🚢 OpenShift Deployment

1. Ensure you have access to an OpenShift cluster and the `oc` CLI tool installed.

2. Log in to your OpenShift cluster:
   ```
   oc login --token=<your-token> --server=<your-server-url>
   ```

3. Apply the OpenShift manifests:
   ```
   oc apply -f openshift-manifests/
   ```

   This will create:
   - A Job for data ingestion
   - A Deployment for the FHIR chatbot
   - A Service to expose the chatbot
   - A Route for external access
   - A Neo4j database pod

4. Monitor the deployment:
   ```
   oc get pods
   oc get services
   oc get routes
   ```

5. Access the chatbot using the Route URL provided by OpenShift.

## 🤖 OpenShift AI Integration

This project uses OpenShift AI to run the VLLM model server. Ensure that you have configured the `VLLM_URL` and `VLLM_MODEL` environment variables to point to your OpenShift AI VLLM endpoint.

## 🔧 Configuration

Key configuration options are set via environment variables:

- `NEO4J_URI`: URI for your Neo4j database
- `NEO4J_USERNAME`: Neo4j database username
- `NEO4J_PASSWORD`: Neo4j database password
- `VLLM_URL`: URL for the VLLM service on OpenShift AI
- `EMBEDDING_MODEL`: HuggingFace model name for embeddings
- `S3_*`: Configuration for S3 data ingestion (if used)

## 📚 API Documentation

### `/chat` (POST)
Submit a question to the AI system.

### `/patients` (GET)
Retrieve a list of patient names.

### `/hospitals` (GET)
Retrieve a list of hospital/organization names.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue in the GitHub issue tracker.
