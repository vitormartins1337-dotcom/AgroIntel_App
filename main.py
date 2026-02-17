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
# 4. PAINEL DE CONTROLE & INTELIGÊNCIA ARTIFICIAL (SDI ENGINE V12.0 - TITANIUM)
# ==============================================================================
# DESCRIÇÃO: Engine física que calcula DLI, PPFD Estimado, Volumetria e Densidade.

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🎛️ Parâmetros de Cultivo & Engenharia")

# --- A. INPUTS BIOLÓGICOS E RADICULARES ---
c_bio1, c_bio2, c_bio3, c_bio4 = st.columns([2, 1.5, 1, 1])

with c_bio1:
    # O sistema puxa as chaves do DB atualizado (THC/CBD/Auto/Foto)
    genetica_sel = st.selectbox("🧬 GENÉTICA & TIPO", list(db.get("GENETICAS_PARAMETROS", {}).keys()), help="Selecione a variante exata para ajuste de DLI e Nutrição.")
with c_bio2:
    ambiente_sel = st.selectbox("🏠 AMBIENTE", ["Indoor (Clima Controlado)", "Estufa (Greenhouse/Misto)", "Outdoor (Sol Pleno)"])
with c_bio3:
    n_plantas = st.number_input("Nº PLANTAS", 1, 1000, 4)
with c_bio4:
    data_inicio = st.date_input("📅 INÍCIO", datetime.date.today() - datetime.timedelta(days=45))

# --- INPUTS DE SUBSTRATO (REFINADO) ---
c_sub1, c_sub2, c_sub3, c_sub4 = st.columns([1.5, 1.2, 1.2, 1.5])
with c_sub1:
     metodo_sel = st.selectbox("🥣 SUBSTRATO / MÉTODO", list(db.get("METODOS_CULTIVO", {}).keys()))
with c_sub2:
    tipo_plantio = st.selectbox("🌱 SISTEMA", ["Vasos", "Canteiro/Solo"])
with c_sub3:
    vol_vaso = 0
    if tipo_plantio == "Vasos":
        vol_vaso = st.selectbox("VOLUME (L)", [4, 7, 11, 15, 20, 25, 30, 40, 50, 100], index=2)
    else:
        vol_vaso = 999 # Solo infinito
with c_sub4:
    # NOVO: Input de Fotoperíodo para cálculo de DLI
    horas_luz = st.number_input("⏰ FOTOPERÍODO (HORAS LUZ)", 10, 24, 18, help="Quantas horas de luz a planta recebe por dia? (Ex: 18h Vega, 12h Flora)")

# --- B. ENGINE SDI (CÁLCULO DE ENGENHARIA AGRONÔMICA) ---
# Inicialização de variáveis de controle
watts_painel = 0; area_cultivo = 0; volume_cultivo = 0
diagnostico_titulo = "AGUARDANDO DADOS..."; diagnostico_texto = ""; sugestao_premium = ""
cor_diag = "#333"; show_diag = False
txt_luz = ""; txt_fisica = ""; txt_raiz = ""; txt_clima = ""
ppfd_estimado = 0; dli_estimado = 0

# Mapa de área física por vaso (Diâmetro médio + folga)
mapa_area_vaso = {4: 0.03, 7: 0.05, 11: 0.07, 15: 0.09, 20: 0.11, 25: 0.13, 30: 0.16, 40: 0.20, 50: 0.25, 100: 0.45}

# === CENÁRIO 1: INDOOR (CÁLCULO COMPLETO PPFD/DLI/VPD) ===
if "Indoor" in ambiente_sel:
    with st.expander("💡 ENGENHARIA INDOOR (DIMENSIONAMENTO & DLI)", expanded=True):
        st.caption("O sistema calculará o PPFD (Densidade de Fluxo de Fótons) e o DLI (Luz Total Diária) baseados na física do seu espaço.")
        col1, col2, col3, col4 = st.columns(4)
        with col1: watts_painel = st.number_input("POTÊNCIA LED (W REAIS):", 50, 5000, 240, help="Soma da potência real extraída da tomada.")
        with col2: largura = st.number_input("LARGURA (cm):", 40, 1000, 80)
        with col3: profundidade = st.number_input("PROFUNDIDADE (cm):", 40, 1000, 80)
        with col4: altura = st.number_input("ALTURA ÚTIL (cm):", 100, 500, 160, help="Usado para cálculo de exaustão/volume.")

        area_m2 = (largura * profundidade) / 10000 
        volume_m3 = area_m2 * (altura / 100)

        if area_m2 > 0:
            show_diag = True
            
            # --- FÍSICA DA LUZ (ALGORITMO SDI) ---
            # Eficiência estimada de LED moderno: 2.2 umol/J (com perdas de reflexão)
            # PPFD = (Watts * Eficiência) / m²
            ppfd_estimado = (watts_painel * 2.2) / area_m2
            
            # DLI = PPFD * Horas * 3600 / 1,000,000 (ou * 0.0036)
            dli_estimado = ppfd_estimado * horas_luz * 0.0036

            # DIAGNÓSTICO DE LUZ (BASEADO EM PPFD e DLI)
            if dli_estimado < 15:
                txt_luz = f"⚠️ <b>BAIXA ENERGIA (DLI {dli_estimado:.1f} mol/dia)</b>: Ritmo lento. Aceitável para clones/seedlings, mas insuficiente para vega robusta."
                cor_diag = "#eab308"
            elif 15 <= dli_estimado < 30:
                txt_luz = f"✅ <b>VEGETATIVO OTIMIZADO (DLI {dli_estimado:.1f} mol/dia)</b>: PPFD de ~{ppfd_estimado:.0f} µmol. Excelente para crescimento estrutural."
                cor_diag = "#38bdf8"
            elif 30 <= dli_estimado < 45:
                txt_luz = f"🚀 <b>FLORAÇÃO INTENSA (DLI {dli_estimado:.1f} mol/dia)</b>: Sweet Spot para produção de flores densas. PPFD ~{ppfd_estimado:.0f} µmol."
                cor_diag = "#22c55e"
            else: # DLI > 45
                txt_luz = f"🔥 <b>SATURAÇÃO LUMINOSA (DLI {dli_estimado:.1f} mol/dia)</b>: Nível extremo. Sem CO2 (1200-1500ppm), a planta vai travar ou queimar."
                cor_diag = "#ef4444"
                sugestao_premium = "OBRIGATÓRIO: Suplementação de CO2 ou reduza a potência/horas de luz."

            # DIAGNÓSTICO DE CLIMA (VOLUMETRIA)
            trocas_ar_min = volume_m3 * 60 # 60 trocas por hora é o ideal
            txt_clima = f"💨 <b>VENTILAÇÃO:</b> Para seu volume de {volume_m3:.2f}m³, seu exaustor precisa de no mínimo <b>{trocas_ar_min:.0f} m³/h</b> reais."

# === CENÁRIO 2: ESTUFA/GREENHOUSE (Luz Mista) ===
elif "Estufa" in ambiente_sel:
    with st.expander("☀️💡 ENGENHARIA DE ESTUFA (DLI Misto)", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1: watts_painel = st.number_input("LUZ COMPLEMENTAR (W):", 0, 5000, 100)
        with col2: largura = st.number_input("LARGURA ESTUFA (cm):", 100, 5000, 200)
        with col3: profundidade = st.number_input("COMPRIMENTO (cm):", 100, 5000, 200)

        area_m2 = (largura * profundidade) / 10000 
        if area_m2 > 0:
            show_diag = True
            ppfd_artificial = (watts_painel * 2.2) / area_m2
            
            # Cálculo Híbrido: Sol (Estimativa média) + LED
            # Sol médio em estufa (filtrado): ~25 DLI em dias bons
            dli_base_sol = 20 
            dli_artificial = ppfd_artificial * horas_luz * 0.0036
            dli_total = dli_base_sol + dli_artificial

            if watts_painel > 0:
                if ppfd_artificial < 50:
                    txt_luz = f"ℹ️ <b>FUNÇÃO: FOTOPERÍODO (Total ~{dli_total:.0f} DLI)</b>: Luz artificial apenas para estender o dia e impedir floração."
                    cor_diag = "#38bdf8"
                else:
                    txt_luz = f"⚡ <b>FUNÇÃO: SUPLEMENTAÇÃO (Total ~{dli_total:.0f} DLI)</b>: Luz artificial adicionando peso real à colheita."
                    cor_diag = "#a855f7"
            else:
                txt_luz = "☀️ <b>100% SOLAR:</b> Dependência total do clima externo."
                cor_diag = "#facc15"

# === CENÁRIO 3: OUTDOOR ===
else:
    area_m2 = 999 
    show_diag = True
    txt_luz = "☀️ <b>SOL PLENO (FULL SPECTRUM):</b> Intensidade máxima (~40-60 DLI). O fator limitante será a capacidade da raiz de buscar água."
    cor_diag = "#facc15"
    txt_clima = "🌧️ <b>PREVENÇÃO:</b> Em outdoor, proteja contra chuvas na floração (Botrytis) e ventos fortes."

# --- CÁLCULO DE FÍSICA DE OCUPAÇÃO & RAÍZES (UNIVERSAL) ---
if show_diag and area_m2 != 999:
    # 1. TAXA DE OCUPAÇÃO DO PISO (Crowding)
    if tipo_plantio == "Vasos":
        area_unitaria = mapa_area_vaso.get(vol_vaso, 0.1)
        area_ocupada_total = n_plantas * area_unitaria
        taxa_ocupacao = (area_ocupada_total / area_m2) * 100
        
        if taxa_ocupacao > 100:
            txt_fisica = f"🚫 <b>ERRO FÍSICO (Ocupação {taxa_ocupacao:.0f}%)</b>: {n_plantas} vasos de {vol_vaso}L ocupam {area_ocupada_total:.2f}m². Você só tem {area_m2:.2f}m². Impossível caber."
            sugestao_premium = "REDUÇÃO CRÍTICA: Diminua o número de plantas em 50% ou use vasos menores."
            cor_diag = "#ef4444"
        elif taxa_ocupacao > 75:
            txt_fisica = f"⚠️ <b>SUPERPOPULAÇÃO ({taxa_ocupacao:.0f}%)</b>: Dossel fechado (SOG). Risco de microclima úmido e mofo. Podas baixas são obrigatórias."
            if cor_diag != "#ef4444": cor_diag = "#eab308"
        elif taxa_ocupacao < 40:
            txt_fisica = f"ℹ️ <b>BAIXA DENSIDADE ({taxa_ocupacao:.0f}%)</b>: Espaço livre. Recomendado treino SCROG (Rede) para preencher os vãos de luz."
        else:
            txt_fisica = f"✅ <b>DENSIDADE OTIMIZADA ({taxa_ocupacao:.0f}%)</b>: Equilíbrio ideal entre aeração e aproveitamento de luz."

    # 2. COMPATIBILIDADE GENÉTICA x VASO x SUBSTRATO
    info_gen = db["GENETICAS_PARAMETROS"][genetica_sel]
    is_coco = "Inerte" in metodo_sel or "Hidro" in metodo_sel
    
    if tipo_plantio == "Vasos":
        # Lógica para Automáticas
        if info_gen['tipo'] == "Auto":
            if vol_vaso > 25:
                txt_raiz = f"ℹ️ <b>DESPERDÍCIO DE SUBSTRATO:</b> Automáticas raramente colonizam vasos acima de 20-25L."
            elif vol_vaso < 7:
                txt_raiz = f"⚠️ <b>RAIZ LIMITADA:</b> 7L é o mínimo recomendado para autos expressarem rendimento."
            else:
                txt_raiz = "✅ <b>VOLUME IDEAL PARA AUTO.</b>"
        
        # Lógica para Fotoperíodo
        else:
            if vol_vaso < 7 and not is_coco:
                txt_raiz = f"⚠️ <b>ROOT BOUND (Raiz Presa):</b> Fotoperíodo em solo orgânico pede min. 11-15L. Em {vol_vaso}L vai travar cedo."
                sugestao_premium = "Faça transplantes progressivos ou mantenha o vegetativo muito curto (1-2 semanas)."
            elif is_coco and vol_vaso >= 15:
                 txt_raiz = f"ℹ️ <b>VOLUME ALTO PARA COCO:</b> Em inerte/coco, a planta cresce muito em vasos pequenos. {vol_vaso}L equivale a 30L+ de solo."

# --- MONTAGEM DO DIAGNÓSTICO FINAL (HTML RICO) ---
if show_diag:
    diagnostico_titulo = f"CONSULTORIA TÉCNICA SDI (ANÁLISE V12.0)"
    
    diagnostico_texto = f"""
    <div style="font-family:sans-serif;">
        <div style="margin-bottom:8px; border-bottom:1px solid #333; padding-bottom:5px;">
            <span style="color:#aaa; font-size:0.75rem; font-weight:bold; letter-spacing:1px;">CLIMA & ILUMINAÇÃO</span><br>
            {txt_luz}
            <div style="font-size:0.8rem; color:#888; margin-top:2px;">{txt_clima}</div>
        </div>
        
        <div style="margin-bottom:8px; border-bottom:1px solid #333; padding-bottom:5px;">
            <span style="color:#aaa; font-size:0.75rem; font-weight:bold; letter-spacing:1px;">ESPAÇO & FÍSICA</span><br>
            {txt_fisica}
        </div>

        <div style="margin-bottom:8px;">
             <span style="color:#aaa; font-size:0.75rem; font-weight:bold; letter-spacing:1px;">SISTEMA RADICULAR</span><br>
            {txt_raiz if txt_raiz else "✅ Compatibilidade Raiz/Genética confirmada."}
        </div>
        
        <div style="margin-top:15px; padding:12px; background:rgba(255,255,255,0.05); border-radius:8px; border-left:3px solid {cor_diag};">
            <span style="color:{cor_diag}; font-weight:bold; font-size:0.85rem;">RECOMENDAÇÃO MASTER:</span><br>
            <span style="color:#ddd; font-size:0.9rem;">
            {sugestao_premium if sugestao_premium else "Configuração agronômica sólida. Mantenha o VPD ajustado e nutrição conforme a marcha de absorção."}
            </span>
        </div>
    </div>
    """

# --- C. MOTOR DE CÁLCULO GERAL (ALIMENTA AS PRÓXIMAS SEÇÕES) ---
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]

# Cálculo de Idade
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# Cálculo de Yield Estimado (Considerando DLI se disponível)
fator_luz = 1.0
if "Indoor" in ambiente_sel and dli_estimado > 0:
    # Se DLI for baixo, reduz estimativa de colheita
    if dli_estimado < 20: fator_luz = 0.6
    elif dli_estimado < 30: fator_luz = 0.85
    elif dli_estimado >= 30: fator_luz = 1.1

yield_total = info_metodo['rendimento_base'] * info_genetica['fator_yield'] * n_plantas * fator_luz
yield_kg = yield_total / 1000 

# Cálculo de Fase
fase_nome = "Indefinida"; fase_dados = {}
range_map = {"Plântula": 14, "Vegetativo": 42, "Pré-Flora": 56, "Flora Inicial": 77, "Flora Final": 200}
fator_ciclo = 0.75 if info_genetica.get("tipo") == "Auto" else 1.0

for k, v in db.get("FASES_DINAMICAS", {}).items():
    chave_limpa = k.split(' ')[0]
    limite = int(range_map.get(chave_limpa, 200) * fator_ciclo)
    if dias_vida <= limite: 
        fase_nome = k
        fase_dados = v
        break

# --- EXIBIÇÃO ÚNICA DO CARD DE DIAGNÓSTICO ---
if show_diag:
    st.markdown(f"""
    <div class="diag-card" style="border-left: 4px solid {cor_diag}; margin-top:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; border-bottom:1px solid #333; padding-bottom:10px;">
            <div style="font-weight:900; color:{cor_diag}; letter-spacing:1px; font-size:1.1rem;">{diagnostico_titulo}</div>
            <div style="background:{cor_diag}20; color:{cor_diag}; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:bold;">IA ENGINE V12</div>
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
