import streamlit as st

st.set_page_config(layout="wide")

# Inicializa o controle de qual aplicativo exibir na sessão atual
if "app_selecionado" not in st.session_state:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# --- CONSTRUÇÃO DO PAINEL LATERAL DE CONTROLE UNIFICADO ---
st.sidebar.title("🎛️ Painel Monitora")
st.sidebar.markdown("---")

# Opções oficiais do menu
opcoes_menu = [
    "🏠 Menu Inicial", 
    "🔍 Consulta Repasses", 
    "📊 Monitoramento"
]

# CORREÇÃO: Garante que o index use a lista exata com os novos nomes do menu
if st.session_state["app_selecionado"] not in opcoes_menu:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# Seletor do Aplicativo
escolha_app = st.sidebar.radio(
    "Selecione o Sistema:",
    opcoes_menu,
    index=opcoes_menu.index(st.session_state["app_selecionado"])
)

# Atualiza a memória de navegação
st.session_state["app_selecionado"] = escolha_app
st.sidebar.markdown("---")

# --- EXECUÇÃO DINÂMICA DAS TELAS ---
if st.session_state["app_selecionado"] == "🏠 Menu Inicial":
    st.title("🛡️ Gestão de Dados — Hub Central de Convênios")
    st.subheader("Bem-vindo ao painel integrado de controle e monitoramento de instrumentos.")
    st.markdown("---")
    
    # Criação de cards visuais modernos para seleção rápida
    col_cards_1, col_cards_2 = st.columns(2)
    
    with col_cards_1:
        st.info("### 🔍 Consulta Repasses\nPainel completo de análise, auditoria visual e consulta de dados consolidados de convênios a partir da base histórica.")
        if st.button("Abrir Conrepass ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🔍 Consulta Repasses" # NOVO NOME
            st.rerun()
            
    with col_cards_2:
        st.success("### 📊 Monitoramento\nFormulário de monitoramento em blocos sequenciais com exportação de dados booleanos.")
        if st.button("Abrir Relatório ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "📊 Monitoramento" # NOVO NOME
            st.rerun()
elif st.session_state["app_selecionado"] == "🔍 Consulta Repasses":
    try:
        # Importa e executa o código do aplicativo Conrepass de forma segura
        import conrepass_app
    except ModuleNotFoundError:
        st.error("Erro operacional: O arquivo 'conrepass_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o aplicativo Conrepass: {e}")

elif st.session_state["app_selecionado"] == "📊 Monitoramento":
    try:
        # CORREÇÃO: Ajustado de relacomp_app para o nome correto 'rel_acomp_app'
        import rel_acomp_app
    except ModuleNotFoundError:
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
