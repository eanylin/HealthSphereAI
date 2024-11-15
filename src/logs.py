/app/src/chatbot.py:12: LangChainDeprecationWarning: Importing Neo4jGraph from langchain.graphs is deprecated. Please replace deprecated imports:

>> from langchain.graphs import Neo4jGraph

with new imports of:

>> from langchain_community.graphs import Neo4jGraph
You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
  from langchain.graphs import Neo4jGraph
/app/src/chatbot.py:13: LangChainDeprecationWarning: Importing Neo4jVector from langchain.vectorstores is deprecated. Please replace deprecated imports:

>> from langchain.vectorstores import Neo4jVector

with new imports of:

>> from langchain_community.vectorstores import Neo4jVector
You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
  from langchain.vectorstores.neo4j_vector import Neo4jVector
/app/src/chatbot.py:14: LangChainDeprecationWarning: Importing HuggingFaceBgeEmbeddings from langchain.embeddings is deprecated. Please replace deprecated imports:

>> from langchain.embeddings import HuggingFaceBgeEmbeddings

with new imports of:

>> from langchain_community.embeddings import HuggingFaceBgeEmbeddings
You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
  from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
/opt/app-root/lib64/python3.11/site-packages/langchain/chat_models/__init__.py:33: LangChainDeprecationWarning: Importing chat models from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:

`from langchain_community.chat_models import ChatOllama`.

To install langchain-community run `pip install -U langchain-community`.
  warnings.warn(
/opt/app-root/lib64/python3.11/site-packages/langchain/__init__.py:30: UserWarning: Importing PromptTemplate from langchain root module is no longer supported. Please use langchain_core.prompts.PromptTemplate instead.
  warnings.warn(
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownLabelWarning} {category: UNRECOGNIZED} {title: The provided label is not in the database.} {description: One of the labels in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing label name is: resource)} {position: line: 2, column: 22, offset: 22} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownPropertyKeyWarning} {category: UNRECOGNIZED} {title: The provided property key is not in the database} {description: One of the property names in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing property name is: resource_type)} {position: line: 3, column: 29, offset: 61} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownLabelWarning} {category: UNRECOGNIZED} {title: The provided label is not in the database.} {description: One of the labels in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing label name is: resource)} {position: line: 6, column: 22, offset: 206} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownPropertyKeyWarning} {category: UNRECOGNIZED} {title: The provided property key is not in the database} {description: One of the property names in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing property name is: resource_type)} {position: line: 7, column: 21, offset: 236} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
[]
(0, 0)
 * Serving Flask app 'app'
 * Debug mode: on
INFO:werkzeug:[31m[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.[0m
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.128.1.193:5000
INFO:werkzeug:[33mPress CTRL+C to quit[0m
INFO:werkzeug: * Restarting with stat
/app/src/chatbot.py:12: LangChainDeprecationWarning: Importing Neo4jGraph from langchain.graphs is deprecated. Please replace deprecated imports:

>> from langchain.graphs import Neo4jGraph

with new imports of:

>> from langchain_community.graphs import Neo4jGraph
You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
  from langchain.graphs import Neo4jGraph
/app/src/chatbot.py:13: LangChainDeprecationWarning: Importing Neo4jVector from langchain.vectorstores is deprecated. Please replace deprecated imports:

>> from langchain.vectorstores import Neo4jVector

with new imports of:

>> from langchain_community.vectorstores import Neo4jVector
You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
  from langchain.vectorstores.neo4j_vector import Neo4jVector
/app/src/chatbot.py:14: LangChainDeprecationWarning: Importing HuggingFaceBgeEmbeddings from langchain.embeddings is deprecated. Please replace deprecated imports:

>> from langchain.embeddings import HuggingFaceBgeEmbeddings

with new imports of:

>> from langchain_community.embeddings import HuggingFaceBgeEmbeddings
You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
  from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
/opt/app-root/lib64/python3.11/site-packages/langchain/chat_models/__init__.py:33: LangChainDeprecationWarning: Importing chat models from langchain is deprecated. Importing from langchain will no longer be supported as of langchain==0.2.0. Please import from langchain-community instead:

`from langchain_community.chat_models import ChatOllama`.

To install langchain-community run `pip install -U langchain-community`.
  warnings.warn(
/opt/app-root/lib64/python3.11/site-packages/langchain/__init__.py:30: UserWarning: Importing PromptTemplate from langchain root module is no longer supported. Please use langchain_core.prompts.PromptTemplate instead.
  warnings.warn(
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownLabelWarning} {category: UNRECOGNIZED} {title: The provided label is not in the database.} {description: One of the labels in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing label name is: resource)} {position: line: 2, column: 22, offset: 22} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownPropertyKeyWarning} {category: UNRECOGNIZED} {title: The provided property key is not in the database} {description: One of the property names in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing property name is: resource_type)} {position: line: 3, column: 29, offset: 61} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownLabelWarning} {category: UNRECOGNIZED} {title: The provided label is not in the database.} {description: One of the labels in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing label name is: resource)} {position: line: 6, column: 22, offset: 206} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownPropertyKeyWarning} {category: UNRECOGNIZED} {title: The provided property key is not in the database} {description: One of the property names in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing property name is: resource_type)} {position: line: 7, column: 21, offset: 236} for query: '\n            MATCH (r:resource) \n            WITH DISTINCT(r.resource_type) AS resource_types\n                ORDER BY resource_types\n            UNWIND resource_types as resource_type\n            MATCH (r:resource)\n            WHERE r.resource_type = resource_type\n            WITH resource_type, COUNT(r) as resource_count\n            RETURN resource_type, resource_count\n                ORDER BY resource_count\n        '
[]
(0, 0)
WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: 121-796-639
