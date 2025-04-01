# ProductSearchAI
Buscas semânticas para e-commerce, integrando componentes como Elasticsearch, LLM e uma interface interativa, Streamlit

---

Aplicação de busca semântica para e-commerce usando Elasticsearch, Kibana, um indexer para produtos,
uma API LLM para vetorização e consulta, e uma interface com Streamlit.

Pré-requisitos:
- Docker
- Docker Compose

Como Executar:
1. Clone o repositório:
   git clone [https://github.com/seuusuario/EcomSemanticSearch.git](https://github.com/kleinlangs/ProductSearchAI.git)
   cd ProductSearchAI

2. Inicie os containers:
   docker compose up --build (ou docker-compose up --build )

Serviços e URLs:
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601
- LLM API: http://localhost:5000
  Endpoints:
    /vectorize – para gerar os embeddings dos produtos
    /query – para consulta semântica
- Streamlit: http://localhost:8501

Fluxo de Uso:
1. O indexer cria o índice "products" e insere 100 produtos.
2. Mande um curl (POST) para http://localhost:5000/vectorize para gerar os vetores dos produtos.
3. Realize consultas semânticas via http://localhost:5000/query ou pela interface do Streamlit.
