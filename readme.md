
docker run -d --name qdrant -p 6333:6333 -v /Users/mohammad/Desktop/text-to-image-search/qdrant:/qdrant/storage qdrant/qdrant

python data_importer.py  -f data/products_1.json --num=2

uvicorn service:app --reload