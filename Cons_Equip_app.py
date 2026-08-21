import pandas as pd
import streamlit as st

# Tentativa de leitura do CSV com fallback de encoding
try:
    df = pd.read_csv("Cons_Equip.csv", sep=";", encoding="utf-8-sig")
except UnicodeDecodeError:
    try:
        df = pd.read_csv("Cons_Equip.csv", sep=";", encoding="latin1")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()

df.columns = df.columns.str.strip()

st.title("Consulta de Equipamentos - Análise Especializada")

# Campo de busca por texto
busca = st.text_input("🔍 Digite parte do nome do equipamento:")

if busca.strip():
    filtrados = df[df["Item"].astype(str).str.lower().str.contains(busca.lower().strip(), na=False)]
    equipamentos = sorted(filtrados["Item"].unique())

    if equipamentos:
        st.markdown(
            "<p style='color:green; font-weight:bold;'>✅ Equipamento encontrado, selecione com um click</p>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Nenhum equipamento encontrado para essa busca.")
else:
    equipamentos = sorted(df["Item"].dropna().unique())

# Sempre mantém a caixa de seleção
equipamentos = ["Selecione..."] + equipamentos
equipamento = st.selectbox("Selecione o equipamento:", equipamentos)

if equipamento != "Selecione...":
    resultado = df[df["Item"].str.lower().str.strip() == equipamento.lower().strip()]
    if not resultado.empty:
        codigo = resultado.iloc[0].get("Cod. Item", "")
        descricao = resultado.iloc[0].get("Definicao", "")
        classificacao = resultado.iloc[0].get("Classificacao", "")
        valor_reais = resultado.iloc[0].get("R$ Valor Sugerido", "")
        valor_dolar = resultado.iloc[0].get("Item Dolarizado", "")
        especificacao = resultado.iloc[0].get("Especificacao Sugerida", "")
        tipo = resultado.iloc[0].get("Tipo", "")

        st.subheader(f"Equipamento: {equipamento}")
        st.write(f"**Código:** {codigo}")
        st.write(f"**Descrição:** {descricao}")
        st.write(f"**Classificação:** {classificacao}")
        st.write(f"**Valor Sugerido (R$):** {valor_reais}")
        st.write(f"**Valor em Dólar:** {valor_dolar}")
        st.write(f"**Especificação Sugerida:** [Abrir link]({especificacao})")
        st.write(f"**Tipo:** {tipo}")

        # --- BLOCO DE DESTAQUE VISUAL (CORRIGIDO E INTERNO) ---
        # Converte de forma segura o valor obtido para texto minúsculo
        tipo_texto = str(tipo).lower().strip() if pd.notna(tipo) else ""

                # --- BLOCO DE DESTAQUE VISUAL (CORRIGIDO) ---
        # Converte de forma segura o valor obtido para texto minúsculo
        tipo_texto = str(tipo).lower().strip() if pd.notna(tipo) else ""

        # Se contiver "não", pula direto para o bloco informativo de NÃO ESPECIALIZADA
        if "não" in tipo_texto or "nao" in tipo_texto:
            st.info("ℹ️ Este equipamento NÃO é de análise especializada")
        # Se não tiver o "não", mas tiver o radical da especialização, é positiva
        elif any(termo in tipo_texto for termo in ["especializada", "especializado", "especializa"]):
            st.success("✅ Este equipamento é de ANÁLISE ESPECIALIZADA")
        else:
            st.info("ℹ️ Este equipamento NÃO é de análise especializada")


# Rodapé discreto
st.markdown(
    "<p style='text-align:right; font-size:12px; color:green;'>Bartolomeu Lima - Corecon-ES 1541</p>",
    unsafe_allow_html=True
)

# Volta para o Menu
st.markdown("[⬅️ Voltar ao Menu](https://menu1app.streamlit.app/)")
