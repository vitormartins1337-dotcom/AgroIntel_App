# ARQUIVO: main.py
# AGRO SDI | VISÃO SÊNIOR DE CAMPO
import streamlit as st
from core_logic import AgroEngine # Certifique-se que o core_logic está na pasta

# --- SETUP INICIAL ---
st.set_page_config(page_title="Agro SDI Pro", page_icon="🚜", layout="wide")
engine = AgroEngine()

# --- CSS: ESTILO "CAMPO DE BATALHA" ---
def load_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0e1611; color: #e2e8f0; }
        
        /* HEADER */
        .header-box {
            background: linear-gradient(180deg, #14532d 0%, #064e3b 100%);
            padding: 20px; border-radius: 12px; border: 1px solid #166534;
            box-shadow: 0 4px 6px rgba(0,0,0,0.4); margin-bottom: 20px;
            display: flex; justify-content: space-between; align-items: center;
        }
        
        /* FASES FENOLÓGICAS (ESTILO CARDS) */
        .phase-card {
            background-color: #1a2e24; border-left: 5px solid #22c55e;
            padding: 15px; border-radius: 8px; margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .phase-title { color: #fff; font-size: 1.2rem; font-weight: bold; }
        .phase-subtitle { color: #86efac; font-size: 0.9rem; margin-bottom: 10px; font-weight: 600;}
        .expert-tip { 
            background: #3f2c22; color: #fdba74; padding: 10px; 
            border-radius: 6px; font-style: italic; font-size: 0.95rem;
            border: 1px solid #9a3412; margin-top: 10px;
        }
        
        /* PRAGAS E DOENÇAS */
        .pest-card {
            background-color: #0f172a; border: 1px solid #1e293b;
            padding: 15px; border-radius: 8px; margin-bottom: 10px;
        }
        .chem-tag {
            background: #0284c7; color: white; padding: 2px 8px;
            border-radius: 4px; font-size: 0.8rem; margin-right: 5px; font-weight: bold;
        }
        
        /* TICKER */
        .ticker-wrap { background: #064e3b; overflow: hidden; white-space: nowrap; padding: 5px; border-radius: 4px; margin-bottom: 15px;}
        .ticker-item { display: inline-block; padding: 0 2rem; color: #a7f3d0; font-family: monospace; font-weight: bold;}
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- HEADER E TICKER ---
st.markdown("""
<div class="header-box">
    <div>
        <h1 style='margin:0; font-size:2rem; color:white;'>AGRO <span style='color:#4ade80'>SDI</span></h1>
        <div style='color:#86efac; font-size:0.8rem; letter-spacing:2px; font-weight:bold;'>SISTEMA DE DECISÃO INTEGRADA</div>
    </div>
    <div style='background:rgba(22,163,74,0.2); border:1px solid #22c55e; color:#4ade80; padding:5px 10px; border-radius:20px; font-size:0.7rem; display:flex; align-items:center; gap:5px;'>
        <div style='width:8px; height:8px; background:#22c55e; border-radius:50%; box-shadow:0 0 5px #22c55e;'></div> ONLINE
    </div>
</div>
<div class="ticker-wrap">
    <div style="display: inline-block; animation: ticker 20s linear infinite;">
        <span class="ticker-item">SOJA CBOT ▼ $12.10</span>
        <span class="ticker-item">MILHO B3 ▲ R$ 58.40</span>
        <span class="ticker-item">BOI GORDO ▲ R$ 245.00</span>
        <span class="ticker-item">DÓLAR PTAX ▲ R$ 5.72</span>
        <span class="ticker-item">UREIA ▼ $380.00</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SELETOR DE CULTURA ---
culturas = engine.listar_culturas()
cultura_sel = st.selectbox("🚜 CULTURA EM FOCO:", culturas)

if cultura_sel:
    # AGORA TEMOS APENAS 2 ABAS
    tab1, tab2 = st.tabs(["🌱 FASES & MANEJO PRÁTICO", "🛡️ SANIDADE (PRAGAS & DOENÇAS)"])

    # =========================================================
    # ABA 1: FENOLOGIA COM VISÃO DE DONO DE FAZENDA
    # =========================================================
    with tab1:
        fases = engine.get_fases(cultura_sel)
        st.caption(f"Guia de campo para {cultura_sel}. Dicas baseadas em alta produtividade.")
        
        for sigla, dados in fases.items():
            # Estrutura visual robusta
            st.markdown(f"""
            <div class="phase-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="phase-title">{sigla}</div>
                    <div style="background:#064e3b; padding:2px 8px; border-radius:4px; font-size:0.7rem; color:#4ade80; border:1px solid #22c55e;">FOCO: {dados['foco'].upper()}</div>
                </div>
                <div class="phase-subtitle">{dados['fase']}</div>
                
                <div style="color:#cbd5e1; font-size:0.95rem; margin-top:5px; line-height:1.4;">
                    {dados['visao_pratica']}
                </div>
                
                <div class="expert-tip">
                    ⚠️ <b>ATENÇÃO DO TÉCNICO:</b> {dados['alerta']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # =========================================================
    # ABA 2: SANIDADE (TUDO EM UM LUGAR SÓ)
    # =========================================================
    with tab2:
        c1, c2 = st.columns([1, 3])
        with c1:
            # Filtro lateral para organizar sem separar abas
            tipo_problema = st.radio("Filtrar por:", ["Todos", "Pragas 🐛", "Doenças 🍄"], index=0)
        with c2:
            termo_busca = st.text_input("Buscar problema específico:", placeholder="Ex: Percevejo, Ferrugem...")

        st.divider()

        # Lógica para pegar tudo e juntar
        lista_final = []
        
        # Busca Pragas
        if tipo_problema in ["Todos", "Pragas 🐛"]:
            pragas = engine.buscar_problema(cultura_sel, termo_busca, "Pragas")
            for k, v in pragas.items(): 
                v['nome_exibicao'] = k
                lista_final.append(v)
        
        # Busca Doenças
        if tipo_problema in ["Todos", "Doenças 🍄"]:
            doencas = engine.buscar_problema(cultura_sel, termo_busca, "Doencas")
            for k, v in doencas.items(): 
                v['nome_exibicao'] = k
                lista_final.append(v)

        if not lista_final:
            st.info("Nenhum problema encontrado com esses filtros.")

        # Exibição dos Cards Unificados
        for item in lista_final:
            # Define cor da borda baseada no tipo
            cor_borda = "#ef4444" if item['tipo'] == "Praga" else "#f97316" # Vermelho praga, Laranja doença
            icone = "🐛" if item['tipo'] == "Praga" else "🍄"
            
            with st.expander(f"{icone} {item['nome_exibicao']}  |  Dano: {item.get('nivel_dano', '-')}", expanded=False):
                st.markdown(f"**Identificação:** {item['identificacao_campo']}")
                if 'fases_criticas' in item:
                    st.markdown(f"**Fases Críticas:** {', '.join(item['fases_criticas'])}")
                
                st.markdown("#### ☠️ Controle Químico")
                for solucao in item['manejo_quimico']:
                    st.markdown(f"""
                    <div style="background:#0f172a; padding:12px; border-radius:6px; border:1px solid #334155; margin-bottom:8px;">
                        <div style="color:#38bdf8; font-weight:bold;">{solucao['ativo']}</div>
                        <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:5px;">Mec: {solucao['mecanismo']} ({solucao['grupo_quimico']})</div>
                        <div>
                           {' '.join([f'<span class="chem-tag">🛒 {p}</span>' for p in solucao['sugestao_produtos']])}
                        </div>
                        <div style="margin-top:5px; font-size:0.85rem; color:#fbbf24; font-style:italic;">👉 {solucao['observacao']}</div>
                    </div>
                    """, unsafe_allow_html=True)
