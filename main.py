# ARQUIVO: main.py
# AGRO SDI | VISUAL ARMY TECH (CORRIGIDO)
import streamlit as st
from core_logic import AgroEngine 
import time

# --- 1. SETUP INICIAL ---
st.set_page_config(page_title="Agro SDI", page_icon="🌱", layout="wide")

# Inicializa o Motor de Inteligência
engine = AgroEngine()

# --- 2. ESTILO VISUAL (O VERDE EXÉRCITO QUE VOCÊ GOSTOU) ---
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
        .up { color: #34d399; } 
        .down { color: #f87171; } 

        /* --- CARD DE FASES (O QUE DEU ERRO ANTES, AGORA CORRIGIDO) --- */
        .phase-card {
            background-color: #1a2e24; 
            border-left: 5px solid #22c55e;
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .expert-tip { 
            background: #3f2c22; 
            color: #fdba74; 
            padding: 10px; 
            border-radius: 6px; 
            font-style: italic; 
            font-size: 0.95rem;
            border: 1px solid #9a3412; 
            margin-top: 10px;
        }

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
ticker_content = """
<div class="ticker-item">USD/BRL <span class="up">R$ 5.72 ▲</span></div>
<div class="ticker-item">SOJA (CBOT) <span class="down">US$ 12.10 ▼</span></div>
<div class="ticker-item">MILHO (B3) <span class="up">R$ 58.40 ▲</span></div>
<div class="ticker-item">BOI GORDO <span class="up">R$ 245.00 ▲</span></div>
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
        {ticker_content} {ticker_content}
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🧠 CÉREBRO DO APLICATIVO
# ==============================================================================

# Filtro Principal
st.markdown('<div class="app-card">', unsafe_allow_html=True)
culturas = engine.listar_culturas()
cultura_sel = st.selectbox("🚜 SELECIONE A CULTURA:", culturas)
st.markdown('</div>', unsafe_allow_html=True)

if cultura_sel:
    # Abas Profissionais
    tab_fases, tab_sanidade = st.tabs(["🌱 FASES & MANEJO PRÁTICO", "🛡️ SANIDADE (PRAGAS & DOENÇAS)"])

    # =========================================================
    # ABA 1: FENOLOGIA (CORRIGIDA - SEM ERRO DE HTML)
    # =========================================================
    with tab_fases:
        fases = engine.get_fases(cultura_sel)
        st.info(f"Guia de campo para {cultura_sel}. Dicas baseadas em alta produtividade.")
        
        for sigla, dados in fases.items():
            # Aqui estava o erro: adicionei unsafe_allow_html=True para funcionar
            st.markdown(f"""
            <div class="phase-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="color: #fff; font-size: 1.2rem; font-weight: bold;">{sigla}</div>
                    <div style="background:#064e3b; padding:2px 8px; border-radius:4px; font-size:0.7rem; color:#4ade80; border:1px solid #22c55e;">FOCO: {dados['foco'].upper()}</div>
                </div>
                <div style="color: #86efac; font-size: 0.9rem; margin-bottom: 10px; font-weight: 600;">{dados['fase']}</div>
                
                <div style="color:#cbd5e1; font-size:0.95rem; margin-top:5px; line-height:1.4;">
                    {dados['visao_pratica']}
                </div>
                
                <div class="expert-tip">
                    ⚠️ <b>ATENÇÃO DO TÉCNICO:</b> {dados['alerta']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================
    # ABA 2: SANIDADE (TUDO EM UM LUGAR SÓ)
    # =========================================================
    with tab_sanidade:
        c1, c2 = st.columns([1, 3])
        with c1:
            tipo_problema = st.radio("Filtrar por:", ["Todos", "Pragas 🐛", "Doenças 🍄"], index=0)
        with c2:
            termo_busca = st.text_input("Buscar problema específico:", placeholder="Ex: Percevejo, Ferrugem...")

        st.divider()

        lista_final = []
        
        # Busca Pragas
        if tipo_problema in ["Todos", "Pragas 🐛"]:
            pragas = engine.buscar_problema(cultura_sel, termo_busca, "Pragas")
            for k, v in pragas.items(): 
                v['nome_exibicao'] = k
                lista_final.append(v)
        
        # Busca Doenças
        if tipo_problema in ["Todos", "Doenças 🍄"]:
            doencas = engine.buscar_problema(cultura_sel, termo_busca, "Doencas")
            for k, v in doencas.items(): 
                v['nome_exibicao'] = k
                lista_final.append(v)

        if not lista_final:
            st.warning("Nenhum problema encontrado com esses filtros.")

        for item in lista_final:
            cor_borda = "#ef4444" if item['tipo'] == "Praga" else "#f97316"
            icone = "🐛" if item['tipo'] == "Praga" else "🍄"
            
            with st.expander(f"{icone} {item['nome_exibicao']}  |  Dano: {item.get('nivel_dano', '-')}", expanded=False):
                # Detalhes Técnicos
                c_detalhe1, c_detalhe2 = st.columns([2,1])
                with c_detalhe1:
                    st.markdown(f"**Identificação:** {item['identificacao_campo']}")
                with c_detalhe2:
                    if 'fases_criticas' in item:
                        st.markdown(f"**Fases Críticas:**\n{', '.join(item['fases_criticas'])}")
                
                st.markdown("---")
                st.markdown("#### ☠️ Controle Químico")
                
                for solucao in item['manejo_quimico']:
                    st.markdown(f"""
                    <div style="background:#0f172a; padding:12px; border-radius:6px; border:1px solid #334155; margin-bottom:8px;">
                        <div style="color:#38bdf8; font-weight:bold;">{solucao['ativo']}</div>
                        <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:5px;">Mec: {solucao['mecanismo']} ({solucao['grupo_quimico']})</div>
                        <div>
                           {' '.join([f'<span style="background:#0c4a6e; color:#7dd3fc; padding:2px 8px; border-radius:4px; font-size:0.8rem; border:1px solid #0284c7; margin-right:5px; font-weight:bold;">🛒 {p}</span>' for p in solucao['sugestao_produtos']])}
                        </div>
                        <div style="margin-top:5px; font-size:0.85rem; color:#fbbf24; font-style:italic;">👉 {solucao['observacao']}</div>
                    </div>
                    """, unsafe_allow_html=True)
