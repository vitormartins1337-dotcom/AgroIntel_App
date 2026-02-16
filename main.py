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

# --- CAPA HERO V.FINAL (SEM INDENTAÇÃO PARA NÃO DAR ERRO) ---
st.markdown("""
<style>
/* 1. CONTAINER DA CAPA (RESPONSIVO E CENTRALIZADO) */
.hero-card {
    position: relative;
    background: linear-gradient(135deg, #1a0b2e 0%, #000000 100%);
    border: 1px solid #a855f7;
    box-shadow: 0 0 50px rgba(168, 85, 247, 0.25);
    border-radius: 20px;
    padding: 60px 20px;
    margin-bottom: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

/* 2. BOTÃO ONLINE (FIXO NO CANTO DIREITO SUPERIOR) */
.status-pill {
    position: absolute;
    top: 15px;
    right: 15px;
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

/* 3. TÍTULO GIGANTE (AJUSTÁVEL) */
.main-title {
    font-size: clamp(2.5rem, 6vw, 5rem); /* Fonte Grande que não vaza */
    font-weight: 900;
    color: #fff;
    line-height: 1;
    letter-spacing: -2px;
    text-align: center;
    text-shadow: 0 0 30px rgba(168, 85, 247, 0.6);
    z-index: 1;
}

/* 4. SUBTÍTULO */
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
</style>

<div class="hero-card">
    <div class="status-pill">
        <span style="font-size:1rem; line-height:1;">🍁</span> ONLINE
    </div>
    <div class="main-title">AGROWER <span style="color:#a855f7">SDI</span></div>
    <div class="sub-title">SISTEMA DE DECISÃO INTEGRADA</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🎮 DASHBOARD DE CONTROLE (CORRIGIDO E SEPARADO)
# ==============================================================================

# 1. INPUTS (CONFIGURAÇÃO)
c1, c2, c3, c4 = st.columns([1.5, 1.5, 1, 1])
with c1: 
    metodo_sel = st.selectbox("MÉTODO DE CULTIVO", list(db.get("METODOS_CULTIVO", {}).keys()))
with c2: 
    genetica_sel = st.selectbox("GENÉTICA", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
with c3: 
    n_plantas = st.number_input("Nº PLANTAS", 1, 500, 6)
with c4: 
    data_inicio = st.date_input("INÍCIO CULTIVO", datetime.date.today() - datetime.timedelta(days=45))

# 2. CÁLCULOS (ENGINE)
# Buscando dados
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]

# Calculando Tempo
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# Calculando Produção (Yield)
yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas
yield_kg = yield_total / 1000 

# Definindo Fase
fase_nome = "Indefinida"
fase_dados = {}
for k, v in db.get("FASES_DINAMICAS", {}).items():
    range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
    chave_limpa = k.split(' ')[0]
    if dias_vida <= range_map.get(chave_limpa, 200):
        fase_nome = k
        fase_dados = v
        break

# 3. ESTILOS CSS (SEM 'f' PARA NÃO DAR ERRO NAS CORES)
st.markdown("""
<style>
/* CARD ROXO (STATUS) */
.status-card {
    background: linear-gradient(145deg, #120520 0%, #050505 100%);
    border: 1px solid #3b0764;
    border-left: 5px solid #a855f7;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    height: 100%;
}

/* CARD DOURADO (YIELD) */
.yield-card {
    background: linear-gradient(135deg, #1e1b10 0%, #000000 100%);
    border: 1px solid #854d0e;
    border-right: 5px solid #eab308;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(234, 179, 8, 0.1);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* TIPOGRAFIA */
.card-label {
    font-size: 0.7rem; 
    color: #9ca3af; 
    text-transform: uppercase; 
    letter-spacing: 1.5px; 
    font-weight: 700; 
    margin-bottom: 5px;
}
.big-val {
    font-size: 2.2rem; 
    font-weight: 900; 
    color: #fff; 
    line-height: 1; 
    margin-bottom: 5px;
}

/* BADGES */
.meta-badge {
    display: inline-block; 
    padding: 4px 8px; 
    border-radius: 4px; 
    font-size: 0.75rem; 
    font-weight: bold; 
    margin-right: 5px;
}
.bg-ph { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid #1e3a8a; }
.bg-ec { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid #064e3b; }
.divider { height: 1px; background: #333; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

# 4. HTML DINÂMICO (COM 'f' PARA OS DADOS)
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns([1.8, 1.2])

with col_a:
    st.markdown(f"""
    <div class="status-card">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div class="card-label" style="color:#d8b4fe;">FASE ATUAL</div>
                <div class="big-val">{fase_nome.upper()}</div>
            </div>
            <div style="text-align:right;">
                <div class="card-label">TEMPO</div>
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
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="yield-card">
        <div class="card-label" style="color:#fcd34d;">ESTIMATIVA DE COLHEITA</div>
        <div class="big-val" style="color:#fef08a;">{yield_total:.0f}g</div>
        <div style="font-size:0.9rem; color:#fde047; margin-bottom:10px;">~ {yield_kg:.2f} kg (Seco)</div>
        <div class="divider" style="background: #422006;"></div>
        <div style="font-size:0.75rem; color:#ca8a04;">
            BASE CÁLCULO:<br>
            <b>{n_plantas} plantas</b> x <b>{info_metodo['rendimento_base']}g</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
