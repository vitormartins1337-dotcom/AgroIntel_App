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
# 4. PAINEL DE CONTROLE & INTELIGÊNCIA ARTIFICIAL (SDI ENGINE V17.0 - TITANIUM)
# ==============================================================================

# --- A. CÁLCULO CRONOLÓGICO PRELIMINAR (Para Contexto da IA) ---
st.markdown("<br>", unsafe_allow_html=True)
c_in1, c_in2, c_in3, c_in4 = st.columns([1.5, 1.8, 1, 1])

with c_in1:
    genetica_sel = st.selectbox("🧬 GENÉTICA", list(db.get("GENETICAS_PARAMETROS", {}).keys()))
with c_in2:
    ambiente_sel = st.selectbox("🏠 AMBIENTE", [
        "Indoor (Luz Artificial Controlada)", 
        "Estufa/Greenhouse (Sol + Luz Complementar)", 
        "Estufa/Greenhouse (Somente Sol)", 
        "Outdoor (Céu Aberto/Quintal)"
    ])
with c_in3:
    n_plantas = st.number_input("Nº PLANTAS", 1, 1000, 4)
with c_in4:
    data_inicio = st.date_input("📅 INÍCIO", datetime.date.today() - datetime.timedelta(days=1))

# Processamento de Dados Cronológicos
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7
fase_atual = "Plântula"
if dias_vida > 14: fase_atual = "Vegetativo"
if dias_vida > 42: fase_atual = "Pré-Flora/Flora"

# --- B. INPUTS FÍSICOS ---
c_sub1, c_sub2, c_sub3, c_sub4 = st.columns([1.5, 1.2, 1.2, 1.5])
with c_sub1:
     metodo_sel = st.selectbox("🥣 MÉTODO/SUBSTRATO", list(db.get("METODOS_CULTIVO", {}).keys()))
with c_sub2:
    tipo_plantio = st.selectbox("🌱 ONDE ESTÃO?", ["Vasos", "Canteiro/Chão"])
with c_sub3:
    vol_vaso = 0
    if tipo_plantio == "Vasos":
        vol_vaso = st.selectbox("TAMANHO VASO", [4, 7, 11, 15, 20, 25, 30, 40, 50, 100], index=2, format_func=lambda x: f"{x} Litros")
    else:
        vol_vaso = 999 
with c_sub4:
    horas_luz = st.number_input("⏰ HORAS DE LUZ/DIA", 10, 24, 18, help="Fotoperíodo diário.")

# --- INICIALIZAÇÃO DE VARIÁVEIS SEGURAS ---
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
mapa_ocupacao = {4: 0.04, 7: 0.06, 11: 0.09, 15: 0.11, 20: 0.14, 25: 0.16, 30: 0.20, 40: 0.25, 50: 0.30, 100: 0.50}

watts_painel = 0; area_m2 = 0; show_consultoria = False
txt_luz_titulo = ""; txt_luz_desc = ""
txt_espaco_titulo = ""; txt_espaco_desc = ""
txt_raiz_titulo = ""; txt_raiz_desc = ""
recomendacao_premium = ""; cor_card = "#a855f7"

# --- C. MOTOR DE INTELIGÊNCIA (ANÁLISE PROFUNDA) ---

# 1. SETUP DO AMBIENTE
if "Indoor" in ambiente_sel:
    with st.expander("💡 CONFIGURAÇÃO DO GROW (Dimensionamento)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: watts_painel = st.number_input("POTÊNCIA LED (Watts Reais):", 50, 5000, 240)
        with c2: largura = st.number_input("LARGURA (cm):", 40, 1000, 80)
        with c3: profundidade = st.number_input("PROFUNDIDADE (cm):", 40, 1000, 80)
        area_m2 = (largura * profundidade) / 10000
        
        if area_m2 > 0:
            show_consultoria = True
            # Cálculo PPFD Estimado (Eficiência média 2.3 umol/J)
            ppfd = (watts_painel * 2.3) / area_m2
            dli = ppfd * horas_luz * 0.0036
            
            # Análise Contextual (Idade x Luz)
            if fase_atual == "Plântula":
                meta_ppfd = 300
                if ppfd > 400:
                    txt_luz_titulo = f"⚠️ ALERTA: LUZ MUITO FORTE ({ppfd:.0f} µmol/s)"
                    txt_luz_desc = "Para plântulas/clones, essa intensidade causa estresse luminosa. As folhas vão 'tacar' (curvar bordas)."
                    recomendacao_premium = "Dimmer em 40% ou afaste o painel para 80cm."
                    cor_card = "#eab308"
                elif ppfd < 150:
                    txt_luz_titulo = "⚠️ LUZ INSUFICIENTE (Estiolamento)"
                    txt_luz_desc = "A planta vai esticar o caule buscando luz, ficando fraca."
                    cor_card = "#eab308"
                else:
                    txt_luz_titulo = "✅ INTENSIDADE PERFEITA (VPD Foco)"
                    txt_luz_desc = "Excelente para enraizamento. Mantenha umidade alta."
                    cor_card = "#22c55e"
            
            elif fase_atual == "Vegetativo":
                if ppfd < 400:
                    txt_luz_titulo = "⚠️ CRESCIMENTO LENTO"
                    txt_luz_desc = "Pouca energia para ramificação lateral. A planta crescerá devagar."
                    cor_card = "#eab308"
                elif ppfd > 700:
                    txt_luz_titulo = "🔥 LIMITE METABÓLICO"
                    txt_luz_desc = "Sem CO2 extra, você está no limite. Monitore deficiência de Magnésio."
                else:
                    txt_luz_titulo = "✅ VEGETATIVO VIGOROSO"
                    txt_luz_desc = "Faixa ideal para criar estrutura robusta antes da flora."
                    cor_card = "#22c55e"
            
            else: # Flora
                if dli < 30:
                    txt_luz_titulo = f"⚠️ BAIXA DENSIDADE DE BUDS (DLI {dli:.1f})"
                    txt_luz_desc = "Falta energia para compactar as flores. Espere buds mais 'aerados'."
                    recomendacao_premium = "Aumente a luz, aproxime o painel ou adicione luz lateral (side-lighting)."
                    cor_card = "#eab308"
                elif dli > 45:
                    txt_luz_titulo = f"🔥 SATURAÇÃO ({dli:.1f} DLI)"
                    txt_luz_desc = "Intensidade extrema. Obrigatório CO2 (1200ppm) e CalMag extra."
                else:
                    txt_luz_titulo = f"🚀 FLORAÇÃO OTIMIZADA ({dli:.1f} DLI)"
                    txt_luz_desc = "Ponto ideal (Sweet Spot) para produção máxima de resina e peso."
                    cor_card = "#22c55e"

elif "Complementar" in ambiente_sel:
    with st.expander("☀️💡 ESTUFA HÍBRIDA", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: watts_painel = st.number_input("W COMPLEMENTAR:", 10, 5000, 100)
        with c2: largura = st.number_input("LARGURA (cm):", 100, 5000, 200)
        with c3: profundidade = st.number_input("COMPRIMENTO (cm):", 100, 5000, 200)
        area_m2 = (largura * profundidade) / 10000
        
        if area_m2 > 0:
            show_consultoria = True
            ppfd_art = (watts_painel * 2.3) / area_m2
            txt_luz_titulo = f"SUPORTE: {ppfd_art:.0f} µmol/s (Artificial)"
            if ppfd_art < 50:
                txt_luz_desc = "Função exclusiva de Fotoperíodo (impedir floração). Não gera peso extra."
            else:
                txt_luz_desc = "Luz suficiente para DLI Extensivo (Aumenta o peso final)."

elif "Somente Sol" in ambiente_sel:
    with st.expander("☀️ ÁREA SOLAR", expanded=True):
        c1, c2 = st.columns(2)
        with c1: largura = st.number_input("LARGURA (cm):", 100, 5000, 200)
        with c2: profundidade = st.number_input("COMPRIMENTO (cm):", 100, 5000, 200)
        area_m2 = (largura * profundidade) / 10000
        show_consultoria = True
        txt_luz_titulo = "☀️ ESPECTRO SOLAR COMPLETO"
        txt_luz_desc = "O Sol fornece UV (aumenta resina) e IR (calor). O desafio é gerenciar a temperatura das raízes."

else: # Outdoor
    area_m2 = 999; show_consultoria = True
    txt_luz_titulo = "☀️ CULTIVO AO AR LIVRE"
    txt_luz_desc = "Exposição total. Monitore tempestades e pragas voadoras (mariposas/lagartas)."

# 2. ANÁLISE DE ENGENHARIA DE ESPAÇO
if area_m2 != 999 and show_consultoria:
    if tipo_plantio == "Vasos":
        area_uni = mapa_ocupacao.get(vol_vaso, 0.15)
        area_req = n_plantas * area_uni
        ocupacao = (area_req / area_m2) * 100
        
        if ocupacao > 110:
            txt_espaco_titulo = f"🚫 ERRO FÍSICO CRÍTICO ({ocupacao:.0f}% Ocupado)"
            txt_espaco_desc = f"Impossível acomodar {n_plantas} plantas. Elas vão crescer umas sobre as outras."
            recomendacao_premium = "Descarte plantas fracas (Culling) para salvar as fortes."
            cor_card = "#ef4444"
        elif ocupacao > 85:
            txt_espaco_titulo = f"⚠️ ALTA DENSIDADE (SOG) - {ocupacao:.0f}%"
            txt_espaco_desc = "Dossel fechado. Risco alto de microclima úmido (Mofo). Exige ventilação inferior."
            if not recomendacao_premium: recomendacao_premium = "Faça Poda Lollipopping (Canela nua) agressiva."
        else:
            txt_espaco_titulo = "✅ ESPAÇAMENTO SAUDÁVEL"
            txt_espaco_desc = "Ar circula livremente. Menor risco de pragas e doenças fúngicas."
    else:
        txt_espaco_titulo = "🌿 SOLO LIVRE"
        txt_espaco_desc = "Sem restrição de vaso. Plantas tendem a triplicar de tamanho na flora."

# 3. ANÁLISE DE SAÚDE RADICULAR (Complexa)
if tipo_plantio == "Vasos":
    is_coco = "Mineral" in metodo_sel or "Hidro" in metodo_sel
    
    # Lógica Automática
    if info_genetica['tipo'] == "Auto":
        if vol_vaso < 7:
            txt_raiz_titulo = "⚠️ VOLUME INSUFICIENTE"
            txt_raiz_desc = "Automáticas não recuperam de estresse de raiz. Vaso pequeno = Planta anã."
        elif vol_vaso > 25:
            txt_raiz_titulo = "ℹ️ SOBRA DE SUBSTRATO"
            txt_raiz_desc = "A planta entrará em floração antes de colonizar o fundo. Risco de zona anaeróbica (água parada) no fundo."
        else:
            txt_raiz_titulo = "✅ BUFFER IDEAL"
            txt_raiz_desc = "Equilíbrio perfeito entre oxigenação e retenção de água."

    # Lógica Fotoperíodo
    else:
        if is_coco: # Substrato Inerte
            if vol_vaso < 4:
                txt_raiz_titulo = "💧 CROP STEERING (Alta Frequência)"
                txt_raiz_desc = "Em coco/lã, vasos pequenos exigem múltiplas regas por dia (4-6x). Se regar 1x, vai secar (Dryback excessivo)."
            else:
                txt_raiz_titulo = "✅ HIDRODENSIDADE OK"
                txt_raiz_desc = "Vaso permite regas volumosas com boa oxigenação."
        else: # Solo Orgânico
            if vol_vaso < 11 and dias_vida > 30:
                txt_raiz_titulo = "⚠️ RISCO DE ROOT BOUND"
                txt_raiz_desc = "No orgânico, a planta come a terra. Vaso pequeno esgota nutrientes rápido. Transplante recomendado."
                recomendacao_premium = "Faça transplante para vaso final (20L+) antes da floração."
            else:
                txt_raiz_titulo = "✅ VIDA DO SOLO ATIVA"
                txt_raiz_desc = "Volume suficiente para manter a microbiologia (fungos/bactérias) estável."
else:
    txt_raiz_titulo = "🌍 RAÍZES NO CHÃO"
    txt_raiz_desc = "Atenção: Solo argiloso pode compactar. Solo arenoso drena demais. Use cobertura morta (Mulching)."

# --- EXIBIÇÃO DO CARD (HTML PURO / SEM RECUO PARA EVITAR ERROS) ---
if show_consultoria:
    titulo_card = f"CONSULTORIA: {ambiente_sel.split('(')[0].upper()}"
    
    # O HTML deve estar colado na margem esquerda (flush left) dentro da f-string
    html_content = f"""
<div class="diag-card" style="border-left: 4px solid {cor_card};">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;">
<div style="font-weight:900; color:{cor_card}; letter-spacing:1px; font-size:1.2rem;">{titulo_card}</div>
<div style="background:{cor_card}20; color:{cor_card}; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:bold;">SDI TITANIUM</div>
</div>
<div style="font-family:sans-serif; color:#e4e4e7;">
<div style="margin-bottom:15px;">
<strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px;">ANÁLISE FOTÔNICA ({fase_atual.upper()})</strong><br>
<div style="font-size:1rem; font-weight:bold; margin-top:4px; color:#fff;">{txt_luz_titulo}</div>
<div style="font-size:0.9rem; color:#ccc; line-height:1.4; margin-top:2px;">{txt_luz_desc}</div>
</div>
<div style="margin-bottom:15px;">
<strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px;">ENGENHARIA DE ESPAÇO</strong><br>
<div style="font-size:1rem; font-weight:bold; margin-top:4px; color:#fff;">{txt_espaco_titulo}</div>
<div style="font-size:0.9rem; color:#ccc; line-height:1.4; margin-top:2px;">{txt_espaco_desc}</div>
</div>
<div style="margin-bottom:15px;">
<strong style="color:#aaa; font-size:0.75rem; letter-spacing:1px;">SAÚDE RADICULAR & MEIO</strong><br>
<div style="font-size:1rem; font-weight:bold; margin-top:4px; color:#fff;">{txt_raiz_titulo}</div>
<div style="font-size:0.9rem; color:#ccc; line-height:1.4; margin-top:2px;">{txt_raiz_desc}</div>
</div>
<div style="margin-top:25px; padding:15px; background:linear-gradient(90deg, {cor_card}15 0%, rgba(0,0,0,0) 100%); border-radius:8px; border-left:4px solid {cor_card};">
<span style="color:{cor_card}; font-weight:bold; font-size:0.9rem;">PLANO DE AÇÃO DO ESPECIALISTA:</span><br>
<span style="color:#fff; font-size:1rem; line-height:1.6; display:block; margin-top:6px;">
{recomendacao_premium if recomendacao_premium else "Seu ecossistema está estável e produtivo. Mantenha o VPD na faixa de 1.0 kPa e monitore o pH do runoff semanalmente."}
</span>
</div>
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)

# --- CÁLCULOS FINAIS PARA INTEGRAÇÃO ---
fator_luz = 1.0
if "Indoor" in ambiente_sel and 'dli' in locals():
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

# C. CARD DE CONSULTORIA SDI (CORRIGIDO: SEM INDENTAÇÃO INTERNA)
if show_consultoria:
    titulo_card = f"CONSULTORIA: {ambiente_sel.split('(')[0].upper()}"
    
    # Cor Fixa Roxa Profissional
    cor_layout = "#a855f7"
    
    # IMPORTANTE: O HTML abaixo não pode ter espaços no início das linhas!
    html_content = f"""
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
"""
    st.markdown(html_content, unsafe_allow_html=True)

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
