
from fastapi import FastAPI, Query
from qdrant_client import QdrantClient
from models.search_engine import SemanticSearchEngine
from fastapi.middleware.cors import CORSMiddleware
import configparser
import uvicorn

#TODO deployment
#TODO keyword search
#TODO think about filters

config = configparser.ConfigParser()
config.read('config.ini')



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

qdrant_client = QdrantClient(url = config['production']['QdrantUrl'])
collection_name = config['production']['CollectionName']

sse = SemanticSearchEngine('semantic search engine', qdrant_client, collection_name)




@app.get("/search")
async def search(
    q: str = Query('', title="Query String", description="The search query string"),
    n: int = Query(5, title="Number of Results", description="Number of results to return")
):
    results = sse.search(q, n)
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)