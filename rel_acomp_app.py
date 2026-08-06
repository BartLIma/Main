import streamlit as st
import pandas as pd

# Título do módulo
st.title("Monitoramento de Convênios")

# Inicializa a memória estável para as 28 perguntas se ainda não existirem
for i in range(1, 29):
    if f"salvo_p{i}" not in st.session_state:
        st.session_state[f"salvo_p{i}"] = False

if "codigo_convenio" not in st.session_state:
    st.session_state["codigo_convenio"] = ""

if "reset_key" not in st.session_state:
    st.session_state["reset_key"] = 0

# Funções de limpeza
def limpar_tudo():
    st.session_state["codigo_convenio"] = ""
    for i in range(1, 29):
        st.session_state[f"salvo_p{i}"] = False
    st.session_state["reset_key"] += 1

def limpar_pta():
    for i in range(1, 6):
        st.session_state[f"salvo_p{i}"] = False
    st.session_state["reset_key"] += 1

def limpar_recursos():
    for i in range(6, 15):
        st.session_state[f"salvo_p{i}"] = False
    st.session_state["reset_key"] += 1

def limpar_financeiro():
    for i in range(15, 24):
        st.session_state[f"salvo_p{i}"] = False
    st.session_state["reset_key"] += 1

def limpar_tramitacao():
    for i in range(24, 29):
        st.session_state[f"salvo_p{i}"] = False
    st.session_state["reset_key"] += 1

# --- AJUSTE DA LARGURA DO CAMPO DO CONVÊNIO ---
col1, _ = st.columns(2)
with col1:
    codigo = st.text_input(
        "Código do Convênio (Instrumento)", 
        value=st.session_state["codigo_convenio"], 
        key=f"campo_codigo_{st.session_state['reset_key']}"
    )
    st.session_state["codigo_convenio"] = codigo

# --- BUSCA AUTOMÁTICA DE DADOS NO CONREPASS (convenios.csv) ---
prop_nome = "Não localizado"
prop_situacao = "Não localizado"
data_inicio = "Não localizado"
data_fim = "Não localizado"
data_limite = "Não localizado"
convenio_encontrado = False

if st.session_state["codigo_convenio"].strip():
    try:
        df_busca = pd.read_csv("convenios.csv", sep=",", encoding="utf-8-sig", dtype={"Instrumento": str})
    except Exception:
        df_busca = pd.read_csv("convenios.csv", sep=";", encoding="utf-8-sig", dtype={"Instrumento": str})
        
    df_busca.columns = df_busca.columns.str.strip()
    
    resultado_busca = df_busca[df_busca["Instrumento"].astype(str).str.strip() == str(st.session_state["codigo_convenio"]).strip()]
    
    if not resultado_busca.empty:
        convenio_encontrado = True
        idx_b = resultado_busca.index
        prop_nome = str(resultado_busca.loc[idx_b, 'Nome Proponente'].values[0])
        prop_situacao = str(resultado_busca.loc[idx_b, 'Situacao'].values[0])
        data_inicio = str(resultado_busca.loc[idx_b, 'Inicio Vigencia'].values[0])
        data_fim = str(resultado_busca.loc[idx_b, 'Fim Vigencia'].values[0])
        data_limite = str(resultado_busca.loc[idx_b, 'Data Limite para Apresentar PC'].values[0])

# --- EXIBIÇÃO AUTOMÁTICA DOS DADOS COLETADOS ---
if st.session_state["codigo_convenio"].strip():
    if convenio_encontrado:
        st.success(f"✅ Dados carregados do Conrepass para o Instrumento nº {st.session_state['codigo_convenio']}")
        c_inf1, c_inf2 = st.columns(2)
        with c_inf1:
            st.markdown(f"**Nome Proponente:** {prop_nome}")
            st.markdown(f"**Situação:** {prop_situacao}")
            st.markdown(f"**Início Vigência:** {data_inicio}")
        with c_inf2:
            st.markdown(f"**Fim Vigência:** {data_fim}")
            st.markdown(f"**Data Limite para Apresentar PC:** {data_limite}")
    else:
        st.error("⚠️ Instrumento (convênio) não localizado na base do Conrepass.")

# --- CONSTRUÇÃO DO MENU LATERAL ---
st.sidebar.header("Menu de Controle")
menu = st.sidebar.radio(
    "Selecione o Bloco de Análise",
    ["📋 Execução do PTA", "📦 Gestão de Recursos", "💰 Movimentação Financeira", "⚙️ Tramitação"]
)

# 🗺️ AJUSTE SOLICITADO: Adicionado setas indicativas explícitas para o usuário ver as opções abaixo
st.sidebar.markdown("<h4 style='text-align: center; color: #ff4b4b; margin: 15px 0 0 0;'>👇 VEJA ABAIXO 👇</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 11px; color: gray; margin: 0 0 15px 0;'>Role a barra lateral para ver as ações</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Ações do Relatório")
st.sidebar.button("Anular Tudo / Limpar", on_click=limpar_tudo, use_container_width=True)

# GERAÇÃO DO DATAFRAME CONSOLIDADO COM A NOVA ORDEM SOLICITADA
respostas = {}
respostas["Instrumento"] = st.session_state["codigo_convenio"]
respostas["Nome Proponente"] = prop_nome
respostas["Situação"] = prop_situacao

for i in range(1, 29):
    respostas[f"P{i:02d}"] = "VERDADEIRO" if st.session_state[f"salvo_p{i}"] else "FALSO"

df_consolidado = pd.DataFrame.from_dict(respostas, orient="index", columns=["Resposta"])
csv_dados = df_consolidado.to_csv().encode("utf-8-sig")

# Botão Salvar Análise no Menu Lateral
if st.sidebar.button("💾 Salvar Análise", use_container_width=True):
    st.session_state["exibir_resultados"] = True
else:
    if "exibir_resultados" not in st.session_state:
        st.session_state["exibir_resultados"] = False

# Botão Baixar CSV no Menu Lateral
nome_arquivo = f"monitoramento_convenio_{st.session_state['codigo_convenio'] if st.session_state['codigo_convenio'] else 'sem_codigo'}.csv"
st.sidebar.download_button(
    label="📥 Baixar CSV (Todos os Blocos)",
    data=csv_dados,
    file_name=nome_arquivo,
    mime="text/csv",
    use_container_width=True
)
# --- LISTAS DE PERGUNTAS DE P1 A P28 ---
perguntas_pta = [
    "P01 - Objeto executado conforme metas do PTA?",
    "P02 - Execução na mesma localidade/endereço?",
    "P03 - Notificação ao Conselho de Saúde etc?",
    "P04 - Houve cotação/divulgação eletrônica?",
    "P05 - Preços compatíveis with referência?"
]

perguntas_recursos = [
    "P06 - Recurso depositado na conta específica?",
    "P07 - Recursos aplicados no mercado financeiro?",
    "P08 - Recursos >30 dias aplicados em poupança?",
    "P09 - Recursos <30 dias aplicados no mercado?",
    "P10 - Execução compatível com edital/contrato?",
    "P11 - Despesas conforme Plano de Aplicação?",
    "P12 - Preços praticados de acordo com PTA?",
    "P13 - Documentação identificada com nº convênio?",
    "P14 - Documentos disponíveis na Plataforma?"
]

perguntas_fin = [
    "P15 - Movimentação financeira em conta específica?",
    "P16 - Pagamentos com comprovantes no mesmo valor?",
    "P17 - Movimentação bancária pertinente ao objeto?",
    "P18 - Extratos demonstrando correto pagamento?",
    "P19 - Ausência de taxa de administração?",
    "P20 - Ausência de taxas bancárias/multas/juros?",
    "P21 - Objeto integralmente executado?",
    "P22 - Recolhimento do saldo em tempo hábil?",
    "P23 - Cancelamento de Resto a Pagar efetivado?"
]

perguntas_tram = [
    "P24 - Parecer técnico emitido?",
    "P25 - Relatórios de execução analisados?",
    "P26 - Parecer financeiro emitido?",
    "P27 - NT especializada emitida?",
    "P28 - Pareceres incluídos na Plataforma?"
]

# EXIBIÇÃO DINÂMICA CONFORME O MENU SELECIONADO
if "📋 Execução do PTA" in menu:
    st.header("Bloco de Análise: Execução do PTA")
    for i, pergunta in enumerate(perguntas_pta, start=1):
        check = st.checkbox(pergunta, value=st.session_state[f"salvo_p{i}"], key=f"tela_p{i}_{st.session_state['reset_key']}")
        st.session_state[f"salvo_p{i}"] = check
    st.button("Limpar Execução do PTA", on_click=limpar_pta)

elif "📦 Gestão de Recursos" in menu:
    st.header("Bloco de Análise: Gestão de Recursos")
    for i, pergunta in enumerate(perguntas_recursos, start=6):
        check = st.checkbox(pergunta, value=st.session_state[f"salvo_p{i}"], key=f"tela_p{i}_{st.session_state['reset_key']}")
        st.session_state[f"salvo_p{i}"] = check
    st.button("Limpar Gestão de Recursos", on_click=limpar_recursos)

elif "💰 Movimentação Financeira" in menu:
    st.header("Bloco de Análise: Movimentação Financeira")
    for i, pergunta in enumerate(perguntas_fin, start=15):
        check = st.checkbox(pergunta, value=st.session_state[f"salvo_p{i}"], key=f"tela_p{i}_{st.session_state['reset_key']}")
        st.session_state[f"salvo_p{i}"] = check
    st.button("Limpar Movimentação Financeira", on_click=limpar_financeiro)

elif "⚙️ Tramitação" in menu:
    st.header("Bloco de Tramitação")
    for i, pergunta in enumerate(perguntas_tram, start=24):
        check = st.checkbox(pergunta, value=st.session_state[f"salvo_p{i}"], key=f"tela_p{i}_{st.session_state['reset_key']}")
        st.session_state[f"salvo_p{i}"] = check
    st.button("Limpar Tramitação", on_click=limpar_tramitacao)

# TABELA CONSOLIDADA NO RODAPÉ COM FUNÇÃO COPIAR DIRETO PARA O EXCEL
if st.session_state["exibir_resultados"]:
    st.markdown("---")
    st.subheader("📊 Resultados Consolidados (Todos os Blocos)")
    
    # 🌟 CORREÇÃO ADICIONADA: Cria o formato de texto ideal para colar direto no Excel (separado por tabulação)
    texto_excel = "Campo\tResposta\n"
    for idx, row in df_consolidado.iterrows():
        texto_excel += f"{idx}\t{row['Resposta']}\n"
        
    col_btn_copy, _ = st.columns([1, 3])
    with col_btn_copy:
        # Novo componente que copia o bloco de dados estruturado com 1 clique para a área de transferência
        st.copy_to_clipboard(texto_excel, label="📋 Copiar Tabela (Formato Excel)", before_copy_label="Copiando...")
        
    st.write(df_consolidado)

# --- RODAPÉ DISCRETO PADRONIZADO ---
st.markdown("---")
st.markdown(
    "<p style='text-align:right; font-size:12px; color:gray;'>Bartolomeu Lima - Corecon-ES 1541</p>",
    unsafe_allow_html=True
)
