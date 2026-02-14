# ARQUIVO: main.py
# AGRO SDI | VERSÃO COM MONITORAMENTO MIP (NÍVEL DE DANO ECONÔMICO)
import streamlit as st
from core_logic import AgroEngine 

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Agro SDI", page_icon="🌱", layout="wide")
engine = AgroEngine()

# --- 2. CSS PROFISSIONAL ---
def load_css():
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem !important; padding-bottom: 3rem !important; }
        .stApp { background-color: #0b120d; color: #e2e8f0; }
        [data-testid="stSidebar"] { background-color: #111e16; border-right: 1px solid #1e3a2f; }

        /* HEADER & TICKER */
        .ticker-container {
            width: 100%; background-color: #020403; border: 1px solid #15803d; border-radius: 20px;
            overflow: hidden; white-space: nowrap; height: 36px; display: flex; align-items: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.4); margin-bottom: 25px; margin-top: 5px;
        }
        .ticker-text { display: inline-block; animation: ticker 35s linear infinite; font-family: 'Courier New', monospace; font-size: 0.9rem; font-weight: bold; }
        @keyframes ticker { 0% { transform: translate3d(100%, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
        .tick-item { margin-right: 40px; color: #cbd5e1; letter-spacing: 0.5px; }
        .up { color: #4ade80; } .down { color: #f87171; }

        .header-box {
            background: linear-gradient(180deg, #14281d 0%, #0b120d 100%);
            border: 1px solid #1e3a2f; border-radius: 12px; padding: 30px 40px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5); margin-bottom: 10px;
        }

        /* CARDS DE MONITORAMENTO (NOVO) */
        .mip-card {
            background-color: #1a2e24; border: 1px solid #1e3a2f; padding: 20px;
            border-radius: 10px; text-align: center; margin-bottom: 10px;
        }
        .mip-value { font-size: 2.5rem; font-weight: 900; color: #fff; }
        .mip-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
        
        .veredito-box {
            padding: 20px; border-radius: 8px; text-align: center; margin-top: 20px; border: 2px solid;
        }
        .veredito-titulo { font-size: 1.5rem; font-weight: 900; letter-spacing: -1px; margin-bottom: 5px; }
        .veredito-desc { font-size: 1rem; opacity: 0.9; }

        /* INPUTS & TABS */
        .stSelectbox div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {
            background-color: #060a07 !important; color: #ecfdf5 !important; border: 1px solid #15803d !important;
        }
        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #111e16; border: 1px solid #1e3a2f; color: #6ee7b7; padding: 10px 20px; font-size: 0.9rem;
        }
        .stTabs [aria-selected="true"] { background-color: #15803d !important; color: #fff !important; font-weight: bold; }
        
        /* CARDS GERAIS */
        .info-box {
            background-color: #16241b; border-left: 4px solid #22c55e;
            padding: 15px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #1e3a2f;
        }
        .plantio-card {
            background-color: #0f172a; border: 1px solid #1e293b; padding: 20px;
            border-radius: 8px; margin-bottom: 15px;
        }
        .plantio-title { color: #38bdf8; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;}
        .plantio-item { margin-bottom: 8px; font-size: 0.9rem; color: #cbd5e1; }
        .plantio-label { color: #94a3b8; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
        </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. HEADER ---
st.markdown("""
<div class="header-box">
    <div>
        <h1 style="margin:0; font-family:'Arial', sans-serif; font-weight:900; font-size:3.5rem; letter-spacing:-2px; color:#fff; line-height: 1;">
            AGRO <span style="color:#22c55e;">SDI</span>
        </h1>
        <div style="font-size:1rem; letter-spacing:4px; color:#86efac; margin-top:8px; font-weight:600; opacity:0.9;">
            SISTEMA DE DECISÃO INTEGRADA
        </div>
    </div>
    <div style="background:rgba(22,163,74,0.2); border:1px solid #22c55e; color:#4ade80; padding:6px 16px; border-radius:30px; font-size:0.85rem; display:flex; align-items:center; gap:10px; font-weight:bold;">
        <div style="width:10px; height:10px; background:#22c55e; border-radius:50%; box-shadow:0 0 10px #22c55e;"></div> ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

ticker_html = """
<div class="ticker-container">
    <div class="ticker-text">
        <span class="tick-item">USD/BRL <span class="up">R$ 5.72 ▲</span></span>
        <span class="tick-item">SOJA (CBOT) <span class="down">US$ 12.10 ▼</span></span>
        <span class="tick-item">MILHO (B3) <span class="up">R$ 58.40 ▲</span></span>
        <span class="tick-item">BOI GORDO <span class="up">R$ 245.00 ▲</span></span>
        <span class="tick-item">UREIA <span class="down">US$ 380.00 ▼</span></span>
    </div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# ==============================================================================
# 🧠 CÉREBRO
# ==============================================================================

culturas = engine.listar_culturas()
cultura_sel = st.selectbox("🚜 SELECIONE A CULTURA:", culturas)

if cultura_sel:
    st.markdown("---")
    # ADICIONEI A QUARTA ABA "🔍 MONITORAMENTO (MIP)"
    tab_fases, tab_sanidade, tab_solo, tab_mip = st.tabs(["🌱 FASES & MANEJO", "🛡️ SANIDADE", "🚜 SOLO & PLANTIO", "🔍 MONITORAMENTO (MIP)"])

    # --- ABA 1: FENOLOGIA ---
    with tab_fases:
        fases = engine.get_fases(cultura_sel)
        st.caption(f"Guia estratégico para {cultura_sel}.")
        for sigla, dados in fases.items():
            html_content = f"""
            <div class="info-box">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="color:#fff; font-size:1.3rem; font-weight:800;">{sigla}</span>
                    <span style="background:#064e3b; padding:3px 8px; border-radius:4px; font-size:0.7rem; color:#4ade80; border:1px solid #22c55e; font-weight:bold;">FOCO: {dados['foco'].upper()}</span>
                </div>
                <div style="color:#86efac; font-size:0.95rem; font-weight:600; margin-bottom:10px; border-bottom:1px solid #1e3a2f; padding-bottom:8px;">{dados['fase']}</div>
                <div style="color:#d1d5db; font-size:0.9rem; line-height:1.5;">{dados['visao_pratica']}</div>
                <div style="background:#2a1810; color:#fdba74; padding:10px; border-radius:4px; font-style:italic; font-size:0.85rem; border:1px solid #7c2d12; margin-top:12px;">⚠️ TÉCNICO: {dados['alerta']}</div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)

    # --- ABA 2: SANIDADE ---
    with tab_sanidade:
        c1, c2 = st.columns([1, 3])
        with c1: tipo = st.radio("Filtrar:", ["Todos", "Pragas 🐛", "Doenças 🍄"], index=0, horizontal=True)
        with c2: busca = st.text_input("Buscar:", placeholder="Digite o nome do problema...")
        st.markdown("<br>", unsafe_allow_html=True)

        lista = []
        if tipo in ["Todos", "Pragas 🐛"]:
            for k, v in engine.buscar_problema(cultura_sel, busca, "Pragas").items():
                v['nome'] = k; lista.append(v)
        if tipo in ["Todos", "Doenças 🍄"]:
            for k, v in engine.buscar_problema(cultura_sel, busca, "Doencas").items():
                v['nome'] = k; lista.append(v)

        if not lista: st.warning("Nenhum problema encontrado.")
        
        for item in lista:
            icone = "🐛" if item['tipo'] == "Praga" else "🍄"
            bg_h = "#0f172a" if item['tipo'] == "Praga" else "#2a1810"
            with st.expander(f"{icone} {item['nome']}  |  Dano: {item.get('nivel_dano', '-')}"):
                st.markdown(f"**Identificação:** {item['identificacao_campo']}")
                if 'fases_criticas' in item: st.markdown(f"**Fases:** {', '.join(item['fases_criticas'])}")
                st.markdown("#### ☠️ Controle Químico")
                for sol in item['manejo_quimico']:
                    html_q = f"""
                    <div style="background:{bg_h}; padding:10px; border-radius:6px; border:1px solid #334155; margin-bottom:8px;">
                        <div style="color:#38bdf8; font-weight:bold;">{sol['ativo']}</div>
                        <div style="font-size:0.75rem; color:#94a3b8;">{sol['grupo_quimico']} | {sol['mecanismo']}</div>
                        <div style="margin-top:5px;">{' '.join([f'<span style="background:#1e293b; color:#bae6fd; padding:2px 6px; border-radius:4px; font-size:0.75rem; border:1px solid #38bdf8; margin-right:5px;">🛒 {p}</span>' for p in sol['sugestao_produtos']])}</div>
                        <div style="margin-top:5px; font-size:0.8rem; color:#fbbf24; font-style:italic;">👉 {sol['observacao']}</div>
                    </div>"""
                    st.markdown(html_q, unsafe_allow_html=True)

    # --- ABA 3: SOLO & CORREÇÃO (AGORA É UMA FERRAMENTA DE TRABALHO) ---
    with tab_solo:
        st.markdown("### 🧪 Interpretador de Análise de Solo")
        st.caption("Digite os dados do seu laudo para obter a recomendação de correção.")

        # --- 1. DADOS DA ANÁLISE (INPUTS) ---
        with st.expander("📝 Inserir Dados da Análise (0 - 20 cm)", expanded=True):
            c_s1, c_s2, c_s3 = st.columns(3)
            argila = c_s1.number_input("Argila (%):", min_value=0.0, max_value=100.0, value=35.0)
            fosoforo = c_s2.number_input("Fósforo (mg/dm³ - Mehlich):", value=8.0)
            potassio = c_s3.number_input("Potássio (mg/dm³):", value=40.0)
            
            c_s4, c_s5, c_s6 = st.columns(3)
            calcio = c_s4.number_input("Cálcio (cmolc/dm³):", value=1.5)
            magnesio = c_s5.number_input("Magnésio (cmolc/dm³):", value=0.5)
            v_atual = c_s6.number_input("V% Atual (Saturação):", value=35.0)
            
            c_s7, c_s8 = st.columns(2)
            ctc = c_s7.number_input("CTC (cmolc/dm³):", value=8.0)
            prnt = c_s8.number_input("PRNT do Calcário (%):", value=85.0)

        # --- 2. MOTOR DE CÁLCULO E INTERPRETAÇÃO ---
        # Definição de metas por cultura (Simplificado para o MVP - Ideal é vir do Database)
        meta_v = 60 # Padrão
        if cultura_sel == "Soja": meta_v = 80
        elif cultura_sel == "Milho": meta_v = 70
        elif cultura_sel == "Algodão": meta_v = 70
        elif cultura_sel == "Arroz": meta_v = 50

        # Lógica de Interpretação (Tabela aproximada Cerrado)
        def interpretar_p(p_teor, argila_teor):
            # Nível Crítico simplificado
            nivel_critico = 15 if argila_teor < 20 else 10 if argila_teor < 40 else 6
            if p_teor < nivel_critico * 0.5: return "MUITO BAIXO", "#ef4444"
            if p_teor < nivel_critico: return "BAIXO", "#f97316"
            if p_teor < nivel_critico * 1.5: return "MÉDIO", "#eab308"
            return "ALTO", "#22c55e"

        classificacao_p, cor_p = interpretar_p(fosoforo, argila)
        
        # Cálculo de Calagem (Método Saturação por Bases)
        nc_ton = 0
        if v_atual < meta_v:
            nc_ton = ((meta_v - v_atual) * ctc) / prnt

        # Cálculo de Gessagem (Método da Argila - Viltani)
        # NG = 50 * Argila (%) ... resultado em kg/ha -> divide por 1000 para ton
        ng_ton = (50 * argila) / 1000 
        
        # --- 3. EXIBIÇÃO DOS RESULTADOS (O RELATÓRIO NA TELA) ---
        st.divider()
        st.markdown(f"#### 📊 Diagnóstico para {cultura_sel}")

        # Colunas de Resultados
        col_res1, col_res2 = st.columns(2)

        with col_res1:
            st.markdown("##### 🪨 Correção (Calagem e Gessagem)")
            
            # Card Calagem
            if nc_ton > 0:
                st.markdown(f"""
                <div style="background:#2a1810; border-left:4px solid #f97316; padding:15px; border-radius:6px; margin-bottom:10px;">
                    <div style="color:#cbd5e1; font-size:0.9rem;">NECESSIDADE DE CALCÁRIO</div>
                    <div style="color:#f97316; font-size:1.8rem; font-weight:bold;">{nc_ton:.1f} ton/ha</div>
                    <div style="color:#94a3b8; font-size:0.8rem;">Para elevar V% de {v_atual}% para {meta_v}% (PRNT {prnt}%)</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ Solo com V% adequada. Calagem não necessária.")

            # Card Gessagem
            st.markdown(f"""
            <div style="background:#1e1e24; border-left:4px solid #cbd5e1; padding:15px; border-radius:6px;">
                <div style="color:#cbd5e1; font-size:0.9rem;">RECOMENDAÇÃO DE GESSO</div>
                <div style="color:#fff; font-size:1.4rem; font-weight:bold;">{ng_ton:.1f} ton/ha</div>
                <div style="color:#94a3b8; font-size:0.8rem;">Baseado no teor de Argila ({argila}%) para condicionamento.</div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("##### 📉 Níveis de Fertilidade")
            
            # Barras de Progresso Visuais
            st.markdown(f"**Fósforo (P):** <span style='color:{cor_p}; font-weight:bold;'>{classificacao_p}</span>", unsafe_allow_html=True)
            st.progress(min(fosoforo/30, 1.0)) # Escala visual até 30mg
            
            st.markdown("**Potássio (K):**")
            k_percent = (potassio / 390) / ctc * 100 # % da CTC
            st.progress(min(k_percent/5, 1.0)) # Meta é 3% a 5% da CTC
            st.caption(f"K ocupa {k_percent:.1f}% da CTC (Ideal: 3% a 5%)")

            st.markdown("**Magnésio (Mg):**")
            mg_percent = magnesio / ctc * 100
            st.progress(min(mg_percent/15, 1.0))
            st.caption(f"Mg ocupa {mg_percent:.1f}% da CTC (Ideal: 10% a 15%)")

        # --- 4. DICAS TÉCNICAS DE APLICAÇÃO ---
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🚜 Dicas de Aplicação e Incorporação", expanded=False):
            st.markdown("""
            * **Calcário:** Aplicar 3 meses antes do plantio. Se a dose for maior que 3 ton/ha, dividir em duas aplicações (metade antes da grade, metade depois).
            * **Gesso:** Não precisa incorporar. Aplicar em cobertura após o calcário reagir. Cuidado: Gesso não corrige pH, apenas fornece Ca e S em profundidade.
            * **Fósforo:** Se o nível estiver "MUITO BAIXO", recomenda-se fazer uma fosfatagem (aplicação a lanço) para elevar o nível crítico antes de adubar no sulco.
            """)
            
            

    # --- ABA 4: MONITORAMENTO MIP (A IDEIA MATADORA) ---
    with tab_mip:
        st.markdown("### 🕵️ Monitoramento Integrado de Pragas")
        st.caption("Insira os dados da amostragem (pano de batida) para calcular o Nível de Dano Econômico.")
        
        # 1. Configuração do Cenário
        with st.expander("⚙️ Configurar Preços e Custos", expanded=True):
            c_conf1, c_conf2 = st.columns(2)
            preco_saca = c_conf1.number_input("Preço da Saca (R$):", value=120.0, step=1.0)
            custo_aplicacao = c_conf2.number_input("Custo Operacional + Produto (R$/ha):", value=85.0, step=5.0)

        st.divider()

        # 2. Contagem no Campo
        pragas_mip = engine.buscar_problema(cultura_sel, None, "Pragas")
        nomes_pragas = list(pragas_mip.keys())
        
        praga_alvo = st.selectbox("Selecione a Praga Monitorada:", nomes_pragas)
        
        if praga_alvo:
            # Pega o nível de dano do texto do DB (uma simplificação para o MVP)
            # Num app final, isso seria um número no JSON. Aqui vamos simular a lógica.
            
            c_mip1, c_mip2, c_mip3 = st.columns([1.5, 1, 1])
            
            with c_mip1:
                st.markdown(f"**Praga:** {praga_alvo}")
                st.markdown(f"<span style='font-size:0.8rem; color:#94a3b8;'>Amostragem: Pano de Batida (1 metro)</span>", unsafe_allow_html=True)
                
            with c_mip2:
                # Botões grandes de + e -
                qtd_praga = st.number_input("Contagem (Média):", min_value=0.0, step=0.5, value=0.0, format="%.1f")
            
            with c_mip3:
                # Simulação de Dano (Lógica simplificada para MVP)
                # Ex: Percevejo Soja -> 1 percevejo = 40kg/ha de perda (hipotético para demo)
                fator_dano = 0
                if "Percevejo" in praga_alvo: fator_dano = 40 # kg/ha perdidos por percevejo
                elif "Lagarta" in praga_alvo: fator_dano = 25
                elif "Bicudo" in praga_alvo: fator_dano = 100
                else: fator_dano = 15
                
                perda_kg = qtd_praga * fator_dano
                perda_sc = perda_kg / 60
                prejuizo_estimado = perda_sc * preco_saca
                
                # Veredito
                cor_veredito = "#22c55e" # Verde
                msg_veredito = "MONITORAR"
                bg_veredito = "rgba(34, 197, 94, 0.1)"
                
                if prejuizo_estimado > custo_aplicacao:
                    cor_veredito = "#ef4444" # Vermelho
                    msg_veredito = "🚨 APLICAR AGORA"
                    bg_veredito = "rgba(239, 68, 68, 0.2)"
            
            st.markdown("---")
            
            # PAINEL DE DECISÃO
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                st.markdown(f"""
                <div class="mip-card">
                    <div class="mip-value" style="color:#fbbf24;">{perda_sc:.1f} sc</div>
                    <div class="mip-label">Perda Estimada (ha)</div>
                </div>""", unsafe_allow_html=True)
                
            with col_d2:
                st.markdown(f"""
                <div class="mip-card">
                    <div class="mip-value" style="color:#ef4444;">R$ {prejuizo_estimado:.2f}</div>
                    <div class="mip-label">Prejuízo Potencial</div>
                </div>""", unsafe_allow_html=True)
                
            with col_d3:
                st.markdown(f"""
                <div class="mip-card">
                    <div class="mip-value" style="color:#94a3b8;">R$ {custo_aplicacao:.2f}</div>
                    <div class="mip-label">Custo Controle</div>
                </div>""", unsafe_allow_html=True)

            # VEREDITO FINAL
            st.markdown(f"""
            <div class="veredito-box" style="background-color:{bg_veredito}; border-color:{cor_veredito}; color:{cor_veredito};">
                <div class="veredito-titulo">{msg_veredito}</div>
                <div class="veredito-desc">O prejuízo (R$ {prejuizo_estimado:.0f}) é {'MAIOR' if prejuizo_estimado > custo_aplicacao else 'MENOR'} que o custo de controle.</div>
            </div>
            """, unsafe_allow_html=True)
