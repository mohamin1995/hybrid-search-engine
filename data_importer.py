import json
import requests
from io import BytesIO
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import uuid
import argparse
from loguru import logger as log


#docker run -d --name qdrant -p 6333:6333 -v /Users/mohammad/Desktop/text-to-image-search/qdrant:/qdrant/storage qdrant/qdrant
#python data_importer.py  -f products_1.json --num=10

# def search_query(query_text, top_k=1):

#     inputs = clip_processor(text=query_text, return_tensors="pt").to(device)
#     with torch.no_grad():
#         query_embedding = clip_model.get_text_features(**inputs)
#         query_embedding = query_embedding.cpu().numpy().flatten()
    
#     results = qdrant_client.search(
#         collection_name=collection_name,
#         query_vector=query_embedding.tolist(),
#         limit=top_k,
#         with_payload=True,
#     )
#     return results

# query = "Designed with a flattering V-neck and a midi length, this dress is perfect for any occasion. The tier detail adds a touch of sophistication, while the delicate lace trim detail adds a feminine charm"
# search_results = search_query(query)
# for result in search_results:
#     print(f"Product ID: {result.payload['name']}, Score: {result.score}")


def import_data(args):
    qdrant_client = QdrantClient(url=args.durl)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    collection_name = args.cname

    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE),
    )

    with open(args.file) as f:
        products = json.load(f)
        
    for product in products[0:args.num]:
        embeddings = []
        for image_url in product['images']:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content)).convert("RGB")
            
            inputs = clip_processor(images=img, return_tensors="pt").to(device)
            with torch.no_grad():
                embedding = clip_model.get_image_features(**inputs)
                embedding = embedding.cpu().numpy().flatten()
                embeddings.append(embedding)
                
        
        points = [
            PointStruct(
                id=uuid.uuid4().__str__(), 
                vector=embedding.tolist(),
                payload={"product_id": str(product['id']), **product},
            )
            for embedding in embeddings
        ]
        qdrant_client.upsert(collection_name=collection_name, points=points)
        log.info('embedding of product {} added to qdrant successfully',str(product['id']))
        
    

if __name__=='__main__':
    
    parser=argparse.ArgumentParser(description="It's a module to import data from a json to qdrant vector database")
     
    parser.add_argument('-d',
                        '--durl',
                        help="qdrant url",
                        type=str,default='http://localhost:6333') 
 
    parser.add_argument('-c',
                        '--cname',
                        help="collection name in qdrant",
                        type=str,default='products')
 
    parser.add_argument('-f',
                        '--file',
                        help="data file (json)",
                        type=str,required=True)
    
    
    parser.add_argument('-n',
                        '--num',
                        help="number of products to add",
                        type=int,default=100)
    
    try:
        args=parser.parse_args()
        import_data(args)
    except Exception as e:
        log.error(str(e))

    