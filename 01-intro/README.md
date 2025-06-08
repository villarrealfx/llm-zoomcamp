## Homework: Introduction

In this homework, we'll learn more about search and use Elastic Search for practice. 

> It's possible that your answers won't match exactly. If it's the case, select the closest one.


## Q1. Running Elastic 

Run Elastic Search 8.17.6, and get the cluster information. If you run it on localhost, this is how you do it:

```bash
curl localhost:9200
```

What's the `version.build_hash` value?

## Answer
`"build_hash" : "dbcbbbd0bc4924cfeb28929dc05d82d662c527b7"`

```bash
curl localhost:9200

{
  "name" : "8ecda94a8498",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "YVhGXINSTB6mxh7Yd8ycEw",
  "version" : {
    "number" : "8.17.6",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "dbcbbbd0bc4924cfeb28929dc05d82d662c527b7",
    "build_date" : "2025-04-30T14:07:12.231372970Z",
    "build_snapshot" : false,
    "lucene_version" : "9.12.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```


## Getting the data

Now let's get the FAQ data. You can run this snippet:

```python
import requests 

docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)
```

Note that you need to have the `requests` library:

```bash
pip install requests
```

## Q2. Indexing the data

Index the data in the same way as was shown in the course videos. Make the `course` field a keyword and the rest should be text. 

Don't forget to install the ElasticSearch client for Python:

```bash
pip install elasticsearch
```

Which function do you use for adding your data to elastic?

* `insert`
* `index`
* `put`
* `add`

## Answer
### `index`
```python
for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)
```

## Q3. Searching

Now let's search in our index. 

We will execute a query "How do execute a command on a Kubernetes pod?". 

Use only `question` and `text` fields and give `question` a boost of 4, and use `"type": "best_fields"`.

What's the score for the top ranking result?

* 84.50
* 64.50
* 44.50
* 24.50

Look at the `_score` field.

## Answer
### `44.50`
For this item, the `search_query` variable was configured as follows:
```python
search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^4", "text"],
                        "type": "best_fields"
                    }
                }
             }
        }
    }
response = es_client.search(index=index_name, body=search_query)
result_docs = []
for hit in response ['hits']['hits']:
    result_docs.append(hit['_score'])
```
`Filter` was removed so that the search would apply to all courses

## Q4. Filtering

Now ask a different question: "How do copy a file to a Docker container?".

This time we are only interested in questions from `machine-learning-zoomcamp`.

Return 3 results. What's the 3rd question returned by the search engine?

* How do I debug a docker container?
* How do I copy files from a different folder into docker container’s working directory?
* How do Lambda container images work?
* How can I annotate a graph?

## Answer
### How do I copy files from a different folder into docker container’s working directory?
For this item, the `search_query` variable was configured as follows:
```python
search_query = {
        "size": 3,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^4", "text"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "machine-learning-zoomcamp"
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body=search_query)
    result_docs = []
    print(response)
    for hit in response ['hits']['hits']:
        result_docs.append(hit['_source']['question'])
```
The `Filter` attribute was placed indicating that the filter will be performed by `machine-learning-zoomcamp`

## Q5. Building a prompt

Now we're ready to build a prompt to send to an LLM. 

Take the records returned from Elasticsearch in Q4 and use this template to build the context. Separate context entries by two linebreaks (`\n\n`)
```python
context_template = """
Q: {question}
A: {text}
""".strip()
```

Now use the context you just created along with the "How do I execute a command in a running docker container?" question 
to construct a prompt using the template below:

```python
prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()
```

What's the length of the resulting prompt? (use the `len` function)

* 946
* 1446
* 1946
* 2446

## Answer
### `1446`
```python
for doc in search_results:
    context = context + f"Q: {doc['question']}\nA: {doc['text']}\n\n"
    
prompt = prompt_template.format(question=query, context=context).strip()
```
```python
query ="How do copy a file to a Docker container?"
sear = elastic_search_mod(query)
prompt_ = build_prompt_mod(query, sear)
len(prompt)
```
`1463`

## Q6. Tokens

When we use the OpenAI Platform, we're charged by the number of 
tokens we send in our prompt and receive in the response.

The OpenAI python package uses `tiktoken` for tokenization:

```bash
pip install tiktoken
```

Let's calculate the number of tokens in our query: 

```python
encoding = tiktoken.encoding_for_model("gpt-4o")
```

Use the `encode` function. How many tokens does our prompt have?

* 120
* 220
* 320
* 420

Note: to decode back a token into a word, you can use the `decode_single_token_bytes` function:

```python
encoding.decode_single_token_bytes(63842)
```
## Answer
### `320`
In my case I am using the LLM Api `DeppSeek-V3` which is not compatible with `tiktoken`, for this case I use `Hugging Face transformers`, with the following implementation:
```bash
pip install transformers
``` 
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-v3")

def count_tokens_deepseek(text: str) -> int:
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return len(tokens)

tokens_prompt = count_tokens_deepseek(prompt_)
tokens_prompt
```
```
output
    333
```

## Bonus: generating the answer (ungraded)

Let's send the prompt to OpenAI. What's the response?  

Note: you can replace OpenAI with Ollama. See module 2.

## Answer
To copy a file to a Docker container, you can use the `docker cp` command with the following syntax:

```bash
docker cp /path/to/local/file_or_directory container_id:/path/in/container
```

For example, if you want to copy a file named `example.txt` from your local machine to a container with ID `abc123` into the `/app` directory inside the container, you would run:  

```bash
docker cp example.txt abc123:/app/
```  

This command works for both files and directories.  

(Source: Hrithik Kumar Advani)