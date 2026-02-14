# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | PROFESSIONAL CANNABIS EDITION
import streamlit as st
from core_logic import AgroEngine 

# --- 1. CONFIGURAÇÃO (LARGURA TOTAL) ---
st.set_page_config(page_title="Agrower SDI", page_icon="🍁", layout="wide")
engine = AgroEngine()

# --- 2. ESTILO "HIGH-TECH GROW" ---
def load_css():
    st.markdown("""
        <style>
        /* BASE DARK */
        .block-container { padding-top: 1rem !important; padding-bottom: 3rem !important; }
        .stApp { background-color: #050505; color: #e0e0e0; } /* Preto Profundo */
        [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #333; }

        /* HEADER & TICKER */
        .header-box {
            background: linear-gradient(90deg, #240b36 0%, #0f172a 100%); /* Roxo Haze -> Azul Noturno */
            border-bottom: 2px solid #a855f7; /* Roxo Neon */
            padding: 25px 30px; border-radius: 0 0 15px 15px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.3); margin-bottom: 20px;
        }

        .ticker-container {
            width: 100%; background-color: #000; border: 1px solid #22c55e; border-radius: 4px;
            overflow: hidden; white-space: nowrap; height: 30px; display: flex; align-items: center;
            margin-bottom: 20px;
        }
        .ticker-text { display: inline-block; animation: ticker 40s linear infinite; font-family: 'Courier New', monospace; font-weight: bold; font-size: 0.85rem;}
        @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .tick-item { margin-right: 50px; color: #a855f7; }
        .tick-val { color: #22c55e; } /* Verde Valor */

        /* CARDS */
        .strain-card {
            background-color: #111; border: 1px solid #333; border-left: 4px solid #a855f7;
            padding: 20px; border-radius: 8px; margin-bottom: 15px;
        }
        .grow-card {
            background-color: #0f172a; border: 1px solid #1e293b; padding: 15px;
            border-radius: 8px; margin-bottom: 15px;
        }
        .grow-label { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
        .grow-val { color: #38bdf8; font-size: 1.1rem; font-weight: bold; }

        /* INPUTS & TABS */
        .stSelectbox div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {
            background-color: #111 !important; color: #fff !important; border: 1px solid #444 !important;
        }
        .stTabs [data-baseweb="tab-list"] { gap: 5px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #111; border: 1px solid #333; color: #888; padding: 8px 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #a855f7 !important; color: #fff !important; font-weight: bold; border: none;
        }
        
        /* ALERTAS */
        .alert-box {
            background: #2a1205; border-left: 4px solid #f97316; padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 0.9rem; color: #fdba74;
        }
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. HEADER "AGROWER" ---
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
        <div style="background:rgba(168, 85, 247, 0.2); border:1px solid #a855f7; color:#d8b4fe; padding:5px 15px; border-radius:20px; font-size:0.8rem; display:inline-flex; align-items:center; gap:8px;">
            🧬 GENETICS LAB
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Ticker com Parâmetros Ideais de Cultivo (VPD, EC, PH)
ticker_html = """
<div class="ticker-container">
    <div class="ticker-text">
        <span class="tick-item">VEG TEMP: <span class="tick-val">22-28°C</span></span>
        <span class="tick-item">VEG UMIDADE: <span class="tick-val">60-70%</span></span>
        <span class="tick-item">VEG VPD: <span class="tick-val">0.8-1.1 kPa</span></span>
        <span class="tick-item">FLORA TEMP: <span class="tick-val">20-25°C</span></span>
        <span class="tick-item">FLORA UMIDADE: <span class="tick-val">40-50%</span></span>
        <span class="tick-item">FLORA VPD: <span class="tick-val">1.2-1.5 kPa</span></span>
        <span class="tick-item">PH SOLO: <span class="tick-val">6.0-6.8</span></span>
        <span class="tick-item">PH HYDRO: <span class="tick-val">5.5-6.5</span></span>
    </div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# ==============================================================================
# 🧠 CÉREBRO CANNÁBICO
# ==============================================================================

# Seletor de Variedade
variedades = engine.listar_culturas()
var_sel = st.selectbox("🧬 SELECIONE A VARIEDADE / GENÉTICA:", variedades)

if var_sel:
    # 3 Abas Focadas no Grower
    tab_gen, tab_setup, tab_doctor = st.tabs(["🧬 GENÉTICA & CICLO", "💡 SETUP & MANEJO", "🛡️ DOCTOR GROW"])

    # --- ABA 1: GENÉTICA & CICLO DE VIDA ---
    with tab_gen:
        dados = engine.db[var_sel]
        
        # Header da Genética
        st.markdown(f"""
        <div class="strain-card">
            <h3 style="color:#a855f7; margin:0;">{var_sel}</h3>
            <p style="color:#e0e0e0; font-size:1.1rem; margin-top:10px;">{dados['descricao']}</p>
            <div style="margin-top:15px;">
                {' '.join([f'<span style="background:#222; border:1px solid #555; padding:4px 10px; border-radius:15px; font-size:0.8rem; color:#fff; margin-right:5px;">🔥 {g}</span>' for g in dados['geneticas_famosas']])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📅 Ciclo de Vida & Fases")
        for fase, info in dados['ciclo_vida'].items():
            with st.expander(f"{fase} | Foco: {info['foco']}", expanded=False):
                st.markdown(f"**Detalhes:** {info['detalhe']}")
                st.markdown(f"""<div class="alert-box">⚠️ {info['alerta']}</div>""", unsafe_allow_html=True)
                
                

    # --- ABA 2: SETUP & MANEJO (O MANUAL TÉCNICO) ---
    with tab_setup:
        manejo = dados['manejo_grow']
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f"""
            <div class="grow-card">
                <div class="grow-label">☀️ Iluminação (PPFD)</div>
                <div class="grow-val">{manejo['luz']}</div>
            </div>
            <div class="grow-card">
                <div class="grow-label">🌡️ Clima (VPD)</div>
                <div class="grow-val">{manejo['clima_ideal']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="grow-card">
                <div class="grow-label">🧪 Nutrição (EC/PPM)</div>
                <div class="grow-val">{manejo['nutricao']}</div>
            </div>
            <div class="grow-card">
                <div class="grow-label">✂️ Treinamento (LST/HST)</div>
                <div class="grow-val">{manejo['treinamento']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.info(f"🪚 **Colheita:** {manejo['colheita']}")

        # Calculadora Rápida de VPD (Bônus)
        st.markdown("---")
        st.markdown("#### 📟 Calculadora Rápida de VPD")
        cv1, cv2 = st.columns(2)
        t_ar = cv1.number_input("Temperatura (°C):", 25.0)
        u_ar = cv2.number_input("Umidade Relativa (%):", 60.0)
        
        if st.button("Calcular VPD"):
            # Fórmula aproximada de VPD
            svp = 0.61078 * 2.71828**((17.27 * t_ar) / (t_ar + 237.3))
            vpd = svp * (1 - (u_ar / 100))
            
            cor_vpd = "#22c55e" # Ideal
            if vpd < 0.4 or vpd > 1.6: cor_vpd = "#ef4444" # Perigo
            elif vpd < 0.8 or vpd > 1.2: cor_vpd = "#eab308" # Atenção
            
            st.markdown(f"""
            <div style="background:{cor_vpd}; color:#000; padding:10px; border-radius:8px; text-align:center; font-weight:bold; font-size:1.5rem;">
                VPD: {vpd:.2f} kPa
            </div>
            """, unsafe_allow_html=True)

    # --- ABA 3: DOCTOR GROW (PRAGAS & DOENÇAS) ---
    with tab_doctor:
        st.caption("Identificação e combate de pragas comuns em cultivos indoor/outdoor.")
        
        tipo_prob = st.radio("Tipo:", ["Pragas 🕷️", "Doenças/Fungos 🍄"], horizontal=True)
        chave = "Pragas" if "Pragas" in tipo_prob else "Doencas"
        
        problemas = engine.buscar_problema(var_sel, None, chave)
        
        for nome, info in problemas.items():
            st.markdown(f"""
            <div style="border:1px solid #333; padding:15px; border-radius:8px; margin-bottom:10px; background:#111;">
                <h4 style="color:#ff6b6b; margin:0;">{nome}</h4>
                <p style="color:#888; font-size:0.9rem;">{info['tipo']}</p>
                <p><b>🔍 Identificação:</b> {info['identificacao']}</p>
                <p><b>☠️ Dano:</b> {info['dano']}</p>
                <div style="margin-top:10px; background:#1e1e1e; padding:10px; border-radius:4px;">
                    <b style="color:#22c55e;">✅ Soluções:</b><br>
                    {' • '.join(info['solucao'])}
                </div>
                <p style="font-size:0.85rem; color:#f97316; margin-top:5px;"><i>⚠️ {info['obs']}</i></p>
            </div>
            """, unsafe_allow_html=True)
