# ARQUIVO: main.py
import streamlit as st
from core_logic import AgroEngine

# Inicializa o Motor
engine = AgroEngine()

st.set_page_config(page_title="AgroPocket Pro", page_icon="📱", layout="centered") # Layout Centered imita celular

# CSS para imitar App Nativo
st.markdown("""
    <style>
    .stApp { background-color: #f1f5f9; }
    .css-1d391kg { padding-top: 2rem; }
    .card-problema {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #059669;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .titulo-ativo {
        font-size: 0.9rem;
        font-weight: bold;
        color: #1e293b;
    }
    .tag-produto {
        background: #e0f2fe;
        color: #0284c7;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #bae6fd;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO DO APP ---
st.title("🛡️ AgroPocket")
st.caption("Consultoria Fitossanitária Offline")

# 1. SELEÇÃO DE CULTURA
culturas = engine.listar_culturas()
cultura_sel = st.selectbox("Selecione a Cultura:", culturas)

if cultura_sel:
    # 2. MENU DE NAVEGAÇÃO (FUNDO DO APP)
    # Em app nativo, isso seria uma BottomBar. Aqui usamos Tabs.
    tab_fases, tab_pragas, tab_doencas = st.tabs(["🌱 Fases", "🐛 Pragas", "🍄 Doenças"])

    # --- ABA FASES ---
    with tab_fases:
        st.subheader(f"Fenologia: {cultura_sel}")
        fases = engine.get_fases(cultura_sel)
        for sigla, desc in fases.items():
            st.markdown(f"**{sigla}** - {desc}")
            st.divider()

    # --- ABA PRAGAS (O CORAÇÃO DO APP) ---
    with tab_pragas:
        st.subheader("Identificação & Controle")
        busca = st.text_input("🔍 Buscar Praga (Ex: Percevejo)", placeholder="Digite o nome...")
        
        resultados = engine.buscar_problema(cultura_sel, busca, "Pragas")
        
        if not resultados:
            st.warning("Nenhuma praga encontrada.")
        
        for nome, dados in resultados.items():
            with st.expander(f"🔴 {nome}"):
                # FICHA TÉCNICA
                st.markdown(f"**Nome Científico:** *{dados['nome_cientifico']}*")
                st.markdown(f"**Nível de Dano:** {dados['nivel_dano']}")
                st.info(f"🔎 **Identificação:** {dados['identificacao_campo']}")
                
                st.markdown("---")
                st.markdown("#### 🧪 Soluções Químicas")
                
                for solucao in dados['manejo_quimico']:
                    st.markdown(f"""
                    <div class="card-problema">
                        <div class="titulo-ativo">{solucao['ativo']}</div>
                        <div style="font-size:0.8rem; color:#64748b; margin-bottom:5px;">
                            Grupo: {solucao['grupo_quimico']}
                        </div>
                        <div>
                            {' '.join([f'<span class="tag-produto">{p}</span>' for p in solucao['sugestao_produtos']])}
                        </div>
                        <div style="margin-top:8px; font-size:0.85rem; font-style:italic; color:#334155;">
                            ⚠️ {solucao['observacao']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # --- ABA DOENÇAS ---
    with tab_doencas:
        st.subheader("Diagnóstico & Fungicidas")
        # Mesma lógica, mas para doenças
        resultados_d = engine.buscar_problema(cultura_sel, None, "Doencas")
        
        for nome, dados in resultados_d.items():
            with st.expander(f"🟠 {nome}"):
                 st.markdown(f"**Nome Científico:** *{dados['nome_cientifico']}*")
                 st.warning(f"⚠️ **Fases Críticas:** {', '.join(dados['fases_criticas'])}")
                 st.markdown(f"**Sintomas:** {dados['sintomas']}")
                 
                 st.markdown("---")
                 st.markdown("#### 🧪 Controle Recomendado")
                 
                 for solucao in dados['manejo_quimico']:
                    st.markdown(f"""
                    <div class="card-problema" style="border-left-color: #ea580c;">
                        <div class="titulo-ativo">{solucao['ativo']}</div>
                        <div style="font-size:0.8rem; color:#64748b;">
                            Mec: {solucao['mecanismo']}
                        </div>
                        <div style="margin-top:5px;">
                            {' '.join([f'<span class="tag-produto">{p}</span>' for p in solucao['sugestao_produtos']])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
