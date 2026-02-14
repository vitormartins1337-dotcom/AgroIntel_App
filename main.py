# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | ULTIMATE EDITION (V.4.21 FIXED)
# DESCRIÇÃO: Interface Gráfica de Alta Performance com Plotly e CSS Avançado.

import streamlit as st
import datetime
import pandas as pd
import plotly.graph_objects as go
from core_logic import AgroEngine 

# --- 1. SETUP DE ALTA PERFORMANCE ---
st.set_page_config(
    page_title="Agrower SDI Pro", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializa Engine
engine = AgroEngine()
db = engine.db 

# --- 2. CSS "GLASSMORPHISM" & NEON ---
def load_pro_css():
    st.markdown("""
        <style>
        /* IMPORT FONT ROBOTO & MONTSERRAT */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;700;900&family=Roboto+Mono:wght@400;700&display=swap');

        /* FUNDO E ESTRUTURA */
        .stApp {
            background-color: #050505;
            background-image: radial-gradient(circle at 50% 0%, #1a0b2e 0%, #050505 60%);
            color: #e0e0e0;
            font-family: 'Montserrat', sans-serif;
        }
        
        /* REMOVER MARGENS PADRÃO */
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }
        
        /* HEADER PREMIUM */
        .header-container {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: 2px solid #a855f7;
            border-radius: 0 0 20px 20px;
            padding: 20px 40px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 30px;
        }
        .app-title {
            font-size: 3rem; font-weight: 900; letter-spacing: -2px; color: #fff;
            text-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
            line-height: 1;
        }
        .app-subtitle {
            font-family: 'Roboto Mono', monospace; font-size: 0.8rem; color: #d8b4fe; letter-spacing: 4px; margin-top: 5px;
        }

        /* TICKER BLOOMBERG STYLE */
        .ticker-box {
            background: #000; border: 1px solid #333; height: 36px; 
            overflow: hidden; white-space: nowrap; position: relative;
            display: flex; align-items: center; border-radius: 4px; margin-bottom: 20px;
        }
        .ticker-content {
            display: inline-block; animation: marquee 40s linear infinite;
            font-family: 'Roboto Mono', monospace; font-size: 0.85rem; font-weight: bold;
        }
        @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

        /* CARDS DE VIDRO (GLASS) */
        .glass-card {
            background: rgba(20, 20, 20, 0.7);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            border-color: #a855f7;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(168, 85, 247, 0.15);
        }
        
        /* TIPOGRAFIA TÉCNICA */
        .tech-label { font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
        .tech-value { font-size: 1.5rem; color: #f8fafc; font-weight: 700; }
        .highlight-purple { color: #c084fc; }
        .highlight-green { color: #4ade80; }
        .highlight-blue { color: #38bdf8; }

        /* INPUTS CUSTOMIZADOS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div, .stTextInput > div > div {
            background-color: #0f0f0f !important;
            border: 1px solid #333 !important;
            color: #fff !important;
            border-radius: 6px !important;
        }
        
        /* TABS FUTURISTAS */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #94a3b8;
            padding: 10px 25px;
            border-radius: 6px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #a855f7 !important;
            color: #fff !important;
            font-weight: 900;
            border: 1px solid #a855f7;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
        }
        
        /* GRÁFICOS PLOTLY TRANSPARENTES */
        .js-plotly-plot .plotly .main-svg { background: transparent !important; }
        </style>
    """, unsafe_allow_html=True)
load_pro_css()

# --- 3. HELPER FUNCTIONS (GRÁFICOS) ---
def create_gauge(val, min_v, max_v, title, suffix, color_hex):
    """Cria um mostrador (Gauge) estilo automotivo profissional"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = val,
        title = {'text': title, 'font': {'size': 14, 'color': "#888"}},
        number = {'suffix': suffix, 'font': {'size': 20, 'color': "white"}},
        gauge = {
            'axis': {'range': [min_v, max_v], 'tickwidth': 1, 'tickcolor': "#333"},
            'bar': {'color': color_hex},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [min_v, max_v], 'color': "rgba(255,255,255,0.05)"}
            ],
        }
    ))
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white", 'family': "Arial"}, height=150, margin=dict(l=20,r=20,t=30,b=20))
    return fig

# --- 4. HEADER MONSTRUOSO ---
st.markdown("""
<div class="header-container">
    <div>
        <div class="app-title">AGROWER <span style="color:#a855f7">SDI</span></div>
        <div class="app-subtitle">SYSTEM OF DECISION INTEGRATED | PRO V4.20</div>
    </div>
    <div style="text-align:right">
        <div style="background:rgba(34, 197, 94, 0.15); border:1px solid #22c55e; color:#4ade80; padding:8px 16px; border-radius:30px; font-size:0.8rem; font-weight:bold; display:flex; align-items:center; gap:8px;">
            <span style="height:8px; width:8px; background:#22c55e; border-radius:50%; box-shadow:0 0 10px #22c55e;"></span>
            LIVE SYSTEM
        </div>
        <div style="margin-top:5px; font-size:0.7rem; color:#64748b;">DATABASE: CONNECTED</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Ticker HTML
st.markdown("""
<div class="ticker-box">
    <div class="ticker-content">
        <span style="margin-right:40px; color:#d8b4fe;">📊 VPD IDEAL: <span style="color:#fff;">0.8 - 1.2 kPa</span></span>
        <span style="margin-right:40px; color:#d8b4fe;">🌡️ TEMP FLORA: <span style="color:#fff;">24°C</span></span>
        <span style="margin-right:40px; color:#d8b4fe;">💧 UMIDADE: <span style="color:#fff;">45% - 50%</span></span>
        <span style="margin-right:40px; color:#d8b4fe;">⚡ PPFD: <span style="color:#fff;">800 - 1000 µmol</span></span>
        <span style="margin-right:40px; color:#d8b4fe;">🧪 PH SOLO: <span style="color:#fff;">6.2 - 6.5</span></span>
        <span style="margin-right:40px; color:#d8b4fe;">🥥 PH COCO: <span style="color:#fff;">5.8 - 6.0</span></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🎮 COCKPIT DE CONTROLE (INPUTS & DASHBOARD)
# ==============================================================================

# Layout de Colunas para Inputs
c_conf1, c_conf2, c_conf3, c_conf4 = st.columns([1.5, 1.5, 1, 1])

with c_conf1:
    # Defesa contra erro de chave vazia
    db_metodos = db.get("METODOS_CULTIVO", {})
    metodo_keys = list(db_metodos.keys()) if db_metodos else ["Carregando..."]
    metodo_sel = st.selectbox("🥣 MÉTODO DE CULTIVO", metodo_keys)

with c_conf2:
    ambiente_sel = st.selectbox("🏠 AMBIENTE", ["Indoor (Estufa)", "Greenhouse", "Outdoor"])

with c_conf3:
    data_inicio = st.date_input("🌱 DATA GERMINAÇÃO", datetime.date.today() - datetime.timedelta(days=35))

with c_conf4:
    n_plantas = st.number_input("🌳 Nº PLANTAS", min_value=1, value=6)

# --- ENGINE LÓGICA (PROCESSAMENTO SDI) ---
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# Determinação de Fase Dinâmica
fase_nome = "Indefinida"
fase_dados = {}
fases_db = db.get("FASES_DINAMICAS", {})

# Lógica de Range de Dias para definir a fase
if dias_vida <= 14: chave_fase = "Plântula"
elif dias_vida <= 42: chave_fase = "Vegetativo"
elif dias_vida <= 56: chave_fase = "Pré-Flora"
elif dias_vida <= 77: chave_fase = "Flora Inicial"
else: chave_fase = "Flora Final"

# Busca no DB (Match parcial de string para robustez)
if fases_db:
    for k, v in fases_db.items():
        if chave_fase in k:
            fase_nome = k
            fase_dados = v
            break

# --- PAINEL VISUAL DE STATUS ---
st.markdown("---")
col_status1, col_status2 = st.columns([1, 2])

with col_status1:
    # Cartão de Tempo (Glassmorphism)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; height:100%; border-left:4px solid #a855f7;">
        <div class="tech-label">STATUS ATUAL</div>
        <div style="font-size:1.8rem; font-weight:900; color:#fff; margin:10px 0;">{fase_nome.upper().split('(')[0]}</div>
        <div style="display:flex; justify-content:space-around; margin-top:15px;">
            <div>
                <div class="tech-value highlight-purple">{dias_vida}</div>
                <div class="tech-label">DIAS</div>
            </div>
            <div>
                <div class="tech-value highlight-blue">{semanas}ª</div>
                <div class="tech-label">SEMANA</div>
            </div>
        </div>
        <div style="margin-top:15px; background:rgba(255,255,255,0.1); height:6px; border-radius:3px; overflow:hidden;">
            <div style="width: {min(dias_vida, 100)}%; background: #a855f7; height:100%;"></div>
        </div>
        <div class="tech-label" style="margin-top:5px; text-align:right;">PROGRESSO ESTIMADO</div>
    </div>
    """, unsafe_allow_html=True)

with col_status2:
    # Painel de Decisão Integrada (SDI)
    if fase_dados:
        foco = fase_dados.get('foco', 'Geral')
        obs = fase_dados.get('obs', 'Monitorar parâmetros.')
        riscos = fase_dados.get('riscos', [])
        
        # Renderiza Riscos como Tags
        riscos_html = "".join([f"<span style='background:#450a0a; border:1px solid #ef4444; color:#fca5a5; padding:4px 10px; border-radius:20px; font-size:0.75rem; margin-right:8px; font-weight:bold;'>☣️ {r}</span>" for r in riscos])
        
        st.markdown(f"""
        <div class="glass-card" style="height:100%;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                <span class="tech-label" style="color:#a855f7;">🎯 OBJETIVO TÁTICO DA SEMANA</span>
                <span class="tech-label">SISTEMA INTELIGENTE</span>
            </div>
            <div style="font-size:1.4rem; color:#fff; font-weight:bold; margin-bottom:10px;">{foco}</div>
            <div style="font-size:1rem; color:#cbd5e1; line-height:1.5; border-left:2px solid #333; padding-left:15px;">
                {obs}
            </div>
            <div style="margin-top:20px;">
                <div class="tech-label" style="margin-bottom:8px;">ALERTA DE RISCOS IMINENTES</div>
                {riscos_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 🎛️ FERRAMENTAS AVANÇADAS (TABS)
# ==============================================================================

st.markdown("<br>", unsafe_allow_html=True)
tab_cultivo, tab_vpd, tab_doctor = st.tabs(["📘 MANUAL DO CULTIVO", "🌡️ CONTROLE AMBIENTAL (VPD)", "🛡️ DOCTOR GROW"])

# --- TAB 1: CULTIVO POR MÉTODO ---
with tab_cultivo:
    # Dados do Método Selecionado
    info_metodo = db.get("METODOS_CULTIVO", {}).get(metodo_sel, {})
    
    if info_metodo:
        col_c1, col_c2 = st.columns([1.5, 1])
        
        with col_c1:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color:#a855f7; margin-top:0;">🥣 RECEITA: {metodo_sel.upper()}</h3>
                <p style="color:#ccc;">{info_metodo.get('descricao')}</p>
                <hr style="border-color:#333;">
                <h4 style="color:#4ade80;">🧪 Substrato & Preparo</h4>
            """, unsafe_allow_html=True)
            
            for item in info_metodo.get('substrato_receita', []):
                st.markdown(f"- {item}")
                
            st.markdown(f"""
                <br><h4 style="color:#38bdf8;">🥪 Nutrição Base</h4>
                <p>{info_metodo.get('nutricao')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_c2:
            # Cards de Parâmetros
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div class="tech-label">PH ALVO</div>
                <div class="tech-value highlight-blue">{info_metodo.get('ph_ideal')}</div>
            </div>
            <div class="glass-card" style="text-align:center;">
                <div class="tech-label">EC / PPM ALVO</div>
                <div class="tech-value highlight-green">{info_metodo.get('ec_ideal')}</div>
            </div>
            <div class="glass-card" style="background:rgba(168, 85, 247, 0.1); border-color:#a855f7;">
                <div class="tech-label" style="color:#d8b4fe;">DICA PRO</div>
                <p style="font-size:0.85rem; color:#fff; margin-top:5px;">
                    Mantenha anotações semanais do Runoff (Saída) para evitar Lockout de nutrientes.
                </p>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: VPD CALCULATOR & AMBIENTE (COM PLOTLY) ---
with tab_vpd:
    c_vpd1, c_vpd2, c_vpd3 = st.columns([1, 1, 2])
    
    with c_vpd1:
        st.markdown('<div class="tech-label">TEMPERATURA (°C)</div>', unsafe_allow_html=True)
        temp_input = st.number_input("T", 10.0, 40.0, 25.0, label_visibility="collapsed")
        
    with c_vpd2:
        st.markdown('<div class="tech-label">UMIDADE (%)</div>', unsafe_allow_html=True)
        humid_input = st.number_input("H", 20.0, 100.0, 60.0, label_visibility="collapsed")
        
    # Cálculo VPD
    svp = 0.61078 * 2.71828**((17.27 * temp_input) / (temp_input + 237.3))
    vpd_val = svp * (1 - (humid_input / 100))
    
    # Definição de Cor do Status
    status_vpd = "PERIGO"
    color_status = "#ef4444" # Red
    
    if 0.4 <= vpd_val <= 0.8: 
        status_vpd = "VEG INICIAL (OK)"
        color_status = "#38bdf8"
    elif 0.8 < vpd_val <= 1.2: 
        status_vpd = "VEG/FLORA (IDEAL)"
        color_status = "#22c55e"
    elif 1.2 < vpd_val <= 1.5: 
        status_vpd = "FLORA FINAL (OK)"
        color_status = "#eab308"
    
    with c_vpd3:
        # Card Resultado VPD
        st.markdown(f"""
        <div style="background:{color_status}; color:#000; padding:15px; border-radius:8px; text-align:center; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-size:0.8rem; font-weight:bold; opacity:0.7;">STATUS</div>
                <div style="font-size:1.2rem; font-weight:900;">{status_vpd}</div>
            </div>
            <div style="font-size:2.5rem; font-weight:900;">{vpd_val:.2f} <span style="font-size:1rem;">kPa</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Gauges Gráficos com Plotly
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(create_gauge(temp_input, 10, 40, "TEMPERATURA", "°C", "#f97316"), use_container_width=True)
    with g2:
        st.plotly_chart(create_gauge(humid_input, 0, 100, "UMIDADE RELATIVA", "%", "#38bdf8"), use_container_width=True)
    with g3:
        # Gauge VPD
        fig_vpd = go.Figure(go.Indicator(
            mode = "gauge+number", value = vpd_val,
            title = {'text': "VPD (kPa)", 'font': {'size': 14, 'color': "#888"}},
            gauge = {
                'axis': {'range': [0, 2.5]},
                'bar': {'color': color_status},
                'bgcolor': "rgba(0,0,0,0)",
                'steps': [
                    {'range': [0.8, 1.2], 'color': "rgba(34, 197, 94, 0.2)"}, # Faixa Ideal Verde
                ],
            }
        ))
        fig_vpd.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "white"}, height=150, margin=dict(l=20,r=20,t=30,b=20))
        st.plotly_chart(fig_vpd, use_container_width=True)

# --- TAB 3: DOCTOR GROW (LISTAGEM AVANÇADA) ---
with tab_doctor:
    c_doc_filter, c_doc_search = st.columns([1, 2])
    with c_doc_filter:
        filtro_doc = st.radio("CATEGORIA:", ["Todas", "Pragas 🕷️", "Doenças 🍄", "Deficiências 🧪"], horizontal=True)
    with c_doc_search:
        busca_doc = st.text_input("🔍 DIAGNÓSTICO RÁPIDO:", placeholder="Ex: manchas brancas, ácaro, folhas amarelas...")

    # Acesso ao DB
    db_doc = db.get("DOCTOR_GROW_MASTER", {})
    
    lista_final = []
    if filtro_doc in ["Todas", "Pragas 🕷️"]:
        for k, v in db_doc.get("Pragas", {}).items(): v['nome'] = k; v['cat'] = 'Praga'; lista_final.append(v)
    if filtro_doc in ["Todas", "Doenças 🍄"]:
        for k, v in db_doc.get("Doencas", {}).items(): v['nome'] = k; v['cat'] = 'Doença'; lista_final.append(v)
    if filtro_doc in ["Todas", "Deficiências 🧪"]:
        for k, v in db_doc.get("Deficiencias", {}).items(): v['nome'] = k; v['cat'] = 'Deficiência'; lista_final.append(v)

    # Renderização
    if not lista_final:
        st.info("Banco de dados Doctor Grow vazio ou não conectado.")
    else:
        for item in lista_final:
            if busca_doc and busca_doc.lower() not in item['nome'].lower() and busca_doc.lower() not in item['identificacao'].lower():
                continue
            
            # Cor baseada na gravidade/tipo
            border = "#333"
            icon = "🐛"
            if item['cat'] == 'Doença': icon = "🍄"
            elif item['cat'] == 'Deficiência': icon = "🧪"
            
            if "CRÍTICA" in item.get('gravidade', ''): border = "#ef4444"
            elif "ALTA" in item.get('gravidade', ''): border = "#f97316"
            elif "Deficiência" in item['cat']: border = "#eab308"
            
            with st.expander(f"{icon} {item['nome']} | Gravidade: {item.get('gravidade')}"):
                c_d1, c_d2 = st.columns([1, 1])
                with c_d1:
                    st.markdown(f"**🕵️ IDENTIFICAÇÃO:**\n{item.get('identificacao')}")
                    st.markdown(f"<br>**🌿 ORGÂNICO:**", unsafe_allow_html=True)
                    for s in item.get('controle_organico', []):
                        st.markdown(f"- {s}")
                        
                with c_d2:
                    st.markdown(f"**🧪 QUÍMICO / CORREÇÃO:**")
                    for s in item.get('controle_quimico', []):
                        st.markdown(f"- {s}")
