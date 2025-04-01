import streamlit as st
import requests

st.title("Busca Semântica de Produtos")
st.write("Simulação de API de busca para um e-commerce.")

query = st.text_input("Digite sua consulta:")

if st.button("Buscar") and query:
    try:
        # Chama o endpoint de consulta da API LLM
        response = requests.post("http://llm:5000/query", json={"query": query})
        if response.status_code == 200:
            results = response.json()
            if results:
                st.write("### Resultados:")
                for res in results:
                    product = res.get("product", {})
                    st.write(f"**{product.get('name', 'Sem nome')}**")
                    st.write(f"Preço: R$ {product.get('price')}")
                    st.write(f"Descrição: {product.get('description')}")
                    st.write(f"Score: {res.get('score'):.2f}")
                    st.markdown("---")
            else:
                st.write("Nenhum resultado encontrado.")
        else:
            st.error("Erro na consulta: " + response.text)
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")

