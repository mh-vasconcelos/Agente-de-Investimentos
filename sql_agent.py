# from sqlalchemy import create_engine
import streamlit as st
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent # <--- A Mágica está aqui

# Load environment variables
load_dotenv()

@st.cache_resource
def get_agent_engine():
    groq_api_key = os.getenv("GROQ_API_KEY") 
    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    DBNAME = os.getenv("DB_NAME")

    user_enc = quote_plus(USER)
    pw_enc = quote_plus(PASSWORD)

    DATABASE_URL = f"postgresql://{user_enc}:{pw_enc}@{HOST}:{PORT}/{DBNAME}"
    # Se der erro de conexão adicionar ?sslmode=disable ou require no final da URL
    db = SQLDatabase.from_uri(DATABASE_URL)

    # model = ChatGoogleGenerativeAI(
    #     model="gemini-2.5-flash", 
    #     temperature=0
    # )
    
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,api_key= groq_api_key)

    # --- 3. Criação do Agente  ---
    # A função create_sql_agent já cria o Toolkit e injeta o System Prompt de SQL automaticamente
    agent_executor = create_sql_agent(
        llm=model,
        db=db,
        agent_type="zero-shot-react-description", # Funciona melhor com Gemini para chamadas de função
        verbose=True # Mostra o "pensamento" do robô no terminal
    )

    return agent_executor

    # --- 4. Execução ---
def agent_sql(question):
    agent = get_agent_engine()
    print(f"🔎 Perguntando: {question}\n")

    try:
        resultado = agent.invoke({"input": question})
        response_text = resultado['output']
        return response_text
        
    except Exception as e:
        return f"Desculpe, ocorreu um erro ao consultar o banco: {str(e)}"
    
def aba_sql():
    question = st.text_input("O que eu devo consultar no banco de dados?")

    if st.button("Pesquisar", type="primary"):
        if not question:
            st.warning("Por favor, digite uma pergunta.")
        else:
            with st.spinner("Consultando as normas..."):
                try:
                    resposta = agent_sql(question=question)
                    
                    st.success("Resposta Encontrada:")
                    st.write(resposta)
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
