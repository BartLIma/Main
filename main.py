import streamlit as st

st.set_page_config(layout="wide")

# Inicializa o controle de qual aplicativo exibir na sessão atual
if "app_selecionado" not in st.session_state:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# --- CONSTRUÇÃO DO PAINEL LATERAL DE CONTROLE UNIFICADO ---
st.sidebar.title("🎛️ Painel Monitora")
st.sidebar.markdown("---")

opcoes_menu = [
    "🏠 Menu Inicial", 
    "🔍 Consulta Repasses", 
    "📊 Monitoramento",
    "🩺 Consulta Secretários"  # 👈 Adicione esta linha aqui
]

if st.session_state["app_selecionado"] not in opcoes_menu:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# Seletor do Aplicativo
escolha_app = st.sidebar.radio(
    "Selecione o Sistema:",
    opcoes_menu,
    index=opcoes_menu.index(st.session_state["app_selecionado"])
)

st.session_state["app_selecionado"] = escolha_app
st.sidebar.markdown("---")

# --- EXECUÇÃO DINÂMICA DAS TELAS ---
if st.session_state["app_selecionado"] == "🏠 Menu Inicial":
    st.title("🛡️ Gestão de Dados — Hub Central de Convênios")
    st.subheader("Bem-vindo ao painel integrado de controle e monitoramento de instrumentos.")
    st.markdown("---")
    
    col_cards_1, col_cards_2 = st.columns(2)
    
    with col_cards_1:
        st.info("### 🔍 Consulta Repasses\nPainel completo de análise, auditoria visual e consulta de dados consolidados de convênios a partir da base histórica.")
        if st.button("Abrir Conrepass ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🔍 Consulta Repasses"
            st.rerun()
            
    with col_cards_2:
        st.success("### 📊 Monitoramento\nFormulário de monitoramento em blocos sequenciais com exportação de dados booleanos.")
        if st.button("Abrir Relatório ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "📊 Monitoramento"
            st.rerun()
elif st.session_state["app_selecionado"] == "🔍 Consulta Repasses":
    try:
        # Método nativo: Importa o arquivo exatamente como se estivesse rodando sozinho
        import importlib
        import sys
        
        if "conrepass_app" in sys.modules:
            # Força o recarregamento do arquivo para aceitar mudanças de aba sem travar
            importlib.reload(sys.modules["conrepass_app"])
        else:
            import conrepass_app
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'conrepass_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o aplicativo Conrepass: {e}")

elif st.session_state["app_selecionado"] == "📊 Monitoramento":
    try:
        # Método nativo: Importa o arquivo exatamente como se estivesse rodando sozinho
        import importlib
        import sys
        
        if "rel_acomp_app" in sys.modules:
            # Força o recarregamento do arquivo para aceitar mudanças de aba sem travar
            importlib.reload(sys.modules["rel_acomp_app"])
        else:
            import rel_acomp_app
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'rel_acomp_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error("Ocorreu uma falha ao renderizar o Relatório de Acompanhamento: {e}")
elif st.session_state["app_selecionado"] == "🩺 Consulta Secretários":
    try:
        with open("consulta_secretarios_app.py", "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
        exec(codigo_fonte, globals())
    except FileNotFoundError:
        st.error("Erro: O arquivo 'consulta_secretarios_app.py' não foi localizado.")
    except Exception as e:
        st.error(f"Falha ao renderizar: {e}")

# --- RODAPÉ DISCRETO PADRONIZADO DO HUB ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; color:gray; margin-top:20px;'>"
    "Bartolomeu Lima - Corecon-ES 1541</p>",
    unsafe_allow_html=True
)

