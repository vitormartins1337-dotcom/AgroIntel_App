# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | INTEGRAÇÃO TOTAL
import streamlit as st
import datetime
from core_logic import AgroEngine 

# --- 1. SETUP ---
st.set_page_config(page_title="Agrower SDI", page_icon="🍁", layout="wide")
engine = AgroEngine()
db = engine.db # Acesso direto

# --- 2. CSS MASTER (NEON & DARK) ---
def load_css():
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem !important; padding-bottom: 3rem !important; }
        .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Roboto', sans-serif; }
        [data-testid="stSidebar"] { background-color: #080808; border-right: 1px solid #222; }

        /* HEADER */
        .header-box {
            background: linear-gradient(90deg, #1a0b2e 0%, #000000 100%);
            border-bottom: 2px solid #a855f7; padding: 25px 30px; border-radius: 0 0 20px 20px;
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
        }

        /* TICKER */
        .ticker-container {
            width: 100%; background: #000; border: 1px solid #333; border-radius: 6px;
            overflow: hidden; white-space: nowrap; height: 32px; display: flex; align-items: center; margin-bottom: 15px;
        }
        .ticker-text { display: inline-block; animation: ticker 40s linear infinite; font-family: 'Courier New', monospace; font-weight: bold; font-size: 0.85rem;}
        @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .tick-item { margin-right: 40px; color: #a855f7; } .tick-val { color: #22c55e; }

        /* DASHBOARD SDI (O CORE) */
        .sdi-panel {
            background-color: #0a0a0a; border: 1px solid #222; border-left: 4px solid #a855f7;
            padding: 20px; border-radius: 10px; margin-bottom: 20px;
        }
        .sdi-title { color: #fff; font-size: 1.2rem; font-weight: 900; letter-spacing: 1px; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;}
        .sdi-metric-box {
            background: #111; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #333;
        }
        .sdi-val { font-size: 1.8rem; font-weight: bold; color: #fff; }
        .sdi-lbl { font-size: 0.75rem; color: #888; text-transform: uppercase; }

        /* CARDS GERAIS */
        .tech-card { background: #111; border: 1px solid #333; padding: 20px; border-radius: 8px; margin-bottom: 15px; }
        .tech-header { color: #a855f7; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; }

        /* DOCTOR GROW */
        .doc-card { background: #1a0505; border: 1px solid #330a0a; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
        .chem-tag { background: #330a0a; color: #fca5a5; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #7f1d1d;}
        .bio-tag { background: #062e18; color: #86efac; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; border: 1px solid #14532d;}

        /* INPUTS */
        .stSelectbox div[data-baseweb="select"] > div, .stDateInput input, .stNumberInput input {
            background-color: #111 !important; color: #fff !important; border: 1px solid #444 !important;
        }
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. HEADER & TICKER ---
st.markdown("""
<div class="header-box">
    <div>
        <h1 style="margin:0; font-family:'Helvetica', sans-serif; font-weight:900; font-size:3rem; letter-spacing:-2px; color:#fff; line-height: 1;">
            AGROWER <span style="color:#a855f7;">SDI</span>
        </h1>
        <div style="font-size:0.9rem; letter-spacing:3px; color:#d8b4fe; margin-top:5px; font-weight:600; opacity:0.9;">
            SISTEMA DE DECISÃO INTEGRADA
        </div>
    </div>
    <div style="text-align:right;">
         <div style="background:rgba(34, 197, 94, 0.1); border:1px solid #22c55e; color:#4ade80; padding:5px 15px; border-radius:20px; font-size:0.8rem; display:inline-flex; align-items:center; gap:8px;">
            🤖 AI ASSISTANT ACTIVE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

ticker_html = """
<div class="ticker-container">
    <div class="ticker-text">
        <span class="tick-item">VEG: <span class="tick-val">24°C / 65% UR</span></span>
        <span class="tick-item">FLORA: <span class="tick-val">22°C / 45% UR</span></span>
        <span class="tick-item">SECAGEM: <span class="tick-val">18°C / 60% UR</span></span>
        <span class="tick-item">VPD IDEAL: <span class="tick-val">0.8-1.2 kPa</span></span>
        <span class="tick-item">EC FLORA: <span class="tick-val">1.8-2.4 mS</span></span>
        <span class="tick-item">PH SOLO: <span class="tick-val">6.2-6.5</span></span>
    </div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# ==============================================================================
# 🎛️ DASHBOARD SDI (O CORE DO SISTEMA)
# ==============================================================================

with st.container():
    st.markdown("""<div class="sdi-title">🎛️ CONFIGURAÇÃO DO CULTIVO (INPUT)</div>""", unsafe_allow_html=True)
    
    # Inputs Profissionais em Grid
    c_in1, c_in2, c_in3, c_in4 = st.columns(4)
    
    with c_in1:
        ambiente = st.selectbox("Ambiente:", ["Indoor (Estufa)", "Outdoor (Sol)", "Greenhouse"])
    with c_in2:
        metodo = st.selectbox("Método:", list(db["METODOS_CULTIVO"].keys()))
    with c_in3:
        data_inicio = st.date_input("Data de Início (Germinação):", datetime.date.today() - datetime.timedelta(days=21))
    with c_in4:
        n_plantas = st.number_input("Nº de Plantas:", min_value=1, value=4)

    # --- CÁLCULO AUTOMÁTICO DA FASE (LÓGICA SDI) ---
    hoje = datetime.date.today()
    dias_vida = (hoje - data_inicio).days
    semanas_vida = dias_vida // 7
    
    # Determinação da Fase
    fase_atual = "Indefinida"
    dados_fase = {}
    
    if dias_vida <= 14: fase_atual = "Plântula (Semana 1-2)"
    elif dias_vida <= 42: fase_atual = "Vegetativo (Semana 3-6)"
    elif dias_vida <= 56: fase_atual = "Pré-Flora (Semana 7-8)"
    elif dias_vida <= 77: fase_atual = "Flora Inicial (Semana 9-11)"
    else: fase_atual = "Flora Final/Engorda (Semana 12+)"
    
    # Pega dados da fase no DB
    fases_db = db.get("FASES_DINAMICAS", {})
    # Fallback simples caso a string exata mude, pega a chave que contem a string
    for chave, valor in fases_db.items():
        if fase_atual.split("(")[0].strip() in chave:
            dados_fase = valor
            fase_atual = chave # Ajusta nome
            break
            
    # --- OUTPUT VISUAL DO DASHBOARD ---
    st.markdown("---")
    st.markdown(f"""<div class="sdi-title">📊 STATUS ATUAL: <span style="color:#a855f7;">{fase_atual.upper()}</span></div>""", unsafe_allow_html=True)
    
    col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
    
    with col_d1:
        st.markdown(f"""
        <div class="sdi-metric-box">
            <div class="sdi-val" style="color:#22c55e;">Dia {dias_vida}</div>
            <div class="sdi-lbl">Tempo de Cultivo</div>
        </div>
        <div class="sdi-metric-box" style="margin-top:10px;">
            <div class="sdi-val">{semanas_vida}ª</div>
            <div class="sdi-lbl">Semana</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_d2:
        # Card de Decisão / Instrução da Fase
        if dados_fase:
            riscos_html = "".join([f"<span style='background:#330a0a; color:#fca5a5; padding:2px 6px; border-radius:4px; font-size:0.8rem; margin-right:5px; border:1px solid #7f1d1d;'>⚠️ {r}</span>" for r in dados_fase['riscos']])
            st.markdown(f"""
            <div class="tech-card" style="border-left: 4px solid #38bdf8; height: 100%;">
                <div class="tech-header">🎯 FOCO DA SEMANA: {dados_fase['foco']}</div>
                <div style="color:#ccc; font-size:0.95rem; margin-bottom:10px;">{dados_fase['obs']}</div>
                <div style="margin-top:15px;">
                    <div style="font-size:0.75rem; color:#888; margin-bottom:5px; text-transform:uppercase;">Riscos Iminentes (Monitorar):</div>
                    {riscos_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_d3:
        # Metas Ambientais (Simuladas baseadas na fase)
        temp_target = "24-26°C" if "Veg" in fase_atual or "Plântula" in fase_atual else "20-24°C"
        humid_target = "60-70%" if "Veg" in fase_atual or "Plântula" in fase_atual else "40-50%"
        
        st.markdown(f"""
        <div class="sdi-metric-box">
            <div style="color:#38bdf8; font-weight:bold;">{temp_target}</div>
            <div class="sdi-lbl">Meta Temp</div>
        </div>
        <div class="sdi-metric-box" style="margin-top:10px;">
            <div style="color:#38bdf8; font-weight:bold;">{humid_target}</div>
            <div class="sdi-lbl">Meta Umidade</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 📑 CONTEÚDO TÉCNICO
# ==============================================================================

st.markdown("<br>", unsafe_allow_html=True)
tab_cultivo, tab_doctor = st.tabs(["📘 ENCICLOPÉDIA DE CULTIVO", "🛡️ DOCTOR GROW (PRAGAS & DOENÇAS)"])

# --- ABA 1: CULTIVO (DETALHADO POR MÉTODO) ---
with tab_cultivo:
    # Mostra primeiro o método selecionado no Dashboard
    dados_metodo = db["METODOS_CULTIVO"][metodo]
    
    st.markdown(f"### 🥣 Guia do Método: <span style='color:#a855f7'>{metodo}</span>", unsafe_allow_html=True)
    
    c_receita, c_params = st.columns([1.5, 1])
    
    with c_receita:
        st.markdown("""<div class="tech-card">""", unsafe_allow_html=True)
        st.markdown("#### 🧪 Receita de Substrato / Preparo")
        for item in dados_metodo['substrato_receita']:
            st.markdown(f"- {item}")
        st.markdown(f"<br><b>🥪 Nutrição:</b> {dados_metodo['nutricao']}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c_params:
        st.markdown(f"""
        <div class="tech-card">
            <div class="tech-header">📊 Parâmetros Chave</div>
            <div style="margin-bottom:10px;">
                <span style="color:#888; font-size:0.8rem;">PH IDEAL</span><br>
                <span style="font-size:1.2rem; font-weight:bold; color:#fff;">{dados_metodo['ph_ideal']}</span>
            </div>
             <div>
                <span style="color:#888; font-size:0.8rem;">EC (CONDUTIVIDADE)</span><br>
                <span style="font-size:1.2rem; font-weight:bold; color:#fff;">{dados_metodo['ec_ideal']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📚 Ver outros métodos de cultivo"):
        for m_nome, m_dados in db["METODOS_CULTIVO"].items():
            if m_nome != metodo:
                st.markdown(f"**{m_nome}:** {m_dados['descricao']}")

# --- ABA 2: DOCTOR GROW (MASTER IPM) ---
with tab_doctor:
    st.markdown("### 🚑 Clínica de Pragas & Doenças")
    st.caption("Base de dados completa com controle Biológico (Orgânico) e Químico.")
    
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        busca_doc = st.text_input("🔍 Buscar Problema (Ex: Ácaro, Oídio):")
    with col_filter:
        filtro_doc = st.selectbox("Filtrar:", ["Todos", "Pragas", "Doenças"])
    
    doc_db = db["DOCTOR_GROW_MASTER"]
    
    # Processamento da Lista
    lista_problemas = []
    if filtro_doc in ["Todos", "Pragas"]:
        for k, v in doc_db["Pragas"].items(): v['nome'] = k; v['tipo'] = 'Praga'; lista_problemas.append(v)
    if filtro_doc in ["Todos", "Doenças"]:
        for k, v in doc_db["Doencas"].items(): v['nome'] = k; v['tipo'] = 'Doença'; lista_problemas.append(v)
        
    # Exibição
    found = False
    for prob in lista_problemas:
        if busca_doc and busca_doc.lower() not in prob['nome'].lower(): continue
        found = True
        
        # Cor da borda baseada na gravidade
        border_color = "#333"
        if "ALTA" in prob['gravidade'] or "CRÍTICA" in prob['gravidade']: border_color = "#ef4444"
        
        st.markdown(f"""
        <div class="doc-card" style="border-left: 5px solid {border_color};">
            <div style="display:flex; justify-content:space-between;">
                <h4 style="color:#fff; margin:0;">{prob['nome']}</h4>
                <span style="font-size:0.7rem; background:#222; padding:2px 8px; border-radius:10px;">{prob['gravidade']}</span>
            </div>
            <p style="color:#ccc; font-size:0.95rem; margin-top:5px;"><i>{prob['identificacao']}</i></p>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-top:10px;">
                <div style="background:#0a1a10; padding:10px; border-radius:6px; border:1px solid #14532d;">
                    <div style="color:#86efac; font-weight:bold; font-size:0.85rem; margin-bottom:5px;">🌿 CONTROLE ORGÂNICO</div>
                    {''.join([f'<div style="font-size:0.85rem; color:#bbf7d0;">• {s}</div>' for s in prob['controle_organico']])}
                </div>
                <div style="background:#2b0e0e; padding:10px; border-radius:6px; border:1px solid #7f1d1d;">
                    <div style="color:#fca5a5; font-weight:bold; font-size:0.85rem; margin-bottom:5px;">🧪 CONTROLE QUÍMICO</div>
                    {''.join([f'<div style="font-size:0.85rem; color:#fecaca;">• {s}</div>' for s in prob['controle_quimico']])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not found: st.info("Nenhum problema encontrado com esse nome.")
