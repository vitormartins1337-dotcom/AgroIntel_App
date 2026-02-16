# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | REVOLUTION V5.0
import streamlit as st
import datetime
from core_logic import AgroEngine 

# --- 1. SETUP & LAYOUT ---
st.set_page_config(page_title="Agrower SDI", page_icon="🍁", layout="wide", initial_sidebar_state="collapsed")
engine = AgroEngine()
db = engine.db 

# --- 2. CSS PROFISSIONAL (CORRIGIDO E OTIMIZADO) ---
def load_css():
    st.markdown("""
        <style>
        /* FONTS & BASE */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&family=JetBrains+Mono:wght@400;700&display=swap');
        
        .stApp { 
            background-color: #09090b; 
            color: #e4e4e7; 
            font-family: 'Inter', sans-serif;
        }
        .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }

        /* HEADER HERO */
        .hero-header {
            background: linear-gradient(135deg, #18181b 0%, #09090b 100%);
            border-bottom: 1px solid #27272a;
            padding: 40px 0;
            margin-bottom: 30px;
            text-align: left;
        }
        .hero-title {
            font-size: 3.5rem; font-weight: 900; color: #fff; letter-spacing: -2px; line-height: 1;
        }
        .hero-subtitle {
            font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #a1a1aa; 
            text-transform: uppercase; letter-spacing: 2px; margin-top: 10px;
        }
        .live-badge {
            background: rgba(34, 197, 94, 0.1); border: 1px solid #15803d; color: #4ade80;
            padding: 6px 12px; border-radius: 99px; font-size: 0.75rem; font-weight: 700;
            display: inline-flex; align-items: center; gap: 6px; vertical-align: middle;
        }

        /* CARDS & CONTAINERS */
        .glass-panel {
            background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 24px;
            margin-bottom: 16px; transition: transform 0.2s;
        }
        .glass-panel:hover { border-color: #3f3f46; }

        /* YIELD CARD (DESTAQUE) */
        .yield-card {
            background: linear-gradient(135deg, #2a1b05 0%, #1a1500 100%);
            border: 1px solid #eab308; border-radius: 12px; padding: 20px;
            text-align: center; color: #fef08a;
        }
        
        /* BADGES (CORREÇÃO DE QUEBRA DE LINHA) */
        .info-badge {
            display: inline-flex; align-items: center; white-space: nowrap; /* SEGREDO PARA NÃO QUEBRAR */
            background: #27272a; border: 1px solid #3f3f46; color: #e4e4e7;
            padding: 6px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; margin-right: 8px; margin-bottom: 8px;
        }
        
        /* INPUTS */
        .stSelectbox > div > div, .stDateInput > div > div, .stNumberInput > div > div {
            background-color: #18181b !important; border: 1px solid #27272a !important; color: #fff !important;
        }

        /* THREAT CARD (AMEAÇAS) */
        .threat-box {
            background: #220505; border-left: 4px solid #ef4444; padding: 15px; border-radius: 6px; margin-top: 10px;
        }
        .threat-title { color: #fca5a5; font-weight: bold; font-size: 0.95rem; margin-bottom: 5px; }
        .solution-tag { font-size: 0.8rem; color: #cbd5e1; font-family: 'JetBrains Mono', monospace; }

        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. HEADER PROFISSIONAL ---
c_head1, c_head2 = st.columns([3, 1])
with c_head1:
    st.markdown("""
    <div>
        <div class="hero-title">AGROWER <span style="color:#22c55e">SDI</span></div>
        <div class="hero-subtitle">Sistema de Decisão Integrada v5.0</div>
    </div>
    """, unsafe_allow_html=True)
with c_head2:
    st.markdown("""
    <div style="text-align:right; padding-top:20px;">
        <span class="live-badge"><span style="width:6px; height:6px; background:#4ade80; border-radius:50%;"></span> ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# 🎮 DASHBOARD DE CONFIGURAÇÃO & PREVISÃO
# ==============================================================================

# Inputs em linha única (Layout Desktop)
c1, c2, c3, c4 = st.columns([1.5, 1.5, 1, 1])

with c1:
    # Busca chaves do DB
    metodo_keys = list(db.get("METODOS_CULTIVO", {}).keys())
    metodo_sel = st.selectbox("MÉTODO DE CULTIVO", metodo_keys)
    
with c2:
    # Busca Genéticas do DB
    genetica_keys = list(db.get("GENETICAS_PARAMETROS", {}).keys())
    genetica_sel = st.selectbox("GENÉTICA PREDOMINANTE", genetica_keys)

with c3:
    n_plantas = st.number_input("Nº PLANTAS", 1, 500, 6)

with c4:
    data_inicio = st.date_input("DATA INÍCIO", datetime.date.today() - datetime.timedelta(days=45))

# --- MOTOR DE CÁLCULO SDI ---
# 1. Dados do Método
info_metodo = db["METODOS_CULTIVO"][metodo_sel]
# 2. Dados da Genética
info_genetica = db["GENETICAS_PARAMETROS"][genetica_sel]

# 3. Cálculo de Tempo
dias_vida = (datetime.date.today() - data_inicio).days
semanas = dias_vida // 7

# 4. Cálculo de Yield (Estimativa)
rendimento_base = info_metodo['rendimento_base_g_planta']
fator_genetica = info_genetica['fator_yield']
estimativa_total_g = rendimento_base * fator_genetica * n_plantas
estimativa_total_kg = estimativa_total_g / 1000

# 5. Determinação da Fase
fase_nome = "Indefinida"
fase_dados = {}
for k, v in db.get("FASES_DINAMICAS", {}).items():
    # Lógica simplificada de dias
    dias_limite = 200 # Default
    if "Plântula" in k: dias_limite = 14
    elif "Vegetativo" in k: dias_limite = 42
    elif "Pré-Flora" in k: dias_limite = 56
    elif "Flora Inicial" in k: dias_limite = 77
    if dias_vida <= dias_limite:
        fase_nome = k
        fase_dados = v
        break

# --- PAINEL VISUAL DE STATUS ---
st.markdown("<br>", unsafe_allow_html=True)

col_painel_1, col_painel_2 = st.columns([2, 1])

with col_painel_1:
    # STATUS CARD
    st.markdown(f"""
    <div class="glass-panel" style="border-left: 4px solid {info_metodo['cor_tema']};">
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div style="font-size:0.8rem; color:#a1a1aa; text-transform:uppercase; font-weight:bold;">FASE ATUAL</div>
                <div style="font-size:2rem; font-weight:900; color:#fff; margin:5px 0;">{fase_nome.upper()}</div>
                <div style="margin-top:10px;">
                    <span class="info-badge">📅 {dias_vida} DIAS</span>
                    <span class="info-badge">📆 SEMANA {semanas}</span>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.8rem; color:#a1a1aa;">PARÂMETROS ALVO</div>
                <div style="margin-top:5px;">
                    <span class="info-badge" style="border-color:{info_metodo['cor_tema']}; color:{info_metodo['cor_tema']};">PH {info_metodo['ph_ideal']}</span>
                </div>
                <div style="margin-top:5px;">
                    <span class="info-badge" style="border-color:{info_metodo['cor_tema']}; color:{info_metodo['cor_tema']};">EC {info_metodo['ec_ideal']}</span>
                </div>
            </div>
        </div>
        <hr style="border-color:#333; margin:15px 0;">
        <div style="color:#e4e4e7; font-size:1.1rem; font-weight:600;">🎯 FOCO DA SEMANA: {fase_dados.get('foco', '-')}</div>
        <div style="color:#a1a1aa; font-size:0.95rem; margin-top:5px;">{fase_dados.get('obs', '-')}</div>
    </div>
    """, unsafe_allow_html=True)

with col_painel_2:
    # YIELD CALCULATOR CARD
    st.markdown(f"""
    <div class="yield-card">
        <div style="font-size:0.8rem; font-weight:bold; letter-spacing:1px; opacity:0.8;">PREVISÃO DE COLHEITA (SECA)</div>
        <div style="font-size:3rem; font-weight:900; line-height:1.2; margin:10px 0;">{estimativa_total_g:.0f}g</div>
        <div style="font-size:0.9rem; opacity:0.8;">~ {estimativa_total_kg:.2f} kg Totais</div>
        <hr style="border-color:#ca8a04; opacity:0.3; margin:15px 0;">
        <div style="font-size:0.8rem;">
            Baseado em: {n_plantas}x {genetica_sel.split(' ')[0]} no {metodo_sel.split(' ')[0]}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🕵️ RADAR DE AMEAÇAS & DOCTOR GROW (INTEGRADO)
# ==============================================================================

# Abas Simplificadas conforme pedido
tab_radar, tab_doctor_full = st.tabs(["🛡️ RADAR DA SEMANA (MANEJO)", "🚑 DOCTOR GROW (COMPLETO)"])

with tab_radar:
    st.markdown(f"### 📡 Ameaças Ativas: {fase_nome}")
    st.caption("Baseado na biologia da planta nesta idade específica, estas são as pragas e problemas mais prováveis. Previna-se agora.")
    
    ameacas = fase_dados.get("ameacas_chave", [])
    if not ameacas:
        st.success("Nenhuma ameaça crítica mapeada para esta fase inicial. Foque no ambiente.")
    
    # Grid de Ameaças
    cols_threat = st.columns(len(ameacas) if len(ameacas) > 0 else 1)
    
    doctor_db = db["DOCTOR_GROW_MASTER"]
    
    for i, ameaca_nome in enumerate(ameacas):
        # Procura a ameaça no DB completo para pegar a solução
        solucao = None
        dados_ameaca = {}
        
        # Varre o DB para achar os dados da ameaça citada na fase
        for cat in doctor_db: # Pragas, Doencas, etc
            if ameaca_nome in doctor_db[cat]:
                dados_ameaca = doctor_db[cat][ameaca_nome]
                break
        
        if not dados_ameaca:
            # Fallback se o nome não bater exato (busca parcial)
            for cat in doctor_db:
                for k, v in doctor_db[cat].items():
                    if ameaca_nome.split(' ')[0] in k:
                        dados_ameaca = v
                        break
        
        # Renderiza o Card de Ação Imediata
        if dados_ameaca:
            with st.expander(f"🚨 RISCO ALTO: {ameaca_nome}", expanded=True):
                st.markdown(f"**Identificação:** {dados_ameaca['identificacao']}")
                
                c_sol1, c_sol2 = st.columns(2)
                with c_sol1:
                    st.markdown(f"<div style='color:#4ade80; font-weight:bold; font-size:0.85rem;'>🌿 CONTROLE BIO</div>", unsafe_allow_html=True)
                    st.markdown(f"{dados_ameaca['controle']}")
                with c_sol2:
                    st.markdown(f"<div style='color:#f87171; font-weight:bold; font-size:0.85rem;'>🧪 PRODUTOS</div>", unsafe_allow_html=True)
                    for prod in dados_ameaca['produtos']:
                         st.markdown(f"- {prod}")
                

with tab_doctor_full:
    st.markdown("### 📚 Enciclopédia de Pragas e Soluções")
    search_doc = st.text_input("🔍 Buscar sintoma ou praga:")
    
    for categoria, itens in doctor_db.items():
        # Filtro de busca
        itens_filtrados = {k:v for k,v in itens.items() if not search_doc or search_doc.lower() in k.lower()}
        
        if itens_filtrados:
            st.markdown(f"#### {categoria}")
            for nome, info in itens_filtrados.items():
                with st.expander(f"{nome}"):
                    st.markdown(f"**Sintomas:** {info['identificacao']}")
                    st.markdown(f"**Solução:** {info['controle']}")
                    st.markdown(f"**Produtos:** {', '.join(info['produtos'])}")
