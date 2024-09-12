# Imports needed

import glob
import json
import os
import re
import boto3
from botocore.client import Config
from dotenv import load_dotenv
import logging

from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings

# Imports from other local python files
from NEO4J_Graph import Graph
from FHIR_to_graph import resource_to_node, resource_to_edges

load_dotenv()

NEO4J_URI = os.getenv('NEO4J_URI')
USERNAME = os.getenv('NEO4J_USERNAME')
PASSWORD = os.getenv('NEO4J_PASSWORD')
DATABASE = os.getenv('NEO4J_DATABASE')

graph = Graph(NEO4J_URI, USERNAME, PASSWORD, DATABASE)
graph.wipe_database()
print(graph.resource_metrics())
print(graph.database_metrics())
graph.wipe_database()

def load_files_from_s3():
    s3_endpoint = os.getenv('S3_ENDPOINT_URL')
    s3_access_key = os.getenv('S3_ACCESS_KEY_ID')
    s3_secret_key = os.getenv('S3_SECRET_ACCESS_KEY')
    s3_region = os.getenv('S3_REGION')
    bucket_name = os.getenv('S3_BUCKET_NAME', 'fhir-data')
    prefix = os.getenv('S3_PREFIX', 'working/bundles/')

    try:
        s3 = boto3.client('s3',
                          endpoint_url=s3_endpoint,
                          aws_access_key_id=s3_access_key,
                          aws_secret_access_key=s3_secret_key,
                          region_name=s3_region,
                          config=Config(signature_version='s3v4'))
        
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        s3_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.json')]
        
        json_data = []
        for file_key in s3_files:
            obj = s3.get_object(Bucket=bucket_name, Key=file_key)
            file_content = obj['Body'].read().decode('utf-8')
            json_data.append(json.loads(file_content))
        
        logging.info(f"Successfully loaded {len(json_data)} JSON files from S3")
        return json_data
    except Exception as e:
        logging.error(f"Error loading files from S3: {str(e)}")
        return None

def process_bundles(bundles):
    nodes = []
    edges = []
    dates = set()
    for bundle in bundles:
        for entry in bundle['entry']:
            resource_type = entry['resource']['resourceType']
            if resource_type != 'Provenance':
                nodes.append(resource_to_node(entry['resource']))
                node_edges, node_dates = resource_to_edges(entry['resource'])
                edges += node_edges
                dates.update(node_dates)
    return nodes, edges, dates

# Main execution
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    graph = Graph(NEO4J_URI, USERNAME, PASSWORD, DATABASE)
    graph.wipe_database()
    logging.info("Database wiped clean")

    # Try to load files from S3
    logging.info(f"Attempting to load files from S3 bucket: {os.getenv('S3_BUCKET_NAME', 'fhir-data')}, prefix: {os.getenv('S3_PREFIX', 'working/bundles/')}")
    s3_bundles = load_files_from_s3()

    if s3_bundles:
        logging.info(f"Processing {len(s3_bundles)} JSON files from S3")
        nodes, edges, dates = process_bundles(s3_bundles)
    else:
        # Fallback to local files if S3 loading fails
        logging.info("Falling back to local files")
        synthea_bundles = glob.glob("./working/bundles/*.json")
        synthea_bundles.sort()
        local_bundles = [json.load(open(file_name)) for file_name in synthea_bundles]
        logging.info(f"Processing {len(local_bundles)} local JSON files")
        nodes, edges, dates = process_bundles(local_bundles)

    # create the nodes for resources
    for node in nodes:
        graph.query(node)

    date_pattern = re.compile(r'([0-9]+)/([0-9]+)/([0-9]+)')

    # create the nodes for dates
    for date in dates:
        date_parts = date_pattern.findall(date)[0]
        cypher_date = f'{date_parts[2]}-{date_parts[0]}-{date_parts[1]}'
        cypher = 'CREATE (:Date {name:"' + date + '", id: "' + date + '", date: date("' + cypher_date + '")})'
        graph.query(cypher)

    # create the edges
    for edge in edges:
        try:
            graph.query(edge)
        except:
            print(f'Failed to create edge: {edge}')

    print(graph.resource_metrics())
    print(graph.database_metrics())

    Neo4jVector.from_existing_graph(
        HuggingFaceBgeEmbeddings(model_name=os.getenv('EMBEDDING_MODEL')),
        url=NEO4J_URI,
        username=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        index_name='fhir_text',
        node_label="resource",
        text_node_properties=['text'],
        embedding_node_property='embedding',
    )