# ARQUIVO: main.py
# FUNÇÃO: Interface de Usuário (UI/UX) - Agro-Intel Enterprise
# VERSÃO: 4.0 (Titanium UI - High Contrast)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai
import io
import base64

# --- IMPORTAÇÃO DOS MOTORES ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError as e:
    st.error(f"ERRO DE IMPORTAÇÃO: {e}")
    st.stop()

# ==============================================================================
# 1. CONFIGURAÇÃO VISUAL DE ALTO NÍVEL (TITANIUM CSS)
# ==============================================================================
st.set_page_config(
    page_title="Agro-Intel Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_img_as_base64(file):
    try:
        with open(file, "rb") as f: data = f.read()
        return base64.b64encode(data).decode()
    except: return None

def load_css():
    """
    Carrega o tema 'Titanium Enterprise'.
    Foco: Contraste Máximo, Sombras Suaves e Tipografia Corporativa.
    """
    img_b64 = get_img_as_base64("fundo_agro.jpg")
    img_url = f"data:image/png;base64,{img_b64}" if img_b64 else "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=1740&auto=format&fit=crop"

    st.markdown(f"""
    <style>
    /* IMPORTAÇÃO DE FONTE 'INTER' (Padrão de Apps Modernos) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    /* FUNDO PRINCIPAL - ESCURO E IMERSIVO */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.95)), url("{img_url}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}

    /* CABEÇALHO (HEADER) - Estilo Dashboard Executivo */
    .titan-header {{
        padding: 40px 0 20px 0;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 40px;
    }}
    .titan-title {{
        color: #ffffff; 
        font-size: 3.2em; 
        font-weight: 800; 
        letter-spacing: -1.5px; 
        margin: 0;
        text-shadow: 0 4px 12px rgba(0,0,0,0.6);
    }}
    .titan-sub {{ 
        color: #94a3b8; 
        font-size: 1.1em; 
        font-weight: 400; 
        letter-spacing: 0.5px;
        margin-top: 5px;
    }}

    /* CARTÕES PROFISSIONAIS (SOLID WHITE) 
       Isso resolve o problema de leitura. O fundo é branco puro. */
    .pro-card {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 28px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2); /* Sombra elegante */
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }}
    
    /* Decoração lateral do card (Barra colorida) */
    .pro-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 6px;
        background: linear-gradient(180deg, #0288d1 0%, #1565c0 100%);
    }}

    /* TIPOGRAFIA INTERNA DOS CARDS */
    .card-title {{
        color: #0f172a; /* Azul Quase Preto */
        font-size: 1.5em; 
        font-weight: 800; 
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    .label-tech {{ 
        color: #64748b; /* Cinza Médio */
        font-size: 0.75em; 
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 0.05em;
        margin-top: 18px;
        margin-bottom: 4px;
    }}
    
    .value-tech {{ 
        color: #334155; /* Cinza Escuro */
        font-size: 1.1em; 
        line-height: 1.6; 
        font-weight: 400;
        text-align: justify;
    }}

    /* LISTAS QUÍMICAS ESTILIZADAS */
    ul.chem-list {{ list-style: none; padding: 0; margin: 0; }}
    li.chem-item {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 12px;
        margin-bottom: 8px;
        border-radius: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s;
    }}
    li.chem-item:hover {{ transform: translateX(5px); border-color: #cbd5e1; }}
    .chem-name {{ font-weight: 700; color: #1e293b; font-size: 0.95em; }}
    .chem-tag {{ background: #e0f2fe; color: #0284c7; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; font-weight: 700; }}

    /* ALERTAS MODERNOS */
    .alert-box {{ 
        padding: 16px; 
        border-radius: 8px; 
        font-weight: 600; 
        margin-bottom: 20px; 
        display: flex; 
        align-items: flex-start; 
        gap: 12px;
        font-size: 0.95em;
        line-height: 1.5;
    }}
    .alert-red {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fca5a5; }}
    .alert-green {{ background: #f0fdf4; color: #15803d; border: 1px solid #86efac; }}

    /* ESTILIZAÇÃO DOS KPI (METRICS) DO STREAMLIT */
    div[data-testid="metric-container"] {{
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }}
    div[data-testid="metric-container"]:hover {{
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }}
    label[data-testid="stMetricLabel"] {{
        color: #64748b !important;
        font-size: 0.9em !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: #0f172a !important;
        font-size: 1.8em !important;
        font-weight: 800 !important;
    }}

    /* BOTÕES */
    .stButton button {{
        font-weight: 600;
        border-radius: 6px;
        height: 45px;
    }}
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==============================================================================
# 2. LÓGICA DE DADOS
# ==============================================================================
BANCO_MASTER = get_database()

if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# ==============================================================================
# 3. TELA DE LOGIN (LOCK SCREEN)
# ==============================================================================
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="pro-card" style="text-align:center; padding: 40px;">
            <h2 style="color:#0f172a; margin-bottom:10px;">🔒 Acesso Seguro</h2>
            <p style="color:#64748b; margin-bottom:30px;">Agro-Intel Enterprise System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Inputs fora do card HTML para funcionarem
        kw = st.text_input("Chave API OpenWeather", type="password")
        kg = st.text_input("Chave API Gemini AI", type="password")
        
        if st.button("ACESSAR PAINEL", type="primary", use_container_width=True):
            if kw and kg:
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
            else:
                st.error("Credenciais incompletas.")
    st.stop()

# ==============================================================================
# 4. DASHBOARD (LAYOUT PRINCIPAL)
# ==============================================================================
st.markdown("""
<div class="titan-header">
    <h1 class="titan-title">AGRO-INTEL</h1>
    <div class="titan-sub">Enterprise Decision Support System v4.0</div>
</div>
""", unsafe_allow_html=True)

# Painel de Controle (Branco e Limpo)
st.markdown('<div class="pro-card" style="padding: 20px;">', unsafe_allow_html=True)
c_loc, c_cult, c_date = st.columns([1.5, 1.5, 1])

with c_loc:
    st.markdown("<span style='color:#0288d1; font-weight:bold;'>📍 LOCALIZAÇÃO</span>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Cidade", "GPS"])
    with t1:
        city = st.text_input("Busca:", placeholder="Ex: Patos de Minas, MG", label_visibility="collapsed")
        if st.button("🔍 Buscar") and city:
            lat, lon = WeatherConn.get_coords(city, url_w)
            if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
    with t2:
        st.code(f"{st.session_state['loc_lat']:.4f}, {st.session_state['loc_lon']:.4f}")

with c_cult:
    st.markdown("<span style='color:#0288d1; font-weight:bold;'>🚜 PRODUÇÃO</span>", unsafe_allow_html=True)
    cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
    cv, cf = st.columns(2)
    var_sel = cv.selectbox("Variedade", list(BANCO_MASTER[cult_sel]['vars'].keys()))
    fase_sel = cf.selectbox("Fase", list(BANCO_MASTER[cult_sel]['fases'].keys()))

with c_date:
    st.markdown("<span style='color:#0288d1; font-weight:bold;'>📆 SAFRA</span>", unsafe_allow_html=True)
    st.session_state['d_plantio'] = st.date_input("Início", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<div style='font-size:2em; font-weight:800; color:#0f172a; text-align:center;'>{dias} Dias</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. INTELIGÊNCIA E DADOS
# ==============================================================================
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info['kc'], BANCO_MASTER[cult_sel]['t_base'])

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # --- STRIP DE KPIs (Métricas Grandes e Claras) ---
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temperatura", f"{hoje['Temp']:.1f}°C", f"Umid: {hoje['Umid']}%")
    
    vpd_val = hoje['VPD']
    delta_color = "normal" if 0.4 <= vpd_val <= 1.3 else "inverse"
    k2.metric("💧 VPD (Pressão)", f"{vpd_val} kPa", "Ideal" if 0.4 <= vpd_val <= 1.3 else "Risco", delta_color=delta_color)
    
    k3.metric("💦 ETc (Consumo)", f"{hoje['ETc']} mm", f"Kc: {info['kc']}")
    
    dt_val = hoje['Delta T']
    dt_status = "Aplicar" if 2 <= dt_val <= 8 else "Parar"
    k4.metric("🛡️ Delta T", f"{dt_val}°C", dt_status, delta_color="normal" if dt_status == "Aplicar" else "inverse")

    st.write("") 

    # --- MENU DE ABAS ---
    tabs = st.tabs(["🎓 CONSULTORIA", "📊 CLIMA", "📡 RADAR", "👁️ IA VISION", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    # ABA 1: CONSULTORIA
    with tabs[0]:
        # Progresso
        st.markdown(f"**Progresso de Maturação (GDA):** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)

        # Alertas Visuais
        if hoje['Umid'] > 85 or hoje['Chuva'] > 2:
            st.markdown("""
            <div class="alert-box alert-red">
                <span>🚨</span>
                <div>
                    <b>ALERTA DE RISCO FITOSSANITÁRIO</b><br>
                    Umidade excessiva favorece fungos. Suspenda produtos de contato. Use sistêmicos.
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-box alert-green">
                <span>✅</span>
                <div>
                    <b>CONDIÇÃO FAVORÁVEL</b><br>
                    Janela climática ideal para aplicações preventivas e manejo cultural.
                </div>
            </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="pro-card">
                <div class="card-title">🧬 Fisiologia Vegetal</div>
                <div class="label-tech">DESCRIÇÃO DA FASE</div><div class="value-tech">{dados_fase['desc']}</div>
                <div class="label-tech">DINÂMICA INTERNA</div><div class="value-tech">{dados_fase['fisiologia']}</div>
                <div class="label-tech">GENÉTICA ({var_sel})</div><div class="value-tech">{info['info']}</div>
            </div>""", unsafe_allow_html=True)
        
        with c2:
            # Lista Química
            chem_html = ""
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    chem_html += f"""
                    <li class="chem-item">
                        <div>
                            <div class="chem-name">{q['Alvo']}: {q['Ativo']}</div>
                        </div>
                        <div class="chem-tag">{q['Grupo']}</div>
                    </li>"""
            else: chem_html = f"<li>{dados_fase['quimica']}</li>"

            st.markdown(f"""
            <div class="pro-card">
                <div class="card-title">🛡️ Protocolo de Manejo</div>
                <div class="label-tech">MANEJO CULTURAL</div><div class="value-tech">{dados_fase.get('manejo', '-')}</div>
                <div class="label-tech" style="margin-top:25px;">🧪 FARMÁCIA DIGITAL</div>
                <ul class="chem-list" style="margin-top:10px;">{chem_html}</ul>
            </div>""", unsafe_allow_html=True)

    # ABA 2: CLIMA
    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#0288d1'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc (mm)', line=dict(color='#d32f2f', width=3)))
        fig.update_layout(template="plotly_white", margin=dict(t=20, b=20, l=20, r=20), height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        balanco = df_clima['Chuva'].sum() - df_clima['ETc'].sum()
        st.info(f"Balanço Hídrico Projetado (5 dias): {balanco:.1f} mm")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 3: RADAR
    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("📡 Estações Virtuais (Perímetro 15km)")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#f0fdf4"
                border = "#fca5a5" if r['Chuva'] == "Sim" else "#86efac"
                with cols[i]: st.markdown(f"""
                <div style="background:{bg}; border:1px solid {border}; padding:15px; border-radius:8px; text-align:center;">
                    <b>{r["Direcao"]}</b><br>
                    <span style="font-size:1.5em; font-weight:800;">{r["Temp"]:.0f}°C</span><br>
                    {r["Chuva"]}
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 4: IA
    with tabs[3]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("👁️ Agrônomo Virtual (Visão Computacional)")
        img = st.camera_input("Capturar Imagem da Folha/Fruto")
        if img and url_g:
            genai.configure(api_key=url_g)
            with st.spinner("Analisando padrões..."):
                res = genai.GenerativeModel('gemini-1.5-flash').generate_content([f"Agrônomo Especialista. Cultura {cult_sel}. Fase {fase_sel}. Identifique problemas visuais e recomende tratamento técnico.", Image.open(img)]).text
                st.markdown(res)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5: CUSTOS
    with tabs[4]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        item = c1.text_input("Descrição do Insumo")
        valor = c2.number_input("Valor (R$)", min_value=0.0)
        if c3.button("➕ Adicionar") and item:
            st.session_state['custos'].append({"Data": date.today(), "Item": item, "Valor": valor})
            st.rerun()
        
        if st.session_state['custos']:
            dfc = pd.DataFrame(st.session_state['custos'])
            st.dataframe(dfc, use_container_width=True)
            st.markdown(f"<h3 style='text-align:right;'>Total: R$ {dfc['Valor'].sum():,.2f}</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA
    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 3])
        with c1:
            nm = st.text_input("Nome do Talhão")
            if st.button("Salvar Localização"):
                if st.session_state.get('last_click'):
                    st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]})
                    st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"📍 {p['nome']}")
        with c2:
            m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            for p in st.session_state['pontos_mapa']: folium.Marker([p['lat'], p['lon']], popup=p['nome']).add_to(m)
            out = st_folium(m, height=500, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last_click'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 7: RELATÓRIOS
    with tabs[6]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("📄 Relatório Técnico Oficial")
        report_text = f"""
        AGRO-INTEL ENTERPRISE - RELATÓRIO TÉCNICO
        ===========================================
        Data de Emissão: {date.today()}
        Localização: {st.session_state['loc_lat']:.4f}, {st.session_state['loc_lon']:.4f}
        
        DADOS DA CULTURA
        ----------------
        Cultura: {cult_sel}
        Variedade: {var_sel}
        Estágio: {fase_sel}
        Idade da Lavoura: {dias} dias
        
        CONDIÇÕES AMBIENTAIS
        --------------------
        Temperatura: {hoje['Temp']} C
        Umidade Relativa: {hoje['Umid']} %
        Déficit de Pressão (VPD): {hoje['VPD']} kPa
        Delta T: {hoje['Delta T']} C
        
        RECOMENDAÇÃO TÉCNICA
        --------------------
        Manejo Sugerido: {dados_fase.get('manejo', 'N/A')}
        
        Protocolo Químico/Biológico:
        {dados_fase['quimica']}
        
        ===========================================
        Gerado automaticamente por Agro-Intel System v4.0
        """
        st.download_button("⬇️ Baixar Laudo (TXT)", data=report_text, file_name=f"Laudo_{cult_sel}_{date.today()}.txt")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Aguardando sincronização com satélites climáticos...")
