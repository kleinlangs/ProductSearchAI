from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import time

# Aguarda o Elasticsearch estar pronto
time.sleep(10)

app = Flask(__name__)
es = Elasticsearch(hosts=["http://elasticsearch:9200"])
model = SentenceTransformer('all-MiniLM-L6-v2')
index_name = "products"

# Endpoint para vectorizar e atualizar documentos sem vetor
@app.route("/vectorize", methods=["POST"])
def vectorize_products():
    # Busca todos os produtos que não possuem o campo "vector"
    query = {
        "query": {
            "bool": {
                "must_not": {
                    "exists": {
                        "field": "vector"
                    }
                }
            }
        }
    }
    res = es.search(index=index_name, body=query, size=1000)
    products = res['hits']['hits']

    for prod in products:
        prod_id = prod['_id']
        doc = prod['_source']
        text = f"{doc.get('name', '')}. {doc.get('description', '')}"
        vector = model.encode(text).tolist()
        es.update(index=index_name, id=prod_id, body={"doc": {"vector": vector}})
    return jsonify({"message": "Vectorização concluída para os produtos."})

# Endpoint para consulta semântica
@app.route("/query", methods=["POST"])
def query():
    data = request.json
    if not data or "query" not in data:
        return jsonify({"error": "Parâmetro 'query' ausente."}), 400

    query_text = data["query"]
    query_vector = model.encode(query_text).tolist()

    # Consulta utilizando cosine similarity via script_score
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    response = es.search(index=index_name, body={"query": script_query})
    results = [
        {"id": hit["_id"], "score": hit["_score"], "product": hit["_source"]}
        for hit in response["hits"]["hits"]
    ]
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

