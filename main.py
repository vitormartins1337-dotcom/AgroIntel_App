# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | MASTER EDITION V9.2 (ATUALIZADO)
# DESCRIÇÃO: Painel Agronômico com Seleção de Ambiente e Nutrição Dinâmica

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
        .stApp { background-color: #050505; color: #e4e4e7; font-family: 'Inter', sans-serif; }
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }

        /* --- HEADER HERO --- */
        .hero-card {
            position: relative;
            background: linear-gradient(135deg, #1a0b2e 0%, #000000 100%);
            border: 1px solid #a855f7;
            box-shadow: 0 0 60px rgba(168, 85, 247, 0.25);
            border-radius: 20px;
            padding: 50px 20px;
            margin-bottom: 30px;
            display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden;
        }
        .main-title {
            font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 900; color: #fff;
            line-height: 1; letter-spacing: -2px; text-align: center;
            text-shadow: 0 0 30px rgba(168, 85, 247, 0.6); z-index: 1;
        }
        .sub-title {
            font-family: 'Courier New', monospace; font-size: clamp(0.7rem, 1.5vw, 1rem);
            color: #d8b4fe; letter-spacing: 4px; text-transform: uppercase;
            margin-top: 15px; font-weight: 600; text-align: center; opacity: 0.9; z-index: 1;
        }
        /* BOTÃO ONLINE (AGORA NO RODAPÉ DIREITO) */
        .status-pill {
            position: absolute;
            bottom: 20px; /* Mudou de top para bottom */
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

        /* --- TICKER --- */
        .ticker-wrap {
            width: 100%; overflow: hidden; background: #000; 
            border-top: 1px solid #333; border-bottom: 1px solid #333; 
            height: 36px; display: flex; align-items: center; margin-bottom: 25px;
        }
        .tick-item { margin-right: 40px; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #a855f7; }
        .tick-val { color: #fff; margin-left: 5px; font-weight: bold; }

        /* --- CARDS DASHBOARD --- */
        .status-card {
            background: linear-gradient(145deg, #120520 0%, #050505 100%);
            border: 1px solid #3b0764; border-left: 5px solid #a855f7;
            border-radius: 12px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); height: 100%;
        }
        .yield-card {
            background: linear-gradient(135deg, #1e1b10 0%, #000000 100%);
            border: 1px solid #854d0e; border-right: 5px solid #eab308;
            border-radius: 12px; padding: 25px; text-align: center; height: 100%;
            display: flex; flex-direction: column; justify-content: center;
            box-shadow: 0 4px 20px rgba(234, 179, 8, 0.15);
        }
        .diag-card {
            background: #0f0f0f; border: 1px solid #333; border-radius: 12px; padding: 20px;
            margin-top: 20px; position: relative;
        }

        /* --- TIPOGRAFIA CARDS --- */
        .card-label { font-size: 0.75rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 8px; }
        .big-val { font-size: 2.5rem; font-weight: 900; color: #fff; line-height: 1; margin-bottom: 5px; }
        .sub-info { font-size: 0.9rem; color: #d1d5db; margin-top: 5px; }
        
        .meta-badge { display: inline-block; padding: 5px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; margin-right: 6px; margin-top: 5px; }
        .bg-ph { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid #1e3a8a; }
        .bg-ec { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid #064e3b; }
        .divider { height: 1px; background: #333; margin: 20px 0; }

        /* INPUTS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div, .stTextInput > div > div {
            background-color: #121212 !important; border: 1px solid #333 !important; color: #e0e0e0 !important; border-radius: 6px !important;
        }
        
        /* NUTRI BALLOONS (BALÕES COLORIDOS) */
        .nutri-ball {
            display: inline-flex; flex-direction: column; align-items: center; justify-content: center;
            width: 80px; height: 80px; border-radius: 50%; margin: 10px;
            border: 2px solid; background: rgba(0,0,0,0.5);
            font-weight: 900; font-size: 1.2rem; box-shadow: 0 0 15px rgba(0,0,0,0.2);
        }
        .ball-label { font-size: 0.6rem; font-weight: normal; margin-bottom: 2px; opacity: 0.8;}

        /* DOCTOR & NUTRI CARDS */
        .doc-card { background: #0f0f0f; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #333; }
        .nutri-card { background: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; height: 100%; position:relative; overflow:hidden;}
        
        .solucao-tag { padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; margin-right: 5px; display: inline-block; margin-bottom: 4px; font-weight:bold;}
        .bio { background: rgba(34, 197, 94, 0.1); border: 1px solid #15803d; color: #86efac; }
        .quim { background: rgba(239, 68, 68, 0.1); border: 1px solid #991b1b; color: #fca5a5; }
        </style>
    """, unsafe_allow_html=True)
load_master_css()

# --- 3. HEADER HERO ---
st.markdown("""
<div class="hero-card">
<div class="status-pill"><span style="font-size:1rem; line-height:1;">🍁</span> ONLINE</div>
<div class="main-title">AGROWER <span style="color:#a855f7">SDI</span></div>
<div class="sub-title">SISTEMA DE DECISÃO INTEGRADA</div>
</div>
""", unsafe_allow_html=True)

# Ticker
st.markdown("""
<div class="ticker-wrap">
    <div style="display:inline-block; white-space:nowrap; animation:ticker 45s linear infinite;">
        <span class="tick-item">VPD IDEAL <span class="tick-val">0.8-1.2 kPa</span></span>
        <span class="tick-item">TEMP FLORA <span class="tick-val">22-26°C</span></span>
        <span class="tick-item">UMIDADE FLORA <span class="tick-val">45-50%</span></span>
        <span class="tick-item">PH SOLO <span class="tick-val">6.0-6.8</span></span>
        <span class="tick-item">EC FLORA <span class="tick-val">1.8-2.4 mS</span></span>
    </div>
</div>
<style>@keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. PAINEL DE CONTROLE & INTELIGÊNCIA ARTIFICIAL (SDI ENGINE V9.7)
# ==============================================================================

# --- A. INPUTS GERAIS ---
st.markdown("<br>", unsafe_allow_html=True)

# Linha 1: Configurações Básicas
c_in1, c_in2, c_in3, c_in4 = st.columns([1.5, 1.5, 1, 1])
with c_in1:
    genetica_sel = st.selectbox("🧬 GENÉTICA PREDOMINANTE", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
with c_in2:
    ambiente_sel = st.selectbox("🏠 AMBIENTE", ["Indoor", "Estufa Outdoor (Complementar)", "Outdoor (Sol Pleno)"])
with c_in3:
    n_plantas = st.number_input("Nº PLANTAS", 1, 500, 4)
with c_in4:
    data_inicio = st.date_input("📅 INÍCIO", datetime.date.today() - datetime.timedelta(days=45))

# Linha 2: Método e Sistema Radicular (NOVO)
c_sub1, c_sub2, c_sub3 = st.columns([1.5, 1.5, 1.5])
with c_sub1:
     metodo_sel = st.selectbox("🥣 SUBSTRATO / MÉTODO", list(db.get("METODOS_CULTIVO", {}).keys()))

with c_sub2:
    # NOVO: Seleção do Sistema de Plantio
    tipo_plantio = st.selectbox("🌱 SISTEMA DE PLANTIO", ["Vasos", "Solo Direto (Chão/Canteiro)"])

with c_sub3:
    # Lógica Condicional para Vasos
    vol_vaso = 0
    if tipo_plantio == "Vasos":
        vol_vaso = st.selectbox("VOLUME DO VASO (L)", [7, 11, 20, 30, 50, 100, 200])
    else:
        st.info("Raízes livres no solo.")
        vol_vaso = 999 # Valor simbólico para solo infinito

# --- B. ENGINE DE DIAGNÓSTICO PROFISSIONAL (SDI LOGIC) ---
watts_painel = 0; area_cultivo = 0; diagnostico_titulo = ""; diagnostico_texto = ""; sugestao_premium = ""; cor_diag = "#333"; show_diag = False

# Lógica Indoor/Estufa
if ambiente_sel in ["Indoor", "Estufa Outdoor (Complementar)"]:
    with st.expander("💡 CONFIGURAÇÃO DE ILUMINAÇÃO & ESPAÇO", expanded=True):
        cl1, cl2, cl3 = st.columns(3)
        with cl1: watts_painel = st.number_input("POTÊNCIA TOTAL (W REAIS):", 50, 5000, 240)
        with cl2: largura = st.number_input("LARGURA (cm):", 40, 1000, 80)
        with cl3: profundidade = st.number_input("PROFUNDIDADE (cm):", 40, 1000, 80)
        
        area_m2 = (largura * profundidade) / 10000 
        if area_m2 > 0:
            show_diag = True
            ppfd_w = watts_painel / area_m2
            densidade = n_plantas / area_m2
            w_planta = watts_painel / n_plantas
            
            # 1. ANÁLISE DE DENSIDADE (PLANTAS)
            is_crowded = False
            if densidade > 16:
                is_crowded = True
                txt_dens = f"⚠️ <b>SUPERPOPULAÇÃO ({densidade:.1f} un/m²)</b>: Muitas plantas! Competição severa."
                cor_diag = "#ef4444"
                sugestao_premium = "Reduza o número de plantas ou use vasos de 4-7L com veg de 1 semana (SOG)."
            elif densidade < 4:
                txt_dens = f"ℹ️ <b>BAIXA DENSIDADE ({densidade:.1f} un/m²)</b>: Espaço sobrando."
                sugestao_premium = "Faça um veg mais longo (6-8 semanas) e use podas/amarras (SCROG) para preencher a luz."
                if cor_diag == "#333": cor_diag = "#38bdf8"
            else:
                txt_dens = f"✅ <b>DENSIDADE OK ({densidade:.1f} un/m²)</b>: Equilíbrio ideal."

            # 2. ANÁLISE DE LUZ
            if ppfd_w < 250:
                txt_luz = f"⚠️ <b>LUZ FRACA ({ppfd_w:.0f} W/m²)</b>: Buds aerados ('pipoca')."
                if cor_diag != "#ef4444": cor_diag = "#eab308"
            elif ppfd_w > 650:
                txt_luz = f"🔥 <b>LUZ EXTREMA ({ppfd_w:.0f} W/m²)</b>: Risco de queima."
                sugestao_premium = "Use CO2 ou suba o painel."
                cor_diag = "#ef4444"
            else:
                txt_luz = f"✅ <b>LUZ PERFEITA ({ppfd_w:.0f} W/m²)</b>: Sweet Spot."
                if cor_diag == "#333": cor_diag = "#22c55e"

            # 3. ANÁLISE DE RAÍZES (NOVO!)
            txt_raiz = ""
            info_gen = db["GENETICAS_PARAMETROS"][genetica_sel]
            
            if tipo_plantio == "Vasos":
                # Fotoperíodo em vaso pequeno = Problema
                if info_gen['tipo'] == "Foto" and vol_vaso < 10:
                    txt_raiz = f"⚠️ <b>RESTRIÇÃO RADICULAR ({vol_vaso}L)</b>: Vaso pequeno para Fotoperíodo. Risco de 'Root Bound'."
                    sugestao_premium = "Para vasos pequenos, não deixe vegar mais de 3 semanas ou a planta travará na flora."
                    if cor_diag != "#ef4444": cor_diag = "#eab308"
                # Automática em vaso gigante = Desperdício
                elif info_gen['tipo'] == "Auto" and vol_vaso > 25:
                    txt_raiz = f"ℹ️ <b>VASO SUPERDIMENSIONADO ({vol_vaso}L)</b>: Automáticas raramente usam mais que 20L."
                else:
                    txt_raiz = f"✅ <b>VOLUME DE RAIZ ({vol_vaso}L)</b>: Adequado para a genética."
            else:
                txt_raiz = "🌿 <b>SOLO LIVRE</b>: Potencial máximo de raiz. Cuidado com altura incontrolável."

            # MONTAGEM FINAL
            diagnostico_titulo = "CONSULTORIA SDI (AMBIENTE & RAÍZES)"
            diagnostico_texto = f"""
            <div style="margin-bottom:5px;">{txt_dens}</div>
            <div style="margin-bottom:5px;">{txt_luz}</div>
            <div style="margin-bottom:10px;">{txt_raiz}</div>
            <div style="margin-top:15px; padding:10px; background:rgba(255,255,255,0.05); border-radius:8px; border-left:3px solid {cor_diag};">
                <span style="color:{cor_diag}; font-weight:bold;">RECOMENDAÇÃO MASTER:</span><br>
                {sugestao_premium if sugestao_premium else "Seu setup está balanceado. Mantenha o VPD constante."}
            </div>
            """

else:
    # Lógica Outdoor
    show_diag = True
    diagnostico_titulo = "CONSULTORIA TÉCNICA (OUTDOOR)"
    cor_diag = "#facc15"
    aviso_vaso = ""
    if tipo_plantio == "Vasos" and vol_vaso < 30:
        aviso_vaso = f"⚠️ <b>ALERTA DE SECA:</b> Em outdoor, vasos de {vol_vaso}L secam muito rápido no sol. Use Mulching (cobertura morta)."
    
    diagnostico_texto = f"""
    <div>☀️ <b>ENERGIA SOLAR (FULL SPECTRUM)</b></div>
    <div style="margin-top:5px; font-size:0.9rem;">O sol fornece luz infinita. O limite é a água e nutrição.</div>
    <div style="margin-top:10px;">{aviso_vaso}</div>
    """

# --- C. MOTOR DE CÁLCULO (DADOS GERAIS) ---
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7
yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas
yield_kg = yield_total / 1000 

fase_nome = "Indefinida"; fase_dados = {}
range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
fator_ciclo = 0.75 if info_genetica.get("tipo") == "Auto" else 1.0
for k, v in db.get("FASES_DINAMICAS", {}).items():
    chave_limpa = k.split(' ')[0]
    limite = int(range_map.get(chave_limpa, 200) * fator_ciclo)
    if dias_vida <= limite: fase_nome = k; fase_dados = v; break

# --- EXIBIÇÃO ÚNICA DO DIAGNÓSTICO ---
if show_diag:
    st.markdown(f"""
    <div class="diag-card" style="border-left: 4px solid {cor_diag}; margin-top:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #333; padding-bottom:10px;">
            <div style="font-weight:900; color:{cor_diag}; letter-spacing:1px; font-size:1.1rem;">{diagnostico_titulo}</div>
            <div style="background:{cor_diag}20; color:{cor_diag}; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:bold;">ANÁLISE IA</div>
        </div>
        <div style="color:#e4e4e7; font-size:0.95rem; line-height:1.6;">{diagnostico_texto}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 5. CARDS DASHBOARD
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns([1.8, 1.2])

with col_a:
    st.markdown(f"""
    <div class="status-card">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div><div class="card-label" style="color:#d8b4fe;">FASE ATUAL ({info_genetica.get('tipo', 'Foto').upper()})</div><div class="big-val">{fase_nome.upper()}</div></div>
            <div style="text-align:right;"><div class="card-label">TEMPO</div><div style="font-size:1.5rem; font-weight:bold; color:#fff;">{dias_vida} <span style="font-size:0.9rem; color:#888;">DIAS</span></div><div style="font-size:0.85rem; color:#a855f7;">SEMANA {semanas}</div></div>
        </div>
        <div class="divider"></div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div><div class="card-label">OBJETIVO TÁTICO</div><div style="color:#fff; font-weight:600;">🎯 {fase_dados.get('foco', '-')}</div></div>
            <div style="text-align:right;"><div class="card-label">METAS DO AMBIENTE</div><div><span class="meta-badge bg-ph">💧 PH {info_metodo['ph_ideal']}</span><span class="meta-badge bg-ec">⚡ EC {info_metodo['ec_ideal']}</span></div></div>
        </div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="yield-card">
        <div class="card-label" style="color:#fcd34d;">ESTIMATIVA DE COLHEITA</div><div class="big-val" style="color:#fef08a;">{yield_total:.0f}g</div><div class="sub-info" style="color:#fde047;">~ {yield_kg:.2f} kg (Seco)</div>
        <div class="divider" style="background: #422006;"></div>
        <div style="font-size:0.75rem; color:#ca8a04;">BASE: <b>{n_plantas} plantas</b> ({info_genetica['tipo']})</div>
    </div>""", unsafe_allow_html=True)

    # CARD DIAGNÓSTICO (ATUALIZADO PARA O NOVO MOTOR IA)
# Este bloco verifica se o motor SDI gerou um diagnóstico (show_diag)
if 'show_diag' in locals() and show_diag:
    st.markdown(f"""
    <div class="diag-card" style="border-left: 4px solid {cor_diag}; margin-top:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #333; padding-bottom:10px;">
            <div style="font-weight:900; color:{cor_diag}; letter-spacing:1px; font-size:1.1rem;">{diagnostico_titulo}</div>
            <div style="background:{cor_diag}20; color:{cor_diag}; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:bold;">ANÁLISE IA</div>
        </div>
        <div style="color:#e4e4e7; font-size:0.95rem; line-height:1.6;">{diagnostico_texto}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. ABAS: NUTRIÇÃO & DOCTOR (ATUALIZADO E CORRIGIDO)
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
tab_nutri, tab_doctor = st.tabs(["🧪 NUTRIÇÃO & MARCHA DE ABSORÇÃO", "🚑 DOCTOR GROW (FITOSSANIDADE)"])

# --- ABA 1: NUTRIÇÃO DINÂMICA (CORRIGIDA) ---
with tab_nutri:
    st.markdown("### 📊 Demanda Nutricional Atual")
    
    nutri = db["NUTRI_MARCHA_ABSORCAO"]
    
    # Lógica Dinâmica: Pega os valores da Semana Atual
    s_idx = min(semanas - 1, 11) if semanas > 0 else 0
    val_n = nutri['N'][s_idx]
    val_p = nutri['P'][s_idx]
    val_k = nutri['K'][s_idx]
    
    # BALÕES COLORIDOS DINÂMICOS
    st.markdown(f"""
    <div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-bottom:20px;">
        <div class="nutri-ball" style="border-color:#22c55e; color:#22c55e;">
            <span class="ball-label">N</span>{val_n}%
        </div>
        <div class="nutri-ball" style="border-color:#3b82f6; color:#3b82f6;">
            <span class="ball-label">P</span>{val_p}%
        </div>
        <div class="nutri-ball" style="border-color:#a855f7; color:#a855f7;">
            <span class="ball-label">K</span>{val_k}%
        </div>
    </div>
    <div style="text-align:center; font-size:0.8rem; color:#888; margin-bottom:20px;">
        DEMANDA RELATIVA NA SEMANA {semanas}
    </div>
    """, unsafe_allow_html=True)

    # GRÁFICO DE LINHAS NEON
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nutri['semanas'], y=nutri['N'], name='Nitrogênio (N)', line=dict(color='#22c55e', width=3)))
    fig.add_trace(go.Scatter(x=nutri['semanas'], y=nutri['P'], name='Fósforo (P)', line=dict(color='#3b82f6', width=3)))
    fig.add_trace(go.Scatter(x=nutri['semanas'], y=nutri['K'], name='Potássio (K)', line=dict(color='#a855f7', width=3)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#ccc"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#333'), height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🔍 Enciclopédia de Deficiências")
    
    # CARDS DE DEFICIÊNCIA (CORRIGIDO PARA O DB V9.0)
    cols_def = st.columns(4)
    defs_items = list(db["DEFICIENCIAS_VISUAIS"].items())
    
    for i, (k, v) in enumerate(defs_items):
        with cols_def[i % 4]:
            # Usa .get para evitar erros se faltar chave, e acessa 'correcao_bio' e 'correcao_quim'
            cor_card = v.get('cor_card', '#333')
            st.markdown(f"""
            <div class="nutri-card" style="border-left: 4px solid {cor_card};">
                <div style="color:{cor_card}; font-weight:bold; margin-bottom:5px; font-size:0.9rem;">{k}</div>
                <div style="font-size:0.75rem; color:#888; text-transform:uppercase; margin-bottom:10px;">{v.get('tipo', 'Macro')}</div>
                
                <div style="font-size:0.85rem; color:#e4e4e7; margin-bottom:15px; height:60px; overflow-y:auto;">
                    {v['sintoma']}
                </div>
                
                <div style="margin-bottom:5px;">
                    <div style="font-size:0.7rem; color:#4ade80; font-weight:bold;">BIO:</div>
                    <div style="font-size:0.75rem; color:#ccc;">{v.get('correcao_bio', '-')}</div>
                </div>
                <div>
                    <div style="font-size:0.7rem; color:#f87171; font-weight:bold;">QUÍMICO:</div>
                    <div style="font-size:0.75rem; color:#ccc;">{v.get('correcao_quim', '-')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ABA 2: DOCTOR GROW ---
with tab_doctor:
    st.markdown("### 🕷️ Identificação e Tratamento")
    busca = st.text_input("Buscar Praga:")
    for nome, info in db["DOCTOR_GROW_FITOSSANIDADE"].items():
        if busca and busca.lower() not in nome.lower(): continue
        
        cor_g = "#ef4444"
        if info['gravidade'] == "MÉDIA": cor_g = "#eab308"
        
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
