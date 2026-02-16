# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | V7.0 (NUTRIÇÃO PRECISION)
import streamlit as st
import datetime
import plotly.graph_objects as go
from core_logic import AgroEngine 

# --- 1. SETUP ---
st.set_page_config(page_title="Agrower SDI", page_icon="🍁", layout="wide", initial_sidebar_state="collapsed")
engine = AgroEngine()
db = engine.db 

# --- 2. CSS PROFISSIONAL ---
def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=JetBrains+Mono:wght@400;700&display=swap');
        .stApp { background-color: #050505; color: #e4e4e7; font-family: 'Inter', sans-serif; }
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }
        
        /* HEADER HERO */
        .hero-container {
            background: linear-gradient(135deg, #1e1b4b 0%, #000000 90%);
            border-bottom: 2px solid #a855f7; padding: 30px 40px; border-radius: 0 0 15px 15px;
            margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 10px 40px rgba(168, 85, 247, 0.2);
        }
        .hero-title { font-size: 3.5rem; font-weight: 900; color: #fff; line-height: 1; white-space: nowrap; text-shadow: 0 0 20px rgba(168, 85, 247, 0.6); }
        .hero-subtitle { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: #d8b4fe; letter-spacing: 4px; margin-top: 5px; text-transform: uppercase; }
        .status-badge { background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #4ade80; padding: 8px 20px; border-radius: 30px; font-weight: bold; font-size: 0.9rem; display: flex; align-items: center; gap: 10px; }

        /* CARDS */
        .glass-panel { background: #111; border: 1px solid #27272a; border-radius: 12px; padding: 24px; margin-bottom: 16px; }
        .yield-card { background: linear-gradient(135deg, #422006 0%, #000 100%); border: 1px solid #eab308; border-radius: 12px; padding: 20px; text-align: center; color: #fef08a; }
        
        /* DOCTOR CARDS */
        .doc-card { background: #0f0f0f; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #333; }
        .doc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .doc-title { font-size: 1.2rem; font-weight: bold; color: #fff; }
        .doc-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
        
        .solucao-tag { padding: 6px 12px; border-radius: 6px; font-size: 0.85rem; margin-bottom: 5px; display: block; }
        .bio { background: rgba(34, 197, 94, 0.1); border: 1px solid #15803d; color: #86efac; }
        .quim { background: rgba(239, 68, 68, 0.1); border: 1px solid #991b1b; color: #fca5a5; }

        /* INPUTS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div { background-color: #0f0f0f !important; border: 1px solid #333 !important; color: #fff !important; }
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. HEADER & TICKER ---
st.markdown("""
<div class="hero-container">
    <div>
        <div class="hero-title">AGROWER <span style="color:#a855f7">SDI</span></div>
        <div class="hero-subtitle">SISTEMA DE DECISÃO INTEGRADA</div>
    </div>
    <div><div class="status-badge"><span style="font-size:1.3rem;">🍁</span> SISTEMA ONLINE</div></div>
</div>
""", unsafe_allow_html=True)

# Ticker HTML (Omitido para economizar espaço, mas pode manter o anterior)

# ==============================================================================
# 🎮 DASHBOARD
# ==============================================================================
c1, c2, c3, c4 = st.columns([1.5, 1.5, 1, 1])
with c1: metodo_sel = st.selectbox("MÉTODO DE CULTIVO", list(db.get("METODOS_CULTIVO", {}).keys()))
with c2: genetica_sel = st.selectbox("GENÉTICA", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
with c3: n_plantas = st.number_input("Nº PLANTAS", 1, 500, 6)
with c4: data_inicio = st.date_input("INÍCIO CULTIVO", datetime.date.today() - datetime.timedelta(days=45))

# Cálculos Engine
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7
yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas
fase_nome = "Indefinida"
fase_dados = {}
for k, v in db.get("FASES_DINAMICAS", {}).items():
    if dias_vida <= {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}.get(k.split(' ')[0], 200):
        fase_nome = k; fase_dados = v; break

# STATUS & YIELD CARDS (MANTIDOS IGUAIS AO ANTERIOR)
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns([2, 1])
with col_a:
    st.markdown(f"""
    <div class="glass-panel" style="border-left: 4px solid #a855f7;">
        <div style="display:flex; justify-content:space-between;">
            <div><div style="color:#a855f7; font-weight:bold;">FASE ATUAL</div><div style="font-size:2.2rem; font-weight:900; color:#fff;">{fase_nome.upper()}</div></div>
            <div style="text-align:right;"><div style="font-size:2rem; font-weight:bold; color:#d8b4fe;">{dias_vida} DIAS</div></div>
        </div>
        <hr style="border-color:#333; opacity:0.5;">
        <div style="font-size:1.1rem; color:#fff; font-weight:600;">🎯 FOCO: {fase_dados.get('foco', '-')}</div>
        <div style="color:#a1a1aa; margin-top:5px;">{fase_dados.get('obs', '-')}</div>
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""
    <div class="yield-card">
        <div style="color:#ca8a04; font-weight:bold;">ESTIMATIVA COLHEITA</div>
        <div style="font-size:3rem; font-weight:900; color:#fef08a;">{yield_total:.0f}g</div>
        <div style="font-size:0.9rem; color:#fde047;">~ {yield_total/1000:.2f} kg (Seco)</div>
    </div>""", unsafe_allow_html=True)

# ==============================================================================
# 🎛️ NOVAS ABAS: NUTRIÇÃO & DOCTOR FITO
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
tab_nutri, tab_doctor = st.tabs(["🧪 NUTRIÇÃO & ABSORÇÃO", "🚑 DOCTOR GROW (FITOSSANIDADE)"])

# --- ABA 1: NUTRIÇÃO PRECISION (GRÁFICOS) ---
with tab_nutri:
    st.markdown("### 📊 Marcha de Absorção de Nutrientes")
    st.caption("Entenda o que a planta consome em cada semana para ajustar seu fertilizante.")
    
    nutri_data = db["NUTRI_MARCHA_ABSORCAO"]
    
    # 1. Gráfico MACRO (N-P-K)
    fig_macro = go.Figure()
    fig_macro.add_trace(go.Scatter(x=nutri_data['semanas'], y=nutri_data['N'], mode='lines+markers', name='Nitrogênio (N)', line=dict(color='#22c55e', width=3)))
    fig_macro.add_trace(go.Scatter(x=nutri_data['semanas'], y=nutri_data['P'], mode='lines+markers', name='Fósforo (P)', line=dict(color='#3b82f6', width=3)))
    fig_macro.add_trace(go.Scatter(x=nutri_data['semanas'], y=nutri_data['K'], mode='lines+markers', name='Potássio (K)', line=dict(color='#a855f7', width=3)))
    
    fig_macro.update_layout(
        title="MACRONUTRIENTES (Demanda %)",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#ccc"), xaxis=dict(title="Semanas", showgrid=False), yaxis=dict(title="Demanda Relativa", showgrid=True, gridcolor='#333'),
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig_macro, use_container_width=True)
    
    # 2. Guia de Deficiências
    st.markdown("---")
    st.markdown("#### 🔍 Diagnóstico Visual de Nutrientes")
    
    cols_def = st.columns(4)
    defs = list(db["DEFICIENCIAS_VISUAIS"].items())
    
    for i, (nome, dados) in enumerate(defs):
        with cols_def[i % 4]:
            st.markdown(f"""
            <div style="background:#18181b; border:1px solid #333; padding:15px; border-radius:8px; height:100%;">
                <div style="color:#facc15; font-weight:bold; margin-bottom:5px;">{nome}</div>
                <div style="font-size:0.85rem; color:#ccc; margin-bottom:10px;">{dados['sintoma']}</div>
                <div style="font-size:0.8rem; color:#a855f7; font-weight:bold;">SOLUÇÃO:</div>
                <div style="font-size:0.8rem; color:#888;">{dados['correcao']}</div>
            </div>
            """, unsafe_allow_html=True)

# --- ABA 2: DOCTOR GROW (FITOSSANIDADE) ---
with tab_doctor:
    st.markdown("### 🕷️ Pragas, Fungos e Insetos")
    c_search, c_filter = st.columns([3, 1])
    with c_search: busca = st.text_input("Buscar Praga:")
    
    db_fito = db["DOCTOR_GROW_FITOSSANIDADE"]
    
    # Grid de Cards Profissionais
    for nome, info in db_fito.items():
        if busca and busca.lower() not in nome.lower(): continue
        
        # Cor da Gravidade
        cor_gravidade = "#3b82f6" # Azul (Baixa)
        if info['gravidade'] == "MÉDIA": cor_gravidade = "#eab308"
        if info['gravidade'] == "ALTA": cor_gravidade = "#f97316"
        if info['gravidade'] == "CRÍTICA" or info['gravidade'] == "FATAL": cor_gravidade = "#ef4444"
        
        st.markdown(f"""
        <div class="doc-card" style="border-left-color: {cor_gravidade};">
            <div class="doc-header">
                <div class="doc-title">{nome}</div>
                <div class="doc-badge" style="background:{cor_gravidade}20; color:{cor_gravidade}; border:1px solid {cor_gravidade};">{info['gravidade']}</div>
            </div>
            <div style="color:#ccc; font-size:0.95rem; margin-bottom:10px;"><i>{info['sintomas']}</i></div>
            <div style="font-size:0.85rem; color:#888; margin-bottom:15px;">⚠️ {info['obs']}</div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <div>
                    <div style="font-size:0.75rem; color:#4ade80; font-weight:bold; margin-bottom:5px;">BIO / ORGÂNICO</div>
                    {''.join([f'<span class="solucao-tag bio">• {s}</span>' for s in info['bio']])}
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#f87171; font-weight:bold; margin-bottom:5px;">QUÍMICO / SOS</div>
                    {''.join([f'<span class="solucao-tag quim">• {s}</span>' for s in info['quimico']])}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
