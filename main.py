# ARQUIVO: main.py
# SISTEMA: AGRO SDI | NATIVE EDITION
# VERSÃO: V-ARMY-GREEN (Visual Clássico + Cérebro Novo)

import streamlit as st
from core_logic import AgroEngine
import time

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Agro SDI", page_icon="🌱", layout="wide")

# Inicializa o Motor de Inteligência (Banco de Dados)
engine = AgroEngine()

# --- 2. ESTILO VISUAL (ARMY GREEN & TECH) ---
def load_css():
    st.markdown("""
        <style>
        /* --- FUNDO E CORES GERAIS --- */
        .stApp {
            background-color: #0e1611; /* Verde Quase Preto (Army Dark) */
            color: #ecfdf5; /* Texto Menta Claro */
        }
        
        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] {
            background-color: #14281d; /* Verde Militar Escuro */
            border-right: 1px solid #1e3a2f;
        }
        
        /* --- CABEÇALHO PERSONALIZADO --- */
        .header-wrapper {
            background: linear-gradient(180deg, #14281d 0%, #0e1611 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #1e3a2f;
            border-bottom: 3px solid #15803d; /* Verde Tech na base */
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        
        /* --- TICKER (FAIXA DE PREÇOS) --- */
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background-color: #064e3b;
            padding: 8px;
            margin-bottom: 20px;
            border-radius: 4px;
            white-space: nowrap;
            box-sizing: border-box;
            border-top: 1px solid #059669;
            border-bottom: 1px solid #059669;
        }
        .ticker {
            display: inline-block;
            animation: ticker 30s linear infinite;
        }
        @keyframes ticker {
            0% { transform: translate3d(100%, 0, 0); }
            100% { transform: translate3d(-100%, 0, 0); }
        }
        .ticker-item {
            display: inline-block;
            padding: 0 2rem;
            font-size: 0.9rem;
            color: #a7f3d0;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }
        .up { color: #34d399; } /* Verde Alta */
        .down { color: #f87171; } /* Vermelho Baixa */

        /* --- ANIMAÇÃO DO PONTO ONLINE (PULSANTE) --- */
        .status-badge {
            background-color: rgba(6, 78, 59, 0.6);
            color: #ecfdf5;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            border: 1px solid #10b981;
            display: flex;
            align-items: center;
            gap: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .status-dot {
            height: 10px;
            width: 10px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse-green 2s infinite;
        }
        @keyframes pulse-green {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        /* --- CARDS DE CONTEÚDO --- */
        .app-card {
            background-color: #111c16;
            border: 1px solid #23362b;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            margin-bottom: 15px;
        }
        
        /* --- Inputs e Selects --- */
        .stSelectbox div[data-baseweb="select"] > div, .stTextInput input {
            background-color: #0e1611 !important;
            color: #fff !important;
            border: 1px solid #10b981 !important;
        }
        
        /* --- Abas --- */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #14281d;
            border: 1px solid #1e3a2f;
            color: #6ee7b7;
        }
        .stTabs [aria-selected="true"] {
            background-color: #064e3b !important;
            border-bottom: 2px solid #34d399 !important;
            color: #fff !important;
        }
        </style>
    """, unsafe_allow_html=True)

load_css()

# --- 3. HEADER & TICKER (IDENTIDADE VISUAL) ---
# Ticker Simulado (Funciona Offline com últimos fechamentos)
ticker_content = """
<div class="ticker-item">USD/BRL <span class="up">R$ 5.72 ▲</span></div>
<div class="ticker-item">SOJA (CBOT) <span class="down">US$ 12.10 ▼</span></div>
<div class="ticker-item">MILHO (B3) <span class="up">R$ 58.40 ▲</span></div>
<div class="ticker-item">BOI GORDO <span class="up">R$ 245.00 ▲</span></div>
<div class="ticker-item">CAFÉ ARÁBICA <span class="down">US$ 230.00 ▼</span></div>
<div class="ticker-item">UREIA <span class="down">US$ 380.00 ▼</span></div>
"""

st.markdown(f"""
<div class="header-wrapper">
    <div>
        <h1 style="margin:0; font-family:'Roboto', sans-serif; font-weight:900; font-size:2rem; letter-spacing:-1px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
            <span style="color:#ffffff;">AGRO</span> <span style="color:#10b981;">SDI</span>
        </h1>
        <div style="font-size:0.75rem; letter-spacing:3px; color:#a7f3d0; margin-top:5px; font-weight:600; opacity:0.8;">
            SISTEMA DE DECISÃO INTEGRADA
        </div>
    </div>
    <div class="status-badge">
        <span class="status-dot"></span>
        SISTEMA ONLINE
    </div>
</div>

<div class="ticker-wrap">
    <div class="ticker">
        {ticker_content} {ticker_content} </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🧠 CÉREBRO DO APLICATIVO (AGRO ENGINE)
# ==============================================================================

# Filtro Principal
st.markdown('<div class="app-card">', unsafe_allow_html=True)
culturas = engine.listar_culturas()
cultura_sel = st.selectbox("🚜 SELECIONE A CULTURA:", culturas)
st.markdown('</div>', unsafe_allow_html=True)

if cultura_sel:
    # Abas Profissionais
    tab_fases, tab_pragas, tab_doencas = st.tabs(["🌱 FASES FENOLÓGICAS", "🐛 PRAGAS & CONTROLE", "🍄 DOENÇAS & FUNGICIDAS"])

    # --- ABA FASES ---
    with tab_fases:
        st.markdown(f"### 📅 Fenologia: {cultura_sel}")
        st.info("Guia rápido para identificação de estádios em campo.")
        fases = engine.get_fases(cultura_sel)
        
        for sigla, desc in fases.items():
            st.markdown(f"""
            <div style="background:#14281d; padding:15px; border-left:4px solid #10b981; margin-bottom:10px; border-radius:4px;">
                <span style="font-size:1.2rem; font-weight:bold; color:#fff;">{sigla}</span><br>
                <span style="color:#a7f3d0;">{desc}</span>
            </div>""", unsafe_allow_html=True)

    # --- ABA PRAGAS ---
    with tab_pragas:
        st.markdown(f"### 🛡️ Identificação e Manejo: {cultura_sel}")
        busca_p = st.text_input("🔍 Buscar Praga (Ex: Lagarta)", placeholder="Nome da praga...")
        
        resultados_p = engine.buscar_problema(cultura_sel, busca_p, "Pragas")
        
        if not resultados_p:
            st.warning("Nenhum registro encontrado no banco de dados offline.")
        
        for nome, dados in resultados_p.items():
            with st.expander(f"🔴 {nome}", expanded=False):
                # Detalhes Técnicos
                c1, c2 = st.columns([2,1])
                with c1:
                    st.markdown(f"**Nome Científico:** *{dados['nome_cientifico']}*")
                    st.markdown(f"**Identificação:** {dados['identificacao_campo']}")
                with c2:
                    st.error(f"**Nível de Dano:**\n{dados['nivel_dano']}")

                st.markdown("---")
                st.markdown("#### 🧪 Protocolo Químico")
                
                for solucao in dados['manejo_quimico']:
                    st.markdown(f"""
                    <div style="background:#0f172a; padding:15px; border:1px solid #1e293b; border-radius:8px; margin-bottom:10px;">
                        <div style="color:#38bdf8; font-weight:bold; font-size:1rem;">{solucao['ativo']}</div>
                        <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:8px;">Grupo: {solucao['grupo_quimico']} | Mecanismo: {solucao['mecanismo']}</div>
                        
                        <div style="margin-bottom:8px;">
                            {' '.join([f'<span style="background:#0c4a6e; color:#7dd3fc; padding:2px 8px; border-radius:4px; font-size:0.8rem; border:1px solid #0284c7; margin-right:5px;">🛒 {p}</span>' for p in solucao['sugestao_produtos']])}
                        </div>
                        
                        <div style="font-size:0.85rem; color:#fbbf24; font-style:italic; border-top:1px solid #334155; padding-top:5px;">
                            ⚠️ {solucao['observacao']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # --- ABA DOENÇAS ---
    with tab_doencas:
        st.markdown(f"### 💊 Patologia: {cultura_sel}")
        busca_d = st.text_input("🔍 Buscar Doença (Ex: Ferrugem)", placeholder="Nome da doença...")
        
        resultados_d = engine.buscar_problema(cultura_sel, busca_d, "Doencas")
        
        for nome, dados in resultados_d.items():
            with st.expander(f"🟠 {nome}", expanded=False):
                st.markdown(f"**Nome Científico:** *{dados['nome_cientifico']}*")
                st.markdown(f"**Sintomas:** {dados['sintomas']}")
                st.warning(f"**Fases Críticas:** {', '.join(dados['fases_criticas'])}")

                st.markdown("---")
                st.markdown("#### 🧪 Fungicidas Recomendados")
                
                for solucao in dados['manejo_quimico']:
                    st.markdown(f"""
                    <div style="background:#2a1810; padding:15px; border:1px solid #431407; border-radius:8px; margin-bottom:10px;">
                        <div style="color:#fdba74; font-weight:bold; font-size:1rem;">{solucao['ativo']}</div>
                        <div style="font-size:0.8rem; color:#d6d3d1; margin-bottom:8px;">Grupo: {solucao['grupo_quimico']}</div>
                        
                        <div style="margin-bottom:8px;">
                            {' '.join([f'<span style="background:#431407; color:#fdba74; padding:2px 8px; border-radius:4px; font-size:0.8rem; border:1px solid #fdba74; margin-right:5px;">🛒 {p}</span>' for p in solucao['sugestao_produtos']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
