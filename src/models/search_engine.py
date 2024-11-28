
from abc import ABC, abstractmethod
import torch
from transformers import CLIPProcessor, CLIPModel
import torch
from loguru import logger as log



class ClipEmbeddingModel:
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
    def get_embedding(self, q : str):
        
        inputs = self.clip_processor(text=q, return_tensors="pt").to(self.device)
        with torch.no_grad():
            query_embedding = self.clip_model.get_text_features(**inputs)
            query_embedding = query_embedding.cpu().numpy().flatten()
        
        return query_embedding
        
        

class SearchEngine(ABC):
    
    def __init__(self,name):
        self.name = name
    
    @abstractmethod
    def search(self,q,k):
        pass



class SemanticSearchEngine(SearchEngine):
    
    def __init__(self, name, qdrant_client, collection_name):
        super().__init__(name)
        self.embedding_model = ClipEmbeddingModel()
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name
        
        
    
    def search(self, q, k):
        
        query_embedding = self.embedding_model.get_embedding(q)
        search_results = self.qdrant_client.search(
        collection_name=self.collection_name,
        query_vector=query_embedding.tolist(),
        limit=100,
        with_payload=True,
    )
        results = {}
        for search_result in search_results:
            if not search_result.payload["id"] in results:
                results[search_result.payload["id"]] = search_result.payload
            
            if len(results) >= k:
                break
             
        
        return list(results.values())
        

class KeywordSearchEngine(SearchEngine):
    
    def __init__(self, name, index):
        super().__init__(name)
        self.index = index
        
    
    def search(self, q, k):
        search_results = self.index.search(q)
        print('im hereeeeeeeeeeeeeeeeeee')
        return search_results['hits'][0:k]        








        

