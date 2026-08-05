import pandas as pd
import streamlit as st
from io import BytesIO

# Senha fixa
senha_correta = "ditre123"

# Inicializa o estado de acesso na sessão se não existir
if "acesso_liberado" not in st.session_state:
    st.session_state["acesso_liberado"] = False

# --- TELA DE LOGIN SEGURA ---
if not st.session_state["acesso_liberado"]:
    st.title("🔐 Guardiã dos Dados - Autenticação")
    
    col_login, _ = st.columns(2)
    with col_login:
        senha = st.text_input("Digite a senha para acessar:", type="password")
        if st.button("Entrar", use_container_width=True):
            if senha == senha_correta:
                st.session_state["acesso_liberado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta! Tente novamente.")

# --- APLICATIVO PRINCIPAL LIBERADO ---
if st.session_state["acesso_liberado"]:
    
    # Carregamento seguro com dupla checagem de encoding para evitar erros de acentuação
    try:
        df = pd.read_csv(
            "convenios.csv",
            sep=";",   
            encoding="latin1",
            dtype={"CNPJ": str},
            converters={"Ano": lambda x: str(x).replace(".0", "").strip()}
        )
    except:
        df = pd.read_csv(
            "convenios.csv",
            sep=";",   
            encoding="utf-8",
            dtype={"CNPJ": str},
            converters={"Ano": lambda x: str(x).replace(".0", "").strip()}
        )
        
    df.columns = df.columns.str.strip()

    st.title("🔍 Consulta de Convênios (Conrepass)")

    # Seleção de convênio em formato compacto no topo da tela
    col_sel, _ = st.columns(2)
    with col_sel:
        instrumentos = sorted(df["Instrumento"].dropna().unique())
        instrumento = st.selectbox("Selecione o número do convênio:", instrumentos)

    if instrumento:
        resultado = df[df["Instrumento"].astype(str).str.strip() == str(instrumento).strip()]
        
        if not resultado.empty:
            idx_registro = resultado.index[0] # Captura a linha exata como número inteiro
            
            # --- MENU LATERAL VERTICALIZADO ---
            st.sidebar.header("Menu de Controle")
            
            menu_blocos = st.sidebar.radio(
                "Selecione o Bloco de Informações",
                [
                    "🔑 Identificação",
                    "📅 Vigência / Datas",
                    "📊 Execução Financeira",
                    "📑 Prestação de Contas",
                    "📝 Monitoramento",
                    "⚠️ Alertas",
                    "🗒️ Anotações e OBS"
                ]
            )
            
            st.sidebar.markdown("---")
            st.sidebar.subheader("Ações do Repass")

            # Botão de Exportar Base
            csv_data = df.to_csv(sep=";", index=False).encode("latin1")
            st.sidebar.download_button(
                label="📥 Baixar Base Completa",
                data=csv_data,
                file_name="convenios_atualizado.csv",
                mime="text/csv",
                use_container_width=True
            )

            # --- CONTEÚDO DINÂMICO CONFORME SELEÇÃO DO MENU ---
            st.markdown("---")
            st.subheader(f"📌 {menu_blocos} — Convênio nº {instrumento}")
            if "🔑 Identificação" in menu_blocos:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Instrumento:** {resultado.loc[idx_registro, 'Instrumento']}")
                    st.write(f"**Ano:** {resultado.loc[idx_registro, 'Ano']}")
                    st.write(f"**Modalidade:** {resultado.loc[idx_registro, 'Modalidade']}")
                    st.write(f"**Processo SEI:** {resultado.loc[idx_registro, 'Processo SEI']}")
                with col_b:
                    st.write(f"**Nome Proponente:** {resultado.loc[idx_registro, 'Nome Proponente']}")
                    st.write(f"**CNPJ:** {resultado.loc[idx_registro, 'CNPJ']}")
                    st.write(f"**Situação:** {resultado.loc[idx_registro, 'Situacao']}")
                st.info(f"**Objeto:** {resultado.loc[idx_registro, 'Objeto']}")

            elif "📅 Vigência / Datas" in menu_blocos:
                st.write(f"**Início Vigência:** {resultado.loc[idx_registro, 'Inicio Vigencia']}")
                st.write(f"**Fim Vigência:** {resultado.loc[idx_registro, 'Fim Vigencia']}")
                st.write(f"**Data Limite para Apresentar PC:** {resultado.loc[idx_registro, 'Data Limite para Apresentar PC']}")
                st.info(f"**Prestação de Contas Apresentada em:** {resultado.loc[idx_registro, 'Data de Envio da  PC']}")

            elif "📊 Execução Financeira" in menu_blocos:
                col_c, col_d = st.columns(2)
                with col_c:
                    st.write(f"**Valor Global:** R$ {resultado.loc[idx_registro, 'Valor Global']}")
                    st.write(f"**Valor Empenhado:** R$ {resultado.loc[idx_registro, 'Valor Empenhado']}")
                    st.write(f"**Valor Liberado:** R$ {resultado.loc[idx_registro, 'Valor Liberado']}")
                    st.write(f"**Valor de Contrapartida:** R$ {resultado.loc[idx_registro, 'Valor de Contrapartida']}")
                    st.write(f"**Ingresso de R$ (Rendimentos/Contrapartida):** {resultado.loc[idx_registro, 'Ingresso de $']}")
                with col_d:
                    st.write(f"**Total em Movimentações:** R$ {resultado.loc[idx_registro, 'Total em Movimentacoes Financeiras']}")
                    st.write(f"**Saldo em Conta:** R$ {resultado.loc[idx_registro, 'Saldo em conta']}")
                    st.write(f"**Vl Devolvido:** R$ {resultado.loc[idx_registro, 'Vl Devolvido']}")
                    st.write(f"**Execução Financeira Conc./Conv.:** R$ {resultado.loc[idx_registro, 'Execucao  Financeira Concedente  e Convenente']}")
                    st.write(f"**Devolução de Saldo p/ União:** R$ {resultado.loc[idx_registro, 'Devolucao de Saldo p Uniao']}")
                st.warning(f"**Resto a Pagar:** R$ {resultado.loc[idx_registro, 'Resto a Pagar']}")

            elif "📑 Prestação de Contas" in menu_blocos:
                col_e, col_f = st.columns(2)
                with col_e:
                    st.write(f"**Dias de Atraso Envio da PC:** {resultado.loc[idx_registro, 'Dias de Atraso Envio da PC']}")
                    st.write(f"**PC Informatizada:** {resultado.loc[idx_registro, 'PC Informatizada']}")
                    st.write(f"**Nota de Risco:** {resultado.loc[idx_registro, 'Nota de Risco']}")
                    st.write(f"**Limite Toler Risco:** {resultado.loc[idx_registro, 'Limite Toler  Risco']}")
                    faixa = resultado.loc[idx_registro, 'Faixa de Risco']
                    st.write(f"**Faixa de Risco:** {faixa if not pd.isna(faixa) else 'Não informado'}")
                    st.write(f"**Grau de Prioridade:** {resultado.loc[idx_registro, 'Grau de Prioridade']}")
                with col_f:
                    st.write(f"**Relatórios de Execução:** {resultado.loc[idx_registro, 'Relatorios de Execucao']}")
                    st.write(f"**Ação de Monitoramento:** {resultado.loc[idx_registro, 'Acao de Monitoramnto']}")
                    st.write(f"**Parecer Financeiro:** {resultado.loc[idx_registro, 'Parecer Financeiro']}")
                    st.write(f"**Parecer Tec-Mérito:** {resultado.loc[idx_registro, 'Parecer Tec -Merito']}")
                    st.write(f"**Análise de Equipamentos:** {resultado.loc[idx_registro, 'Analise de Equipamentos']}")
                    st.write(f"**Ação de Análise de PC:** {resultado.loc[idx_registro, 'Acao de Analise de PC']}")
                st.info(f"**Percentual de Evolução da Análise:** {resultado.loc[idx_registro, 'Percentual de Evolucao da Analise']}")
                st.write(f"**Pareceres Incluídos na Plataforma:** {resultado.loc[idx_registro, 'Pareceres Incluidos na Plataforma']}")

            elif "📝 Monitoramento" in menu_blocos:
                col_g, col_h = st.columns(2)
                with col_g:
                    st.write(f"**Situação do Convênio:** {resultado.loc[idx_registro, 'Status de Execucao']}")
                    st.write(f"**Percentual de Execução:** {resultado.loc[idx_registro, 'Percental  Exec']}")
                with col_h:
                    st.write(f"**Técnico / Analista:** {resultado.loc[idx_registro, 'Tecnico / Analista']}")
                    st.write(f"**Data de Vínculo Fiscal:** {resultado.loc[idx_registro, 'Data de Vinculo Fiscal']}")

            elif "⚠️ Alertas" in menu_blocos:
                st.error(f"⚠️ **ALERTA de Execução Financeira:** {resultado.loc[idx_registro, 'ALERTA de Execucao Financeira']}")
                st.error(f"⚠️ **ALERTA Sem Desembolso:** {resultado.loc[idx_registro, 'ALERTA Sem Desembolso']}")
                st.error(f"⚠️ **ALERTA Sem Pgt + 150 Dias:** {resultado.loc[idx_registro, 'ALERTA Sem Pgt + 150 Dias']}")
                st.write(f"**Acórdão TCU1203:** {resultado.loc[idx_registro, 'Acordao  TCU1203']}")
                st.write(f"**Grau de Prioridade:** {resultado.loc[idx_registro, 'GRAU DE PRIORIDADE']}")

            elif "🗒️ Anotações e OBS" in menu_blocos:
                st.text_area(
                    "🗒️ Observações registradas para este convênio:", 
                    value=str(resultado.loc[idx_registro, 'ANOTACOES OBS']).strip(), 
                    height=250, 
                    disabled=True
                )

# --- RODAPÉ DISCRETO PADRONIZADO ---
st.markdown("---")
st.markdown(
    "<p style='text-align:right; font-size:12px; color:gray;'>Bartolomeu Lima - Corecon-ES 1541</p>",
    unsafe_allow_html=True
)
