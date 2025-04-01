from elasticsearch import Elasticsearch
import random
import time
import sys

def wait_for_elasticsearch(host, timeout=60):
    es = Elasticsearch(hosts=[host])
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if es.ping():
                print("Elasticsearch está disponível!")
                return True
        except Exception as e:
            pass
        print("Aguardando Elasticsearch...")
        time.sleep(2)
    return False

# Aguarda o Elasticsearch estar disponível
if not wait_for_elasticsearch("http://elasticsearch:9200", timeout=60):
    print("Elasticsearch não está disponível após 60 segundos. Abortando.")
    sys.exit(1)

es = Elasticsearch(hosts=["http://elasticsearch:9200"])
index_name = "products"

# Se o índice já existir, deleta para recriar
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Criação do índice com mapping (lembre-se de ajustar as dimensões do vetor conforme o modelo)
mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "description": {"type": "text"},
            "price": {"type": "float"},
            "vector": {"type": "dense_vector", "dims": 384}  # Ajuste para 384 dimensões, conforme o modelo all-MiniLM-L6-v2
        }
    }
}
es.indices.create(index=index_name, body=mapping)

# Lista de produtos realistas
products_base = [
    {
        "name": "Apple iPhone 13",
        "description": "Smartphone com tela de 6.1 polegadas, chip A15 Bionic e sistema de câmera avançado.",
        "price": 799.99
    },
    {
        "name": "Samsung Galaxy S21",
        "description": "Smartphone com display Dynamic AMOLED 2X de 6.2 polegadas, excelente para multitarefas.",
        "price": 699.99
    },
    {
        "name": "Dell XPS 15",
        "description": "Laptop com performance robusta, tela de 15.6 polegadas e design premium.",
        "price": 1299.99
    },
    {
        "name": "Sony WH-1000XM4",
        "description": "Fones de ouvido com cancelamento de ruído líder de mercado, conforto e qualidade de som excepcional.",
        "price": 349.99
    },
    {
        "name": "LG 55\" OLED TV",
        "description": "Televisor OLED 4K com cores vibrantes e contraste impressionante, ideal para home theater.",
        "price": 1199.99
    },
    {
        "name": "Bose SoundLink Revolve+",
        "description": "Caixa de som portátil com som 360° e bateria de longa duração.",
        "price": 299.99
    },
    {
        "name": "Canon EOS R6",
        "description": "Câmera mirrorless com alta performance em baixa luminosidade e gravação em 4K.",
        "price": 2499.99
    },
    {
        "name": "HP Envy 6055",
        "description": "Impressora multifuncional com conexão wireless e design compacto.",
        "price": 199.99
    },
    {
        "name": "Amazon Echo Dot (4ª Geração)",
        "description": "Smart speaker com assistente Alexa integrado, design compacto.",
        "price": 49.99
    },
    {
        "name": "Fitbit Charge 5",
        "description": "Rastreador de atividades com monitoramento avançado de saúde e sono.",
        "price": 149.99
    },
]

# Insere 100 produtos, escolhendo aleatoriamente da lista base e gerando pequenas variações
for i in range(100):
    product = random.choice(products_base).copy()
    # Adiciona uma variação no nome para identificar registros distintos
    product["name"] += f" - Variante {i}"
    # Aplica uma variação aleatória no preço (±5%)
    product["price"] = round(product["price"] * random.uniform(0.95, 1.05), 2)
    es.index(index=index_name, document=product)

print("Índice 'products' criado com 100 produtos realistas.")

