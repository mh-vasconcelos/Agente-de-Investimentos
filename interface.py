# interface.py
import streamlit as st
from rag_agent import aba_qa
from sql_agent import aba_sql

# --- CONFIGURAÇÃO DE PÁGINA ---
st.set_page_config(
    page_title="Portal de Compliance | Invest Vasconcelos",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
        /* Cores da Marca */
        :root {
            --primary-color: #C5A059; /* Dourado */
            --secondary-color: #0A1E3C; /* Azul Marinho Profundo */
            --background-light: #F8F9FA; /* Off-white para o fundo */
        }
        
        /* Ajusta a cor de fundo principal */
        .stApp {
            background-color: var(--background-light);
        }

        /* Estiliza os títulos principais (H1, H2) com a cor da marca */
        h1, h2, h3 {
            color: var(--secondary-color) !important;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        h1 { font-weight: 800; letter-spacing: -1px; }
        h2 { font-weight: 600; }
        
        /* Destaques em dourado */
        .highlight-gold {
            color: var(--primary-color);
            font-weight: bold;
        }

        /* Estilo para os Cards de Funcionalidade */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #eee;
            transition: transform 0.2s;
        }
        /* Efeito hover sutil nos cards */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.1);
            border-color: var(--primary-color);
        }
        
        /* Ajuste fino na sidebar */
        section[data-testid="stSidebar"] {
            background-color: #f0f2f6;
            border-right: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)


# --- FUNÇÃO PRINCIPAL ---
def main():
    # --- SIDEBAR DE NAVEGAÇÃO ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #0A1E3C;'>Navegação</h2>", unsafe_allow_html=True)
        st.write("---")
        
        escolha = st.radio(
            "Selecione o Módulo:",
            ["🏠 Home", "💬 Assistente de Política (RAG)", "🗃️ Análise de Mercado (SQL)"],
            index=0, # Começa na Home
            label_visibility="collapsed"
        )
        
        st.write("---")
        st.caption("🔒 Ambiente Seguro | v4.3")
        st.caption("© 2024 Invest Vasconcelos Asset Management")


    # --- LÓGICA DE EXIBIÇÃO ---
    if escolha == "🏠 Home":
        # --- CABEÇALHO DA HOME ---
        col_logo_header, col_title_header = st.columns([1, 3])
        with col_logo_header:
            try:
                st.image("imgs/logo-iv.png", width=220)
            except:
                st.markdown("### 🏛️ INVEST VASCONCELOS")

        with col_title_header:
            st.title("Portal de Compliance e Inteligência")
            st.markdown("#### <span class='highlight-gold'>Invest Vasconcelos Asset Management</span>", unsafe_allow_html=True)
        
        st.write("---")

        # --- INTRODUÇÃO E CONTEXTO ---
        col_intro_text, col_intro_stat = st.columns([3, 1])
        
        with col_intro_text:
            st.subheader("Bem-vindo ao Sistema de Apoio à Decisão")
            st.write("""
            Esta ferramenta foi desenvolvida para centralizar a inteligência corporativa e garantir 
            a aderência rigorosa às normas da instituição. Nossa missão é fornecer acesso rápido e 
            confiável a dados estratégicos, unindo **políticas internas** e **dados de mercado** em uma única interface.
            """)
            st.info("💡 Dica: Utilize o menu lateral para navegar entre os módulos especializados.")

        with col_intro_stat:
            with st.container(border=True):
                st.metric(label="Status da Política de Investimentos", value="Ativo", delta="Versão 4.3 Vigente")


        st.write("") # Espaçamento
        st.subheader("Módulos do Sistema")
        st.write("") # Espaçamento

        # --- CARDS DE FUNCIONALIDADES ---
        # Substitui a lista de bullets por cards visuais lado a lado
        col_card_rag, col_card_sql = st.columns(2, gap="medium")

        with col_card_rag:
            # O CSS personalizado estiliza este container automaticamente
            with st.container():
                st.markdown("### 🤖 Assistente de Política Interna (RAG)")
                st.write("---")
                st.write("""
                Consulte diretamente a documentação oficial de compliance e governança.
                Ideal para tirar dúvidas sobre:
                """)
                # Ícones pequenos para facilitar a leitura rápida
                st.markdown("""
                * 🛡️ Limites de Alocação e Risco
                * 📜 Regras de *Stop-Loss* e Desenquadramento
                * ⚖️ Governança e Processos Operacionais
                """)
                st.markdown("<br>**Fonte:** Documentação v4.3 (PDFs indexados)", unsafe_allow_html=True)

        with col_card_sql:
            with st.container():
                st.markdown("### 🗃️ Análise de Dados de Mercado (SQL Agent)")
                st.write("---")
                st.write("""
                Acesse a base de dados histórica para realizar análises quantitativas.
                Ideal para verificar:
                """)
                 # Ícones pequenos para facilitar a leitura rápida
                st.markdown("""
                * 📈 Histórico de Preços (Bitcoin, Ativos)
                * 📉 Simulação de Cenários de Volatilidade
                * 📊 Verificação de Conformidade com Regras de Risco
                """)
                st.markdown("<br>**Fonte:** Banco de Dados Estruturado (PostgreSQL)", unsafe_allow_html=True)

    # --- PÁGINAS DOS AGENTES ---
    # O layout limpo dessas páginas depende da implementação dentro de rag_agent.py e sql_agent.py
    elif escolha == "💬 Assistente de Política (RAG)":
        st.title("💬 Assistente de Política de Investimentos")
        st.caption("Pergunte diretamente aos documentos oficiais da Invest Vasconcelos.")
        st.write("---")
        aba_qa() # Chama sua função existente
        
    elif escolha == "🗃️ Análise de Mercado (SQL)":
        st.title("🗃️ Análise Quantitativa de Mercado")
        st.caption("Agente autônomo para consulta de dados históricos estruturados.")
        st.write("---")
        aba_sql() # Chama sua função existente

if __name__ == "__main__":
    main()