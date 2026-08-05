import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Guardiã dos Dados - Análise de Convênios")

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
# Criamos 4 colunas: a primeira curta para o código, as outras 3 apenas para empurrar o espaço
col1, col2, col3, col4 = st.columns([2, 3, 3, 3])

with col1:
    codigo = st.text_input(
        "Código do Convênio (6 dígitos)", 
        value=st.session_state["codigo_convenio"], 
        max_chars=6,
        key=f"campo_codigo_{st.session_state['reset_key']}"
    )
    st.session_state["codigo_convenio"] = codigo


# --- CONSTRUÇÃO DO MENU LATERAL ---
st.sidebar.header("Menu de Controle")

# Menu de seleção de blocos agora com ícones visuais
menu = st.sidebar.radio(
    "Selecione o Bloco de Análise",
    [
        "📋 Execução do PTA", 
        "📦 Gestão de Recursos", 
        "💰 Movimentação Financeira", 
        "⚙️ Tramitação"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Ações do Relatório")

# Botão de limpar tudo
st.sidebar.button("Anular Tudo / Limpar", on_click=limpar_tudo, use_container_width=True)

# Gera o DataFrame consolidado alterado para retornar VERDADEIRO ou FALSO
respostas = {}
for i in range(1, 29):
    respostas[f"P{i:02d}"] = "VERDADEIRO" if st.session_state[f"salvo_p{i}"] else "FALSO"

df_consolidado = pd.DataFrame.from_dict(respostas, orient="index", columns=["Resposta"])
df_consolidado.loc["Convênio"] = st.session_state["codigo_convenio"]
csv_dados = df_consolidado.to_csv().encode("utf-8")

# Botão Salvar Análise no Menu Lateral
if st.sidebar.button("💾 Salvar Análise", use_container_width=True):
    st.session_state["exibir_resultados"] = True
else:
    if "exibir_resultados" not in st.session_state:
        st.session_state["exibir_resultados"] = False

# Botão Baixar CSV no Menu Lateral
nome_arquivo = f"analise_convenio_{st.session_state['codigo_convenio'] if st.session_state['codigo_convenio'] else 'sem_codigo'}.csv"
st.sidebar.download_button(
    label="📥 Baixar CSV (Todos os Blocos)",
    data=csv_dados,
    file_name=nome_arquivo,
    mime="text/csv",
    use_container_width=True
)


# --- CONTEÚDO PRINCIPAL (CHECKBOXES) ---
perguntas_pta = [
    "P01 - Objeto executado conforme metas do PTA?",
    "P02 - Execução na mesma localidade/endereço?",
    "P03 - Notificação ao Conselho de Saúde etc?",
    "P04 - Houve cotação/divulgação eletrônica?",
    "P05 - Preços compatíveis com referência?"
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

# Validação do menu contendo os novos nomes com ícones
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

# Exibição da tabela consolidada com os novos termos lógicos (VERDADEIRO / FALSO)
if st.session_state["exibir_resultados"]:
    st.markdown("---")
    st.subheader("📊 Resultados Consolidados (Todos os Blocos)")
    st.write(df_consolidado)
