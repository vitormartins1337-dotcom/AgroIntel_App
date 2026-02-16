# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | MASTER EDITION V9.0 (FINAL)
# DESCRIÇÃO: Painel de Controle Agronômico de Alta Performance

import streamlit as st
import datetime
import plotly.graph_objects as go
from core_logic import AgroEngine 

# --- 1. SETUP INICIAL ---
st.set_page_config(
    page_title="Agrower SDI Pro", 
    page_icon="🍁", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializa Engine e Banco de Dados
engine = AgroEngine()
db = engine.db 

# --- 2. CSS "MONSTRUOSO" (ESTILO PROFISSIONAL) ---
def load_master_css():
    st.markdown("""
        <style>
        /* FONTES MODERNAS */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* FUNDO GERAL DARK */
        .stApp { 
            background-color: #050505; 
            color: #e4e4e7; 
            font-family: 'Inter', sans-serif;
        }
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }

        /* --- HEADER HERO (CAPA DA REVISTA) --- */
        .hero-card {
            position: relative;
            background: linear-gradient(135deg, #1a0b2e 0%, #000000 100%); /* Roxo Profundo */
            border: 1px solid #a855f7; /* Borda Neon */
            box-shadow: 0 0 60px rgba(168, 85, 247, 0.25); /* Glow */
            border-radius: 20px;
            padding: 50px 20px;
            margin-bottom: 30px;
            
            /* CENTRALIZAÇÃO TOTAL */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        /* TÍTULO GIGANTE (RESPONSIVO) */
        .main-title {
            font-size: clamp(2.5rem, 6vw, 5rem); /* Elástico: Cresce e Diminui sem vazar */
            font-weight: 900;
            color: #fff;
            line-height: 1;
            letter-spacing: -2px;
            text-align: center;
            text-shadow: 0 0 30px rgba(168, 85, 247, 0.6);
            z-index: 1;
        }

        /* SUBTÍTULO */
        .sub-title {
            font-family: 'Courier New', monospace;
            font-size: clamp(0.7rem, 1.5vw, 1rem);
            color: #d8b4fe;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-top: 15px;
            font-weight: 600;
            text-align: center;
            opacity: 0.9;
            z-index: 1;
        }

        /* BOTÃO ONLINE (FLUTUANTE NO CANTO) */
        .status-pill {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid #059669;
            color: #4ade80;
            padding: 6px 14px;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 700;
            font-family: sans-serif;
            display: flex;
            align-items: center;
            gap: 6px;
            z-index: 2;
        }

        /* --- TICKER (BARRA DE COTAÇÕES) --- */
        .ticker-wrap {
            width: 100%; overflow: hidden; background: #000; 
            border-top: 1px solid #333; border-bottom: 1px solid #333; 
            height: 36px; display: flex; align-items: center; margin-bottom: 25px;
        }
        .tick-item { margin-right: 40px; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #a855f7; }
        .tick-val { color: #fff; margin-left: 5px; font-weight: bold; }

        /* --- CARDS DASHBOARD --- */
        /* Status (Roxo) */
        .status-card {
            background: linear-gradient(145deg, #120520 0%, #050505 100%);
            border: 1px solid #3b0764;
            border-left: 5px solid #a855f7;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            height: 100%;
        }
        
        /* Yield (Dourado) */
        .yield-card {
            background: linear-gradient(135deg, #1e1b10 0%, #000000 100%);
            border: 1px solid #854d0e;
            border-right: 5px solid #eab308;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            height: 100%;
            display: flex; flex-direction: column; justify-content: center;
            box-shadow: 0 4px 20px rgba(234, 179, 8, 0.15);
        }

        /* Diagnóstico Luz (SDI) */
        .diag-card {
            background: #0f0f0f; border: 1px solid #333; border-radius: 12px; padding: 20px;
            margin-top: 20px; position: relative;
        }

        /* --- TIPOGRAFIA CARDS --- */
        .card-label { font-size: 0.75rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 8px; }
        .big-val { font-size: 2.5rem; font-weight: 900; color: #fff; line-height: 1; margin-bottom: 5px; }
        .sub-info { font-size: 0.9rem; color: #d1d5db; margin-top: 5px; }
        
        /* BADGES METAS */
        .meta-badge { display: inline-block; padding: 5px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; margin-right: 6px; margin-top: 5px; }
        .bg-ph { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid #1e3a8a; }
        .bg-ec { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid #064e3b; }
        .divider { height: 1px; background: #333; margin: 20px 0; }

        /* INPUTS ESTILIZADOS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div, .stTextInput > div > div {
            background-color: #121212 !important; border: 1px solid #333 !important; color: #e0e0e0 !important; border-radius: 6px !important;
        }
        
        /* DOCTOR GROW CARDS */
        .doc-card { background: #0f0f0f; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #333; }
        .solucao-tag { padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; margin-right: 5px; display: inline-block; margin-bottom: 4px;}
        .bio { background: rgba(34, 197, 94, 0.1); border: 1px solid #15803d; color: #86efac; }
        .quim { background: rgba(239, 68, 68, 0.1); border: 1px solid #991b1b; color: #fca5a5; }
        </style>
    """, unsafe_allow_html=True)
load_master_css()

# --- 3. HEADER "HERO" (CAPA PROFISSIONAL SEM INDENTAÇÃO) ---
st.markdown("""
<div class="hero-card">
<div class="status-pill"><span style="font-size:1rem; line-height:1;">🍁</span> ONLINE</div>
<div class="main-title">AGROWER <span style="color:#a855f7">SDI</span></div>
<div class="sub-title">SISTEMA DE DECISÃO INTEGRADA</div>
</div>
""", unsafe_allow_html=True)

# Ticker Bloomberg (Opcional - Visual Tech)
st.markdown("""
<div class="ticker-wrap">
    <div style="display:inline-block; white-space:nowrap; animation:ticker 45s linear infinite;">
        <span class="tick-item">VPD IDEAL <span class="tick-val">0.8-1.2 kPa</span></span>
        <span class="tick-item">TEMP FLORA <span class="tick-val">22-26°C</span></span>
        <span class="tick-item">UMIDADE FLORA <span class="tick-val">45-50%</span></span>
        <span class="tick-item">PPFD FLORA <span class="tick-val">800-1000 µmol</span></span>
        <span class="tick-item">PH SOLO <span class="tick-val">6.0-6.8</span></span>
        <span class="tick-item">PH COCO <span class="tick-val">5.8-6.2</span></span>
        <span class="tick-item">EC FLORA <span class="tick-val">1.8-2.4 mS</span></span>
    </div>
</div>
<style>@keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. PAINEL DE CONTROLE (INPUTS & ENGINE SDI)
# ==============================================================================

# --- A. INPUTS PRINCIPAIS ---
st.markdown("<br>", unsafe_allow_html=True)
c_in1, c_in2, c_in3, c_in4 = st.columns([1.5, 1.5, 1, 1])

with c_in1:
    # Genética (Agora com Foto/Auto)
    genetica_sel = st.selectbox("🧬 GENÉTICA", list(db.get("GENETICAS_PARAMETROS", {}).keys()))

with c_in2:
    # Método (Orgânico, Mineral, Hidro...)
    metodo_sel = st.selectbox("🥣 MÉTODO", list(db.get("METODOS_CULTIVO", {}).keys()))

with c_in3:
    # Ambiente (Define a lógica de Luz)
    ambiente_sel = st.selectbox("🏠 AMBIENTE", ["Indoor (Estufa)", "Estufa Outdoor", "Outdoor (Sol Pleno)"])

with c_in4:
    # Data
    data_inicio = st.date_input("📅 INÍCIO", datetime.date.today() - datetime.timedelta(days=45))

# --- B. LÓGICA DE ILUMINAÇÃO & ESPAÇO (SDI) ---
watts_painel = 0
area_cultivo = 0
diagnostico_luz = ""
analise_texto = ""
cor_diag = "#333"

# Se não for Outdoor puro, pede dados técnicos
if ambiente_sel != "Outdoor (Sol Pleno)":
    with st.expander("💡 CONFIGURAÇÃO DE ILUMINAÇÃO & ESPAÇO (OBRIGATÓRIO)", expanded=True):
        cl1, cl2, cl3, cl4 = st.columns(4)
        with cl1: watts_painel = st.number_input("POTÊNCIA LED (W Reais):", 50, 2000, 240, help="Watts reais consumidos da tomada.")
        with cl2: largura = st.number_input("LARGURA (cm):", 40, 500, 80)
        with cl3: profundidade = st.number_input("PROFUNDIDADE (cm):", 40, 500, 80)
        with cl4: n_plantas = st.number_input("Nº PLANTAS:", 1, 100, 4)
        
        # Engenharia Reversa
        area_cultivo = (largura * profundidade) / 10000 # m2
        wm2 = watts_painel / area_cultivo if area_cultivo > 0 else 0
        
        # Diagnóstico Agronômico (W/m2)
        if wm2 < 250:
            diagnostico_luz = "BAIXA INTENSIDADE"
            cor_diag = "#eab308" # Amarelo
            analise_texto = f"⚠️ <b>{wm2:.0f} W/m²</b>. Luz insuficiente para floração densa. Risco de estiolamento e buds aerados (pipoca)."
        elif 250 <= wm2 <= 550:
            diagnostico_luz = "ALTA PERFORMANCE"
            cor_diag = "#22c55e" # Verde
            analise_texto = f"🚀 <b>{wm2:.0f} W/m²</b>. Sweet Spot (Ponto Ideal). Potencial máximo de rendimento e produção de resina."
        else:
            diagnostico_luz = "EXTREMO (CO2)"
            cor_diag = "#ef4444" # Vermelho
            analise_texto = f"🔥 <b>{wm2:.0f} W/m²</b>. Intensidade muito alta. Risco de branqueamento (Light Bleach). Obrigatório CO2 suplementar."
else:
    # Outdoor
    n_plantas = st.number_input("Nº PLANTAS (OUTDOOR):", 1, 500, 6)
    diagnostico_luz = "SOLAR"
    cor_diag = "#facc15"
    analise_texto = "☀️ Cultivo guiado pelo ciclo solar natural. Atenção a chuvas na floração."

# --- C. MOTOR DE CÁLCULO (YIELD & FASES) ---
# Recupera dados do DB
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]

# Tempo
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# Yield Estimado (Kg)
yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas
yield_kg = yield_total / 1000 

# Fase Dinâmica (Detecta se é Auto ou Foto)
fase_nome = "Indefinida"
fase_dados = {}
for k, v in db.get("FASES_DINAMICAS", {}).items():
    # Mapa de dias padrão para Fotoperíodo
    range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
    chave_limpa = k.split(' ')[0]
    limite = range_map.get(chave_limpa, 200)
    
    # Se for Automática, reduz o ciclo em 20%
    if info_genetica.get("tipo") == "Auto": 
        limite = int(limite * 0.8) 
        
    if dias_vida <= limite:
        fase_nome = k
        fase_dados = v
        break

# ==============================================================================
# 5. VISUAL DASHBOARD (CARDS NEON & GLASS)
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns([1.8, 1.2])

with col_a:
    # CARD DE STATUS (ROXO)
    st.markdown(f"""
    <div class="status-card">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div class="card-label" style="color:#d8b4fe;">FASE ATUAL ({info_genetica.get('tipo', 'Foto').upper()})</div>
                <div class="big-val">{fase_nome.upper()}</div>
            </div>
            <div style="text-align:right;">
                <div class="card-label">TEMPO DE CULTIVO</div>
                <div style="font-size:1.5rem; font-weight:bold; color:#fff;">{dias_vida} <span style="font-size:0.9rem; color:#888;">DIAS</span></div>
                <div style="font-size:0.85rem; color:#a855f7;">SEMANA {semanas}</div>
            </div>
        </div>
        <div class="divider"></div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="card-label">OBJETIVO TÁTICO</div>
                <div style="color:#fff; font-weight:600;">🎯 {fase_dados.get('foco', '-')}</div>
            </div>
            <div style="text-align:right;">
                <div class="card-label">METAS DO AMBIENTE</div>
                <div>
                    <span class="meta-badge bg-ph">💧 PH {info_metodo['ph_ideal']}</span>
                    <span class="meta-badge bg-ec">⚡ EC {info_metodo['ec_ideal']}</span>
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

with col_b:
    # CARD DE YIELD (DOURADO)
    st.markdown(f"""
    <div class="yield-card">
        <div class="card-label" style="color:#fcd34d;">ESTIMATIVA DE COLHEITA</div>
        <div class="big-val" style="color:#fef08a;">{yield_total:.0f}g</div>
        <div class="sub-info" style="color:#fde047;">~ {yield_kg:.2f} kg (Seco)</div>
        <div class="divider" style="background: #422006;"></div>
        <div style="font-size:0.75rem; color:#ca8a04;">
            BASE CÁLCULO:<br>
            <b>{n_plantas} plantas</b> x <b>{info_metodo['rendimento_base']}g</b>
        </div>
    </div>""", unsafe_allow_html=True)

# CARD DIAGNÓSTICO (CONDICIONAL)
if diagnostico_luz:
    st.markdown(f"""
    <div class="diag-card" style="border-left: 4px solid {cor_diag};">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="font-weight:bold; color:{cor_diag}; letter-spacing:1px;">DIAGNÓSTICO DE ILUMINAÇÃO (SDI)</div>
            <div style="background:{cor_diag}20; color:{cor_diag}; padding:4px 10px; border-radius:4px; font-size:0.8rem; font-weight:bold;">{diagnostico_luz}</div>
        </div>
        <div style="color:#e4e4e7; font-size:0.95rem; line-height:1.5;">{analise_texto}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. FERRAMENTAS AVANÇADAS (NUTRIÇÃO & DOCTOR)
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
tab_nutri, tab_doctor = st.tabs(["🧪 NUTRIÇÃO PRECISION (MARCHA DE ABSORÇÃO)", "🚑 DOCTOR GROW (FITOSSANIDADE)"])

# --- ABA 1: NUTRIÇÃO ---
with tab_nutri:
    st.markdown("### 📊 Marcha de Absorção de Nutrientes")
    st.caption("Entenda o consumo relativo da planta ao longo das semanas.")
    
    nutri = db["NUTRI_MARCHA_ABSORCAO"]
    
    # Gráfico Plotly Neon
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nutri['semanas'], y=nutri['N'], name='Nitrogênio (N)', line=dict(color='#22c55e', width=3)))
    fig.add_trace(go.Scatter(x=nutri['semanas'], y=nutri['P'], name='Fósforo (P)', line=dict(color='#3b82f6', width=3)))
    fig.add_trace(go.Scatter(x=nutri['semanas'], y=nutri['K'], name='Potássio (K)', line=dict(color='#a855f7', width=3)))
    
    fig.update_layout(
        title="",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#ccc"),
        xaxis=dict(title="Semanas", showgrid=False),
        yaxis=dict(title="Demanda (%)", showgrid=True, gridcolor='#333'),
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🔍 Diagnóstico Visual de Deficiências")
    
    # Grid de Deficiências
    cols_def = st.columns(4)
    defs_items = list(db["DEFICIENCIAS_VISUAIS"].items())
    
    for i, (k, v) in enumerate(defs_items):
        with cols_def[i % 4]:
            st.markdown(f"""
            <div style="background:#111; border:1px solid #333; padding:15px; border-radius:8px; height:100%;">
                <div style="color:#facc15; font-weight:bold; margin-bottom:5px;">{k}</div>
                <div style="font-size:0.85rem; color:#ccc; margin-bottom:10px; height:40px;">{v['sintoma']}</div>
                <div style="font-size:0.8rem; color:#a855f7; font-weight:bold;">SOLUÇÃO:</div>
                <div style="font-size:0.8rem; color:#888;">{v['correcao']}</div>
            </div>
            """, unsafe_allow_html=True)

# --- ABA 2: DOCTOR GROW ---
with tab_doctor:
    st.markdown("### 🕷️ Identificação e Tratamento")
    
    c_busca, c_filtro = st.columns([3, 1])
    with c_busca: busca = st.text_input("🔍 Buscar Praga ou Doença (Ex: Ácaro):")
    
    db_fito = db["DOCTOR_GROW_FITOSSANIDADE"]
    
    for nome, info in db_fito.items():
        if busca and busca.lower() not in nome.lower(): continue
        
        # Cor da Gravidade
        cor_g = "#3b82f6"
        if info['gravidade'] == "MÉDIA": cor_g = "#eab308"
        if info['gravidade'] in ["ALTA", "CRÍTICA", "FATAL"]: cor_g = "#ef4444"
        
        st.markdown(f"""
        <div class="doc-card" style="border-left-color: {cor_g};">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <div style="font-weight:bold; font-size:1.1rem; color:#fff;">{nome}</div>
                <div style="background:{cor_g}20; color:{cor_g}; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:bold;">{info['gravidade']}</div>
            </div>
            <div style="color:#ccc; font-size:0.95rem; margin-bottom:10px;"><i>{info['sintomas']}</i></div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
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
