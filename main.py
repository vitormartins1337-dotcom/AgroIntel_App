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

def load_css():
    st.markdown("""
        <style>
        /* IMPORT FONTES */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* FUNDO GERAL */
        .stApp { 
            background-color: #09090b; 
            color: #e4e4e7; 
            font-family: 'Inter', sans-serif;
        }
        
        /* AJUSTE DE MARGEM DO TOPO */
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }

        /* --- CAPA PROFISSIONAL (RESPONSIVA) --- */
        .hero-container {
            background: linear-gradient(90deg, #2e1065 0%, #000000 100%); /* Roxo Profundo -> Preto */
            border-bottom: 2px solid #a855f7; /* Linha Neon */
            border-radius: 0 0 16px 16px; /* Cantos arredondados embaixo */
            padding: 20px 25px; /* Espaçamento interno controlado */
            margin-bottom: 25px;
            
            /* FLEXBOX PARA ALINHAMENTO PERFEITO */
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 15px; /* Espaço mínimo entre titulo e botão */
            
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); /* Sombra elegante */
        }
        
        .title-wrapper {
            display: flex;
            flex-direction: column;
        }
        
        .hero-title {
            /* O SEGREDO DO NÃO-VAZAMENTO: CLAMP */
            /* Mínimo 1.5rem, Ideal 3vw, Máximo 2.2rem */
            font-size: clamp(1.5rem, 3vw, 2.2rem); 
            font-weight: 900; /* Gramatura pesada */
            color: #fff;
            line-height: 1.1;
            letter-spacing: -1px;
            white-space: nowrap; /* Não quebra linha */
        }
        
        .hero-subtitle {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem; /* Subtítulo pequeno e discreto */
            color: #c084fc; /* Roxo claro */
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 4px;
            font-weight: 600;
        }
        
        /* BOTÃO ONLINE COMPACTO */
        .status-pill {
            background: rgba(16, 185, 129, 0.1); /* Fundo verde transparente */
            border: 1px solid #059669; /* Borda verde escura */
            color: #4ade80; /* Texto verde neon */
            padding: 6px 14px; /* Tamanho reduzido */
            border-radius: 99px; /* Formato pílula */
            font-size: 0.75rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
            display: flex;
            align-items: center;
            gap: 8px; /* Espaço entre folha e texto */
            white-space: nowrap;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.15); /* Glow sutil */
        }

        /* --- OUTROS ELEMENTOS (MANTIDOS) --- */
        .ticker-wrap { width: 100%; background: #000; border-y: 1px solid #333; height: 32px; overflow: hidden; display: flex; align-items: center; margin-bottom: 20px; }
        .glass-panel { background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
        .yield-card { background: linear-gradient(135deg, #2a1b05 0%, #000 100%); border: 1px solid #eab308; border-radius: 12px; padding: 20px; text-align: center; color: #fef08a; }
        .badge-param { display: inline-block; background: #111; border: 1px solid #333; color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; margin-right: 5px; margin-bottom: 5px; }
        .badge-green { border-color: #22c55e; color: #4ade80; } .badge-blue { border-color: #38bdf8; color: #bae6fd; }
        
        /* INPUTS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div, .stTextInput > div > div {
            background-color: #121212 !important; border: 1px solid #333 !important; color: #e0e0e0 !important; border-radius: 6px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- CAPA PROFISSIONAL (CORRIGIDA) ---
# O segredo aqui é não deixar espaço no início das linhas de HTML dentro das aspas """
st.markdown("""
<style>
/* 1. O CARD ROXO PROFISSIONAL */
.header-card {
    background: linear-gradient(135deg, #240b36 0%, #000000 90%);
    border-bottom: 2px solid #a855f7;
    box-shadow: 0 0 30px rgba(168, 85, 247, 0.2);
    border-radius: 16px;
    padding: 20px 30px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 2. TÍTULO E SUBTÍTULO */
.title-box {
    display: flex;
    flex-direction: column;
}

.main-title {
    font-size: clamp(1.5rem, 4vw, 3rem); /* Fonte elástica para não vazar */
    font-weight: 900;
    color: #fff;
    line-height: 1;
    white-space: nowrap;
}

.sub-title {
    font-family: 'Courier New', monospace;
    font-size: clamp(0.7rem, 1vw, 0.9rem);
    color: #d8b4fe;
    letter-spacing: 3px;
    margin-top: 5px;
    text-transform: uppercase;
}

/* 3. BOTÃO ONLINE (PÍLULA) */
.status-pill {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid #10b981;
    color: #4ade80;
    padding: 6px 16px;
    border-radius: 50px;
    font-weight: bold;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
}
</style>

<div class="header-card">
    <div class="title-box">
        <div class="main-title">AGROWER <span style="color:#a855f7;">SDI</span></div>
        <div class="sub-title">SISTEMA DE DECISÃO INTEGRADA</div>
    </div>
    <div class="status-pill">
        <span style="font-size:1.2rem; line-height:1;">🍁</span> ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

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
