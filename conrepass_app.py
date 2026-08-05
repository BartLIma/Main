import streamlit as st

st.set_page_config(layout="wide")

# --- TRUQUE CSS: Enxuga o espaço em branco do topo da tela e da barra lateral ---
st.markdown(
    """
    <style>
        /* Reduz o recuo superior do conteúdo principal */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }
        /* Reduz o recuo superior do menu lateral */
        [data-testid="stSidebarUserContent"] {
            padding-top: 1.5rem !important;
        }
        /* Ajusta o espaçamento dos títulos */
        h1 {
            margin-top: -1rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializa o controle de qual aplicativo exibir na sessão atual se não existir
if "app_selecionado" not in st.session_state:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# Funções Callback (Garantem que a troca de tela aconteça em apenas 1 clique)
def ir_para_conrepass():
    st.session_state["app_selecionado"] = "🔍 Consulta Repasses"

def ir_para_monitoramento():
    st.session_state["app_selecionado"] = "📊 Monitoramento"

# --- CONSTRUÇÃO DO PAINEL LATERAL DE CONTROLE UNIFICADO ---
st.sidebar.title("🎛️ Painel Monitora")
st.sidebar.markdown("---")

opcoes_menu = [
    "🏠 Menu Inicial", 
    "🔍 Consulta Repasses", 
    "📊 Monitoramento"
]

# Seletor do Aplicativo amarrado nativamente ao session_state via key
escolha_app = st.sidebar.radio(
    "Selecione o Sistema:",
    opcoes_menu,
    key="app_selecionado" # Amarração nativa direta elimina a necessidade de index manual
)

st.sidebar.markdown("---")

# --- EXECUÇÃO DINÂMICA DAS TELAS ---
if st.session_state["app_selecionado"] == "🏠 Menu Inicial":
    st.title("🛡️ Gestão de Dados — Hub Central de Convênios")
    st.subheader("Bem-vindo ao painel integrado de controle e monitoramento de instrumentos.")
    st.markdown("---")
    
    col_cards_1, col_cards_2 = st.columns(2)
    
    with col_cards_1:
        st.info("### 🔍 Consulta Repasses\nPainel completo de análise, auditoria visual e consulta de dados consolidados de convênios a partir da base histórica.")
        # Correção: O clique ativa o callback e muda de tela na hora
        st.button("Abrir Conrepass ➡️", use_container_width=True, on_click=ir_para_conrepass)
            
    with col_cards_2:
        st.success("### 📊 Monitoramento\nFormulário de monitoramento em blocos sequenciais com exportação de dados booleanos.")
        # Correção: O clique ativa o callback e muda de tela na hora
        st.button("Abrir Relatório ➡️", use_container_width=True, on_click=ir_para_monitoramento)
elif st.session_state["app_selecionado"] == "🔍 Consulta Repasses":
    try:
        with open("conrepass_app.py", "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
        exec(codigo_fonte, globals())
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'conrepass_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o aplicativo Conrepass: {e}")

elif st.session_state["app_selecionado"] == "📊 Monitoramento":
    try:
        with open("rel_acomp_app.py", "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
        exec(codigo_fonte, globals())
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'rel_acomp_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o Relatório de Acompanhamento: {e}")

# --- RODAPÉ DISCRETO PADRONIZADO DO HUB ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; color:gray; margin-top:20px;'>"
    "Bartolomeu Lima - Corecon-ES 1541</p>",
    unsafe_allow_html=True
)
