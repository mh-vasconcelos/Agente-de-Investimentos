from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("ERRO: A chave GOOGLE_API_KEY não foi encontrada no arquivo .env")
    exit()




PASTA_BASE = "base"

def criar_db():
    documentos = carregar_documentos()
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

def carregar_documentos():
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf")
    documentos = carregador.load()
    return documentos



def dividir_chunks(documentos):
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=2000, # Tamanho de cada chunk em caracteres que está no documento analisado
        chunk_overlap=500, # Quantos caracteres eu permito que estejam sobrepostos entre os chunks
                           # Evita que informações importantes sejam perdidas na divisão
        length_function=len,
        add_start_index=True
    )
    chunks = separador_documentos.split_documents(documentos)
    print(len(chunks))
    return chunks

google_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY"))
def vetorizar_chunks(chunks):
    db = Chroma.from_documents(
    chunks,
    google_embeddings, # Utiliza o modelo de embeddings do Google 
    persist_directory="db", # Diretório onde o banco de dados será salvo
    collection_metadata={"hnsw:space": "cosine"}
    )
    print("Banco de Dados criado")

criar_db()