from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

CAMINHO_DB = "db"
prompt_template = """
Responda a pergunta do usuário:
{pergunta} 

com base nessas informações abaixo:

{base_conhecimento}
"""
@st.cache_resource
def perguntar(pergunta: str) -> str:

    chave_api_google = os.getenv("GOOGLE_API_KEY") 
    chave_api_groq = os.getenv("GROQ_API_KEY") 
    
    google_embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=chave_api_google
    )
    
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=google_embeddings)

    # comparar a pergunta
    resultados = db.similarity_search_with_relevance_scores(query=pergunta, k=3)
    
    if len(resultados) == 0 or resultados[0][1] < 0.1:
        print("Desculpe, não sei a resposta para isso")
        return
      
    textos_resultado = []
    for resultado in resultados:
        texto = resultado[0].page_content
        textos_resultado.append(texto)
  
    base_conhecimento = "\n\n----\n\n".join(textos_resultado)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    chain = prompt | ChatGroq(
        model="llama-3.3-70b-versatile", 
        api_key=chave_api_groq
    )

    response = chain.invoke({"pergunta": pergunta, "base_conhecimento": base_conhecimento})
  
    return response.content

def aba_qa():
    pergunta = st.text_input("Qual a sua dúvida?")

    if st.button("Pesquisar Resposta", type="primary"):
        if not pergunta:
            st.warning("Por favor, digite uma pergunta.")
        else:
            with st.spinner("Consultando as normas..."):
                try:
                    resposta = perguntar(pergunta)
                    
                    st.success("Resposta Encontrada:")
                    st.write(resposta)
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")



