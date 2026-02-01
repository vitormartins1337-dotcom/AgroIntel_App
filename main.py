# ARQUIVO: main.py
# PROJETO: AGRO SDI (Sistema de Decisão Integrada)
# VERSÃO: V17 (Visual Enterprise Premium + Blindagem de Erros)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# ==============================================================================
# 1. MOTOR DE INICIALIZAÇÃO E BLINDAGEM
# ==============================================================================
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("🚨 ERRO DE SISTEMA: Motores (data_engine/calc_engine) offline.")
    st.stop()

# Configuração da Página (Aba do Navegador)
st.set_page_config(
    page_title="Agro SDI | Enterprise", 
    page_icon="🛰️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. DESIGN SYSTEM "AGRO SDI" (CSS AVANÇADO)
# ==============================================================================
def load_css():
    st.markdown("""
    <style>
    /* IMPORTAÇÃO DE FONTES PREMIUM (Google Fonts) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Montserrat:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #f0f2f5; /* Cinza Executivo */
        color: #1d1d1f;
    }

    /* --- HERO HEADER: IDENTIDADE VISUAL AGRO SDI --- */
    .hero-container {
        position: relative;
        /* Fundo Gradiente Tecnológico (Dark Navy -> Deep Forest) */
        background: linear-gradient(120deg, #0f172a 0%, #14532d 100%);
        border-radius: 16px;
        padding: 50px 40px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
        color: white;
        overflow: hidden;
    }
    
    /* Elemento decorativo de fundo (Círculo sutil) */
    .hero-container::after {
        content: "";
        position: absolute;
        top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(74, 222, 128, 0.15) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%;
    }

    /* LOGOMARCA CSS (AGRO SDI) */
    .brand-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 3.8rem;
        font-weight: 900; /* Extra Bold */
        letter-spacing: -2px;
        line-height: 1;
        margin: 0;
        text-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .brand-accent {
        color: #4ade80; /* Verde Neon Tech */
    }

    .brand-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.1rem;
        font-weight: 400;
        color: #bbf7d0;
        letter-spacing: 4px; /* Espaçamento Premium */
        text-transform: uppercase;
        margin-top: 10px;
        margin-bottom: 5px;
        border-left: 3px solid #4ade80;
        padding-left: 15px;
    }
    
    .hero-badge {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(74, 222, 128, 0.4);
        color: #fff;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 15px;
        backdrop-filter: blur(5px);
    }

    /* --- CONTAINERS E CARDS --- */
    .filter-card {
        background: white; 
        border-radius: 12px; 
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06); 
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }
    
    /* --- ABAS (TABS) REESTILIZADAS --- */
    button[data-baseweb="tab"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 16px !important; 
        font-weight: 600 !important;
        padding: 16px 24px !important;
        background-color: transparent !important;
        border: none !important;
        color: #64748b !important;
        transition: all 0.3s ease;
    }
    button[data-baseweb="tab"]:hover {
        color: #15803d !important;
        background-color: #f0fdf4 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #15803d !important; /* Verde SDI */
        border-bottom: 3px solid #15803d !important;
        background-color: white !important;
    }

    /* --- KPI COCKPIT (PAINEL INTELIGENTE) --- */
    .kpi-container { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 10px; }
    
    .kpi-card {
        flex: 1; min-width: 210px; background: white; border-radius: 14px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04); 
        border: 1px solid #f1f5f9;
        overflow: hidden; 
        transition: transform 0.2s, box-shadow 0.2s;
        display: flex; flex-direction: column;
    }
    .kpi-card:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); }
    
    .kpi-header { 
        font-size: 0.8rem; font-weight: 700; color: #94a3b8; 
        letter-spacing: 1.2px; text-transform: uppercase; 
        padding: 18px 20px 5px 20px;
    }
    .kpi-body { padding: 0 20px 15px 20px; flex-grow: 1; }
    .kpi-value { font-family: 'Montserrat', sans-serif; font-size: 2.4rem; font-weight: 800; color: #0f172a; }
    .kpi-unit { font-size: 1rem; color: #64748b; font-weight: 500; margin-left: 4px; }
    .kpi-footer { padding: 12px 20px; color: white; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.5px; }

    /* TAGS DE QUÍMICA */
    .chem-tag {
        display: inline-block; padding: 4px 10px; border-radius: 20px; 
        font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
load_css()

# ==============================================================================
# 3. SETUP DE DADOS
# ==============================================================================
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# ==============================================================================
# 4. TELA DE LOGIN (BRANDED)
# ==============================================================================
if not url_w:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        # Card de Login Profissional
        st.markdown("""
        <div style="background:white; padding:50px; border-radius:24px; box-shadow:0 20px 50px rgba(0,0,0,0.08); text-align:center; border:1px solid #f0f0f0;">
            <div style="font-family:'Montserrat'; font-weight:900; font-size:2.5rem; color:#0f172a; line-height:1;">
                AGRO <span style="color:#15803d;">SDI</span>
            </div>
            <p style="color:#64748b; font-size:0.9rem; letter-spacing:2px; text-transform:uppercase; margin-top:5px;">Sistema de Decisão Integrada</p>
            <hr style="margin: 25px 0; border:0; border-top:1px solid #f0f0f0;">
            <p style="color:#94a3b8; font-size:0.9rem; margin-bottom:20px;">Ambiente Seguro | Acesso Corporativo</p>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        kw = st.text_input("CHAVE METEOROLÓGICA (API)", type="password")
        kg = st.text_input("CHAVE INTELIGÊNCIA ARTIFICIAL (API)", type="password")
        
        if st.button("AUTENTICAR NO SISTEMA", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# ==============================================================================
# 5. HEADER (HERO SECTION - AGRO SDI)
# ==============================================================================
# Aqui está a nova logomarca profissional criada via CSS
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">PLATAFORMA ENTERPRISE v3.0</div>
    <h1 class="brand-title">AGRO <span class="brand-accent">SDI</span></h1>
    <div class="brand-subtitle">SISTEMA DE DECISÃO INTEGRADA</div>
    <p style="opacity:0.8; font-weight:300; margin-top:15px; max-width:600px;">
        Monitoramento climático de precisão, inteligência artificial generativa e protocolos agronômicos de alta performance em uma única interface.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. FILTROS GLOBAIS (BARRA DE CONTROLE)
# ==============================================================================
st.markdown('<div class="filter-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])

with c1:
    st.markdown("### 📍 Unidade Produtiva")
    city = st.text_input("Local", label_visibility="collapsed", placeholder="Buscar Fazenda ou Município...")
    if st.button("🔄 Sincronizar Satélite") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: 
            st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon
            st.rerun()

with c2:
    st.markdown("### 🚜 Cultura e Genética")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())), label_visibility="collapsed")
        try:
            vars_disponiveis = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
            fases_disponiveis = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
            var_sel = st.selectbox("Variedade", vars_disponiveis)
        except: st.stop()
    else: st.stop()

with c3:
    st.markdown("### 📊 Estádio Fenológico")
    fase_sel = st.selectbox("Fase", fases_disponiveis, label_visibility="collapsed")

with c4:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Plantio", st.session_state['d_plantio'], label_visibility="collapsed")
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<div style='text-align:center; font-size:1.8rem; font-weight:800; color:#15803d; line-height:1;'>{dias}</div><div style='text-align:center; font-size:0.7rem; color:#64748b; font-weight:600; text-transform:uppercase;'>Dias (DAE)</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. PROCESSAMENTO LÓGICO & COCKPIT INTELIGENTE
# ==============================================================================
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # --- LÓGICA DE CORES (TRAFFIC LIGHT SYSTEM) ---
    # Temperatura
    temp = hoje['Temp']
    if temp < 18: s_t, c_t = "Baixa ❄️", "#3b82f6" # Azul
    elif 18 <= temp <= 32: s_t, c_t = "Ótima ✅", "#22c55e" # Verde
    else: s_t, c_t = "Crítica 🔥", "#ef4444" # Vermelho

    # Delta T (Segurança na Aplicação)
    delta_t = hoje['Delta T']
    if 2 <= delta_t <= 8: s_d, c_d = "APTO ✅", "#22c55e"
    elif 8 < delta_t <= 10: s_d, c_d = "Atenção ⚠️", "#f59e0b" # Laranja
    else: s_d, c_d = "NÃO APLICAR 🛑", "#ef4444"

    # Umidade
    umid = hoje['Umid']
    if 40 <= umid <= 80: s_u, c_u = "Ideal ✅", "#22c55e"
    else: s_u, c_u = "Alerta ⚠️", "#f59e0b"

    # --- RENDERIZAÇÃO DO COCKPIT (HTML) ---
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-header">🌡️ Temperatura</div>
            <div class="kpi-body"><span class="kpi-value">{temp:.1f}</span><span class="kpi-unit">°C</span></div>
            <div class="kpi-footer" style="background:{c_t}">{s_t}</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-header">💧 Umidade Ar</div>
            <div class="kpi-body"><span class="kpi-value">{umid}</span><span class="kpi-unit">%</span></div>
            <div class="kpi-footer" style="background:{c_u}">{s_u}</div>
        </div>
        
        <div class="kpi-card" style="border: 2px solid {c_d}">
            <div class="kpi-header" style="color:{c_d}">🛡️ Delta T (Aplicação)</div>
            <div class="kpi-body"><span class="kpi-value" style="color:{c_d}">{delta_t}</span><span class="kpi-unit">°C</span></div>
            <div class="kpi-footer" style="background:{c_d}">{s_d}</div>
        </div>
        
        <div class="kpi-card">
            <div class="kpi-header">☀️ GDA Acumulado</div>
            <div class="kpi-body"><span class="kpi-value">{gda_acum:.0f}</span><span class="kpi-unit">°GD</span></div>
            <div class="kpi-footer" style="background:#334155">Meta: {info.get('gda_meta', 1500)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # 8. ABAS DE CONTEÚDO (ENTERPRISE CONTENT)
    # ==============================================================================
    tabs = st.tabs(["TÉCNICO 🧬", "CLIMA ☁️", "RADAR 📡", "IA VISION 👁️", "CUSTOS 💰", "MAPA 🗺️", "LAUDO 📄"])

    # --- ABA 1: TÉCNICO E MANEJO ---
    with tabs[0]: 
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown(f"**Evolução do Ciclo Produtivo:** {progresso*100:.1f}%")
        st.progress(progresso)
        
        # --- CORREÇÃO DA IMAGEM (BLINDAGEM CONTRA ERROS) ---
        if "Soja" in str(cult_sel):
            try:
                # Layout de colunas para imagem não ficar gigante
                ci1, ci2 = st.columns([1, 3])
                with ci1:
                    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Soybean.jpg/800px-Soybean.jpg", use_container_width=True, caption="Estádio Fenológico")
            except Exception:
                st.info("ℹ️ Imagem de referência indisponível.")

        # --- CONTEÚDO TÉCNICO (PADRÃO OURO) ---
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("🧬 Perfil Genético (Expandir)", expanded=True):
                # Usa 'info' ou chaves alternativas para evitar "None"
                info_texto = info.get('info') or info.get('desc') or "Dados não disponíveis."
                st.info(f"**{var_sel}**\n\n{info_texto}")
        with col2:
            with st.expander("🌱 Fisiologia da Planta (Expandir)", expanded=True):
                fisio_texto = dados_fase.get('fisiologia') or "Dados não disponíveis."
                st.write(fisio_texto)
        
        st.markdown("---")
        st.subheader("🛡️ Protocolo de Manejo Integrado")
        st.markdown(f"**Diretriz:** {dados_fase.get('manejo', 'Consulte o Responsável Técnico.')}")
        
        # --- CARDS DE QUÍMICA (DESIGN MELHORADO) ---
        if isinstance(dados_fase.get('quimica'), list):
            for q in dados_fase['quimica']:
                tipo = q.get('Tipo', 'Geral')
                # Cores baseadas no tipo
                if "Químico" in tipo: cor, bg_icon, icon = "#ef4444", "#fee2e2", "☠️"
                elif "Biológico" in tipo: cor, bg_icon, icon = "#22c55e", "#dcfce7", "🦠"
                else: cor, bg_icon, icon = "#3b82f6", "#dbeafe", "🧪"
                
                # Tratamento de dados ausentes
                alvo = q.get('Alvo') or "Alvo não especificado"
                ativo = q.get('Ativo') or "Consultar bula"
                estrategia = q.get('Estrategia') or q.get('Obs') or "Sem observações adicionais"

                st.markdown(f"""
                <div style="background:white; border-left:4px solid {cor}; padding:15px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.05); margin-bottom:12px; display:flex; align-items:flex-start; gap:15px;">
                    <div style="background:{bg_icon}; padding:10px; border-radius:50%; font-size:1.5rem;">{icon}</div>
                    <div style="flex-grow:1;">
                        <div style="font-weight:bold; font-size:1.05rem; color:#1e293b; display:flex; justify-content:space-between;">
                            {alvo} 
                            <span class="chem-tag" style="background:{cor}; color:white;">{tipo}</span>
                        </div>
                        <div style="color:#475569; margin-top:5px; font-size:0.95rem;">
                            <b>Ingrediente Ativo:</b> {ativo}
                        </div>
                        <div style="color:#334155; font-size:0.9rem; margin-top:8px; background:#f8fafc; padding:8px; border-radius:6px; border:1px dashed #cbd5e1;">
                            💡 <b>Estratégia:</b> {estrategia}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum produto cadastrado para esta etapa.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA 2: CLIMA ---
    with tabs[1]:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Evapotranspiração (mm)', line=dict(color='#ef4444', width=3)))
        fig.update_layout(title="Balanço Hídrico (15 Dias)", template="plotly_white", height=380, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA 3: RADAR ---
    with tabs[2]:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown("### 📡 Simulação de Radar Meteorológico")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                with cols[i]:
                    bg = "#fef2f2" if r['Chuva'] == "Sim" else "#f0fdf4"
                    txt = "#b91c1c" if r['Chuva'] == "Sim" else "#15803d"
                    st.markdown(f"""
                    <div style="background:{bg}; padding:20px; border-radius:12px; text-align:center; border:1px solid {txt}20;">
                        <div style="font-weight:bold; color:#64748b; font-size:0.8rem; text-transform:uppercase;">{r["Direcao"]}</div>
                        <div style="font-size:2.2rem; font-weight:800; color:{txt}; margin:10px 0;">{r["Temp"]:.0f}°</div>
                        <div style="font-size:0.9rem; font-weight:700; color:{txt};">{r["Chuva"]}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA 4: IA VISION ---
    with tabs[3]:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c_ia1, c_ia2 = st.columns([1, 1])
        with c_ia1: 
            st.markdown("### 📸 Diagnóstico Visual")
            img = st.camera_input("Tirar foto da folha/fruto")
        with c_ia2:
            st.markdown("### 🧠 Análise Gemini AI")
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("Processando imagem com Inteligência Artificial..."):
                    try:
                        prompt = f"Atue como um Engenheiro Agrônomo Sênior. Cultura: {cult_sel}, Fase: {fase_sel}. Identifique a praga, doença ou deficiência nutricional na imagem. Seja técnico, direto e sugira ingredientes ativos para controle."
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content([prompt, Image.open(img)])
                        st.success("Diagnóstico Concluído")
                        st.markdown(response.text)
                    except Exception as e: st.error(f"Erro na conexão com IA: {e}")
            else:
                st.info("Aguardando imagem para análise...")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA 5: CUSTOS ---
    with tabs[4]:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown("### 💰 Gestão de Custos da Safra")
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Descrição do Insumo/Serviço")
        v = c2.number_input("Valor (R$)", min_value=0.0)
        if c3.button("➕ Lançar Despesa") and i: 
            st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v})
            st.rerun()
            
        if st.session_state['custos']:
            df_c = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df_c, use_container_width=True, hide_index=True)
            total = df_c['Valor'].sum()
            st.markdown(f"""
            <div style="background:#f8fafc; padding:20px; border-radius:10px; text-align:right; border:1px solid #e2e8f0;">
                <span style="color:#64748b; font-size:1.1rem; margin-right:10px;">Custo Total Acumulado:</span>
                <span style="color:#dc2626; font-size:2rem; font-weight:800;">R$ {total:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA 6: MAPA ---
    with tabs[5]:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            st.markdown("### 📍 Pontos de Interesse")
            nm = st.text_input("Nome do Talhão/Ponto")
            if st.button("Gravar Coordenada GPS") and st.session_state.get('last_click'): 
                st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]})
                st.rerun()
            
            st.markdown("---")
            for p in st.session_state['pontos_mapa']: 
                st.markdown(f"**📍 {p['nome']}**")
                st.caption(f"{p['lat']:.4f}, {p['lon']:.4f}")
                
        with c2:
            m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=16)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            
            # Adiciona marcadores salvos
            for p in st.session_state['pontos_mapa']:
                folium.Marker([p['lat'], p['lon']], popup=p['nome'], icon=folium.Icon(color='green', icon='leaf')).add_to(m)

            out = st_folium(m, height=550, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last_click'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABA 7: LAUDO ---
    with tabs[6]:
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.subheader("📝 Emissão de Receituário Agronômico")
        obs = st.text_area("Observações Técnicas Adicionais")
        
        if st.button("🖨️ Gerar PDF para Impressão"):
            st.success("Documento gerado com sucesso.")
            # Template de Laudo Profissional
            st.markdown(f"""
            <div style="border:1px solid #94a3b8; padding:40px; background:white; font-family:'Times New Roman', serif; color:black;">
                <div style="text-align:center; border-bottom:2px solid black; padding-bottom:10px; margin-bottom:20px;">
                    <h2 style="margin:0;">AGRO SDI - RECEITUÁRIO AGRONÔMICO</h2>
                    <p style="margin:0;">Sistema de Decisão Integrada | Emissão Digital</p>
                </div>
                
                <p><b>DATA:</b> {date.today().strftime('%d/%m/%Y')} &nbsp;&nbsp;&nbsp; <b>LOCAL:</b> {city or 'Não Informado'}</p>
                
                <h4 style="background:#f1f5f9; padding:5px;">1. IDENTIFICAÇÃO DA CULTURA</h4>
                <p><b>Espécie:</b> {cult_sel} &nbsp;&nbsp; <b>Genética:</b> {var_sel}</p>
                <p><b>Estádio Fenológico Atual:</b> {fase_sel}</p>
                
                <h4 style="background:#f1f5f9; padding:5px;">2. DIAGNÓSTICO DE CAMPO</h4>
                <p>{dados_fase.get('desc')}</p>
                <p><i>Fisiologia: {dados_fase.get('fisiologia')}</i></p>
                
                <h4 style="background:#f1f5f9; padding:5px;">3. PRESCRIÇÃO TÉCNICA E MANEJO</h4>
                <p>{dados_fase.get('manejo')}</p>
                
                <h4 style="background:#f1f5f9; padding:5px;">4. OBSERVAÇÕES E RECOMENDAÇÕES COMPLEMENTARES</h4>
                <p>{obs}</p>
                
                <br><br><br>
                <div style="display:flex; justify-content:space-between; margin-top:50px;">
                    <div style="text-align:center;">
                        _______________________________________<br>
                        <b>Assinatura do Produtor</b>
                    </div>
                    <div style="text-align:center;">
                        _______________________________________<br>
                        <b>Engenheiro Agrônomo Responsável</b><br>
                        CREA: 000000/XX
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
