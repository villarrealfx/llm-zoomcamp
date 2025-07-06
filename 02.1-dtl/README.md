# Homework

## Question 1. dlt Version

In this homework, we will load the data from our FAQ to Qdrant

Let's install dlt with Qdrant support and Qdrant client:

```bash
pip install -q "dlt[qdrant]" "qdrant-client[fastembed]"
```

What's the version of dlt that you installed?

## Answer: '1.12.3'

```python
import dlt
dlt.__version__
```
```
'1.12.3'
```
terminal:

```bash
❯ dlt --version
dlt 1.12.3
```

## dlt Resourse

For reading the FAQ data, we have this helper function:

```python
def zoomcamp_data():
    docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
    docs_response = requests.get(docs_url)
    documents_raw = docs_response.json()

    for course in documents_raw:
        course_name = course['course']

        for doc in course['documents']:
            doc['course'] = course_name
            yield doc
```

Annotate it with `@dlt.resource`. We will use it when creating
a dlt pipeline.

## Question 2. dlt pipeline

Now let's create a pipeline. 

We need to define a destination for that. Let's use the `qdrant` one:

```python
from dlt.destinations import qdrant

qdrant_destination = qdrant(
  qd_path="db.qdrant", 
)
```

In this case, we tell dlt (and Qdrant) to create a folder with
our data, and the name for it will be `db.qdrant`

Let's run it:

```python
pipeline = dlt.pipeline(
    pipeline_name="zoomcamp_pipeline",
    destination=qdrant_destination,
    dataset_name="zoomcamp_tagged_data"

)
load_info = pipeline.run(zoomcamp_data())
print(pipeline.last_trace)
```

How many rows were inserted into the `zoomcamp_data` collection?

Look for `"Normalized data for the following tables:"` in the trace output.

## Answer: 948 rows

```
Normalized data for the following tables:
- _dlt_pipeline_state: 1 row(s)
- zoomcamp_data: 948 row(s)
```
## Question 3. Embeddings

When inserting the data, an embedding model was used. Which one?

You can find this out by inspecting the `meta.json` file created
in the target folder.

## Answer: "fast-bge-small-en"

```json
{
   "collections":{
      "zoomcamp_tagged_data":{
         "vectors":{
            "fast-bge-small-en":{
               "size":384,
               "distance":"Cosine",
               "hnsw_config":null,
               "quantization_config":null,
               "on_disk":null,
               "datatype":null,
               "multivector_config":null
            }
         },
         "shard_number":null,
         "sharding_method":null,
         "replication_factor":null,
         "write_consistency_factor":null,
         "on_disk_payload":null,
         "hnsw_config":null,
         "wal_config":null,
         "optimizers_config":null,
         "init_from":null,
         "quantization_config":null,
         "sparse_vectors":null,
         "strict_mode_config":null
      },
      "zoomcamp_tagged_data_zoomcamp_data":{
         "vectors":{
            "fast-bge-small-en":{
               "size":384,
               "distance":"Cosine",
               "hnsw_config":null,
               "quantization_config":null,
               "on_disk":null,
               "datatype":null,
               "multivector_config":null
            }
         },
         "shard_number":null,
         "sharding_method":null,
         "replication_factor":null,
         "write_consistency_factor":null,
         "on_disk_payload":null,
         "hnsw_config":null,
         "wal_config":null,
         "optimizers_config":null,
         "init_from":null,
         "quantization_config":null,
         "sparse_vectors":null,
         "strict_mode_config":null
      },
      "zoomcamp_tagged_data__dlt_pipeline_state":{
         "vectors":{
            "fast-bge-small-en":{
               "size":384,
               "distance":"Cosine",
               "hnsw_config":null,
               "quantization_config":null,
               "on_disk":null,
               "datatype":null,
               "multivector_config":null
            }
         },
         "shard_number":null,
         "sharding_method":null,
         "replication_factor":null,
         "write_consistency_factor":null,
         "on_disk_payload":null,
         "hnsw_config":null,
         "wal_config":null,
         "optimizers_config":null,
         "init_from":null,
         "quantization_config":null,
         "sparse_vectors":null,
         "strict_mode_config":null
      },
      "zoomcamp_tagged_data__dlt_loads":{
         "vectors":{
            "fast-bge-small-en":{
               "size":384,
               "distance":"Cosine",
               "hnsw_config":null,
               "quantization_config":null,
               "on_disk":null,
               "datatype":null,
               "multivector_config":null
            }
         },
         "shard_number":null,
         "sharding_method":null,
         "replication_factor":null,
         "write_consistency_factor":null,
         "on_disk_payload":null,
         "hnsw_config":null,
         "wal_config":null,
         "optimizers_config":null,
         "init_from":null,
         "quantization_config":null,
         "sparse_vectors":null,
         "strict_mode_config":null
      },
      "zoomcamp_tagged_data__dlt_version":{
         "vectors":{
            "fast-bge-small-en":{
               "size":384,
               "distance":"Cosine",
               "hnsw_config":null,
               "quantization_config":null,
               "on_disk":null,
               "datatype":null,
               "multivector_config":null
            }
         },
         "shard_number":null,
         "sharding_method":null,
         "replication_factor":null,
         "write_consistency_factor":null,
         "on_disk_payload":null,
         "hnsw_config":null,
         "wal_config":null,
         "optimizers_config":null,
         "init_from":null,
         "quantization_config":null,
         "sparse_vectors":null,
         "strict_mode_config":null
      }
   },
   "aliases":{
      
   }
}
```

## Submit the results

* Submit your results here: https://courses.datatalks.club/llm-zoomcamp-2025/homework/dlt