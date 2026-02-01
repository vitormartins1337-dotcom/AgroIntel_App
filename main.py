# ARQUIVO: main.py
# VERSÃO: V15 (Design System Agro-Tech Premium - Visual John Deere/FieldView)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# --- 1. IMPORTAÇÃO SEGURA DOS MOTORES ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("🚨 ERRO CRÍTICO: Motores não encontrados.")
    st.stop()

# --- 2. CONFIGURAÇÃO DA PÁGINA & CSS AVANÇADO ---
st.set_page_config(page_title="Agro Intel Enterprise", page_icon="🌱", layout="wide")

def load_css():
    st.markdown("""
    <style>
    /* IMPORTANDO FONTE PREMIUM (INTER) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #f4f7f6; /* Cinza Gelo Profissional */
        color: #1d1d1f;
    }

    /* --- HERO HEADER COM IMAGEM DE FUNDO --- */
    .hero-container {
        position: relative;
        background-image: linear-gradient(to right, rgba(0, 30, 0, 0.85), rgba(0, 50, 20, 0.7)), 
                          url('https://images.unsplash.com/photo-1625246333195-5819623c7a11?q=80&w=1000&auto=format&fit=crop'); 
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 60px 40px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
        text-align: left; /* Alinhado a esquerda como softwares Enterprise */
    }
    
    .hero-title {
        font-size: 3.5rem; /* Letra Grande */
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        font-weight: 300;
        color: #e0e0e0;
        margin-top: 10px;
        max-width: 600px;
    }
    
    .hero-badge {
        background-color: #00e676; /* Verde Neon Tech */
        color: #003300;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        display: inline-block;
    }

    /* --- CARDS E FILTROS --- */
    .filter-card {
        background: white; 
        border-radius: 12px; 
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); 
        border: 1px solid #edf2f7;
        margin-bottom: 25px;
    }
    
    /* TITULOS DAS SEÇÕES */
    h3 { font-weight: 700 !important; color: #2d3748 !important; font-size: 1.1rem !important; }

    /* --- ABAS GRANDES E MODERNAS --- */
    button[data-baseweb="tab"] {
        font-size: 16px !important; 
        font-weight: 600 !important;
        padding: 15px 30px !important;
        background-color: transparent !important;
        border: none !important;
        color: #718096 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #10a37f !important; /* Verde OpenAI/Agro */
        border-bottom: 3px solid #10a37f !important;
        background-color: rgba(16, 163, 127, 0.05) !important;
    }

    /* --- KPI CARDS (COCKPIT) --- */
    .kpi-container { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 10px; }
    .kpi-card {
        flex: 1; min-width: 200px; background: white; border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;
        overflow: hidden; transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    
    .kpi-header { 
        font-size: 0.85rem; font-weight: 700; color: #a0aec0; letter-spacing: 1px; text-transform: uppercase; 
        padding: 15px 20px 5px 20px;
    }
    .kpi-body { padding: 0 20px 15px 20px; }
    .kpi-value { font-size: 2.5rem; font-weight: 800; color: #1a202c; }
    .kpi-unit { font-size: 1rem; color: #718096; font-weight: 500; margin-left: 4px; }
    .kpi-footer { padding: 10px 20px; color: white; font-weight: 600; font-size: 0.9rem; }

    </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. INICIALIZAÇÃO ---
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# --- 4. TELA DE LOGIN (CLEAN) ---
if not url_w:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div style="background:white; padding:40px; border-radius:20px; box-shadow:0 10px 40px rgba(0,0,0,0.1); text-align:center;">
            <div style="font-size: 4rem;">🌱</div>
            <h2 style="margin-top:10px; color:#1a202c;">Agro Intel Enterprise</h2>
            <p style="color:#718096;">Acesso Seguro ao Sistema de Gestão</p>
        </div>
        <br>
        """, unsafe_allow_html=True)
        kw = st.text_input("🔑 Chave Meteorológica (OpenWeather)", type="password")
        kg = st.text_input("🧠 Chave Inteligência (Gemini AI)", type="password")
        if st.button("ACESSAR DASHBOARD", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# --- 5. CABEÇALHO (HERO SECTION) ---
# Aqui está a mágica da imagem de fundo e letras grandes
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">Versão Enterprise 2.0</div>
    <h1 class="hero-title">Agro Intel Cockpit</h1>
    <p class="hero-subtitle">Sistema Integrado de Apoio à Decisão Agronômica e Monitoramento Climático de Precisão.</p>
</div>
""", unsafe_allow_html=True)

# --- 6. BARRA DE FILTROS (DESIGN CARD) ---
st.markdown('<div class="filter-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])

with c1:
    st.markdown("### 📍 Unidade Produtiva")
    city = st.text_input("Local", label_visibility="collapsed", placeholder="Buscar Fazenda/Cidade...")
    if st.button("🔄 Sincronizar GPS") and city:
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
            var_sel = st.selectbox("Variedade", vars_disponiveis) # Variedade abaixo da cultura
        except: st.stop()
    else: st.stop()

with c3:
    st.markdown("### 📊 Estádio Atual")
    fase_sel = st.selectbox("Fase", fases_disponiveis, label_visibility="collapsed")

with c4:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Plantio", st.session_state['d_plantio'], label_visibility="collapsed")
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<div style='text-align:center; font-size:2rem; font-weight:800; color:#10a37f;'>{dias}</div><div style='text-align:center; font-size:0.8rem; color:#718096;'>Dias (DAE)</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 7. PROCESSAMENTO E COCKPIT ---
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # Lógica Visual (Traffic Light)
    temp = hoje['Temp']
    if temp < 18: s_t, c_t = "Baixa ❄️", "#3182ce"
    elif 18 <= temp <= 32: s_t, c_t = "Ótima ✅", "#38a169"
    else: s_t, c_t = "Crítica 🔥", "#e53e3e"

    delta_t = hoje['Delta T']
    if 2 <= delta_t <= 8: s_d, c_d = "APTO ✅", "#38a169"
    elif 8 < delta_t <= 10: s_d, c_d = "Atenção ⚠️", "#dd6b20"
    else: s_d, c_d = "NÃO APLICAR 🛑", "#e53e3e"

    umid = hoje['Umid']
    if 40 <= umid <= 80: s_u, c_u = "Ideal ✅", "#38a169"
    else: s_u, c_u = "Alerta ⚠️", "#dd6b20"

    # HTML DO COCKPIT (VISUAL FINAL)
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
            <div class="kpi-footer" style="background:#2d3748">Meta: {info.get('gda_meta', 1500)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 8. ABAS DE CONTEÚDO ---
    # Usando ícones maiores e nomes curtos para mobile
    tabs = st.tabs(["TÉCNICO 🧬", "CLIMA ☁️", "RADAR 📡", "IA VISION 👁️", "CUSTOS 💰", "MAPA 🗺️", "LAUDO 📄"])

    with tabs[0]: # TÉCNICO
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.markdown(f"**Progresso do Ciclo:** {progresso*100:.1f}%")
        st.progress(progresso)
        
        # Inserindo imagem ilustrativa da soja se estiver selecionada
        if "Soja" in cult_sel:
            # Imagem de contexto (ilustração técnica)
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Soybean.jpg/800px-Soybean.jpg", height=200, caption="Glycine max - Referência Visual")

        col1, col2 = st.columns(2)
        with col1:
            with st.expander("🧬 Perfil Genético (Expandir)", expanded=True):
                st.info(f"{var_sel}\n\n{info.get('info', '')}")
        with col2:
            with st.expander("🌱 Fisiologia (Expandir)", expanded=True):
                st.write(dados_fase.get('fisiologia', ''))
        
        st.markdown("---")
        st.subheader("🛡️ Protocolo de Manejo Integrado")
        
        # Cards Químicos melhorados
        if isinstance(dados_fase.get('quimica'), list):
            for q in dados_fase['quimica']:
                tipo = q.get('Tipo', 'Geral')
                cor = "#e53e3e" if "Químico" in tipo else "#38a169" if "Biológico" in tipo else "#3182ce"
                st.markdown(f"""
                <div style="background:white; border-left:4px solid {cor}; padding:15px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.05); margin-bottom:10px;">
                    <div style="font-weight:bold; font-size:1.1rem; color:#2d3748;">{q.get('Alvo')} <span style="font-size:0.7rem; background:{cor}; color:white; padding:3px 8px; border-radius:10px; vertical-align:middle; margin-left:10px;">{tipo}</span></div>
                    <div style="color:#4a5568; margin-top:5px;">🧪 <b>{q.get('Ativo')}</b></div>
                    <div style="color:#718096; font-size:0.9rem; margin-top:5px;">💡 {q.get('Estrategia')}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]: # CLIMA
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3182ce'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Evapo (mm)', line=dict(color='#e53e3e', width=3)))
        fig.update_layout(title="Balanço Hídrico (15 Dias)", template="plotly_white", height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]: # RADAR
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                with cols[i]:
                    bg = "#fff5f5" if r['Chuva'] == "Sim" else "#f0fff4"
                    txt = "#c53030" if r['Chuva'] == "Sim" else "#2f855a"
                    st.markdown(f"""
                    <div style="background:{bg}; padding:20px; border-radius:12px; text-align:center; border:1px solid {txt}20;">
                        <div style="font-weight:bold; color:#4a5568;">{r["Direcao"]}</div>
                        <div style="font-size:2rem; font-weight:800; color:{txt};">{r["Temp"]:.0f}°</div>
                        <div style="font-size:0.9rem; font-weight:600; color:{txt};">{r["Chuva"]}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]: # IA
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c_ia1, c_ia2 = st.columns([1, 1])
        with c_ia1: 
            img = st.camera_input("📸 Diagnóstico de Campo")
        with c_ia2:
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("🧠 IA Analisando Patógenos..."):
                    try:
                        prompt = f"Sou Agrônomo. Cultura: {cult_sel}, Fase: {fase_sel}. Identifique a praga/doença. Seja técnico e direto."
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content([prompt, Image.open(img)])
                        st.success("Diagnóstico Concluído")
                        st.markdown(response.text)
                    except: st.error("Erro na conexão com IA.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]: # CUSTOS
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Descrição")
        v = c2.number_input("Valor (R$)", min_value=0.0)
        if c3.button("➕ Lançar") and i: 
            st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v})
            st.rerun()
        if st.session_state['custos']:
            df_c = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df_c, use_container_width=True, hide_index=True)
            st.metric("Custo Total", f"R$ {df_c['Valor'].sum():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[5]: # MAPA
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Ponto de Interesse")
            if st.button("📍 Gravar GPS") and st.session_state.get('last_click'): 
                st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]})
                st.rerun()
            for p in st.session_state['pontos_mapa']: st.markdown(f"**📍 {p['nome']}**")
        with c2:
            m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=16)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            out = st_folium(m, height=500, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last_click'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[6]: # LAUDO
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.subheader("📝 Emissão de Receituário")
        obs = st.text_area("Observações Adicionais")
        if st.button("🖨️ Gerar PDF"):
            st.success("Documento gerado.")
            st.markdown(f"""
            <div style="border:1px solid #ddd; padding:20px; background:white;">
                <h3>LAUDO TÉCNICO - {date.today()}</h3>
                <p><b>Cultura:</b> {cult_sel} ({var_sel})</p>
                <p><b>Diagnóstico:</b> {dados_fase.get('desc')}</p>
                <p><b>Prescrição:</b> {dados_fase.get('manejo')}</p>
                <hr>
                <p><b>Nota:</b> {obs}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
