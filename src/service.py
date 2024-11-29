
from fastapi import FastAPI, Query
from qdrant_client import QdrantClient
from models.search_engine import *
from fastapi.middleware.cors import CORSMiddleware
from meilisearch import Client
import configparser
import uvicorn
import os

config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

qdrant_client = QdrantClient(url = config[os.getenv('ENV')]['QdrantUrl'])
collection_name = config[os.getenv('ENV')]['CollectionName']

client = Client(config[os.getenv('ENV')]['MeiliUrl'])
index = client.get_index(config[os.getenv('ENV')]['MeiliIndex'])

sse = SemanticSearchEngine('semantic search engine', qdrant_client, collection_name)
kse = KeywordSearchEngine('keyword search engine', index)

hse = HybridSearchEngine('hybrid search engine', sse, kse, 0.7)

@app.get("/search")
async def search(
    q: str = Query('', title="Query String"),
    n: int = Query(20, title="Number of Results"),
    p: float = Query(0.7,title="proportion of semantic results")
):
    hse.semantic_proportion = p
    results = hse.search(q, n)
    
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)