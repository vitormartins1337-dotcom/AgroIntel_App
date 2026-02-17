# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | PLATINUM EDITION V15.0
# DESCRIÇÃO: Interface Limpa (Sidebar), Lógica Robusta e Consultoria Integrada.

import streamlit as st
import datetime
import plotly.graph_objects as go
from core_logic import AgroEngine 

# --- 1. SETUP INICIAL ---
st.set_page_config(
    page_title="Agrower SDI Pro", 
    page_icon="🍁", 
    layout="wide",
    initial_sidebar_state="expanded" # Sidebar aberta por padrão
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
        
        /* SIDEBAR PERSONALIZADA */
        [data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 1px solid #333;
        }
        
        /* HEADER HERO */
        .hero-card {
            position: relative;
            background: linear-gradient(135deg, #1a0b2e 0%, #000000 100%);
            border: 1px solid #a855f7;
            box-shadow: 0 0 60px rgba(168, 85, 247, 0.25);
            border-radius: 20px;
            padding: 40px 20px;
            margin-bottom: 20px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .main-title {
            font-size: clamp(2rem, 5vw, 4rem); font-weight: 900; color: #fff;
            line-height: 1; letter-spacing: -2px; text-align: center;
            text-shadow: 0 0 30px rgba(168, 85, 247, 0.6);
        }
        .sub-title {
            font-family: 'Courier New', monospace; font-size: clamp(0.7rem, 1.5vw, 0.9rem);
            color: #d8b4fe; letter-spacing: 4px; text-transform: uppercase;
            margin-top: 10px; font-weight: 600; text-align: center; opacity: 0.9;
        }
        
        /* STATUS PILL (ONLINE) - RODAPÉ DIREITO DO HERO */
        .status-pill {
            position: absolute; bottom: 15px; right: 20px;
            background: rgba(16, 185, 129, 0.1); border: 1px solid #059669;
            color: #4ade80; padding: 4px 12px; border-radius: 99px;
            font-size: 0.7rem; font-weight: 700; display: flex; align-items: center; gap: 6px;
        }

        /* TICKER */
        .ticker-wrap {
            width: 100%; overflow: hidden; background: #000; 
            border-top: 1px solid #333; border-bottom: 1px solid #333; 
            height: 30px; display: flex; align-items: center; margin-bottom: 20px;
        }
        .tick-item { margin-right: 40px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #a855f7; }
        .tick-val { color: #fff; margin-left: 5px; font-weight: bold; }

        /* CARDS DASHBOARD */
        .status-card {
            background: linear-gradient(145deg, #120520 0%, #050505 100%);
            border: 1px solid #3b0764; border-left: 5px solid #a855f7;
            border-radius: 12px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); height: 100%;
        }
        .yield-card {
            background: linear-gradient(135deg, #1e1b10 0%, #000000 100%);
            border: 1px solid #854d0e; border-right: 5px solid #eab308;
            border-radius: 12px; padding: 20px; text-align: center; height: 100%;
            display: flex; flex-direction: column; justify-content: center;
        }
        
        /* CONSULTORIA CARD (ESTILO PREMIUM) */
        .diag-card {
            background: #0f0f0f; border: 1px solid #333; border-radius: 12px; padding: 25px;
            margin-top: 25px; margin-bottom: 25px; position: relative;
        }

        /* TIPOGRAFIA */
        .card-label { font-size: 0.7rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; margin-bottom: 5px; }
        .big-val { font-size: 2.2rem; font-weight: 900; color: #fff; line-height: 1; margin-bottom: 5px; }
        .sub-info { font-size: 0.85rem; color: #d1d5db; margin-top: 5px; }
        .meta-badge { display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; margin-right: 5px; margin-top: 5px; }
        .bg-ph { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid #1e3a8a; }
        .bg-ec { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid #064e3b; }
        
        /* BALLOONS & GRAPHS */
        .nutri-ball {
            display: inline-flex; flex-direction: column; align-items: center; justify-content: center;
            width: 70px; height: 70px; border-radius: 50%; margin: 5px;
            border: 2px solid; background: rgba(0,0,0,0.5); font-weight: 900; font-size: 1.1rem;
        }
        .doc-card { background: #0f0f0f; border-radius: 10px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #333; }
        </style>
    """, unsafe_allow_html=True)
load_master_css()

# ==============================================================================
# 3. SIDEBAR (PAINEL DE CONTROLE OCULTO) - AQUI COMEÇA A LÓGICA
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎛️ PAINEL DE COMANDO")
    st.caption("Configure os parâmetros do cultivo.")
    st.markdown("---")

    # A. BIOLOGIA
    st.markdown("#### 🧬 Genética & Ambiente")
    genetica_sel = st.selectbox("Genética Predominante", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
    ambiente_sel = st.selectbox("Ambiente de Cultivo", [
        "Indoor (Luz Artificial)", 
        "Estufa (Luz Híbrida)", 
        "Estufa (Somente Sol)", 
        "Outdoor (Sol Pleno)"
    ])
    
    # B. CRONOGRAMA
    st.markdown("#### 📅 Cronograma")
    data_inicio = st.date_input("Início do Ciclo", datetime.date.today() - datetime.timedelta(days=45))
    n_plantas = st.number_input("Quantidade de Plantas", 1, 500, 4)

    # C. SISTEMA RADICULAR
    st.markdown("#### 🌱 Raízes & Método")
    metodo_sel = st.selectbox("Substrato/Método", list(db.get("METODOS_CULTIVO", {}).keys()))
    tipo_plantio = st.radio("Sistema de Plantio", ["Vasos", "Canteiro/Chão"], horizontal=True)
    
    vol_vaso = 999
    if tipo_plantio == "Vasos":
        vol_vaso = st.select_slider("Tamanho do Vaso (Litros)", options=[4, 7, 11, 15, 20, 25, 30, 40, 50, 100], value=11)
        horas_luz = st.slider("Fotoperíodo (Horas Luz)", 10, 24, 18)
    else:
        st.info("Raízes livres no solo.")
        horas_luz = st.slider("Fotoperíodo (Horas Luz)", 10, 24, 18)

    st.markdown("---")
    
    # D. ENGENHARIA DO AMBIENTE (Inputs Dinâmicos na Sidebar)
    st.markdown("#### 💡 Engenharia")
    
    watts_painel = 0; area_m2 = 0
    largura = 0; profundidade = 0

    if "Indoor" in ambiente_sel:
        watts_painel = st.number_input("Potência LED (Watts Reais)", 50, 5000, 240)
        largura = st.number_input("Largura Grow (cm)", 40, 1000, 80)
        profundidade = st.number_input("Profundidade (cm)", 40, 1000, 80)
        area_m2 = (largura * profundidade) / 10000
        
    elif "Híbrida" in ambiente_sel: # Estufa com Luz
        watts_painel = st.number_input("Luz Complementar (Watts)", 10, 5000, 100)
        largura = st.number_input("Largura Estufa (cm)", 100, 5000, 200)
        profundidade = st.number_input("Comprimento (cm)", 100, 5000, 200)
        area_m2 = (largura * profundidade) / 10000

    elif "Somente Sol" in ambiente_sel:
        largura = st.number_input("Largura Estufa (cm)", 100, 5000, 200)
        profundidade = st.number_input("Comprimento (cm)", 100, 5000, 200)
        area_m2 = (largura * profundidade) / 10000
    
    else: # Outdoor
        area_m2 = 999
        st.info("Cultivo em área aberta.")

    st.caption(f"Área Calculada: {area_m2:.2f} m²")


# ==============================================================================
# 4. SDI ENGINE (CÉREBRO LÓGICO) - CÁLCULOS ANTES DA EXIBIÇÃO
# ==============================================================================

# --- Inicialização Segura de Variáveis (Evita NameError) ---
show_consultoria = False
titulo_consultoria = "ANÁLISE SDI"
txt_luz = ""; txt_espaco = ""; txt_raiz = ""; recomendacao_premium = ""
cor_diag = "#333" # Cor padrão Dark
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]
info_metodo = db["METODOS_CULTIVO"][metodo_sel]

# Mapa de Ocupação Física (m²)
mapa_ocupacao = {4: 0.04, 7: 0.06, 11: 0.09, 15: 0.11, 20: 0.14, 25: 0.16, 30: 0.20, 40: 0.25, 50: 0.30, 100: 0.50}

# --- A. LÓGICA DE ILUMINAÇÃO (PPFD & DLI) ---
dli = 0
if area_m2 > 0 and area_m2 != 999:
    show_consultoria = True
    
    if "Indoor" in ambiente_sel:
        ppfd = (watts_painel * 2.2) / area_m2
        dli = ppfd * horas_luz * 0.0036
        
        if dli < 15:
            txt_luz = "⚠️ <b>BAIXA ENERGIA:</b> Luz fraca para floração densa. Buds ficarão 'aerados'."
            cor_diag = "#eab308"
            recomendacao_premium = "Aumente a potência do painel ou reduza a área de cultivo aproximando as paredes reflexivas."
        elif 15 <= dli < 45:
            txt_luz = "✅ <b>LUZ OTIMIZADA:</b> Quantidade perfeita de fótons para fotossíntese."
            cor_diag = "#22c55e"
        else:
            txt_luz = "🔥 <b>LUZ EXTREMA:</b> Risco de queima. Obrigatório uso de CO2 (1200ppm)."
            cor_diag = "#ef4444"
            recomendacao_premium = "Afaste o painel ou use Dimmer para 80%."

    elif "Híbrida" in ambiente_sel:
        ppfd_art = (watts_painel * 2.2) / area_m2
        if ppfd_art < 40:
            txt_luz = "ℹ️ <b>SUPORTE FOTOPERÍODO:</b> Luz apenas para impedir floração precoce."
            cor_diag = "#38bdf8"
        else:
            txt_luz = "⚡ <b>SUPLEMENTAÇÃO ATIVA:</b> Luz forte o suficiente para engorda."
            cor_diag = "#a855f7"

    elif "Somente Sol" in ambiente_sel:
        txt_luz = "☀️ <b>ENERGIA SOLAR:</b> Dependência total do clima. Monitore dias nublados."
        cor_diag = "#facc15"
    
    else:
        txt_luz = "☀️ <b>SOL PLENO:</b> Intensidade máxima. O limite é a água."

# --- B. LÓGICA DE ESPAÇO (FÍSICA) ---
if area_m2 != 999 and show_consultoria:
    if tipo_plantio == "Vasos":
        area_uni = mapa_ocupacao.get(vol_vaso, 0.15)
        area_total = n_plantas * area_uni
        ocupacao = (area_total / area_m2) * 100
        
        if ocupacao > 100:
            txt_espaco = f"🚫 <b>SEM ESPAÇO:</b> Impossível colocar {n_plantas} vasos nesse local."
            cor_diag = "#ef4444"
            recomendacao_premium = "Reduza a quantidade de plantas pela metade urgentemente."
        elif ocupacao > 85:
            txt_espaco = f"⚠️ <b>SUPERLOTAÇÃO:</b> Plantas coladas. Risco crítico de mofo."
            if not recomendacao_premium: recomendacao_premium = "Faça desfolhação pesada na base para circular ar."
            if cor_diag != "#ef4444": cor_diag = "#eab308"
        else:
            txt_espaco = "✅ <b>ESPAÇAMENTO CORRETO:</b> Boa circulação de ar prevista."
    else:
        txt_espaco = "🌿 <b>CANTEIRO:</b> Sem restrição de vasos."

# --- C. LÓGICA DE RAÍZES (GENÉTICA) ---
if tipo_plantio == "Vasos":
    # Automáticas
    if info_genetica['tipo'] == "Auto":
        if vol_vaso > 25: txt_raiz = "ℹ️ <b>DESPERDÍCIO:</b> Autos não usam mais que 25L."
        elif vol_vaso < 7: txt_raiz = "⚠️ <b>VASO PEQUENO:</b> Vai limitar o tamanho da automática."
        else: txt_raiz = "✅ <b>VOLUME IDEAL:</b> Perfeito para ciclo automático."
    # Fotoperíodo
    else:
        if vol_vaso < 7: 
            txt_raiz = "⚠️ <b>RAIZ PRESA:</b> Vaso muito pequeno para fotoperíodo."
            if not recomendacao_premium: recomendacao_premium = "Faça ciclo vegetativo curto (max 2 semanas) ou transplante."
        else: 
            txt_raiz = "✅ <b>VOLUME ADEQUADO:</b> Sustenta bem a planta."
else:
    txt_raiz = "🌿 <b>RAÍZES LIVRES:</b> Atenção à altura incontrolável."

# --- D. CÁLCULOS GERAIS (TEMPO E YIELD) ---
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

fator_luz = 1.0
if "Indoor" in ambiente_sel and dli > 0:
    if dli < 20: fator_luz = 0.6
    elif dli > 40: fator_luz = 1.1

yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas * fator_luz
yield_kg = yield_total / 1000 

fase_nome = "Indefinida"; fase_dados = {}
range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
fator_ciclo = 0.75 if info_genetica.get("tipo") == "Auto" else 1.0

for k, v in db.get("FASES_DINAMICAS", {}).items():
    chave_limpa = k.split(' ')[0]
    limite = int(range_map.get(chave_limpa, 200) * fator_ciclo)
    if dias_vida <= limite: fase_nome = k; fase_dados = v; break

# FIM DA PARTE 1 - COPIE E COLE A PARTE 2 ABAIXO DESTA LINHA

# --- INÍCIO DA PARTE 2 (INTERFACE VISUAL) ---

# ==============================================================================
# 5. DASHBOARD VISUAL (O PALCO)
# ==============================================================================

# A. HERO & TICKER
st.markdown("""
<div class="hero-card">
    <div class="status-pill"><span style="font-size:1rem; line-height:1;">🍁</span> SISTEMA ONLINE</div>
    <div class="main-title">AGROWER <span style="color:#a855f7">SDI</span></div>
    <div class="sub-title">SISTEMA DE DECISÃO INTEGRADA</div>
</div>
""", unsafe_allow_html=True)

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

# B. CARDS DE STATUS (LINHA SUPERIOR)
col_a, col_b = st.columns([1.8, 1.2])

with col_a:
    st.markdown(f"""
    <div class="status-card">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div><div class="card-label" style="color:#d8b4fe;">FASE ATUAL ({info_genetica.get('tipo', 'Foto').upper()})</div><div class="big-val">{fase_nome.upper()}</div></div>
            <div style="text-align:right;"><div class="card-label">TEMPO</div><div style="font-size:1.5rem; font-weight:bold; color:#fff;">{dias_vida} <span style="font-size:0.9rem; color:#888;">DIAS</span></div><div style="font-size:0.85rem; color:#a855f7;">SEMANA {semanas}</div></div>
        </div>
        <div style="height:1px; background:#333; margin:15px 0;"></div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div><div class="card-label">OBJETIVO TÁTICO</div><div style="color:#fff; font-weight:600;">🎯 {fase_dados.get('foco', '-')}</div></div>
            <div style="text-align:right;"><div class="card-label">METAS DO AMBIENTE</div><div><span class="meta-badge bg-ph">💧 PH {info_metodo['ph_ideal']}</span><span class="meta-badge bg-ec">⚡ EC {info_metodo['ec_ideal']}</span></div></div>
        </div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="yield-card">
        <div class="card-label" style="color:#fcd34d;">ESTIMATIVA DE COLHEITA</div><div class="big-val" style="color:#fef08a;">{yield_total:.0f}g</div><div class="sub-info" style="color:#fde047;">~ {yield_kg:.2f} kg (Seco)</div>
        <div style="height:1px; background:#422006; margin:15px 0;"></div>
        <div style="font-size:0.75rem; color:#ca8a04;">BASE: <b>{n_plantas} plantas</b> ({info_genetica['tipo']})</div>
        <div style="font-size:0.7rem; color:#888; margin-top:5px;">Considerando método {metodo_sel.split(' ')[0]}</div>
    </div>""", unsafe_allow_html=True)

# C. CARD DE CONSULTORIA SDI (CORRIGIDO: VISUAL ROXO & RENDERIZAÇÃO HTML)
if show_consultoria:
    titulo_card = f"CONSULTORIA: {ambiente_sel.split('(')[0].upper()}"
    
    # Define a cor ROXA PROFISSIONAL fixa para o layout do card
    cor_layout = "#a855f7"
    
    # ATENÇÃO: Copie exatamente até o final do parênteses do st.markdown
    st.markdown(f"""
    <div class="diag-card" style="border-left: 4px solid {cor_layout};">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #333; padding-bottom:10px;">
            <div style="font-weight:900; color:{cor_layout}; letter-spacing:1px; font-size:1.1rem;">{titulo_card}</div>
            <div style="background:{cor_layout}20; color:{cor_layout}; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:bold;">ANÁLISE PREMIUM</div>
        </div>
        
        <div style="font-family:sans-serif; color:#e4e4e7;">
            <div style="margin-bottom:12px;">
                <strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px;">LUZ & ENERGIA</strong><br>
                <div style="font-size:0.95rem; margin-top:3px;">{txt_luz}</div>
            </div>
            
            <div style="margin-bottom:12px;">
                 <strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px;">FÍSICA & ESPAÇO</strong><br>
                <div style="font-size:0.95rem; margin-top:3px;">{txt_espaco if txt_espaco else "Sem restrições físicas."}</div>
            </div>

            <div style="margin-bottom:12px;">
                 <strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px;">RAÍZES</strong><br>
                <div style="font-size:0.95rem; margin-top:3px;">{txt_raiz}</div>
            </div>
            
            <div style="margin-top:20px; padding:15px; background:rgba(255,255,255,0.05); border-radius:8px; border-left:3px solid {cor_layout};">
                <span style="color:{cor_layout}; font-weight:bold; font-size:0.9rem;">SUGESTÃO DO ESPECIALISTA:</span><br>
                <span style="color:#fff; font-size:1rem; line-height:1.5;">
                {recomendacao_premium if recomendacao_premium else "Seu setup está tecnicamente equilibrado. Mantenha a constância nos parâmetros."}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. ABAS: NUTRIÇÃO & DOCTOR (ESTILO MASTER V13)
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
tab_nutri, tab_doctor = st.tabs(["🧪 NUTRIÇÃO & ABSORÇÃO", "🚑 DOCTOR GROW"])

with tab_nutri:
    # 1. DIAGNÓSTICO VISUAL (PRIORIDADE)
    st.markdown("#### 🔍 Diagnóstico Visual")
    cols_def = st.columns(4)
    defs_items = list(db["DEFICIENCIAS_VISUAIS"].items())
    
    for i, (k, v) in enumerate(defs_items):
        with cols_def[i % 4]:
            cor_card = v.get('cor_card', '#333')
            nome_limpo = k.split('(')[0].strip()
            with st.expander(f"👁️ {k}"):
                st.markdown(f"""
                <div style="border-left: 3px solid {cor_card}; padding-left: 10px;">
                    <div style="font-size: 0.85rem; color: #eee; margin-bottom: 10px;">{v['sintoma']}</div>
                    <div style="background: rgba(34, 197, 94, 0.1); padding: 5px; margin-bottom: 5px; border-radius: 4px;">
                        <span style="color:#4ade80; font-weight:bold; font-size:0.7rem;">BIO:</span> {v.get('correcao_bio', '-')}
                    </div>
                    <div style="background: rgba(239, 68, 68, 0.1); padding: 5px; border-radius: 4px;">
                        <span style="color:#f87171; font-weight:bold; font-size:0.7rem;">MINERAL:</span> {v.get('correcao_quim', '-')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 2. GRÁFICO (BARRAS LARGAS)
    st.markdown(f"#### 📊 Marcha de Absorção (Semana {semanas})")
    nutri = db["NUTRI_MARCHA_ABSORCAO"]
    s_idx = min(semanas - 1, 11) if semanas > 0 else 0
    
    macros_config = {
        "N":  {"nome": "Nitrogênio", "cor": "#22c55e", "val": nutri['N'][s_idx]},
        "P":  {"nome": "Fósforo",    "cor": "#3b82f6", "val": nutri['P'][s_idx]},
        "K":  {"nome": "Potássio",   "cor": "#a855f7", "val": nutri['K'][s_idx]},
        "Ca": {"nome": "Cálcio",     "cor": "#f97316", "val": nutri['Ca'][s_idx]},
        "Mg": {"nome": "Magnésio",   "cor": "#eab308", "val": nutri['Mg'][s_idx]},
        "S":  {"nome": "Enxofre",    "cor": "#facc15", "val": nutri['S'][s_idx]}
    }
    
    fig = go.Figure()
    for symbol, d in macros_config.items():
        fig.add_trace(go.Bar(
            name=symbol, x=nutri['semanas'], y=nutri[symbol],
            marker_color=d['cor'], opacity=0.9, text=symbol, textposition='inside',
            hovertemplate=f"Semana %{{x}}<br>{d['nome']}: %{{y}}%<extra></extra>"
        ))
    fig.add_vline(x=semanas, line_width=4, line_color="rgba(255,255,255,0.5)")
    fig.update_layout(
        barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#ccc"), height=500, margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#222'),
        bargap=0.05, bargroupgap=0.02, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. CARDS DE LEITURA
    st.markdown("<br>", unsafe_allow_html=True)
    c_m = st.columns(6)
    for i, (symbol, d) in enumerate(macros_config.items()):
        with c_m[i]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border-top:3px solid {d['cor']}; border-radius:6px; padding:10px; text-align:center;">
                <div style="font-size:1.2rem; font-weight:900; color:#fff;">{d['val']}%</div>
                <div style="font-size:0.6rem; color:{d['cor']}; font-weight:bold;">{d['nome'].upper()}</div>
            </div>
            """, unsafe_allow_html=True)

with tab_doctor:
    st.markdown("### 🚑 Doctor Grow")
    busca = st.text_input("🔍 Buscar Sintoma ou Praga:", placeholder="Ex: Manchas brancas, ácaros...")
    
    for nome, info in db["DOCTOR_GROW_FITOSSANIDADE"].items():
        if busca and busca.lower() not in nome.lower() and busca.lower() not in info['sintomas'].lower(): continue
        
        cor_g = "#ef4444" if info['gravidade'] in ["ALTA", "CRÍTICA", "FATAL"] else "#eab308"
        
        st.markdown(f"""
        <div class="doc-card" style="border-left-color: {cor_g};">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <div style="font-weight:bold; font-size:1.1rem; color:#fff;">{nome}</div>
                <div style="background:{cor_g}20; color:{cor_g}; padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:bold;">{info['gravidade']}</div>
            </div>
            <div style="color:#ccc; font-size:0.9rem; margin-bottom:10px;"><i>{info['sintomas']}</i></div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <div>
                    <div style="font-size:0.7rem; color:#4ade80; font-weight:bold;">BIO:</div>
                    <div style="font-size:0.8rem; color:#ccc;">{', '.join(info['bio'])}</div>
                </div>
                <div>
                    <div style="font-size:0.7rem; color:#f87171; font-weight:bold;">SOS:</div>
                    <div style="font-size:0.8rem; color:#ccc;">{', '.join(info['quimico'])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
