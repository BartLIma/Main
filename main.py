import streamlit as st

st.set_page_config(layout="wide")

# Inicializa o controle de qual aplicativo exibir na sessão atual
if "app_selecionado" not in st.session_state:
    st.session_state["app_selecionado"] = "🏠 Menu Inicial"

# --- CONSTRUÇÃO DO PAINEL LATERAL DE CONTROLE UNIFICADO ---
st.sidebar.title("Gestão de Dados de Transferências")
st.sidebar.markdown("---")

# Lista unificada de opções - Atualizada com Cadastro de Obras e Dados Municípios PB
opcoes_menu = [
    "🏠 Menu Inicial", 
    "🔍 Consulta Repasses", 
    "📊 Monitoramento",
    "🏥 Consulta Secretários",
    "%s" % "🩺 Consulta Equipamentos",
    "🏗️ Monitoramento de Obras",
    "📝 Cadastro de Obras",  # 👈 Novo item incluído aqui
    "🏛️ Emendas Parlamentares",
    "🌴 Dados Municípios PB"
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
        st.success("### 📊 Monitoramento\nFormulário de monitoramento de convênios em blocos sequenciais com exportação de dados booleanos.")
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

    # Terceira linha de cards (Gestão de Obras e Emendas)
    col_cards_5, col_cards_6 = st.columns(2)
    
    with col_cards_5:
        st.info("### 🏗️ Monitoramento de Obras\nAcompanhamento estratégico das obras do Novo PAC e Retomada com foco em pendências no SISMOB.")
        if st.button("Abrir Gestão de Obras ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🏗️ Monitoramento de Obras"
            st.rerun()

    with col_cards_6:
        st.success("### 🏛️ Emendas Parlamentares\nConsulta unificada de destinações e emendas federais enviadas à Paraíba (Período 2023-2026).")
        if st.button("Abrir Painel de Emendas ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🏛️ Emendas Parlamentares"
            st.rerun()

    st.markdown("---")

    # Quarta linha de cards (Cadastro de Obras e Dados de Municípios)
    col_cards_7, col_cards_8 = st.columns(2)

    with col_cards_7:
        # --- 📝 ADIÇÃO DO NOVO CARD DE CADASTRO DE OBRAS ---
        st.info("### 📝 Cadastro de Obras\nRelatório Geral de Obras com consolidação financeira automatizada, geolocalização por GPS e gerador de resumos para cópia rápida.")
        if st.button("Abrir Cadastro de Obras ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "📝 Cadastro de Obras"
            st.rerun()
            
    with col_cards_8:
        # --- 🌵 CARD DE MUNICÍPIOS ---
        st.warning("### 🌵 Dados Municípios PB\nColeta de dados institucionais, e-mails, contatos e imagens oficiais das prefeituras da Paraíba via raspagem automatizada.")
        if st.button("Abrir Dados dos Municípios ➡️", use_container_width=True):
            st.session_state["app_selecionado"] = "🌴 Dados Municípios PB"
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

# --- NOVO BLOCO: EXECUÇÃO DO CADASTRO DE OBRAS (CHAMA O FILHO PROPOSTO) ---
elif st.session_state["app_selecionado"] == "📝 Cadastro de Obras":
    try:
        import importlib
        import sys
        if "monit_relatorio" in sys.modules:
            importlib.reload(sys.modules["monit_relatorio"])
        else:
            import monit_relatorio
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'monit_relatorio.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o Cadastro de Obras: {e}")

elif st.session_state["app_selecionado"] == "🏛️ Emendas Parlamentares":
    try:
        import importlib
        import sys
        if "Emendas_app" in sys.modules:
            importlib.reload(sys.modules["Emendas_app"])
        else:
            import Emendas_app
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'Emendas_app.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar o Painel de Emendas: {e}")

elif st.session_state["app_selecionado"] == "🌴 Dados Municípios PB":
    try:
        import importlib
        import sys
        if "MunicipiosPb" in sys.modules:
            importlib.reload(sys.modules["MunicipiosPb"])
        else:
            import MunicipiosPb
    except FileNotFoundError:
        st.error("Erro operacional: O arquivo 'MunicipiosPb.py' não foi localizado na mesma pasta deste Hub.")
    except Exception as e:
        st.error(f"Ocorreu uma falha ao renderizar os Dados dos Municípios: {e}")

# --- RODAPÉ DISCRETO PADRONIZADO DO HUB (AUTORIA E PARCERIA) ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='text-align:center; font-size:12px; color:gray; margin-top:20px; line-height:1.6;'>"
    "<b>Autoria:</b> Bartolomeu Lima - Corecon-ES 1541<br>"
    "<b>Parceria:</b> Inteligência Artificial (Google Gemini)"
    "</p>",
    unsafe_allow_html=True
)
