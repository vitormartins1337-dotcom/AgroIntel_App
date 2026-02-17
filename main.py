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
# 4. PAINEL DE CONTROLE & INTELIGÊNCIA ARTIFICIAL (SDI ENGINE V14.0 - DIDÁTICA)
# ==============================================================================

# --- A. INPUTS PRINCIPAIS (COMANDO DE BORDO) ---
st.markdown("<br>", unsafe_allow_html=True)

# LINHA 1: Definições Básicas
c_in1, c_in2, c_in3, c_in4 = st.columns([1.5, 1.8, 1, 1])
with c_in1:
    genetica_sel = st.selectbox("🧬 GENÉTICA", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
with c_in2:
    # SELEÇÃO DE AMBIENTE REFINADA E ESPECÍFICA
    ambiente_sel = st.selectbox("🏠 ONDE VOCÊ PLANTA?", [
        "Indoor (Luz Artificial Controlada)", 
        "Estufa/Greenhouse (Sol + Luz Complementar)", 
        "Estufa/Greenhouse (Somente Sol)", 
        "Outdoor (Céu Aberto/Quintal)"
    ])
with c_in3:
    n_plantas = st.number_input("Nº PLANTAS", 1, 1000, 4)
with c_in4:
    data_inicio = st.date_input("📅 INÍCIO", datetime.date.today() - datetime.timedelta(days=45))

# LINHA 2: Substrato e Fotoperíodo
c_sub1, c_sub2, c_sub3, c_sub4 = st.columns([1.5, 1.2, 1.2, 1.5])
with c_sub1:
     metodo_sel = st.selectbox("🥣 MÉTODO", list(db.get("METODOS_CULTIVO", {}).keys()))
with c_sub2:
    tipo_plantio = st.selectbox("🌱 ONDE ESTÃO?", ["Vasos", "Canteiro/Chão"])
with c_sub3:
    vol_vaso = 0
    if tipo_plantio == "Vasos":
        vol_vaso = st.selectbox("TAMANHO VASO", [4, 7, 11, 15, 20, 25, 30, 40, 50, 100], index=2, format_func=lambda x: f"{x} Litros")
    else:
        vol_vaso = 999 # Solo infinito
with c_sub4:
    horas_luz = st.number_input("⏰ HORAS DE LUZ/DIA", 10, 24, 18, help="Quanto tempo a planta recebe luz por dia?")

# --- B. CÉREBRO DO SISTEMA (CÁLCULOS E TRADUÇÃO PARA LEIGOS) ---
# Inicialização
watts_painel = 0; area_m2 = 0; show_diag = False
titulo_diag = ""; texto_diag = ""; cor_diag = "#333"; recomendacao_premium = ""
txt_luz = ""; txt_espaco = ""; txt_raiz = ""

# MAPA FÍSICO: Quanto espaço cada vaso ocupa (Diâmetro + Folga para manuseio)
mapa_ocupacao = {4: 0.04, 7: 0.06, 11: 0.09, 15: 0.11, 20: 0.14, 25: 0.16, 30: 0.20, 40: 0.25, 50: 0.30, 100: 0.50}

# === ANÁLISE DO AMBIENTE ===

# CENÁRIO 1: INDOOR (Luz Artificial é tudo)
if "Indoor" in ambiente_sel:
    with st.expander("💡 CONFIGURAR MEU GROW (Luz e Tamanho)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: watts_painel = st.number_input("POTÊNCIA DO LED (Watts Reais):", 50, 5000, 240)
        with c2: largura = st.number_input("LARGURA (cm):", 40, 1000, 80)
        with c3: profundidade = st.number_input("PROFUNDIDADE (cm):", 40, 1000, 80)
        
        area_m2 = (largura * profundidade) / 10000
        if area_m2 > 0:
            show_diag = True
            ppfd = (watts_painel * 2.2) / area_m2 # Estimativa técnica
            dli = ppfd * horas_luz * 0.0036 # Luz total no dia
            
            if dli < 15:
                txt_luz = f"⚠️ <b>LUZ FRACA DEMAIS:</b> Sua planta vai crescer devagar e com galhos finos. Para floração, isso não vai dar buds gordos."
                cor_diag = "#eab308"
                recomendacao_premium = "Aproxime a luz das plantas (cuidado com calor) ou compre mais luz para a flora."
            elif 15 <= dli < 45:
                txt_luz = f"✅ <b>ILUMINAÇÃO PERFEITA:</b> Você está na faixa ideal. A planta tem energia suficiente para engordar as flores."
                cor_diag = "#22c55e"
            else:
                txt_luz = f"🔥 <b>PERIGO DE QUEIMA:</b> A luz está muito forte! Sem CO2 extra, as folhas vão amarelar e travar."
                cor_diag = "#ef4444"
                recomendacao_premium = "Afaste o painel ou diminua a potência (Dimmer) para evitar estresse."

# CENÁRIO 2: ESTUFA COM LUZ EXTRA (Híbrido)
elif "Complementar" in ambiente_sel:
    with st.expander("☀️💡 CONFIGURAR ESTUFA (Luz Extra)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: watts_painel = st.number_input("POTÊNCIA DA LUZ EXTRA (W):", 10, 5000, 100)
        with c2: largura = st.number_input("LARGURA ESTUFA (cm):", 100, 5000, 200)
        with c3: profundidade = st.number_input("COMPRIMENTO (cm):", 100, 5000, 200)

        area_m2 = (largura * profundidade) / 10000
        if area_m2 > 0:
            show_diag = True
            ppfd_art = (watts_painel * 2.2) / area_m2
            
            if ppfd_art < 40:
                txt_luz = "ℹ️ <b>CONTROLE DE FLORAÇÃO:</b> Essa luz serve apenas para 'acordar' a planta e impedir que ela floresça antes da hora. Não ajuda a engordar."
                cor_diag = "#38bdf8"
            else:
                txt_luz = "⚡ <b>TURBO LUMINOSO:</b> Sua luz extra está forte o suficiente para ajudar a planta a crescer mais, mesmo em dias nublados."
                cor_diag = "#a855f7"

# CENÁRIO 3: ESTUFA SÓ SOL ou OUTDOOR (Área Física Importa)
elif "Somente Sol" in ambiente_sel:
    with st.expander("☀️ CONFIGURAR ÁREA DA ESTUFA", expanded=True):
        c1, c2 = st.columns(2)
        with c1: largura = st.number_input("LARGURA ESTUFA (cm):", 100, 5000, 200)
        with c2: profundidade = st.number_input("COMPRIMENTO (cm):", 100, 5000, 200)
        area_m2 = (largura * profundidade) / 10000
        show_diag = True
        txt_luz = "☀️ <b>ENERGIA SOLAR:</b> O sol é a melhor luz que existe. Seu desafio aqui será controlar o calor e a umidade."
        cor_diag = "#facc15"

else: # Outdoor Céu Aberto
    area_m2 = 999 # Infinito
    show_diag = True
    txt_luz = "☀️ <b>SOL PLENO:</b> Cultivo no tempo. Atenção total a chuvas na floração (causa mofo) e ventos fortes."
    cor_diag = "#facc15"

# === ANÁLISE DE ESPAÇO E RAÍZES (VALIDAÇÃO FÍSICA) ===
if show_diag and area_m2 != 999:
    # 1. CABE TUDO ISSO?
    if tipo_plantio == "Vasos":
        area_uni = mapa_ocupacao.get(vol_vaso, 0.15)
        area_total_plantas = n_plantas * area_uni
        lotacao = (area_total_plantas / area_m2) * 100
        
        if lotacao > 100:
            txt_espaco = f"🚫 <b>NÃO VAI CABER:</b> Fisicamente impossível colocar {n_plantas} vasos desse tamanho no seu espaço."
            recomendacao_premium = "Diminua a quantidade de plantas pela metade ou use vasos menores."
            cor_diag = "#ef4444"
        elif lotacao > 80:
            txt_espaco = f"⚠️ <b>MUITA PLANTA JUNTO:</b> Elas vão ficar 'coladas'. O ar não circula e o risco de mofo é altíssimo."
            if not recomendacao_premium: recomendacao_premium = "Faça podas constantes nas partes baixas para o ar circular."
            if cor_diag != "#ef4444": cor_diag = "#eab308"
        else:
            txt_espaco = f"✅ <b>ESPAÇO CONFORTÁVEL:</b> As plantas têm espaço para crescer sem sufocar umas às outras."

# 2. O VASO TÁ CERTO PRA PLANTA?
info_gen = db["GENETICAS_PARAMETROS"][genetica_sel]
if tipo_plantio == "Vasos":
    # Automáticas
    if info_gen['tipo'] == "Auto":
        if vol_vaso > 25:
            txt_raiz = "ℹ️ <b>DESPERDÍCIO DE TERRA:</b> Plantas automáticas não dão conta de encher vasos tão grandes. 20 Litros é o teto."
        elif vol_vaso < 7:
            txt_raiz = "⚠️ <b>VASO MUITO PEQUENO:</b> Automáticas precisam de espaço logo no começo. Nesse vaso ela vai ficar anã."
        else:
            txt_raiz = "✅ <b>TAMANHO IDEAL:</b> Vaso perfeito para o ciclo de vida dessa genética."
    # Fotoperíodo
    else:
        if vol_vaso < 7:
            txt_raiz = "⚠️ <b>RAIZ SUFOCADA:</b> Para plantas fotoperíodo, esse vaso é minúsculo. Ela vai travar se você demorar para florir."
            if not recomendacao_premium: recomendacao_premium = "Não deixe ela crescer muito tempo (Vega curta) ou mude para um vaso maior antes de florir."
        else:
            txt_raiz = "✅ <b>VOLUME BOM:</b> Tem terra suficiente para desenvolver uma planta saudável."
else:
    txt_raiz = "🌿 <b>RAÍZES LIVRES:</b> No chão, a planta cresce o quanto quiser. Cuidado com a altura final!"

# === CÁLCULOS FINAIS PARA O RESTO DO APP ===
# (Isso garante que os cards lá embaixo funcionem)
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# Ajuste de Yield baseado na luz (Simulação de realidade)
fator_luz = 1.0
if "Indoor" in ambiente_sel and 'dli' in locals():
    if dli < 20: fator_luz = 0.6 # Luz fraca = menos colheita
    elif dli > 40: fator_luz = 1.1

yield_total = info_metodo['rendimento_base'] * info_gen['fator_yield'] * n_plantas * fator_luz
yield_kg = yield_total / 1000 

# Identificação da Fase
fase_nome = "Indefinida"; fase_dados = {}
range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
fator_ciclo = 0.75 if info_gen.get("tipo") == "Auto" else 1.0

for k, v in db.get("FASES_DINAMICAS", {}).items():
    chave_limpa = k.split(' ')[0]
    limite = int(range_map.get(chave_limpa, 200) * fator_ciclo)
    if dias_vida <= limite: 
        fase_nome = k; fase_dados = v; break

# === EXIBIÇÃO DA CONSULTORIA (CARD ÚNICO E INTELIGENTE) ===
if show_diag:
    # Título dinâmico dependendo do ambiente
    titulo_consultoria = f"CONSULTORIA: {ambiente_sel.split('(')[0].upper()}"
    
    st.markdown(f"""
    <div class="diag-card" style="border-left: 4px solid {cor_diag}; margin-top:15px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #333; padding-bottom:10px;">
            <div style="font-weight:900; color:{cor_diag}; letter-spacing:1px; font-size:1.1rem;">{titulo_consultoria}</div>
            <div style="background:{cor_diag}20; color:{cor_diag}; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:bold;">ANÁLISE PREMIUM</div>
        </div>
        
        <div style="font-family:sans-serif; color:#e4e4e7;">
            <div style="margin-bottom:12px;">
                <strong style="color:#aaa; font-size:0.8rem;">SOBRE A LUZ:</strong><br>
                {txt_luz}
            </div>
            
            <div style="margin-bottom:12px;">
                 <strong style="color:#aaa; font-size:0.8rem;">SOBRE O ESPAÇO:</strong><br>
                {txt_espaco if txt_espaco else "Sem restrições físicas detectadas."}
            </div>

            <div style="margin-bottom:12px;">
                 <strong style="color:#aaa; font-size:0.8rem;">SOBRE AS RAÍZES:</strong><br>
                {txt_raiz}
            </div>
            
            <div style="margin-top:15px; padding:15px; background:rgba(255,255,255,0.05); border-radius:8px; border-left:3px solid {cor_diag};">
                <span style="color:{cor_diag}; font-weight:bold; font-size:0.9rem;">SUGESTÃO DO ESPECIALISTA:</span><br>
                <span style="color:#fff; font-size:0.95rem; line-height:1.5;">
                {recomendacao_premium if recomendacao_premium else "Seu setup está muito bem equilibrado! O segredo agora é manter a temperatura e o pH estáveis."}
                </span>
            </div>
        </div>
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

# --- ABA 1: NUTRIÇÃO & MARCHA DE ABSORÇÃO (SDI MASTER V12.0) ---
with tab_nutri:
    # 1. GRÁFICO DE BARRAS AGRUPADAS (AMPLIADO E EM PRIMEIRO PLANO)
    st.markdown(f"#### 📊 Marcha de Absorção - Ciclo Fenológico (Semana {semanas} em Destaque)")
    
    nutri = db["NUTRI_MARCHA_ABSORCAO"]
    s_idx = min(semanas - 1, 11) if semanas > 0 else 0
    
    # Configuração Técnica dos Nutrientes
    macros_config = {
        "N":  {"nome": "Nitrogênio", "cor": "#22c55e", "val": nutri['N'][s_idx]},
        "P":  {"nome": "Fósforo",    "cor": "#3b82f6", "val": nutri['P'][s_idx]},
        "K":  {"nome": "Potássio",   "cor": "#a855f7", "val": nutri['K'][s_idx]},
        "Ca": {"nome": "Cálcio",     "cor": "#f97316", "val": nutri['Ca'][s_idx]},
        "Mg": {"nome": "Magnésio",   "cor": "#eab308", "val": nutri['Mg'][s_idx]},
        "S":  {"nome": "Enxofre",    "cor": "#facc15", "val": nutri['S'][s_idx]}
    }
    
    fig = go.Figure()

    # Adicionando Barras para cada Nutriente
    for simbolo, d in macros_config.items():
        fig.add_trace(go.Bar(
            name=f"{simbolo} - {d['nome']}",
            x=nutri['semanas'],
            y=nutri[simbolo],
            marker_color=d['cor'],
            opacity=0.9,
            hovertemplate=f"Semana %{{x}}<br>{d['nome']}: %{{y}}%<extra></extra>"
        ))

    # Linha de Referência da Semana Atual (Indicador Vertical)
    fig.add_vline(x=semanas, line_width=4, line_dash="solid", line_color="#ffffff", opacity=0.7)

    fig.update_layout(
        barmode='group', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#ccc"),
        height=550, # Tamanho ampliado conforme solicitado
        margin=dict(l=10, r=10, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=11)),
        xaxis=dict(
            title="SEMANAS DO CICLO",
            tickmode='linear',
            showgrid=False,
            fixedrange=True
        ),
        yaxis=dict(
            title="DEMANDA DE ABSORÇÃO (%)",
            gridcolor='#222',
            range=[0, 105],
            fixedrange=True
        ),
        bargap=0.18,
        bargroupgap=0.04
    )
    
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. CARDS HORIZONTAIS DE LEITURA RÁPIDA (DEPOIS DO GRÁFICO)
    st.markdown("#### 🧪 Demanda Bioquímica da Semana Atual")
    
    c_met = st.columns(6)
    for i, (simbolo, d) in enumerate(macros_config.items()):
        with c_met[i]:
            st.markdown(f"""
            <div style="background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0) 100%); 
                        border: 1px solid {d['cor']}44; border-top: 4px solid {d['cor']}; 
                        border-radius: 8px; padding: 15px 5px; text-align: center;">
                <div style="font-size: 0.75rem; color: #999; font-weight: 800; margin-bottom: 5px; letter-spacing: 1px;">{simbolo}</div>
                <div style="font-size: 1.5rem; font-weight: 900; color: #fff; line-height: 1;">{d['val']}%</div>
                <div style="font-size: 0.6rem; color: {d['cor']}; text-transform: uppercase; font-weight:bold; margin-top: 5px;">{d['nome']}</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. ENCICLOPÉDIA DE DEFICIÊNCIAS (EXPANDÍVEL)
    st.markdown("---")
    st.markdown("#### 🔍 Diagnóstico Visual de Deficiências")
    st.caption("Clique no elemento para abrir o guia de identificação por foto e o protocolo de correção.")

    cols_def = st.columns(4)
    defs_items = list(db["DEFICIENCIAS_VISUAIS"].items())
    
    for i, (k, v) in enumerate(defs_items):
        with cols_def[i % 4]:
            cor_card = v.get('cor_card', '#333')
            nome_limpo = k.split('(')[0].strip()

            with st.expander(f"👁️ {k}"):
                st.markdown(f"**Referência Fotográfica:**")
                
                
                st.markdown(f"""
                <div style="border-left: 3px solid {cor_card}; padding-left: 12px; margin-top: 10px;">
                    <div style="font-size: 0.85rem; color: #eee; margin-bottom: 12px; line-height: 1.4;">
                        <b>Sintoma Clínico:</b> {v['sintoma']}
                    </div>
                    
                    <div style="background: rgba(34, 197, 94, 0.08); border: 1px solid #15803d; padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                        <div style="font-size: 0.7rem; color: #4ade80; font-weight: 900; letter-spacing: 1px;">PROTOCOLO BIO</div>
                        <div style="font-size: 0.8rem; color: #ccc; margin-top: 4px;">{v.get('correcao_bio', '-')}</div>
                    </div>
                    
                    <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid #991b1b; padding: 10px; border-radius: 8px;">
                        <div style="font-size: 0.7rem; color: #f87171; font-weight: 900; letter-spacing: 1px;">PROTOCOLO MINERAL</div>
                        <div style="font-size: 0.8rem; color: #ccc; margin-top: 4px;">{v.get('correcao_quim', '-')}</div>
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
