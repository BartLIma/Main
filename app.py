import pandas as pd
import streamlit as st
import unicodedata

st.set_page_config(layout="wide", page_title="Consulta de Secretários", page_icon="🔍")

# --- TRUQUE CSS ATUALIZADO: Design moderno e espaçamentos equilibrados ---
st.markdown(
    """
    # --- TRUQUE CSS ATUALIZADO: Tema Bordo para Versao Estatica Local ---
st.markdown(
    """
   # --- TRUQUE CSS ATUALIZADO: Tema Bordo para Versao Estatica Local ---
st.markdown(
    """
    <style>
        .block-container { 
            padding-top: 2rem !important; 
            padding-bottom: 2rem !important; 
        }
        div[data-testid="stVerticalBlock"] > div { 
            border-radius: 0px; 
        }
        h2, h3 {
            color: #7F1D1D;
            font-weight: 600 !important;
        }
        .stMarkdown p { 
            margin-bottom: 0.5rem !important; 
        }
    </style>
    """,
    unsafe_allow_html=True
)


if "indice_secretario_consultado" not in st.session_state:
    st.session_state["indice_secretario_consultado"] = None

# --- CARREGAMENTO SEGURO DOS DADOS ---
encodings_para_testar = ["utf-8-sig", "ISO-8859-1", "cp1252"]
df = None

for enc in encodings_para_testar:
    try:
        df = pd.read_csv("secretarios_cosems_pb.csv", sep=",", encoding=enc, dtype=str, skip_blank_lines=True)
        break
    except Exception:
        continue

if df is None:
    for enc in encodings_para_testar:
        try:
            df = pd.read_csv("secretarios_cosems_pb.csv", sep=";", encoding=enc, dtype=str, skip_blank_lines=True)
            break
        except Exception:
            continue

if df is None:
    st.error("❌ Não foi possível ler o arquivo 'secretarios_cosems_pb.csv'. Verifique se o arquivo está na pasta ou se o formato é válido.")
    st.stop()
    
df = df.dropna(how="all")

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto.strip().lower().replace("-", "").replace(" ", "").replace("_", "")

mapeamento_colunas = {}
for col in df.columns:
    col_limpa = normalizar_texto(col)
    if "municip" in col_limpa: mapeamento_colunas[col] = "Município"
    elif "secretar" in col_limpa or "nome" in col_limpa: mapeamento_colunas[col] = "Secretário"
    elif "emailinstitucional" in col_limpa: mapeamento_colunas[col] = "Email Institucional"
    elif "email" in col_limpa: mapeamento_colunas[col] = "Email"
    elif "telefoneinstitucional" in col_limpa: mapeamento_colunas[col] = "Telefone Institucional"
    elif "telefon" in col_limpa: mapeamento_colunas[col] = "Telefone"
    elif "enderec" in col_limpa: mapeamento_colunas[col] = "Endereço da SEMUS"
    elif "fundodesaud" in col_limpa: mapeamento_colunas[col] = "Fundo de Saúde"
    elif "cnpj" in col_limpa: mapeamento_colunas[col] = "CNPJ"
    elif "regiaodesaud" in col_limpa: mapeamento_colunas[col] = "Região de Saúde"

df = df.rename(columns=mapeamento_colunas)

lista_colunas_secretarios = ["Município", "Secretário", "Email", "Email Institucional", "Telefone", "Telefone Institucional", "Endereço da SEMUS", "Fundo de Saúde", "CNPJ", "Região de Saúde"]
for col_nome in lista_colunas_secretarios:
    if col_nome not in df.columns:
        df[col_nome] = ""

# Preserva o nome original para exibição, mas cria uma chave de busca tratada
df["Municipio_Exibicao"] = df["Município"].astype(str).str.strip()
df["Secretário"] = df["Secretário"].astype(str).str.strip()
# --- BANCO DE COORDENADAS PARAÍBA (CHAVES 100% NORMALIZADAS) ---
# Funciona offline, sem APIs externas e sem conflitos com o Menu Principal
COORDENADAS_PB = {
    "aguabranca": (-7.51, -37.63), "aguiar": (-7.09, -38.16), "alagoanova": (-7.04, -35.75), "alagoagrande": (-7.04, -35.62),
    "alagoinha": (-6.94, -35.54), "alcantil": (-7.74, -36.05), "algodaodejandaira": (-6.93, -35.93), "alhandra": (-7.43, -34.90),
    "amparo": (-7.56, -36.91), "aparecida": (-6.78, -38.08), "aracagi": (-6.85, -35.38), "arara": (-6.82, -35.75),
    "araruna": (-6.55, -35.73), "areia": (-6.96, -35.69), "areiadebaraunas": (-7.13, -36.93), "areial": (-7.05, -35.92),
    "aroeiras": (-7.47, -35.68), "assuncao": (-7.06, -36.71), "baiadatraicao": (-6.68, -34.93), "bananeiras": (-6.75, -35.63),
    "barauna": (-6.65, -36.25), "barradesantana": (-7.53, -35.99), "barradesantarosa": (-6.72, -36.06), "barradesaomiguel": (-7.75, -36.31),
    "bayeux": (-7.12, -34.93), "belem": (-6.74, -35.51), "belemdobrejodocruz": (-6.18, -37.53), "bernardinobatista": (-6.45, -38.54),
    "boaventura": (-7.42, -38.21), "boavista": (-7.25, -36.23), "bomjesus": (-6.73, -38.60), "bomsucesso": (-6.45, -37.93),
    "bonitodesantafe": (-7.18, -38.75), "boqueirao": (-7.48, -36.13), "borborema": (-6.80, -35.62), "brejodocruz": (-6.35, -37.48),
    "brejodossantos": (-6.41, -37.54), "caapora": (-7.51, -34.90), "cabaceiras": (-7.48, -36.28), "cabedelo": (-6.97, -34.83),
    "cachoeiradosindios": (-6.83, -38.60), "cacimbadedentro": (-6.64, -35.78), "cacimbadeareia": (-7.12, -37.16), "cacimbas": (-7.29, -37.15),
    "caicara": (-6.61, -35.40), "cajazeiras": (-6.88, -38.55), "cajazeirinhas": (-6.91, -37.81), "caldasbrandao": (-7.22, -35.56),
    "camalau": (-7.89, -36.82), "campinagrande": (-7.22, -35.88), "capim": (-6.78, -35.16), "caraubas": (-7.71, -36.49),
    "carrapateira": (-7.03, -38.38), "casserengue": (-6.71, -35.67), "atingba": (-6.82, -35.11), "catoledorocha": (-6.34, -37.74),
    "caturite": (-7.42, -36.03), "conceicao": (-7.56, -38.50), "condado": (-6.90, -37.60), "conde": (-7.25, -34.90),
    "congo": (-7.79, -36.78), "coremas": (-7.01, -37.94), "coxixola": (-7.63, -36.60), "cruvdoespiritosanto": (-7.23, -35.08),
    "cruvdeespiritosanto": (-7.23, -35.08), "cubati": (-6.88, -36.22), "cuite": (-6.48, -36.15), "cuitedemamanguape": (-6.92, -35.15),
    "cuitegi": (-6.83, -35.53), "curraldecima": (-6.73, -35.25), "curralvelho": (-7.49, -38.12), "damiao": (-6.63, -36.02),
    "desterro": (-7.29, -37.09), "vistaserrana": (-6.73, -37.56), "diamante": (-7.41, -38.19), "donaines": (-6.62, -35.64),
    "duasestradas": (-6.71, -35.41), "emas": (-7.11, -37.62), "esperanca": (-7.02, -35.85), "fagundes": (-7.36, -35.77),
    "freimartinho": (-6.41, -36.46), "gadobravo": (-7.53, -35.78), "guarabira": (-6.85, -35.49), "gurjao": (-7.24, -36.49),
    "gurinhem": (-7.12, -35.42), "imaculada": (-7.38, -37.50), "inga": (-7.31, -35.61), "itabaiana": (-7.32, -35.33),
    "itaporanga": (-7.40, -38.15), "itapororoca": (-6.84, -35.15), "itatuba": (-7.38, -35.54), "jacarau": (-6.61, -35.13),
    "jerico": (-6.50, -37.80), "joaopessoa": (-7.11, -34.86), "jocaclaudino": (-6.49, -38.46), "juareztavora": (-7.16, -35.59),
    "juazeirinho": (-7.06, -36.57), "juncodoserido": (-6.98, -36.72), "juripiranga": (-7.40, -35.25), "juru": (-7.53, -37.83),
    "lagoa": (-6.56, -37.91), "lagoadedentro": (-6.80, -35.28), "lagoaseca": (-7.16, -35.85), "lastro": (-6.64, -38.25),
    "livramento": (-7.38, -36.94), "logradouro": (-6.66, -35.38), "lucena": (-6.90, -34.86), "maedagua": (-7.26, -37.29),
    "malta": (-6.90, -37.52), "mamanguape": (-6.83, -35.12), "manaira": (-7.70, -38.15), "marcao": (-6.75, -34.99),
    "marizopolis": (-6.84, -38.28), "massaranduba": (-7.20, -35.79), "mataraca": (-6.50, -34.97), "matinhas": (-7.09, -35.79),
    "matoesdonorte": (-7.50, -35.40), "matogrosso": (-6.41, -37.75), "matureia": (-7.26, -37.22), "mogeiro": (-7.28, -35.47),
    "montadas": (-7.09, -35.95), "montehorebe": (-7.18, -38.58), "monteiro": (-7.88, -37.11), "mulungu": (-7.02, -35.45),
    "natuba": (-7.64, -35.55), "nazarezinho": (-6.90, -38.43), "novafloresta": (-6.45, -36.20), "novaolinda": (-7.48, -38.04),
    "novapalmeira": (-6.66, -36.42), "olhodagua": (-7.23, -37.73), "olivedos": (-6.97, -36.24), "ourovelho": (-7.91, -37.15),
    "parari": (-7.46, -36.65), "passagem": (-7.10, -37.05), "patos": (-7.02, -37.27), "paulista": (-6.59, -37.62),
    "pedrabranca": (-7.46, -38.12), "pedralavrada": (-6.75, -36.43), "pedrasdefogo": (-7.40, -35.11), "pedroregis": (-6.69, -35.11),
    "pianco": (-7.19, -37.92), "picaunha": (-7.20, -35.25), "piloes": (-6.85, -35.60), "piloezinhos": (-6.83, -35.55),
    "pirpirituba": (-6.79, -35.49), "pitimbu": (-7.47, -34.80), "pocinhos": (-7.07, -36.05), "pombal": (-6.77, -37.79),
    "prata": (-7.93, -37.08), "princesaisabel": (-7.73, -37.99), "puxinana": (-7.15, -35.97), "queimadas": (-7.35, -35.89),
    "quixaba": (-7.01, -37.15), "remigio": (-6.90, -35.83), "riachao": (-6.54, -35.63), "riachaodobacamarte": (-7.26, -35.66),
    "riachaodopoco": (-7.10, -35.23), "riachodesantoantonio": (-7.64, -36.01), "riachodoscavalos": (-6.43, -37.65),
    "riotinto": (-6.80, -35.07), "salgadinho": (-7.05, -36.85), "salgadosaofelix": (-7.35, -35.44), "santacecilia": (-7.63, -35.89),
    "santacruz": (-6.51, -38.05), "santahelena": (-6.72, -38.63), "santaines": (-7.65, -38.55), "santaluzia": (-6.87, -36.92),
    "santanademangueira": (-7.55, -38.43), "santanadosgarrotes": (-7.40, -37.95), "santarita": (-7.16, -34.97),
    "santateresinha": (-7.01, -37.45), "santoandre": (-7.19, -36.63), "saobento": (-6.28, -37.45), "saobentinho": (-6.83, -37.74),
    "saodomingosdocariri": (-7.55, -36.51), "saodomingos": (-6.81, -37.93), "saofrancisco": (-6.76, -38.00),
    "saojoaodocariri": (-7.38, -36.53), "saojoaodotigre": (-8.07, -36.84), "saojoaodariodopeixe": (-6.73, -38.44),
    "saojosedalagoatapada": (-6.94, -38.16), "saojosedecaiana": (-7.46, -38.31), "saojosedespinharas": (-6.84, -37.32),
    "saojosedosramos": (-7.28, -35.31), "saojosedepiranhas": (-7.11, -38.50), "saojosedeprincesa": (-7.73, -38.09),
    "saojosedobonfim": (-7.16, -37.31), "saojosedobrejodocruz": (-6.17, -37.35), "saojosedosabugi": (-6.86, -36.87),
    "saojosedoscordeiros": (-7.45, -36.80), "saomamede": (-6.92, -37.11), "saomigueldetaipu": (-7.23, -35.22),
    "saosebastiaodelagoaderoca": (-7.06, -35.84), "saosebastiaodoumbuzeiro": (-8.14, -36.94), "sape": (-7.09, -35.23),
    "serrabranca": (-7.48, -36.66), "serradaraiz": (-6.68, -35.43), "serragrande": (-7.21, -38.36), "serraria": (-6.82, -35.63),
    "sertaozinho": (-6.75, -35.44), "sobrado": (-7.13, -35.23), "soledade": (-7.05, -36.36), "sossego": (-6.88, -36.26),
    "sousa": (-6.76, -38.22), "sume": (-7.67, -36.88), "tacima": (-6.48, -35.63), "taperoa": (-7.21, -36.82),
    "tavares": (-7.63, -37.89), "teixeira": (-7.22, -37.25), "tenorio": (-6.93, -36.63), "triunfo": (-6.57, -38.53),
    "uirauna": (-6.52, -38.41), "umburana": (-6.68, -36.16), "varzea": (-6.88, -36.83), "vieiropolis": (-6.79, -38.24),
    "zabele": (-7.97, -37.10)
}

def buscar_coordenadas_municipio(nome_municipio):
    """Resgata a coordenada exata cruzando o texto normalizado estrutural"""
    if not nome_municipio:
        return -7.0600, -36.3600
    
    # Executa a mesma limpeza agressiva feita nas colunas do DataFrame para garantir o match
    texto = unicodedata.normalize('NFKD', str(nome_municipio)).encode('ascii', 'ignore').decode('utf-8')
    chave_limpa = texto.strip().lower().replace("-", "").replace(" ", "").replace("_", "")
    
    if chave_limpa in COORDENADAS_PB:
        return COORDENADAS_PB[chave_limpa]
        
    return -7.0600, -36.3600
# --- PAINEL LATERAL DE BUSCA ---
with st.sidebar:
    st.header("🔍 Painel de Busca")
    st.write("Selecione:")
    
    busca_termo = st.text_input("Digite o Município ou Secretário:", value="")
    
    if busca_termo.strip():
        termo = busca_termo.lower().strip()
        filtro = df["Municipio_Exibicao"].str.lower().str.contains(termo) | df["Secretário"].str.lower().str.contains(termo)
        registros_encontrados = df[filtro]
        
        if not registros_encontrados.empty:
            opcoes_secretarios = {}
            for idx, row in registros_encontrados.iterrows():
                muni = row["Municipio_Exibicao"]
                sec = f" ({row['Secretário']})" if pd.notna(row["Secretário"]) and row["Secretário"].strip() and row["Secretário"].lower() != 'nan' else ""
                opcoes_secretarios[f"{muni}{sec}"] = idx
            
            lista_ordenada = ["-- Selecione o registro --"] + sorted(list(opcoes_secretarios.keys()))
            selecao = st.selectbox("Registros localizados:", lista_ordenada)
            
            if selecao and selecao != "-- Selecione o registro --":
                st.session_state["indice_secretario_consultado"] = opcoes_secretarios[selecao]
            else:
                st.session_state["indice_secretario_consultado"] = None
        else:
            st.session_state["indice_secretario_consultado"] = None
            st.sidebar.warning("Nenhum registro localizado.")
    else:
        st.session_state["indice_secretario_consultado"] = None

# --- ÁREA PRINCIPAL ---
st.title("🏛️ Consulta — Secretarias Municipais de Saúde da Paraíba")
# Etiqueta de identificação exclusiva desta versão
st.caption("🏷️ *Ambiente Ativo: Mapeamento Geográfico via Banco de Dados Estático Local*")

if st.session_state["indice_secretario_consultado"] is not None and st.session_state["indice_secretario_consultado"] in df.index:
    s_idx = st.session_state["indice_secretario_consultado"]
    
    municipio_atual = df.loc[s_idx, 'Municipio_Exibicao']
    secretario_atual = df.loc[s_idx, 'Secretário']
    regiao_atual = df.loc[s_idx, 'Região de Saúde']
    
    def obter_valor_valido(campo):
        val = df.loc[s_idx, campo]
        if pd.isna(val) or str(val).lower() == 'nan' or str(val).strip() == "":
            return "Não informado"
        return str(val).strip()

    txt_em = obter_valor_valido("Email")
    txt_emi = obter_valor_valido("Email Institucional")
    txt_tl = obter_valor_valido("Telefone")
    txt_tli = obter_valor_valido("Telefone Institucional")
    txt_end = obter_valor_valido("Endereço da SEMUS")
    txt_fund = obter_valor_valido("Fundo de Saúde")
    txt_cnpj = obter_valor_valido("CNPJ")

    texto_exportacao = f"""### 📍 MUNICÍPIO — {municipio_atual.upper()}
    
👤 **Secretário(a):** {secretario_atual}
🗺️ **Região de Saúde (CIR):** {regiao_atual}
📧 **E-mail Pessoal:** {txt_em}
🏢 **E-mail Institucional:** {txt_emi}
📱 **Telefone Celular:** {txt_tl}
☎️ **Telefone Institucional:** {txt_tli}
🏢 **Endereço da SEMUS:** {txt_end}
🏥 **Fundo de Saúde:** {txt_fund}
📋 **CNPJ:** {txt_cnpj}
"""

    col_ficha, col_mapa = st.columns([1.2, 0.8], gap="large")
    
    with col_ficha:
        with st.container(border=True):
            st.subheader(f"📍 Município — {municipio_atual}")
            st.markdown("---")
            
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.markdown(f"👤 **Secretário(a) de Saúde:**<br><span style='font-size: 18px; color: #2563EB; font-weight: bold;'>{secretario_atual}</span>", unsafe_allow_html=True)
                st.write("") 
                st.write(f"📧 **E-mail Pessoal:** {txt_em}")
                st.write(f"🏢 **E-mail Institucional:** {txt_emi}")
                
            with f_col2:
                st.markdown(f"🗺️ **Região de Saúde (CIR):**<br><span style='font-size: 18px; color: #10B981; font-weight: bold;'>{regiao_atual}</span>", unsafe_allow_html=True)
                st.write("") 
                st.write(f"📱 **Telefone Celular:** {txt_tl}")
                st.write(f"☎️ **Telefone Institucional:** {txt_tli}")
            
            st.markdown("---")
            st.info(f"🏢 **Endereço da SEMUS:** {txt_end}")
            st.warning(f"🏥 **Fundo de Saúde:** {txt_fund}  |  📋 **CNPJ:** {txt_cnpj}")

    with col_mapa:
        with st.container(border=True):
            st.subheader("🛠️ Ações e Localização")
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    label="📥 Baixar Dados (TXT)",
                    data=texto_exportacao,
                    file_name=f"ficha_saude_{municipio_atual.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with c2:
                with st.popover("📋 Copiar Dados", use_container_width=True):
                    st.code(texto_exportacao, language="markdown")
            
            st.markdown(" ")
            st.markdown("🗺️ **Geolocalização**")
            
            # --- RENDERIZAÇÃO MATEMÁTICA E LOCAL DO MAPA ---
            lat, lon = buscar_coordenadas_municipio(municipio_atual)
            df_mapa = pd.DataFrame({"lat": [lat], "lon": [lon]})
            
            st.map(df_mapa, size=60, color="#1E3A8A", zoom=11)

else:
    st.markdown("---")
    st.info("💡 **Aguardando consulta:** Utilize o menu ao lado esquerdo para digitar o nome de uma cidade ou gestor e abrir a ficha cadastral completa.")

# --- RODAPÉ DISCRETO ---
st.markdown("---")
st.markdown("<p style='text-align:right; font-size:12px; color:#A3A3A3;'>Bartolomeu Lima - Corecon-ES 1541</p>", unsafe_allow_html=True)
