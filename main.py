# ARQUIVO: main.py
# SISTEMA: AGROWER SDI | MASTER GENETICS EDITION
import streamlit as st
from core_logic import AgroEngine 

# --- 1. CONFIGURAÇÃO (LARGURA TOTAL & DARK MODE) ---
st.set_page_config(page_title="Agrower SDI", page_icon="🍁", layout="wide")
engine = AgroEngine()

# --- 2. CSS CUSTOMIZADO (VISUAL GROW SHOP) ---
def load_css():
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem !important; padding-bottom: 3rem !important; }
        .stApp { background-color: #050505; color: #e0e0e0; font-family: 'Roboto', sans-serif; }
        [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #222; }

        /* HEADER */
        .header-box {
            background: linear-gradient(90deg, #3b0764 0%, #000000 100%);
            border-bottom: 2px solid #a855f7; padding: 30px; border-radius: 0 0 20px 20px;
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
            box-shadow: 0 0 25px rgba(168, 85, 247, 0.15);
        }

        /* TICKER PARAMETROS */
        .ticker-container {
            width: 100%; background-color: #000; border: 1px solid #22c55e; border-radius: 6px;
            overflow: hidden; white-space: nowrap; height: 32px; display: flex; align-items: center; margin-bottom: 20px;
        }
        .ticker-text { display: inline-block; animation: ticker 40s linear infinite; font-family: 'Courier New', monospace; font-weight: bold; font-size: 0.85rem;}
        @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .tick-item { margin-right: 50px; color: #d8b4fe; } .tick-val { color: #22c55e; }

        /* CARDS DE GENÉTICA (ESTILO RPG) */
        .gen-card {
            background-color: #111; border: 1px solid #333; border-radius: 10px; padding: 20px; margin-bottom: 20px;
            transition: transform 0.2s; position: relative; overflow: hidden;
        }
        .gen-card:hover { border-color: #a855f7; transform: translateY(-2px); }
        .gen-title { font-size: 1.6rem; font-weight: 900; color: #fff; margin: 0; line-height:1.2; }
        .gen-bank { font-size: 0.9rem; color: #888; margin-bottom: 10px; font-style: italic; }
        .tag-thc { background: #3b0764; color: #d8b4fe; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; border: 1px solid #a855f7; }
        .tag-terp { background: #064e3b; color: #4ade80; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-right: 4px; }
        
        .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; background: #000; padding: 10px; border-radius: 6px; }
        .stat-item { font-size: 0.85rem; color: #ccc; }
        .stat-label { color: #666; font-size: 0.7rem; text-transform: uppercase; display: block; }
        
        /* CARD BOTANICA */
        .bot-card { background: #1a1a1a; padding: 15px; border-left: 5px solid #22c55e; margin-bottom: 10px; border-radius: 4px; }

        /* INPUTS */
        .stSelectbox div[data-baseweb="select"] > div, .stTextInput input { background-color: #111 !important; color: #fff !important; border: 1px solid #444 !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 5px; }
        .stTabs [data-baseweb="tab"] { background-color: #111; border: 1px solid #333; color: #888; padding: 10px 20px; }
        .stTabs [aria-selected="true"] { background-color: #a855f7 !important; color: #fff !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. HEADER ---
st.markdown("""
<div class="header-box">
    <div>
        <h1 style="margin:0; font-family:'Helvetica', sans-serif; font-weight:900; font-size:3.5rem; letter-spacing:-2px; color:#fff; line-height: 1;">
            AGROWER <span style="color:#a855f7;">SDI</span>
        </h1>
        <div style="font-size:1rem; letter-spacing:4px; color:#d8b4fe; margin-top:5px; font-weight:600; opacity:0.9;">
            MASTER GENETICS DATABASE
        </div>
    </div>
    <div style="text-align:right;">
        <div style="background:rgba(168, 85, 247, 0.2); border:1px solid #a855f7; color:#d8b4fe; padding:6px 16px; border-radius:30px; font-size:0.8rem; display:inline-flex; align-items:center; gap:8px;">
            🍁 PRO VERSION
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

ticker_html = """
<div class="ticker-container">
    <div class="ticker-text">
        <span class="tick-item">VEG TEMP: <span class="tick-val">22-28°C</span></span>
        <span class="tick-item">VEG UMIDADE: <span class="tick-val">60-70%</span></span>
        <span class="tick-item">FLORA TEMP: <span class="tick-val">20-25°C</span></span>
        <span class="tick-item">FLORA UMIDADE: <span class="tick-val">40-50%</span></span>
        <span class="tick-item">PH SOLO: <span class="tick-val">6.0-6.8</span></span>
        <span class="tick-item">EC FLORA: <span class="tick-val">1.6-2.2</span></span>
        <span class="tick-item">PPFD FLORA: <span class="tick-val">800-1000</span></span>
    </div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# ==============================================================================
# 🧠 CÉREBRO
# ==============================================================================
db = engine.db # Acesso direto ao DB Mestre

# Abas Principais
tab_catalogo, tab_botanica, tab_setup, tab_doctor = st.tabs(["🧬 CATÁLOGO DE GENÉTICAS", "📚 BOTÂNICA & SEXAGEM", "💡 SETUP & MANEJO", "🛡️ DOCTOR GROW"])

# --- ABA 1: CATÁLOGO MASTER ---
with tab_catalogo:
    # Filtros
    c_filt1, c_filt2 = st.columns([1, 2])
    with c_filt1:
        # Pega as categorias (Indica, Sativa, etc) excluindo as chaves de Botanica/Setup
        categorias = [k for k in db.keys() if "GENÉTICAS" in k]
        # Dentro da chave "GENÉTICAS REAIS", pega as subcategorias
        subcats = list(db["🧬 GENÉTICAS REAIS (CATÁLOGO MASTER)"].keys())
        cat_sel = st.selectbox("📂 Categoria:", ["Todas"] + subcats)
    
    with c_filt2:
        busca = st.text_input("🔍 Buscar Genética (Ex: Haze, Kush):")

    st.markdown("---")

    # Lógica de Exibição
    root_gen = db["🧬 GENÉTICAS REAIS (CATÁLOGO MASTER)"]
    found = False
    
    for subcat, strains in root_gen.items():
        # Filtro de Categoria
        if cat_sel != "Todas" and cat_sel != subcat: continue
        
        # Header da Categoria
        if not busca: st.markdown(f"#### {subcat}")
        
        cols = st.columns(2) # Grid de 2 colunas
        idx = 0
        
        for nome_strain, dados in strains.items():
            # Filtro de Busca Texto
            if busca and busca.lower() not in nome_strain.lower(): continue
            found = True
            
            # Card
            with cols[idx % 2]:
                html_card = f"""
                <div class="gen-card">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <div>
                            <h3 class="gen-title">{nome_strain}</h3>
                            <div class="gen-bank">{dados['banco']}</div>
                        </div>
                        <div style="text-align:right;">
                            <span class="tag-thc">THC: {dados['thc']}</span>
                            <div style="font-size:0.7rem; color:#888; margin-top:5px;">CBD: {dados['cbd']}</div>
                        </div>
                    </div>
                    
                    <div style="margin: 10px 0;">
                        {' '.join([f'<span class="tag-terp">{t}</span>' for t in dados['terpenos']])}
                    </div>
                    
                    <p style="color:#e0e0e0; font-size:0.9rem; margin-bottom:10px;">
                        <i>"{dados['efeito']}"</i>
                    </p>
                    
                    <div class="stat-grid">
                        <div class="stat-item"><span class="stat-label">Sabor</span>{dados['sabor']}</div>
                        <div class="stat-item"><span class="stat-label">Medicinal</span>{dados['medicinal']}</div>
                        <div class="stat-item"><span class="stat-label">Tempo Flora</span>{dados['cultivo']['tempo_flora']}</div>
                        <div class="stat-item"><span class="stat-label">Rendimento</span>{dados['cultivo']['rendimento_indoor']}</div>
                        <div class="stat-item"><span class="stat-label">Dificuldade</span>{dados['cultivo']['dificuldade']}</div>
                        <div class="stat-item"><span class="stat-label">Clima</span>{dados['cultivo']['clima']}</div>
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
            idx += 1
            
    if not found:
        st.warning("Nenhuma genética encontrada com esse nome.")

# --- ABA 2: BOTÂNICA ---
with tab_botanica:
    botanica = db["📚 BOTÂNICA & SEXAGEM"]["tipos"]
    st.markdown("### 🌱 Morfologia e Sexagem da Cannabis")
    st.caption("Guia essencial para identificar e evitar polinização indesejada.")
    
    c_b1, c_b2, c_b3 = st.columns(3)
    
    with c_b1:
        femea = botanica["Fêmea (Sinsemilla)"]
        st.markdown(f"""
        <div class="bot-card" style="border-left-color: #d8b4fe;">
            <h4 style="color:#d8b4fe;">♀️ FÊMEA</h4>
            <p style="font-size:0.9rem;">{femea['descricao']}</p>
            <hr style="border-color:#333;">
            <p style="font-size:0.85rem; color:#ccc;"><b>🔎 Identificação:</b> {femea['identificacao']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_b2:
        macho = botanica["Macho"]
        st.markdown(f"""
        <div class="bot-card" style="border-left-color: #38bdf8;">
            <h4 style="color:#38bdf8;">♂️ MACHO</h4>
            <p style="font-size:0.9rem;">{macho['descricao']}</p>
            <hr style="border-color:#333;">
            <p style="font-size:0.85rem; color:#ccc;"><b>🔎 Identificação:</b> {macho['identificacao']}</p>
            <p style="font-size:0.8rem; color:#f87171; background:#3f1010; padding:5px; border-radius:4px; margin-top:5px;">⚠️ {macho['alerta']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_b3:
        herma = botanica["Hermafrodita (Hermie)"]
        st.markdown(f"""
        <div class="bot-card" style="border-left-color: #facc15;">
            <h4 style="color:#facc15;">⚧️ HERMAFRODITA</h4>
            <p style="font-size:0.9rem;">{herma['descricao']}</p>
            <hr style="border-color:#333;">
            <p style="font-size:0.85rem; color:#ccc;"><b>🔎 Identificação:</b> {herma['identificacao']}</p>
            <p style="font-size:0.85rem; color:#facc15;"><b>🛠️ Ação:</b> {herma['acao']}</p>
        </div>
        """, unsafe_allow_html=True)

# --- ABA 3: SETUP & MANEJO ---
with tab_setup:
    info_grow = db["💡 SETUP & MANEJO"]
    st.markdown("### 💡 Parâmetros Ideais de Cultivo")
    
    st.markdown(f"""
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
        <div class="gen-card">
            <h4 style="color:#a855f7;">☀️ Iluminação</h4>
            <div style="font-size:1.1rem; font-weight:bold;">{info_grow['luz']}</div>
        </div>
        <div class="gen-card">
            <h4 style="color:#38bdf8;">🌡️ Clima (VPD)</h4>
            <div style="font-size:1.1rem; font-weight:bold;">{info_grow['clima_ideal']}</div>
        </div>
        <div class="gen-card">
            <h4 style="color:#22c55e;">🧪 Nutrição & pH</h4>
            <div style="font-size:1.1rem; font-weight:bold;">{info_grow['nutricao']}</div>
        </div>
        <div class="gen-card">
            <h4 style="color:#facc15;">🪚 Colheita Perfeita</h4>
            <div style="font-size:1.1rem; font-weight:bold;">{info_grow['colheita']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- ABA 4: DOCTOR ---
with tab_doctor:
    st.markdown("### 🚑 SOS Grower: Pragas e Doenças")
    doc_db = db["🛡️ DOCTOR GROW (PROBLEMAS)"]
    
    c_doc1, c_doc2 = st.columns(2)
    
    with c_doc1:
        st.markdown("#### 🕷️ Pragas Comuns")
        for nome, dados in doc_db["Pragas"].items():
             st.markdown(f"""
            <div style="background:#1a0505; border:1px solid #450a0a; padding:15px; border-radius:8px; margin-bottom:10px;">
                <div style="color:#f87171; font-weight:bold;">{nome}</div>
                <div style="font-size:0.9rem; color:#ccc;">{dados['identificacao']}</div>
                <div style="font-size:0.85rem; color:#aaa; margin-top:5px;">☠️ {dados['dano']}</div>
                <div style="margin-top:8px;">
                     {' '.join([f'<span style="background:#450a0a; color:#fca5a5; padding:2px 6px; border-radius:4px; font-size:0.8rem;">🛡️ {s}</span>' for s in dados['solucao']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with c_doc2:
        st.markdown("#### 🍄 Fungos e Doenças")
        for nome, dados in doc_db["Doencas"].items():
             st.markdown(f"""
            <div style="background:#1a1005; border:1px solid #431407; padding:15px; border-radius:8px; margin-bottom:10px;">
                <div style="color:#fdba74; font-weight:bold;">{nome}</div>
                <div style="font-size:0.9rem; color:#ccc;">{dados['identificacao']}</div>
                <div style="font-size:0.85rem; color:#aaa; margin-top:5px;">☠️ {dados['dano']}</div>
                <div style="margin-top:8px;">
                     {' '.join([f'<span style="background:#431407; color:#fdba74; padding:2px 6px; border-radius:4px; font-size:0.8rem;">🛡️ {s}</span>' for s in dados['solucao']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
