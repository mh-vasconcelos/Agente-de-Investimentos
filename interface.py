# interface.py
import streamlit as st
from rag_agent import aba_qa
from sql_agent import aba_sql

st.set_page_config(page_title="Política de Investimentos", page_icon="imgs/page-icon.png")

def main():
    with st.container(border=False):
        try:
            col_spacer_esq, col_logo = st.columns([2, 2.5], gap="small")
            
            with col_spacer_esq:
                # Alinhado à coluna central-esquerda
                st.image("imgs/logo-iv.png", width=600)
            
            with col_logo:
                # Alinhado à coluna central-direita
                st.image("imgs/banner.png", width=300)

        except:
            # Fallback silencioso ou título texto caso as imagens falhem
            pass

    with st.container(border=True):
        st.title("Política de Investimentos", text_alignment="center")
        st.subheader("Invest Vasconcelos")
        st.markdown("---")
        st.markdown("""
        ### Bem-vindo ao Portal de Compliance
        
        Esta ferramenta foi desenvolvida para apoiar a tomada de decisão e garantir a aderência às normas da **Invest Vasconcelos Asset Management**.
        
        **Funcionalidades do Sistema:**
        * **💬 Assistente de Política (RAG):** Tire dúvidas sobre limites de alocação, *stop-loss*, governança e regras operacionais consultando diretamente a documentação oficial (v4.3).
        * **🗃️ Análise de Mercado (SQL):** Consulte a base histórica de preços (Bitcoin, Ações) para simular cenários e verificar conformidade com as regras de risco.
        
        *Utilize o menu lateral para alternar entre os módulos.*
        """)

        st.markdown("---")
    
    # Menu Lateral (Lazy Loading)
    with st.sidebar:
        st.header("Menu")
        escolha = st.radio("Navegação", ("💬 Perguntas e Respostas", "🗃️ Consultar Base Histórica"))

    # Controle de Exibição das Abas
    if escolha == "💬 Perguntas e Respostas":
        aba_qa()
    elif escolha == "🗃️ Consultar Base Histórica":
        aba_sql()
        
        # st.markdown("""
        # ### Bem-vindo!
        # Tire suas dúvidas sobre a política da empresa e sobre sugestões da consultoria.
        # """)
        # with st.expander("Perguntas e Respostas"):
        #     aba_qa()
        # with st.expander("Consultar Base"):
        #     aba_sql()


if __name__ == "__main__":
    main()