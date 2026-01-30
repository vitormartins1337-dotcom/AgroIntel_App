# ARQUIVO: main.py
# FUNÇÃO: Interface de Usuário (UI/UX) - Agro-Intel Enterprise
# VERSÃO: 3.0 (Frontend Modular)

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

# --- IMPORTAÇÃO DOS MOTORES (MODULARIZAÇÃO) ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError as e:
    st.error(f"ERRO CRÍTICO: Não foi possível importar os motores do sistema. Verifique se 'data_engine.py' e 'calc_engine.py' estão na mesma pasta. Detalhe: {e}")
    st.stop()

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & ESTILO (THEME ENGINE)
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
    """Carrega o tema Enterprise High-Contrast."""
    img_b64 = get_img_as_base64("fundo_agro.jpg")
    img_url = f"data:image/png;base64,{img_b64}" if img_b64 else "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=1740&auto=format&fit=crop"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Roboto', sans-serif; }}

    /* FUNDO ESCURO PROFISSIONAL (OVERLAY) */
    .stApp {{
        background-image: linear-gradient(rgba(10, 20, 30, 0.92), rgba(10, 20, 30, 0.95)), url("{img_url}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* HEADER */
    .titan-header {{
        padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px;
    }}
    .titan-title {{
        color: white; font-size: 3em; font-weight: 900; letter-spacing: -1px; margin: 0;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}
    .titan-sub {{ color: #94a3b8; font-size: 1.1em; letter-spacing: 1px; font-weight: 300; }}

    /* CARTÕES BRANCOS SÓLIDOS (ALTO CONTRASTE) */
    .glass-card {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        border-left: 5px solid #0288d1;
        margin-bottom: 20px;
        color: #1e293b;
    }}
    
    .card-header {{
        color: #0f172a; font-size: 1.4em; font-weight: 800; border-bottom: 2px solid #f1f5f9;
        padding-bottom: 15px; margin-bottom: 20px;
    }}
    
    .label-tech {{ color: #64748b; font-size: 0.8em; font-weight: 700; text-transform: uppercase; margin-top: 15px; }}
    .value-tech {{ color: #334155; font-size: 1.05em; line-height: 1.6; }}

    /* ALERTAS */
    .alert-box {{ padding: 15px; border-radius: 8px; font-weight: 600; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }}
    .alert-red {{ background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; }}
    .alert-green {{ background: #f0fdf4; color: #166534; border: 1px solid #86efac; }}

    /* KPIs */
    div[data-testid="metric-container"] {{
        background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==============================================================================
# 2. LÓGICA DE SESSÃO E DADOS
# ==============================================================================
# Carrega o Banco de Dados do data_engine
BANCO_MASTER = get_database()

# Inicializa Variáveis de Estado
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

# Pega credenciais da URL (Login persistente simples)
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# ==============================================================================
# 3. INTERFACE DE LOGIN (BLOQUEIO)
# ==============================================================================
if not url_w:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div class="glass-card" style="text-align:center;"><h2>🔒 Agro-Intel Enterprise</h2><p>Acesso Restrito ao Sistema Corporativo</p></div>', unsafe_allow_html=True)
        key_w = st.text_input("Chave API OpenWeather", type="password")
        key_g = st.text_input("Chave API Gemini AI", type="password")
        if st.button("AUTENTICAR SISTEMA", type="primary", use_container_width=True):
            if key_w and key_g:
                st.query_params["w_key"] = key_w
                st.query_params["g_key"] = key_g
                st.rerun()
            else:
                st.error("Insira ambas as chaves para prosseguir.")
    st.stop()

# ==============================================================================
# 4. DASHBOARD PRINCIPAL
# ==============================================================================
# Header
st.markdown("""
<div class="titan-header">
    <h1 class="titan-title">AGRO-INTEL SYSTEM</h1>
    <div class="titan-sub">Enterprise Management Platform v3.0</div>
</div>
""", unsafe_allow_html=True)

# Painel de Controle (Branco)
st.markdown('<div class="glass-card" style="padding: 15px;">', unsafe_allow_html=True)
c_loc, c_cult, c_date = st.columns([1.5, 1.5, 1])

with c_loc:
    st.markdown("**📍 GEOLOCALIZAÇÃO**")
    t1, t2 = st.tabs(["Cidade", "GPS"])
    with t1:
        city = st.text_input("Busca:", placeholder="Ex: Cristalina, GO", label_visibility="collapsed")
        if st.button("🔍 Buscar") and city:
            lat, lon = WeatherConn.get_coords(city, url_w)
            if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
    with t2:
        st.caption(f"Lat: {st.session_state['loc_lat']:.4f} | Lon: {st.session_state['loc_lon']:.4f}")

with c_cult:
    st.markdown("**🚜 LAVOURA**")
    cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
    
    # Lógica de dependência (Variedade depende da Cultura)
    col_v, col_f = st.columns(2)
    var_sel = col_v.selectbox("Variedade", list(BANCO_MASTER[cult_sel]['vars'].keys()))
    fase_sel = col_f.selectbox("Fase", list(BANCO_MASTER[cult_sel]['fases'].keys()))

with c_date:
    st.markdown("**📆 CICLO**")
    st.session_state['d_plantio'] = st.date_input("Início", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<h3 style='margin:0; color:#0288d1;'>{dias} Dias</h3>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. PROCESSAMENTO DE DADOS (USANDO OS MOTORES)
# ==============================================================================
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]

# Chama o Motor de Cálculo (Calc Engine)
df_clima = WeatherConn.get_forecast_dataframe(
    url_w, 
    st.session_state['loc_lat'], 
    st.session_state['loc_lon'], 
    info['kc'], 
    BANCO_MASTER[cult_sel]['t_base']
)

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean() # Estimativa simples
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # --- KPI STRIP ---
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🌡️ Temperatura", f"{hoje['Temp']:.1f}°C", f"Umid: {hoje['Umid']}%")
    
    vpd_status = "Ideal" if 0.4 <= hoje['VPD'] <= 1.3 else "Alerta"
    k2.metric("💧 VPD (Pressão)", f"{hoje['VPD']} kPa", vpd_status, delta_color="normal" if vpd_status == "Ideal" else "inverse")
    
    k3.metric("💦 ETc (Demanda)", f"{hoje['ETc']} mm", f"Kc: {info['kc']}")
    
    dt_status = "Aplicar" if 2 <= hoje['Delta T'] <= 8 else "Risco"
    k4.metric("🛡️ Delta T", f"{hoje['Delta T']}°C", dt_status, delta_color="normal" if dt_status == "Aplicar" else "inverse")

    st.write("") # Espaçamento

    # --- ABAS DE CONTEÚDO ---
    tabs = st.tabs(["🎓 CONSULTORIA", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 RELATÓRIOS"])

    # ABA 1: CONSULTORIA TÉCNICA
    with tabs[0]:
        st.markdown(f"**Maturação Térmica (GDA):** {gda_acum:.0f} / {info.get('gda_meta', 1500)}")
        st.progress(progresso)
        
        # Lógica de Alerta
        if hoje['Umid'] > 85 or hoje['Chuva'] > 2:
            st.markdown('<div class="alert-box alert-red">🚨 ALERTA: Umidade alta favorece patógenos. Suspenda produtos de contato.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-box alert-green">✅ CLIMA: Janela favorável para aplicações preventivas.</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="glass-card">
                <div class="card-header">🧬 FISIOLOGIA</div>
                <div class="label-tech">DESCRIÇÃO</div><div class="value-tech">{dados_fase['desc']}</div>
                <div class="label-tech">DINÂMICA</div><div class="value-tech">{dados_fase['fisiologia']}</div>
                <div class="label-tech">GENÉTICA ({var_sel})</div><div class="value-tech">{info['info']}</div>
            </div>""", unsafe_allow_html=True)
        
        with c2:
            # Renderizador HTML da Lista Química
            chem_html = ""
            if isinstance(dados_fase['quimica'], list):
                for q in dados_fase['quimica']:
                    chem_html += f"<li><b>{q['Alvo']}</b>: {q['Ativo']} <br><small style='color:#666;'>{q['Grupo']} • {q['Tipo']}</small></li><hr style='margin:5px 0; border-top:1px solid #eee;'>"
            else: chem_html = f"<li>{dados_fase['quimica']}</li>"

            st.markdown(f"""
            <div class="glass-card">
                <div class="card-header">🛡️ MANEJO</div>
                <div class="label-tech">ESTRATÉGIA CULTURAL</div><div class="value-tech">{dados_fase.get('manejo', '-')}</div>
                <div class="label-tech" style="margin-top:20px;">🧪 FARMÁCIA DIGITAL</div>
                <ul style="padding-left:20px; margin-top:10px;">{chem_html}</ul>
            </div>""", unsafe_allow_html=True)

    # ABA 2: CLIMA
    with tabs[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#0288d1'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc (mm)', line=dict(color='#d32f2f', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"Saldo Hídrico (Previsão): {df_clima['Chuva'].sum() - df_clima['ETc'].sum():.1f} mm")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 3: RADAR
    with tabs[2]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📡 Estações Virtuais (15km)")
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#f1f8e9"
                with cols[i]: st.markdown(f'<div style="background:{bg}; padding:15px; border-radius:8px; text-align:center;"><b>{r["Direcao"]}</b><br><h3>{r["Temp"]:.0f}°C</h3>{r["Chuva"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 4: IA
    with tabs[3]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👁️ Diagnóstico Fitopatológico")
        img = st.camera_input("Captura")
        if img and url_g:
            genai.configure(api_key=url_g)
            with st.spinner("Analisando..."):
                res = genai.GenerativeModel('gemini-1.5-flash').generate_content([f"Agrônomo. {cult_sel}. Fase {fase_sel}. Diagnóstico e Solução.", Image.open(img)]).text
                st.markdown(res)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5: CUSTOS
    with tabs[4]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item")
        v = c2.number_input("Valor R$")
        if c3.button("Salvar") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']: 
            dfc = pd.DataFrame(st.session_state['custos'])
            st.dataframe(dfc, use_container_width=True)
            st.metric("Total", f"R$ {dfc['Valor'].sum():,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA
    with tabs[5]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Nome Talhão")
            if st.button("Salvar Ponto"):
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
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📄 Emissão de Laudo Técnico")
        
        # Gera o relatório em memória (Texto simples simulando PDF para evitar libs externas complexas)
        report_text = f"""RELATÓRIO TÉCNICO - AGRO-INTEL
----------------------------------
DATA: {date.today()}
LOCAL: {st.session_state['loc_lat']}, {st.session_state['loc_lon']}
CULTURA: {cult_sel} ({var_sel})
FASE: {fase_sel}
IDADE: {dias} dias

CLIMA ATUAL:
Temp: {hoje['Temp']} C | Umid: {hoje['Umid']}% | VPD: {hoje['VPD']}

RECOMENDAÇÃO TÉCNICA:
{dados_fase['manejo']}

QUÍMICOS RECOMENDADOS:
{dados_fase['quimica']}
----------------------------------
Assinatura: _______________________
Agro-Intel System Enterprise
"""
        st.download_button("⬇️ Baixar Laudo (TXT/PDF)", data=report_text, file_name="Laudo_Tecnico.txt")
        st.markdown('</div>', unsafe_allow_html=True)
