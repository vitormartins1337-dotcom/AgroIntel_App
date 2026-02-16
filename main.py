# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | VISUAL NEON PRO (RESTORED & FIXED)
import streamlit as st
import datetime
from core_logic import AgroEngine 

# --- 1. SETUP ---
st.set_page_config(page_title="Agrower SDI", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")
engine = AgroEngine()
db = engine.db 

# --- 2. CSS NEON PROFISSIONAL (CORRIGIDO) ---
def load_css():
    st.markdown("""
        <style>
        /* BASE DARK */
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }
        .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Roboto', sans-serif; }
        
        /* HEADER (CAPA) ROXO NEON */
        .header-box {
            background: linear-gradient(90deg, #240b36 0%, #000000 100%);
            border-bottom: 2px solid #a855f7;
            padding: 30px; border-radius: 0 0 20px 20px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 0 25px rgba(168, 85, 247, 0.2); margin-bottom: 20px;
        }

        /* TICKER BLOOMBERG STYLE */
        .ticker-container {
            width: 100%; background: #000; border: 1px solid #333; border-radius: 6px;
            overflow: hidden; white-space: nowrap; height: 32px; display: flex; align-items: center; margin-bottom: 15px;
        }
        .ticker-text { display: inline-block; animation: ticker 40s linear infinite; font-family: 'Courier New', monospace; font-weight: bold; font-size: 0.85rem;}
        @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .tick-item { margin-right: 40px; color: #a855f7; } .tick-val { color: #22c55e; }

        /* CARDS DE VIDRO (GLASSMORPHISM) */
        .glass-card {
            background: rgba(20, 20, 20, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.3); /* Borda Roxa Sutil */
            padding: 20px; border-radius: 12px; margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        /* YIELD CARD (DESTAQUE DOURADO) */
        .yield-card {
            background: linear-gradient(135deg, #1a1200 0%, #000 100%);
            border: 1px solid #eab308; border-radius: 12px; padding: 20px;
            text-align: center; color: #fef08a; box-shadow: 0 0 15px rgba(234, 179, 8, 0.2);
        }

        /* BADGES (BALÕES) - AGORA COM NO-WRAP PARA NÃO QUEBRAR */
        .badge-param {
            display: inline-block; white-space: nowrap; /* O SEGREDO */
            background: #111; border: 1px solid #333; color: #fff;
            padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;
            margin-right: 8px; margin-bottom: 5px;
        }
        .badge-purple { border-color: #a855f7; color: #d8b4fe; }
        .badge-green { border-color: #22c55e; color: #4ade80; }
        .badge-blue { border-color: #38bdf8; color: #bae6fd; }

        /* INPUTS ESTILIZADOS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div {
            background-color: #0f0f0f !important; border: 1px solid #333 !important; color: #fff !important;
        }
        
        /* ABAS */
        .stTabs [data-baseweb="tab-list"] { gap: 5px; }
        .stTabs [data-baseweb="tab"] { background-color: #111; border: 1px solid #333; color: #888; }
        .stTabs [aria-selected="true"] { background-color: #a855f7 !important; color: #fff !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. HEADER PROFISSIONAL (VOLTA DO ROXO NEON) ---
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
        <div style="background:rgba(168, 85, 247, 0.2); border:1px solid #a855f7; color:#d8b4fe; padding:6px 16px; border-radius:30px; font-size:0.8rem; display:inline-flex; align-items:center; gap:8px;">
            🧬 GENETICS LAB
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Ticker Bloomberg Style
st.markdown("""
<div class="ticker-container">
    <div class="ticker-text">
        <span class="tick-item">VEG TEMP: <span class="tick-val">24°C</span></span>
        <span class="tick-item">VEG UMIDADE: <span class="tick-val">65%</span></span>
        <span class="tick-item">FLORA TEMP: <span class="tick-val">22°C</span></span>
        <span class="tick-item">FLORA UMIDADE: <span class="tick-val">45%</span></span>
        <span class="tick-item">VPD IDEAL: <span class="tick-val">0.8-1.2 kPa</span></span>
        <span class="tick-item">EC FLORA: <span class="tick-val">1.8-2.4 mS</span></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🎮 CONFIGURAÇÃO E CÁLCULOS (O CÉREBRO)
# ==============================================================================

# Inputs (Grid Layout)
c1, c2, c3, c4 = st.columns([1.5, 1.5, 1, 1])

with c1:
    metodo_keys = list(db.get("METODOS_CULTIVO", {}).keys())
    metodo_sel = st.selectbox("🥣 MÉTODO CULTIVO", metodo_keys)
    
with c2:
    # AQUI ESTAVA O ERRO: Agora a chave existe no DB
    genetica_keys = list(db.get("GENETICAS_PARAMETROS", {}).keys())
    genetica_sel = st.selectbox("🧬 GENÉTICA", genetica_keys)

with c3:
    n_plantas = st.number_input("🌳 Nº PLANTAS", 1, 500, 6)

with c4:
    data_inicio = st.date_input("📅 INÍCIO", datetime.date.today() - datetime.timedelta(days=45))

# --- CÁLCULOS AUTOMÁTICOS ---
# 1. Dados
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]

# 2. Tempo
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# 3. Yield Estimado
rendimento_base = info_metodo['rendimento_base']
fator_gen = info_genetica['fator_yield']
yield_total = rendimento_base * fator_gen * n_plantas
yield_kg = yield_total / 1000

# 4. Fase Dinâmica
fase_nome = "Indefinida"
fase_dados = {}
for k, v in db.get("FASES_DINAMICAS", {}).items():
    range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
    chave_limpa = k.split(' ')[0]
    if dias_vida <= range_map.get(chave_limpa, 200):
        fase_nome = k; fase_dados = v; break

# ==============================================================================
# 📊 DASHBOARD PRINCIPAL (VISUAL NEON RESTAURADO)
# ==============================================================================

col_dash1, col_dash2 = st.columns([2, 1])

with col_dash1:
    # Card de Status Principal
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid #a855f7;">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div style="color:#a855f7; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">FASE ATUAL</div>
                <div style="font-size:2.2rem; font-weight:900; color:#fff; margin-bottom:10px;">{fase_nome.upper()}</div>
                <div>
                    <span class="badge-param">📅 {dias_vida} DIAS</span>
                    <span class="badge-param">📆 SEMANA {semanas}</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="color:#888; font-size:0.8rem; margin-bottom:5px;">METAS DA FASE</div>
                <div><span class="badge-param badge-blue">PH {info_metodo['ph_ideal']}</span></div>
                <div><span class="badge-param badge-green">EC {info_metodo['ec_ideal']}</span></div>
            </div>
        </div>
        <hr style="border-color:#333; opacity:0.5; margin:15px 0;">
        <div style="color:#d8b4fe; font-size:1.1rem; font-weight:bold;">🎯 FOCO: {fase_dados.get('foco','-')}</div>
        <div style="color:#ccc; font-size:0.9rem; margin-top:5px;">{fase_dados.get('obs','-')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_dash2:
    # Card de Yield Dourado
    st.markdown(f"""
    <div class="yield-card">
        <div style="color:#ca8a04; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">PREVISÃO COLHEITA</div>
        <div style="font-size:2.5rem; font-weight:900; color:#fef08a; margin:10px 0;">{yield_total:.0f}g</div>
        <div style="font-size:0.9rem; color:#fde047;">~ {yield_kg:.2f} kg (Seco)</div>
        <hr style="border-color:#ca8a04; opacity:0.3; margin:15px 0;">
        <div style="font-size:0.8rem; color:#eab308;">
            {n_plantas}x {genetica_sel.split(' ')[0]}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🛡️ RADAR DE MANEJO & DOCTOR GROW
# ==============================================================================

tab_radar, tab_doctor = st.tabs(["📡 RADAR DA SEMANA", "🚑 DOCTOR GROW (ENCICLOPÉDIA)"])

with tab_radar:
    st.markdown(f"### Ameaças Ativas: {fase_nome}")
    st.caption("Baseado na idade da planta, estas são as pragas e deficiências mais prováveis agora.")
    
    ameacas = fase_dados.get("ameacas", [])
    
    if not ameacas:
        st.success("Nenhuma ameaça crítica mapeada para esta fase. Mantenha o VPD estável.")
    else:
        # Busca detalhes no DB Doctor Grow
        db_doc = db["DOCTOR_GROW_MASTER"]
        
        for ameaca_nome in ameacas:
            # Lógica de busca no DB
            detalhes = None
            for nome_db, info in db_doc.items():
                if ameaca_nome in nome_db: # Busca parcial
                    detalhes = info
                    nome_exibicao = nome_db
                    break
            
            if detalhes:
                # Cor baseada no tipo
                cor_borda = "#ef4444" # Vermelho padrão
                icone = "🚨"
                if detalhes['tipo'] == "Nutrição": 
                    cor_borda = "#eab308"; icone = "🧪"
                elif detalhes['tipo'] == "Fungo":
                    cor_borda = "#a855f7"; icone = "🍄"

                # Card de Ameaça Integrado
                with st.expander(f"{icone} ALERTA: {nome_exibicao}", expanded=True):
                    c_a1, c_a2 = st.columns(2)
                    with c_a1:
                        st.markdown(f"**Identificação:** {detalhes['identificacao']}")
                        st.markdown(f"**Controle:** {detalhes['controle']}")
                    with c_a2:
                        st.markdown(f"**🛒 Produtos Sugeridos:**")
                        for p in detalhes['produtos']:
                            st.markdown(f"- {p}")
                    

with tab_doctor:
    st.markdown("### 📚 Banco de Dados Completo")
    busca = st.text_input("🔍 Pesquisar problema (Ex: Ácaro, Mofo, Nitrogênio):")
    
    db_full = db["DOCTOR_GROW_MASTER"]
    
    for nome, info in db_full.items():
        if busca and busca.lower() not in nome.lower(): continue
        
        with st.expander(f"{nome} ({info['tipo']})"):
            st.write(f"**ID:** {info['identificacao']}")
            st.write(f"**Controle:** {info['controle']}")
            st.write(f"**Produtos:** {', '.join(info['produtos'])}")
