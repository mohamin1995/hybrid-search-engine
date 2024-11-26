
from fastapi import FastAPI, Query
from qdrant_client import QdrantClient
from models import SemanticSearchEngine
from fastapi.middleware.cors import CORSMiddleware

#TODO think about filters
#TODO config
#TODO packaging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, replace "*" with specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all HTTP headers
)

qdrant_client = QdrantClient(url='http://localhost:6333')
collection_name = 'products'

sse = SemanticSearchEngine('semantic search engine', qdrant_client, collection_name)




@app.get("/search")
async def search(
    q: str = Query('', title="Query String", description="The search query string"),
    n: int = Query(5, title="Number of Results", description="Number of results to return")
):
    results = sse.search(q, n)
    return results