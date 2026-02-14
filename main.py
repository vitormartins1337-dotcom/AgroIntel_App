# ARQUIVO: main.py
# AGRO SDI | VISUAL PRO + CAPA GIGANTE + TICKER BALÃO
import streamlit as st
from core_logic import AgroEngine 

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Agro SDI", page_icon="🌱", layout="wide")
engine = AgroEngine()

# --- 2. CSS PROFISSIONAL ---
def load_css():
    st.markdown("""
        <style>
        /* Ajuste para remover margens brancas padrão */
        .block-container { padding-top: 1rem !important; padding-bottom: 3rem !important; }
        
        /* CORES E FUNDO */
        .stApp {
            background-color: #0b120d; /* Verde Deep Army */
            color: #e2e8f0;
        }

        /* BARRA LATERAL */
        [data-testid="stSidebar"] {
            background-color: #111e16;
            border-right: 1px solid #1e3a2f;
        }

        /* --- TICKER BLOOMBERG (ESTILO BALÃOZINHO) --- */
        .ticker-container {
            width: 100%;
            background-color: #020403; /* Preto Profundo */
            border: 1px solid #15803d; /* Borda completa */
            border-radius: 20px; /* ARREDONDADO (BALÃO) */
            overflow: hidden;
            white-space: nowrap;
            height: 36px;
            display: flex;
            align-items: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.4);
            margin-bottom: 25px; /* Espaço abaixo */
            margin-top: 5px;
        }
        .ticker-text {
            display: inline-block;
            animation: ticker 35s linear infinite;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem; 
            font-weight: bold;
        }
        @keyframes ticker {
            0% { transform: translate3d(100%, 0, 0); }
            100% { transform: translate3d(-100%, 0, 0); }
        }
        .tick-item { margin-right: 40px; color: #cbd5e1; letter-spacing: 0.5px; }
        .up { color: #4ade80; } /* Verde Neon */
        .down { color: #f87171; } /* Vermelho */

        /* --- HEADER (CAPA GIGANTE) --- */
        .header-box {
            background: linear-gradient(180deg, #14281d 0%, #0b120d 100%);
            border: 1px solid #1e3a2f;
            border-radius: 12px;
            padding: 30px 40px; /* AUMENTEI O ESPAÇAMENTO */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            margin-bottom: 10px;
        }

        /* --- CARDS DE FASES --- */
        .phase-box {
            background-color: #16241b;
            border-left: 4px solid #22c55e;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            border: 1px solid #1e3a2f;
        }
        
        /* --- Inputs e Selects --- */
        .stSelectbox div[data-baseweb="select"] > div, .stTextInput input {
            background-color: #060a07 !important;
            color: #ecfdf5 !important;
            border: 1px solid #15803d !important;
        }
        
        /* --- Abas --- */
        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #111e16;
            border: 1px solid #1e3a2f;
            color: #6ee7b7;
            padding: 8px 20px;
            font-size: 0.9rem;
        }
        .stTabs [aria-selected="true"] {
            background-color: #15803d !important;
            color: #fff !important;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

load_css()

# --- 3. HEADER (CAPA AUMENTADA) ---
st.markdown("""
<div class="header-box">
    <div>
        <h1 style="margin:0; font-family:'Arial', sans-serif; font-weight:900; font-size:3.5rem; letter-spacing:-2px; color:#fff; line-height: 1;">
            AGRO <span style="color:#22c55e;">SDI</span>
        </h1>
        <div style="font-size:1rem; letter-spacing:4px; color:#86efac; margin-top:8px; font-weight:600; opacity:0.9;">
            SISTEMA DE DECISÃO INTEGRADA
        </div>
    </div>
    <div style="background:rgba(22,163,74,0.2); border:1px solid #22c55e; color:#4ade80; padding:6px 16px; border-radius:30px; font-size:0.85rem; display:flex; align-items:center; gap:10px; font-weight:bold;">
        <div style="width:10px; height:10px; background:#22c55e; border-radius:50%; box-shadow:0 0 10px #22c55e;"></div> ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. TICKER BLOOMBERG (ESTILO BALÃOZINHO) ---
ticker_html = """
<div class="ticker-container">
    <div class="ticker-text">
        <span class="tick-item">USD/BRL <span class="up">R$ 5.72 ▲</span></span>
        <span class="tick-item">SOJA (CBOT) <span class="down">US$ 12.10 ▼</span></span>
        <span class="tick-item">MILHO (B3) <span class="up">R$ 58.40 ▲</span></span>
        <span class="tick-item">BOI GORDO <span class="up">R$ 245.00 ▲</span></span>
        <span class="tick-item">CAFÉ ARÁBICA <span class="down">US$ 230.00 ▼</span></span>
        <span class="tick-item">UREIA <span class="down">US$ 380.00 ▼</span></span>
        <span class="tick-item">CLORETO DE POTÁSSIO <span class="down">US$ 310.00 ▼</span></span>
    </div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# ==============================================================================
# 🧠 CÉREBRO DO APLICATIVO (INTACTO)
# ==============================================================================

culturas = engine.listar_culturas()
cultura_sel = st.selectbox("🚜 SELECIONE A CULTURA:", culturas)

if cultura_sel:
    st.markdown("---")
    tab_fases, tab_sanidade = st.tabs(["🌱 FASES & MANEJO PRÁTICO", "🛡️ SANIDADE (PRAGAS & DOENÇAS)"])

    # =========================================================
    # ABA 1: FENOLOGIA
    # =========================================================
    with tab_fases:
        fases = engine.get_fases(cultura_sel)
        st.caption(f"Guia estratégico para {cultura_sel}.")
        
        for sigla, dados in fases.items():
            html_content = f"""
<div class="phase-box">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span style="color:#fff; font-size:1.3rem; font-weight:800;">{sigla}</span>
        <span style="background:#064e3b; padding:3px 8px; border-radius:4px; font-size:0.7rem; color:#4ade80; border:1px solid #22c55e; font-weight:bold;">FOCO: {dados['foco'].upper()}</span>
    </div>
    <div style="color:#86efac; font-size:0.95rem; font-weight:600; margin-bottom:10px; border-bottom:1px solid #1e3a2f; padding-bottom:8px;">{dados['fase']}</div>
    <div style="color:#d1d5db; font-size:0.9rem; line-height:1.5;">{dados['visao_pratica']}</div>
    <div style="background:#2a1810; color:#fdba74; padding:10px; border-radius:4px; font-style:italic; font-size:0.85rem; border:1px solid #7c2d12; margin-top:12px;">⚠️ TÉCNICO: {dados['alerta']}</div>
</div>
"""
            st.markdown(html_content, unsafe_allow_html=True)

    # =========================================================
    # ABA 2: SANIDADE
    # =========================================================
    with tab_sanidade:
        c1, c2 = st.columns([1, 3])
        with c1:
            tipo_problema = st.radio("Filtrar:", ["Todos", "Pragas 🐛", "Doenças 🍄"], index=0, horizontal=True)
        with c2:
            termo_busca = st.text_input("Buscar:", placeholder="Digite o nome do problema...")

        st.markdown("<br>", unsafe_allow_html=True)

        lista_final = []
        if tipo_problema in ["Todos", "Pragas 🐛"]:
            pragas = engine.buscar_problema(cultura_sel, termo_busca, "Pragas")
            for k, v in pragas.items(): 
                v['nome_exibicao'] = k
                lista_final.append(v)
        
        if tipo_problema in ["Todos", "Doenças 🍄"]:
            doencas = engine.buscar_problema(cultura_sel, termo_busca, "Doencas")
            for k, v in doencas.items(): 
                v['nome_exibicao'] = k
                lista_final.append(v)

        if not lista_final:
            st.warning("Nenhum problema encontrado.")
        
        for item in lista_final:
            icone = "🐛" if item['tipo'] == "Praga" else "🍄"
            bg_header = "#0f172a" if item['tipo'] == "Praga" else "#2a1810"
            
            with st.expander(f"{icone} {item['nome_exibicao']}  |  Dano: {item.get('nivel_dano', '-')}"):
                c_d1, c_d2 = st.columns([2,1])
                with c_d1: st.markdown(f"**Identificação:** {item['identificacao_campo']}")
                with c_d2: 
                    if 'fases_criticas' in item: st.markdown(f"**Fases:** {', '.join(item['fases_criticas'])}")
                
                st.markdown("#### ☠️ Controle Químico")
                for solucao in item['manejo_quimico']:
                    html_quimica = f"""
                    <div style="background:{bg_header}; padding:10px; border-radius:6px; border:1px solid #334155; margin-bottom:8px;">
                        <div style="color:#38bdf8; font-weight:bold;">{solucao['ativo']}</div>
                        <div style="font-size:0.75rem; color:#94a3b8;">{solucao['grupo_quimico']} | {solucao['mecanismo']}</div>
                        <div style="margin-top:5px;">
                           {' '.join([f'<span style="background:#1e293b; color:#bae6fd; padding:2px 6px; border-radius:4px; font-size:0.75rem; border:1px solid #38bdf8; margin-right:5px;">🛒 {p}</span>' for p in solucao['sugestao_produtos']])}
                        </div>
                        <div style="margin-top:5px; font-size:0.8rem; color:#fbbf24; font-style:italic;">👉 {solucao['observacao']}</div>
                    </div>
                    """
                    st.markdown(html_quimica, unsafe_allow_html=True)
