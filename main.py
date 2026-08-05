import streamlit as st

st.set_page_config(layout="wide")

# Inicializa o controle de qual aplicativo exibir na sessão atual
if "app_selecionado" not in st.session_state:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# --- CONSTRUÇÃO DO PAINEL LATERAL DE CONTROLE UNIFICADO ---
st.sidebar.title("🎛️ Painel Monitora")
st.sidebar.markdown("---")

# Seletor do Aplicativo que gerencia o fluxo de telas
escolha_app = st.sidebar.radio(
    "Selecione o Sistema:",
    [
        "🏠 Menu Inicial",
        "🔍 Consulta Conrepass",
        "📊 Relatório de Acompanhamento"
    ],
    index=["🏠 Menu Inicial", "🔍 Consulta Conrepass", "📊 Relatório de Acompanhamento"].index(st.session_state["app_selecionado"])
)

# Atualiza a memória de navegação caso o usuário altere a opção manual no menu
st.session_state["app_selecionado"] = escolha_app
st.sidebar.markdown("---")

# --- EXECUÇÃO DINÂMICA DAS TELAS ---
if st.session_state["app_selecionado"] == "🏠 Menu Inicial":
    st.title("🛡️ Gestão de Dados — Hub Central de Convênios")
    st.subheader("Bem-vindo ao painel integrado de controle e monitoramento de instrumentos.")
    st.markdown("---")
    
    # Criação de cards visuais modernos para seleção rápida no corpo da página
    col_cards_1, col_cards_2 = st.columns(2)
    
    with col_cards_1:
        st.info("### 🔍 Consulta Conrepass\nPainel completo de análise, auditoria visual e consulta de dados consolidados de convênios a partir da base histórica.")
        if st.button("Abrir Conrepass ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🔍 Consulta Conrepass"
            st.rerun()
            
    with col_cards_2:
        st.success("### 📊 Relatório de Acompanhamento\nFormulário de preenchimento automatizado em 4 blocos sequenciais com exportação de dados booleanos.")
        if st.button("Abrir Relatório ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "📊 Relatório de Acompanhamento"
            st.rerun()
elif st.session_state["app_selecionado"] == "🔍 Consulta Conrepass":
    try:
        # Importa e executa o código do aplicativo Conrepass de forma segura
        import conrepass_app
    except ModuleNotFoundError:
        st.error("Erro operacional: O arquivo 'conrepass_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o aplicativo Conrepass: {e}")

elif st.session_state["app_selecionado"] == "📊 Relatório de Acompanhamento":
    try:
        # Importa e executa o código do aplicativo Rel_Acomp de forma segura
        import relacomp_app
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
