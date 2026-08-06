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
    
    # 🌟 CORREÇÃO ABSOLUTA: Função robusta que converte qualquer formato científico (maiúsculo, minúsculo, com vírgula ou ponto)
    def tratar_formato_cientifico(valor, eh_cnpj=False):
        s = str(valor).strip()
        if not s or s.lower() == "nan": 
            return ""
        
        # Remove o '.0' caso o Excel tenha colocado
        if s.endswith('.0'): 
            s = s[:-2]
            
        # Padroniza a vírgula para ponto e força tudo para minúsculo para checar notação científica
        s_checagem = s.replace(",", ".").lower()
        
        if 'e+' in s_checagem:
            try:
                # Converte o número científico de volta para texto numérico inteiro puro
                num_puro = f"{float(s_checagem):.0f}"
                s = num_puro
            except Exception:
                pass
        
        # Tratamento exclusivo para o CNPJ manter o padrão de 14 dígitos com zeros na frente
        if eh_cnpj:
            s_limpo = s.replace(".", "").replace(",", "").replace("-", "").replace("/", "").strip()
            if s_limpo.isdigit() and len(s_limpo) < 14:
                s = s_limpo.zfill(14)
            else:
                s = s_limpo
                
        return s

    # Criação dos conversores amarrados à nova função mestre
    def tratar_sei(x):
        return tratar_formato_cientifico(x, eh_cnpj=False)

    def tratar_cnpj(x):
        return tratar_formato_cientifico(x, eh_cnpj=True)

    # CARREGAMENTO TRI-SEGURO ATUALIZADO
    try:
        df = pd.read_csv(
            "convenios.csv",
            sep=",",   
            encoding="utf-8-sig",
            dtype={"Instrumento": str},
            converters={
                "Ano": lambda x: str(x).replace(".0", "").strip(),
                "CNPJ": tratar_cnpj,       
                "Processo SEI": tratar_sei 
            }
        )
    except Exception:
        df = pd.read_csv(
            "convenios.csv",
            sep=";",   
            encoding="utf-8-sig",
            dtype={"Instrumento": str},
            converters={
                "Ano": lambda x: str(x).replace(".0", "").strip(),
                "CNPJ": tratar_cnpj,
                "Processo SEI": tratar_sei
            }
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
            idx_registro = resultado.index # Captura a linha exata como número inteiro puro
            
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

            # Botão de Exportar Base adaptado para manter a codificação correta
            csv_data = df.to_csv(sep=";", index=False, encoding="utf-8-sig").encode("utf-8-sig")
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
                    st.write(f"**Instrumento:** {resultado.loc[idx_registro, 'Instrumento'].values[0]}")
                    st.write(f"**Ano:** {resultado.loc[idx_registro, 'Ano'].values[0]}")
                    st.write(f"**Modalidade:** {resultado.loc[idx_registro, 'Modalidade'].values[0]}")
                    st.write(f"**Processo SEI:** {resultado.loc[idx_registro, 'Processo SEI'].values[0]}")
                with col_b:
                    st.write(f"**Nome Proponente:** {resultado.loc[idx_registro, 'Nome Proponente'].values[0]}")
                    st.write(f"**CNPJ:** {resultado.loc[idx_registro, 'CNPJ'].values[0]}")
                    st.write(f"**Situação:** {resultado.loc[idx_registro, 'Situacao'].values[0]}")
                st.info(f"**Objeto:** {resultado.loc[idx_registro, 'Objeto'].values[0]}")

            elif "📅 Vigência / Datas" in menu_blocos:
                st.write(f"**Início Vigência:** {resultado.loc[idx_registro, 'Inicio Vigencia'].values[0]}")
                st.write(f"**Fim Vigência:** {resultado.loc[idx_registro, 'Fim Vigencia'].values[0]}")
                st.write(f"**Data Limite para Apresentar PC:** {resultado.loc[idx_registro, 'Data Limite para Apresentar PC'].values[0]}")
                st.info(f"**Prestação de Contas Apresentada em:** {resultado.loc[idx_registro, 'Data de Envio da  PC'].values[0]}")

            elif "📊 Execução Financeira" in menu_blocos:
                col_c, col_d = st.columns(2)
                with col_c:
                    st.write(f"**Valor Global:** R$ {resultado.loc[idx_registro, 'Valor Global'].values[0]}")
                    st.write(f"**Valor Empenhado:** R$ {resultado.loc[idx_registro, 'Valor Empenhado'].values[0]}")
                    st.write(f"**Valor Liberado:** R$ {resultado.loc[idx_registro, 'Valor Liberado'].values[0]}")
                    st.write(f"**Valor de Contrapartida:** R$ {resultado.loc[idx_registro, 'Valor de Contrapartida'].values[0]}")
                    st.write(f"**Ingresso de R$ (Rendimentos/Contrapartida):** {resultado.loc[idx_registro, 'Ingresso de $'].values[0]}")
                with col_d:
                    st.write(f"**Total em Movimentações:** R$ {resultado.loc[idx_registro, 'Total em Movimentacoes Financeiras'].values[0]}")
                    st.write(f"**Saldo em Conta:** R$ {resultado.loc[idx_registro, 'Saldo em conta'].values[0]}")
                    st.write(f"**Vl Devolvido:** R$ {resultado.loc[idx_registro, 'Vl Devolvido'].values[0]}")
                    st.write(f"**Execução Financeira Conc./Conv.:** R$ {resultado.loc[idx_registro, 'Execucao  Financeira Concedente  e Convenente'].values[0]}")
                    st.write(f"**Devolução de Saldo p/ União:** R$ {resultado.loc[idx_registro, 'Devolucao de Saldo p Uniao'].values[0]}")
                st.warning(f"**Resto a Pagar:** R$ {resultado.loc[idx_registro, 'Resto a Pagar'].values[0]}")

            elif "📑 Prestação de Contas" in menu_blocos:
                col_e, col_f = st.columns(2)
                with col_e:
                    st.write(f"**Dias de Atraso Envio da PC:** {resultado.loc[idx_registro, 'Dias de Atraso Envio da PC'].values[0]}")
                    st.write(f"**PC Informatizada:** {resultado.loc[idx_registro, 'PC Informatizada'].values[0]}")
                    st.write(f"**Nota de Risco:** {resultado.loc[idx_registro, 'Nota de Risco'].values[0]}")
                    st.write(f"**Limite Toler Risco:** {resultado.loc[idx_registro, 'Limite Toler  Risco'].values[0]}")
                    faixa = resultado.loc[idx_registro, 'Faixa de Risco'].values[0]
                    st.write(f"**Faixa de Risco:** {faixa if not pd.isna(faixa) else 'Não informado'}")
                    st.write(f"**Grau de Prioridade:** {resultado.loc[idx_registro, 'Grau de Prioridade'].values[0]}")
                with col_f:
                    st.write(f"**Relatórios de Execução:** {resultado.loc[idx_registro, 'Relatorios de Execucao'].values[0]}")
                    st.write(f"**Ação de Monitoramento:** {resultado.loc[idx_registro, 'Acao de Monitoramnto'].values[0]}")
                    st.write(f"**Parecer Financeiro:** {resultado.loc[idx_registro, 'Parecer Financeiro'].values[0]}")
                    st.write(f"**Parecer Tec-Mérito:** {resultado.loc[idx_registro, 'Parecer Tec -Merito'].values[0]}")
                    st.write(f"**Análise de Equipamentos:** {resultado.loc[idx_registro, 'Analise de Equipamentos'].values[0]}")
                    st.write(f"**Ação de Análise de PC:** {resultado.loc[idx_registro, 'Acao de Analise de PC'].values[0]}")
                st.info(f"**Percentual de Evolução da Análise:** {resultado.loc[idx_registro, 'Percentual de Evolucao da Analise'].values[0]}")
                st.write(f"**Pareceres Incluídos na Plataforma:** {resultado.loc[idx_registro, 'Pareceres Incluidos na Plataforma'].values[0]}")

            elif "📝 Monitoramento" in menu_blocos:
                col_g, col_h = st.columns(2)
                with col_g:
                    st.write(f"**Situação do Convênio:** {resultado.loc[idx_registro, 'Status de Execucao'].values[0]}")
                    st.write(f"**Percentual de Execução:** {resultado.loc[idx_registro, 'Percental  Exec'].values[0]}")
                with col_h:
                    st.write(f"**Técnico / Analista:** {resultado.loc[idx_registro, 'Tecnico / Analista'].values[0]}")
                    st.write(f"**Data de Vínculo Fiscal:** {resultado.loc[idx_registro, 'Data de Vinculo Fiscal'].values[0]}")

            elif "⚠️ Alertas" in menu_blocos:
                st.error(f"⚠️ **ALERTA de Execução Financeira:** {resultado.loc[idx_registro, 'ALERTA de Execucao Financeira'].values[0]}")
                st.error(f"⚠️ **ALERTA Sem Desembolso:** {resultado.loc[idx_registro, 'ALERTA Sem Desembolso'].values[0]}")
                st.error(f"⚠️ **ALERTA Sem Pgt + 150 Dias:** {resultado.loc[idx_registro, 'ALERTA Sem Pgt + 150 Dias'].values[0]}")
                st.write(f"**Acórdão TCU1203:** {resultado.loc[idx_registro, 'Acordao  TCU1203'].values[0]}")
                st.write(f"**Grau de Prioridade:** {resultado.loc[idx_registro, 'GRAU DE PRIORIDADE'].values[0]}")

            elif "🗒️ Anotações e OBS" in menu_blocos:
                st.text_area(
                    "🗒️ Observações registradas para este convênio:", 
                    value=str(resultado.loc[idx_registro, 'ANOTACOES OBS'].values[0]).strip(), 
                    height=250, 
                    disabled=True
                )

# --- RODAPÉ DISCRETO PADRONIZADO ---
st.markdown("---")
st.markdown(
    "<p style='text-align:right; font-size:12px; color:gray;'>Bartolomeu Lima - Corecon-ES 1541</p>",
    unsafe_allow_html=True
)
