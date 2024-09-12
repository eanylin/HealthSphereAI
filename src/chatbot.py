import glob
import json
import os
import re
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import httpx

load_dotenv()
import httpx
from langchain.graphs import Neo4jGraph
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.chat_models import ChatOllama
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.prompts import PromptTemplate

# Imports from other local python files
from NEO4J_Graph import Graph
from FHIR_to_graph import resource_to_node, resource_to_edges

NEO4J_URI = os.getenv('NEO4J_URI')
USERNAME = os.getenv('NEO4J_USERNAME')
PASSWORD = os.getenv('NEO4J_PASSWORD')
DATABASE = os.getenv('NEO4J_DATABASE')
VLLM_URL = os.getenv('VLLM_URL')
VLLM_MODEL = os.getenv('VLLM_MODEL', 'mistral')

def get_vllm_instance():
    client = httpx.Client(verify=False)
    return ChatOpenAI(
        model=VLLM_MODEL,
        openai_api_key="NOT_NEEDED",
        openai_api_base=VLLM_URL,
        max_tokens=1024,
        temperature=1,
        http_client=client,
        max_retries=3,
        request_timeout=300,
    )

graph = Graph(NEO4J_URI, USERNAME, PASSWORD, DATABASE)
print(graph.resource_metrics())
print(graph.database_metrics())

vector_index = None

def refresh_vector_index():
    global vector_index
    vector_index = Neo4jVector.from_existing_index(
        HuggingFaceBgeEmbeddings(model_name=os.getenv('EMBEDDING_MODEL')),
        url=NEO4J_URI,
        username=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        index_name='fhir_text'
    )

def get_vector_index():
    global vector_index
    if vector_index is None:
        refresh_vector_index()
    return vector_index

default_prompt='''
System: Use the following pieces of context to answer the user's question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
{context}
Human: {question}
'''

my_prompt='''
System: The following information contains entries about the patient. 
Use the primary entry and then the secondary entries to answer the user's question.
Each entry is its own type of data and secondary entries are supporting data for the primary one.
Ensure that you always look into secondary entries for information.
You should restrict your answer to using the information in the entries provided. but be very detailed in your answer.Ensure no detail in primary or secondary entries are missed.
If you are asked about the patient's name and one the entries is of type patient, you should look for the first given name and family name and answer with: [given] [family]
Highlights the important information in the entries to make it easier for the user to understand.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
{context}
----------------
User: {question}
'''

my_prompt_2='''
System: The context below contains entries about the patient's healthcare. 
Please limit your answer to the information provided in the context. Do not make up facts. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
If you are asked about the patient's name and one the entries is of type patient, you should look for the first given name and family name and answer with: [given] [family]
----------------
{context}
Human: {question}
'''

prompt = PromptTemplate.from_template(my_prompt)

#ollama_model = os.getenv('OLLAMA_MODEL', 'mistral') # mistral, orca-mini, llama2
#ollama_model = get_ollama_instance()
vllm_model = get_vllm_instance()

k_nearest = int(os.getenv('K_NEAREST', 500))

def date_for_question(question_to_find_date, model):
    _llm = model if model else get_vllm_instance()
    prompt = f'''
    system:Given the following question from the user, extract the date the question is asking about.
    Return the answer formatted as JSON only, as a single line.
    Use the form:
    
    {{"date":"[THE DATE IN THE QUESTION]"}}
    
    Use the date format of month/day/year.
    Use two digits for the month and day.
    Use four digits for the year.
    So 3/4/23 should be returned as {{"date":"03/04/2023"}}.
    So 04/14/89 should be returned as {{"date":"04/14/1989"}}.
    
    Please do not include any special formatting characters, like new lines or "\\n".
    Please do not include the word "json".
    Please do not include triple quotes.
    
    If there is no date, do not make one up. 
    If there is no date return the word "none", like: {{"date":"none"}}
    
    user:{question_to_find_date}
    '''
    _response = _llm.invoke(prompt)
    try:
        date_json = json.loads(_response.content)
        return date_json['date']
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {_response.content}")
        return None

def create_contextualized_vectorstore_with_date(date_to_look_for):
    if date_to_look_for == 'none':
        contextualize_query_with_date = """
        match (node)<-[]->(sc:resource)
        with node.text as self, reduce(s="", item in collect(distinct sc.text)[..5] | s + "\n\nSecondary Entry:\n" + item ) as ctxt, score, {} as metadata limit 10
        return "Primary Entry:\n" + self + ctxt as text, score, metadata
        """
    else:
        contextualize_query_with_date = f"""
        match (node)<-[]->(sc:resource)
        where exists {{
             (node)-[]->(d:Date {{id: '{date_to_look_for}'}})
        }}
        with node.text as self, reduce(s="", item in collect(distinct sc.text)[..5] | s + "\n\nSecondary Entry:\n" + item ) as ctxt, score, {{}} as metadata limit 10
        return "Primary Entry:\n" + self + ctxt as text, score, metadata
        """
    
    _contextualized_vectorstore_with_date = Neo4jVector.from_existing_index(
        HuggingFaceBgeEmbeddings(model_name=os.getenv('EMBEDDING_MODEL')),
        url=NEO4J_URI,
        username=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        index_name='fhir_text',
        retrieval_query=contextualize_query_with_date,
    )
    return _contextualized_vectorstore_with_date

# Define a custom document prompt that doesn't require the 'source' metadata
CUSTOM_DOCUMENT_PROMPT = PromptTemplate(
    input_variables=["page_content"],
    template="{page_content}"
)

import logging

logger = logging.getLogger(__name__)

def ask_date_question(question_to_ask, model=vllm_model, prompt_to_use=prompt):
    logger.info(f"Received question: {question_to_ask}")
    _date_str = date_for_question(question_to_ask, model)
    logger.info(f"Extracted date: {_date_str}")
    _index = create_contextualized_vectorstore_with_date(_date_str)
    
    # Create a retriever
    retriever = _index.as_retriever(search_kwargs={'k': k_nearest})
    
    # Determine the correct document variable name
    if isinstance(prompt_to_use, PromptTemplate):
        doc_var_name = 'summaries' if 'summaries' in prompt_to_use.input_variables else 'context'
    else:
        doc_var_name = 'context'  # default to 'context' if not a PromptTemplate
    logger.info(f"Using document variable name: {doc_var_name}")
    
    # Create the RetrievalQAWithSourcesChain
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt_to_use,
            "document_variable_name": doc_var_name,
            "document_prompt": CUSTOM_DOCUMENT_PROMPT
        }
    )
    
    # Run the query
    try:
        logger.info("Running QA chain")
        result = qa_chain.invoke({"question": question_to_ask})
        logger.info(f"QA chain result: {result}")
    except Exception as e:
        logger.error(f"Error running QA chain: {str(e)}")
        return {
            "formatted_answer": f"An error occurred: {str(e)}",
            "raw_answer": "",
            "date": _date_str if _date_str != "none" else None,
            "confidence": 0,
            "sources": ""
        }
    
    # Extract the answer and sources
    answer = result.get('answer', '')
    sources = result.get('sources', 'No sources provided')
    
    if not answer:
        logger.warning("No answer generated")
        answer = "I'm sorry, but I couldn't generate an answer based on the available information."
    
    # Format the final response
    formatted_response = f"""{answer}"""
    
    logger.info(f"Formatted response: {formatted_response}")
    
    return {
        "formatted_answer": formatted_response,
        "raw_answer": answer,
        "date": _date_str if _date_str != "none" else None,
        "confidence": 0.95 if answer else 0,
        "sources": sources
    }

logger = logging.getLogger(__name__)
def get_all_patient_names():
    query = """
    MATCH (p:Patient)
    RETURN p.name as name
    LIMIT 100
    """
    try:
        results = graph.query(query)
        logger.debug(f"Query results: {results}")

        patient_names = []
        if results and isinstance(results, tuple) and len(results) > 0:
            # Extract the list of patient names from the first element of the tuple
            patient_list = results[0]
            for patient in patient_list:
                if isinstance(patient, list) and len(patient) > 0:
                    patient_names.append(patient[0])
                elif isinstance(patient, str):
                    patient_names.append(patient)

        logger.info(f"Retrieved {len(patient_names)} patient names")
        return patient_names
    except Exception as e:
        logger.error(f"Error fetching patient names: {str(e)}", exc_info=True)
        return []

def get_all_hospital_names():
    query = """
    MATCH (o:Organization)
    RETURN o.name as name
    LIMIT 100
    """
    try:
        results = graph.query(query)
        logger.debug(f"Query results for organizations: {results}")

        organization_names = []
        if results and isinstance(results, tuple) and len(results) > 0:
            org_list = results[0]
            for org in org_list:
                if isinstance(org, list) and len(org) > 0:
                    organization_names.append(org[0])
                elif isinstance(org, str):
                    organization_names.append(org)

        logger.info(f"Retrieved {len(organization_names)} organization names")
        
        if len(organization_names) == 0:
            # If no organizations found, let's check what types of nodes exist
            check_query = """
            MATCH (n)
            RETURN DISTINCT labels(n) as node_types
            """
            check_results = graph.query(check_query)
            logger.debug(f"Available node types: {check_results}")

        return organization_names
    except Exception as e:
        logger.error(f"Error fetching organization names: {str(e)}", exc_info=True)
        return []

# Make sure this line is at the end of your chatbot.py file
__all__ = ['ask_date_question', 'get_all_patient_names', 'get_all_hospital_names', 'refresh_vector_index']

