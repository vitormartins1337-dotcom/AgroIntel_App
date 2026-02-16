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
# 4. PAINEL DE CONTROLE & INTELIGÊNCIA ARTIFICIAL (SDI ENGINE V10.0 - PHYSICS)
# ==============================================================================

# --- A. INPUTS GERAIS ---
st.markdown("<br>", unsafe_allow_html=True)

# LINHA 1: Definições Biológicas e Espaciais
c_in1, c_in2, c_in3, c_in4 = st.columns([1.5, 1.5, 1, 1])
with c_in1:
    genetica_sel = st.selectbox("🧬 GENÉTICA PREDOMINANTE", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
with c_in2:
    ambiente_sel = st.selectbox("🏠 AMBIENTE", ["Indoor", "Estufa Outdoor (Complementar)", "Outdoor (Sol Pleno)"])
with c_in3:
    n_plantas = st.number_input("Nº PLANTAS", 1, 500, 4)
with c_in4:
    data_inicio = st.date_input("📅 INÍCIO", datetime.date.today() - datetime.timedelta(days=45))

# LINHA 2: Sistema Radicular (CRUCIAL PARA O CÁLCULO FÍSICO)
c_sub1, c_sub2, c_sub3 = st.columns([1.5, 1.5, 1.5])
with c_sub1:
     metodo_sel = st.selectbox("🥣 SUBSTRATO / MÉTODO", list(db.get("METODOS_CULTIVO", {}).keys()))
with c_sub2:
    tipo_plantio = st.selectbox("🌱 SISTEMA DE PLANTIO", ["Vasos", "Solo Direto (Chão/Canteiro)"])
with c_sub3:
    vol_vaso = 0
    if tipo_plantio == "Vasos":
        # Seleção de Litragem (Define o diâmetro físico)
        vol_vaso = st.selectbox("VOLUME DO VASO (L)", [4, 7, 11, 15, 20, 30, 50, 100])
    else:
        st.info("Raízes livres (Canteiro).")
        vol_vaso = 999 

# --- B. ENGINE SDI (CÁLCULO DE VIABILIDADE FÍSICA E AGRONÔMICA) ---
# Inicialização de variáveis
watts_painel = 0; area_cultivo = 0; diagnostico_titulo = ""; diagnostico_texto = ""; sugestao_premium = ""; cor_diag = "#333"; show_diag = False
txt_fisica = ""; txt_luz = ""; txt_raiz = ""

# MAPA DE DIMENSÕES FÍSICAS (Estimativa de Diâmetro de Vasos Padrão)
# Vaso 4L ~18cm | 7L ~22cm | 11L ~25cm | 20L ~30cm | 30L ~36cm | 50L ~45cm
mapa_area_vaso = {
    4: 0.03, 7: 0.05, 11: 0.06, 15: 0.07, 20: 0.09, 30: 0.13, 50: 0.20, 100: 0.40
}

if ambiente_sel in ["Indoor", "Estufa Outdoor (Complementar)"]:
    with st.expander("💡 CONFIGURAÇÃO DE ILUMINAÇÃO & ESPAÇO", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1: watts_painel = st.number_input("POTÊNCIA TOTAL (W):", 50, 5000, 240)
        with col2: largura = st.number_input("LARGURA (cm):", 40, 1000, 80)
        with col3: profundidade = st.number_input("PROFUNDIDADE (cm):", 40, 1000, 80)
        
        # --- CÉREBRO DO SISTEMA (CÁLCULOS CRUZADOS) ---
        area_m2 = (largura * profundidade) / 10000 
        
        if area_m2 > 0:
            show_diag = True
            
            # 1. ANÁLISE FÍSICA (Ocupação de Piso)
            # Verifica se os vasos cabem no chão fisicamente
            area_ocupada_vasos = 0
            ocupacao_piso = 0
            
            if tipo_plantio == "Vasos":
                area_unitaria = mapa_area_vaso.get(vol_vaso, 0.09)
                area_ocupada_vasos = n_plantas * area_unitaria
                ocupacao_piso = (area_ocupada_vasos / area_m2) * 100 # Em %
                
                if ocupacao_piso > 100:
                    # IMPOSSÍVEL FÍSICO
                    txt_fisica = f"🚫 <b>ERRO FÍSICO CRÍTICO (OCUPAÇÃO {ocupacao_piso:.0f}%)</b>: Impossível colocar {n_plantas} vasos de {vol_vaso}L neste espaço. Eles ocupam {area_ocupada_vasos:.2f}m² e você só tem {area_m2:.2f}m²."
                    sugestao_premium = f"REDUÇÃO OBRIGATÓRIA: Para vasos de {vol_vaso}L neste espaço, o máximo absoluto são {int(area_m2 / area_unitaria)} plantas (coladas umas nas outras)."
                    cor_diag = "#ef4444" # Vermelho Fatal
                elif ocupacao_piso > 75:
                    # SUPERLOTAÇÃO DE DOSSEL
                    txt_fisica = f"⚠️ <b>SUPERLOTAÇÃO SEVERA (PISO {ocupacao_piso:.0f}%)</b>: Os vasos cabem, mas ficarão colados. Não haverá espaço para circulação de ar, rega ou crescimento lateral."
                    sugestao_premium = "Diminua o tamanho dos vasos para 7L-11L ou reduza a quantidade de plantas pela metade."
                    if cor_diag == "#333": cor_diag = "#ef4444"
                elif ocupacao_piso > 50:
                    # ALTA DENSIDADE (SOG)
                    txt_fisica = f"⚠️ <b>ALTA DENSIDADE (PISO {ocupacao_piso:.0f}%)</b>: Configuração SOG (Sea of Green). As plantas vão brigar por luz lateral."
                    if not sugestao_premium: sugestao_premium = "Ciclo Vegetativo MÁXIMO de 2 semanas. Faça poda Lollipopping urgente na pré-flora."
                    if cor_diag == "#333": cor_diag = "#eab308"
                else:
                    txt_fisica = f"✅ <b>ESPAÇAMENTO OTIMIZADO (PISO {ocupacao_piso:.0f}%)</b>: Espaço ideal para desenvolvimento lateral e circulação de ar."
                    if cor_diag == "#333": cor_diag = "#22c55e"
            else:
                txt_fisica = "🌿 <b>CANTEIRO/SOLO</b>: Área de raiz compartilhada. Atenção apenas à competição por luz."

            # 2. ANÁLISE DE LUZ (W/m²)
            ppfd_w = watts_painel / area_m2
            if ppfd_w < 250:
                txt_luz = f"⚠️ <b>LUZ FRACA ({ppfd_w:.0f} W/m²)</b>: Buds 'pipoca' (aerados)."
                if cor_diag == "#22c55e": cor_diag = "#eab308"
            elif ppfd_w > 650:
                txt_luz = f"🔥 <b>LUZ EXTREMA ({ppfd_w:.0f} W/m²)</b>: Necessário CO2 suplementar."
                if cor_diag != "#ef4444": sugestao_premium = "Adicione CO2 ou suba o painel para 60cm+."
            else:
                txt_luz = f"✅ <b>LUZ IDEAL ({ppfd_w:.0f} W/m²)</b>: Sweet Spot."

            # 3. ANÁLISE DE RAÍZES (GENÉTICA x VASO)
            # Cruzamento inteligente: Genética vs Tempo vs Litragem
            info_gen = db["GENETICAS_PARAMETROS"][genetica_sel]
            
            if tipo_plantio == "Vasos":
                # Erro comum: Automática em vaso gigante (desperdício de substrato/luz)
                if info_gen['tipo'] == "Auto" and vol_vaso > 25:
                    txt_raiz = f"ℹ️ <b>DESPERDÍCIO ({vol_vaso}L)</b>: Automáticas raramente colonizam mais que 20L."
                # Erro comum: Fotoperíodo em vaso minúsculo (Root Bound)
                elif info_gen['tipo'] == "Foto" and vol_vaso < 7:
                    txt_raiz = f"⚠️ <b>RAIZ LIMITADA ({vol_vaso}L)</b>: Vaso muito pequeno para fotoperíodo. Risco de travar na flora."
                    if not sugestao_premium: sugestao_premium = "Mantenha o vegetativo curto (max 15 dias) ou transplante antes da flora."
                else:
                    txt_raiz = f"✅ <b>RAIZ COMPATÍVEL</b>: Volume adequado para {info_gen['tipo']}."

            # CONSTRUÇÃO DO CARD DE DIAGNÓSTICO
            diagnostico_titulo = "CONSULTORIA SDI (ANÁLISE DE VIABILIDADE)"
            diagnostico_texto = f"""
            <div style="margin-bottom:8px;">{txt_fisica}</div>
            <div style="margin-bottom:8px;">{txt_luz}</div>
            <div style="margin-bottom:10px;">{txt_raiz}</div>
            <div style="margin-top:15px; padding:12px; background:rgba(255,255,255,0.05); border-radius:8px; border-left:3px solid {cor_diag};">
                <span style="color:{cor_diag}; font-weight:bold; font-size:0.85rem;">RECOMENDAÇÃO MASTER:</span><br>
                {sugestao_premium if sugestao_premium else "Configuração balanceada. Mantenha VPD e nutrição constantes."}
            </div>
            """

else:
    # Lógica Outdoor
    show_diag = True
    diagnostico_titulo = "CONSULTORIA TÉCNICA (OUTDOOR)"
    cor_diag = "#facc15"
    aviso_vaso = ""
    if tipo_plantio == "Vasos" and vol_vaso < 30:
        aviso_vaso = f"⚠️ <b>RISCO DE DESIDRATAÇÃO ({vol_vaso}L):</b> No sol pleno, vasos menores que 30L aquecem e secam em horas. Use Mulching."
    
    diagnostico_texto = f"""
    <div>☀️ <b>ENERGIA SOLAR (FULL SPECTRUM)</b></div>
    <div style="margin-top:5px; font-size:0.9rem;">
        Outdoor: O limite é o volume de raiz. Para {n_plantas} plantas grandes, garanta nutrição pesada.
    </div>
    <div style="margin-top:10px;">{aviso_vaso}</div>
    """

# --- C. MOTOR DE CÁLCULO GERAL (NECESSÁRIO PARA OS CARDS SEGUINTES) ---
# Mantém o cálculo de Yield e Fase para não dar erro lá embaixo
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
    limite = int(range_map.get(chave_limpa, 200) * fator_ciclo) # chave_limpa corrigida abaixo
    chave_limpa = k.split(' ')[0]
    limite = int(range_map.get(chave_limpa, 200) * fator_ciclo)
    if dias_vida <= limite: fase_nome = k; fase_dados = v; break

# --- EXIBIÇÃO DO DIAGNÓSTICO (ÚNICA VEZ) ---
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
