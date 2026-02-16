# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | PRO VISUAL V7.0
import streamlit as st
import datetime
from core_logic import AgroEngine 

# --- 1. SETUP ---
st.set_page_config(page_title="Agrower SDI", page_icon="🍁", layout="wide", initial_sidebar_state="collapsed")
engine = AgroEngine()
db = engine.db 

# --- 2. CSS MONSTRUOSO (NEON & GLASS) ---
def load_css():
    st.markdown("""
        <style>
        /* IMPORT FONTES MODERNAS */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* FUNDO GERAL */
        .stApp { 
            background-color: #050505; 
            color: #e4e4e7; 
            font-family: 'Inter', sans-serif;
        }
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }

        /* --- HEADER HERO (CAPA PROFISSIONAL) --- */
        .hero-container {
            background: linear-gradient(135deg, #1e1b4b 0%, #000000 90%); /* Roxo Profundo para Preto */
            border-bottom: 2px solid #a855f7; /* Linha Neon Roxa */
            padding: 30px 40px;
            border-radius: 0 0 15px 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 40px rgba(168, 85, 247, 0.2); /* Glow Roxo */
        }
        
        .hero-title {
            font-size: 3.5rem; 
            font-weight: 900; 
            color: #fff; 
            line-height: 1; 
            white-space: nowrap; /* Título numa linha só */
            text-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
        }
        
        .hero-subtitle {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #d8b4fe;
            letter-spacing: 4px;
            margin-top: 5px;
            text-transform: uppercase;
        }
        
        /* BADGE ONLINE (COM FOLHA) */
        .status-badge {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid #10b981;
            color: #4ade80;
            padding: 8px 20px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
        }

        /* --- TICKER BLOOMBERG --- */
        .ticker-wrap {
            width: 100%; overflow: hidden; background-color: #000; border-top: 1px solid #333; border-bottom: 1px solid #333;
            height: 40px; display: flex; align-items: center; margin-bottom: 30px;
        }
        .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; }
        @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .tick-item { margin-right: 50px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #a855f7; }
        .tick-val { color: #fff; margin-left: 5px; }

        /* --- CARDS & PAINEIS --- */
        .glass-panel {
            background: #111; border: 1px solid #27272a; border-radius: 12px; padding: 24px;
            margin-bottom: 16px; transition: transform 0.2s; position: relative;
        }
        .glass-panel:hover { border-color: #a855f7; box-shadow: 0 0 20px rgba(168, 85, 247, 0.1); }
        
        /* Yield Card Dourado */
        .yield-card {
            background: linear-gradient(135deg, #422006 0%, #000 100%);
            border: 1px solid #eab308; border-radius: 12px; padding: 20px;
            text-align: center; color: #fef08a; box-shadow: 0 0 15px rgba(234, 179, 8, 0.2);
        }

        /* Doctor Grow Cards */
        .doc-card-container {
            background: #0f0f0f; border: 1px solid #333; border-radius: 10px; padding: 15px; margin-bottom: 15px;
        }
        .doc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #222; padding-bottom: 10px; }
        .doc-title { font-size: 1.2rem; font-weight: bold; color: #fff; }
        .doc-type { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #888; }
        
        .solucao-box { padding: 8px; border-radius: 6px; margin-bottom: 5px; font-size: 0.85rem; }
        .bio-box { background: rgba(34, 197, 94, 0.1); border: 1px solid #15803d; color: #86efac; }
        .quim-box { background: rgba(239, 68, 68, 0.1); border: 1px solid #991b1b; color: #fca5a5; }

        /* INPUTS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div {
            background-color: #0f0f0f !important; border: 1px solid #333 !important; color: #fff !important;
        }
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. CAPA PROFISSIONAL (FIXED) ---
st.markdown("""
<div class="hero-container">
    <div>
        <div class="hero-title">AGROWER <span style="color:#a855f7">SDI</span></div>
        <div class="hero-subtitle">SISTEMA DE DECISÃO INTEGRADA</div>
    </div>
    <div>
        <div class="status-badge">
            <span style="font-size:1.3rem;">🍁</span> SISTEMA ONLINE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. TICKER BLOOMBERG (VOLTOU!) ---
st.markdown("""
<div class="ticker-wrap">
    <div class="ticker-move">
        <span class="tick-item">VPD IDEAL <span class="tick-val">0.8-1.2 kPa</span></span>
        <span class="tick-item">TEMP FLORA <span class="tick-val">22-25°C</span></span>
        <span class="tick-item">UMIDADE FLORA <span class="tick-val">45-50%</span></span>
        <span class="tick-item">PPFD <span class="tick-val">800-1000 µmol</span></span>
        <span class="tick-item">PH SOLO <span class="tick-val">6.2-6.5</span></span>
        <span class="tick-item">EC FLORA <span class="tick-val">1.8-2.4 mS</span></span>
        <span class="tick-item">CO2 <span class="tick-val">800-1200 ppm</span></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🎮 DASHBOARD (INPUTS & STATUS)
# ==============================================================================

# Inputs Limpos
c1, c2, c3, c4 = st.columns([1.5, 1.5, 1, 1])
with c1: metodo_sel = st.selectbox("MÉTODO DE CULTIVO", list(db.get("METODOS_CULTIVO", {}).keys()))
with c2: genetica_sel = st.selectbox("GENÉTICA", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
with c3: n_plantas = st.number_input("Nº PLANTAS", 1, 500, 6)
with c4: data_inicio = st.date_input("INÍCIO CULTIVO", datetime.date.today() - datetime.timedelta(days=45))

# --- CÁLCULOS SDI ---
# 1. Dados
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]

# 2. Tempo
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# 3. Yield (Dourado)
yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas
yield_kg = yield_total / 1000

# 4. Fase Dinâmica
fase_nome = "Indefinida"
fase_dados = {}
for k, v in db.get("FASES_DINAMICAS", {}).items():
    range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
    chave_limpa = k.split(' ')[0] # Pega "Plântula" de "Plântula (Semana 1-2)" (se houver parenteses)
    # Ajuste para nomes limpos do novo DB
    if dias_vida <= range_map.get(k, 200):
        fase_nome = k; fase_dados = v; break

# --- VISUAL DASHBOARD ---
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns([2, 1])

with col_a:
    # Card Principal Roxo
    st.markdown(f"""
    <div class="glass-panel" style="border-left: 4px solid #a855f7;">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div style="color:#a855f7; font-size:0.8rem; font-weight:bold; letter-spacing:1px; margin-bottom:5px;">STATUS ATUAL</div>
                <div style="font-size:2.5rem; font-weight:900; color:#fff; line-height:1;">{fase_nome.upper()}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:2rem; font-weight:bold; color:#d8b4fe;">{dias_vida} <span style="font-size:1rem; color:#888;">DIAS</span></div>
                <div style="font-size:0.9rem; color:#a855f7;">SEMANA {semanas}</div>
            </div>
        </div>
        <hr style="border-color:#333; opacity:0.5; margin:20px 0;">
        <div style="font-size:1.1rem; color:#fff; font-weight:600;">🎯 FOCO: {fase_dados.get('foco', '-')}</div>
        <div style="color:#a1a1aa; font-size:0.95rem; margin-top:5px;">{fase_dados.get('obs', '-')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    # Card Yield Dourado
    st.markdown(f"""
    <div class="yield-card">
        <div style="color:#ca8a04; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">ESTIMATIVA COLHEITA</div>
        <div style="font-size:3rem; font-weight:900; color:#fef08a; margin:10px 0;">{yield_total:.0f}g</div>
        <div style="font-size:0.9rem; color:#fde047; opacity:0.9;">~ {yield_kg:.2f} kg (Seco)</div>
        <div style="margin-top:15px; font-size:0.75rem; color:#eab308; border-top:1px solid rgba(234,179,8,0.3); padding-top:10px;">
            BASE: {n_plantas} plantas | {info_metodo['rendimento_base']}g/un
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🛡️ DOCTOR GROW (PROFISSIONAL & VISUAL)
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🚑 DOCTOR GROW (ENCICLOPÉDIA)")

col_busca, col_filtro = st.columns([3, 1])
with col_busca: busca = st.text_input("🔍 Buscar Sintoma (Ex: Raiz, Mancha, Folha Amarela):")
with col_filtro: filtro = st.selectbox("Filtrar:", ["Todos", "Pragas", "Doenças", "Nutrição"])

# Lógica de Exibição em Grid
db_doc = db["DOCTOR_GROW_MASTER"]

for nome, info in db_doc.items():
    # Filtros
    if busca and busca.lower() not in nome.lower() and busca.lower() not in info['sintomas'].lower(): continue
    if filtro != "Todos" and filtro.lower() not in info['tipo'].lower(): continue

    # Layout do Card Profissional
    with st.expander(f"{nome} | {info['tipo']}", expanded=False):
        c_img, c_info = st.columns([1, 2])
        
        with c_img:
            # Placeholder para foto (Usuario pode substituir URL no DB)
            if 'img_placeholder' in info:
                st.image(info['img_placeholder'], use_container_width=True)
            else:
                st.markdown(f"<div style='height:150px; background:#111; display:flex; align-items:center; justify-content:center; color:#333; border:1px dashed #444;'>[FOTO: {nome}]</div>", unsafe_allow_html=True)
        
        with c_info:
            st.markdown(f"**🕵️ Sintomas:** {info['sintomas']}")
            st.markdown("---")
            
            c_bio, c_quim = st.columns(2)
            with c_bio:
                st.markdown("<div style='color:#4ade80; font-weight:bold; font-size:0.9rem; margin-bottom:5px;'>🌿 BIO / ORGÂNICO</div>", unsafe_allow_html=True)
                for item in info['bio']:
                    st.markdown(f"<div class='solucao-box bio-box'>• {item}</div>", unsafe_allow_html=True)
            
            with c_quim:
                st.markdown("<div style='color:#f87171; font-weight:bold; font-size:0.9rem; margin-bottom:5px;'>🧪 QUÍMICO / SOS</div>", unsafe_allow_html=True)
                for item in info['quimico']:
                    st.markdown(f"<div class='solucao-box quim-box'>• {item}</div>", unsafe_allow_html=True)
