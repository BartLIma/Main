import streamlit as st

st.set_page_config(layout="wide")

# Inicializa o controle de qual aplicativo exibir na sessão atual
if "app_selecionado" not in st.session_state:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# --- CONSTRUÇÃO DO PAINEL LATERAL DE CONTROLE UNIFICADO ---
st.sidebar.title("Gestão de Dados de Convênios")
st.sidebar.markdown("---")

# Lista unificada de opções - Atualizada com o Monitoramento de Obras
opcoes_menu = [
    "🏠 Menu Inicial", 
    "🔍 Consulta Repasses", 
    "📊 Monitoramento",
    "🏥 Consulta Secretários",
    "%s" % "🩺 Consulta Equipamentos",
    "🏗️ Monitoramento de Obras"  # 👈 Novo item incluído aqui
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
    st.markdown("---")
    
    # Primeira linha de cards (Repasses e Monitoramento)
    col_cards_1, col_cards_2 = st.columns(2)
    
    with col_cards_1:
        st.info("### 💵 Consulta Repasses\nPainel completo de análise, auditoria visual e consulta de dados consolidados de convênios a partir da base histórica.")
        if st.button("Abrir Conrepass ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🔍 Consulta Repasses"
            st.rerun()
            
    with col_cards_2:
        st.success("### 📊 Monitoramento\nFormulário de monitoramento em blocos sequenciais com exportação de dados booleanos.")
        if st.button("Abrir Relatório ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "📊 Monitoramento"
            st.rerun()
            
    st.markdown("---")
    
    # Segunda linha de cards (Secretários e Equipamentos)
    col_cards_3, col_cards_4 = st.columns(2)
    
    with col_cards_3:
        st.warning("### 🏥 Consulta Secretários\nPainel de consulta e gerenciamento de informações de secretários municipais e estaduais.")
        if st.button("Abrir Secretários ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🏥 Consulta Secretários"
            st.rerun()

    with col_cards_4:
        st.info("### 🩺 Consulta Equipamentos\nConsulta técnica de equipamentos com classificação automatizada de exigência de Análise Especializada.")
        if st.button("Abrir Equipamentos ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🩺 Consulta Equipamentos"
            st.rerun()

    st.markdown("---")

    # Terceira linha de cards - Dedicada ao novo Monitoramento de Obras SISMOB
    col_cards_5, _ = st.columns(2) # Usa a primeira coluna e deixa a segunda vazia para manter o tamanho
    
    with col_cards_5:
        st.info("### 🏗️ Monitoramento de Obras\nAcompanhamento estratégico de engenharia para obras do Novo PAC e Retomada com foco em pendências no SISMOB.")
        if st.button("Abrir Gestão de Obras ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🏗️ Monitoramento de Obras"
            st.rerun()

elif st.session_state["app_selecionado"] == "🔍 Consulta Repasses":
    try:
        import importlib
        import sys
        if "conrepass_app" in sys.modules:
            importlib.reload(sys.modules["conrepass_app"])
        else:
            import conrepass_app
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'conrepass_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o aplicativo Conrepass: {e}")

elif st.session_state["app_selecionado"] == "📊 Monitoramento":
    try:
        import importlib
        import sys
        if "rel_acomp_app" in sys.modules:
            importlib.reload(sys.modules["rel_acomp_app"])
        else:
            import rel_acomp_app
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'rel_acomp_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o Relatório de Acompanhamento: {e}")

elif st.session_state["app_selecionado"] == "🏥 Consulta Secretários":
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
        exec(codigo_fonte, globals())
    except FileNotFoundError:
        st.error("Erro: O arquivo 'app.py' não foi localizado.")
    except Exception as e:
        st.error(f"Falha ao renderizar: {e}")

elif st.session_state["app_selecionado"] == "🩺 Consulta Equipamentos":
    try:
        import importlib
        import sys
        if "Cons_Equip_app" in sys.modules:
            importlib.reload(sys.modules["Cons_Equip_app"])
        else:
            import Cons_Equip_app
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'Cons_Equip_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar a Consulta de Equipamentos: {e}")

# --- NOVO BLOCO: EXECUÇÃO DO MONITORAMENTO DE OBRAS ---
elif st.session_state["app_selecionado"] == "🏗️ Monitoramento de Obras":
    try:
        import importlib
        import sys
        if "monit_obras" in sys.modules:
            importlib.reload(sys.modules["monit_obras"])
        else:
            import monit_obras
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'monit_obras.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o Monitoramento de Obras: {e}")

# --- RODAPÉ DISCRETO PADRONIZADO DO HUB ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; color:gray; margin-top:20px;'>"
    "Bartolomeu Lima - Corecon-ES 1541</p>",
    unsafe_allow_html=True
)
