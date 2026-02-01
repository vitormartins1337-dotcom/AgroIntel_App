# ARQUIVO: main.py
# VERSÃO: V16 (Data Integrity - Prioridade Total à Informação Agronômica)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai

# --- 1. BLINDAGEM DE IMPORTAÇÃO ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
except ImportError:
    st.error("🚨 ERRO CRÍTICO: Motores não encontrados.")
    st.stop()

# --- 2. SETUP VISUAL ROBUSTO ---
st.set_page_config(page_title="Agro Intel Enterprise", page_icon="🌱", layout="wide")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #f8f9fa; 
        color: #212529;
    }

    /* HERO HEADER SÓBRIO E PROFISSIONAL */
    .hero-container {
        background: linear-gradient(135deg, #1b4332 0%, #081c15 100%);
        border-radius: 12px;
        padding: 40px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .filter-card {
        background: white; border-radius: 10px; padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }
    
    /* ABAS CLÁSSICAS E LEGÍVEIS */
    button[data-baseweb="tab"] {
        font-size: 18px !important; font-weight: 600 !important;
        padding: 12px 30px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #198754 !important; border-bottom: 3px solid #198754 !important;
        background-color: #f1f8e9 !important;
    }

    /* KPI CARDS (PAINEL DE DECISÃO) */
    .kpi-container { display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 10px; }
    .kpi-card {
        flex: 1; min-width: 200px; background: white; border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e9ecef;
        overflow: hidden;
    }
    .kpi-header { font-size: 0.8rem; font-weight: 700; color: #6c757d; padding: 12px 15px; background: #f8f9fa; text-transform: uppercase;}
    .kpi-body { padding: 10px 15px; }
    .kpi-value { font-size: 2.2rem; font-weight: 800; color: #212529; }
    .kpi-footer { padding: 8px 15px; color: white; font-weight: 600; font-size: 0.85rem; }

    /* TEXTOS AGRONÔMICOS */
    .agro-text { font-size: 1rem; line-height: 1.6; color: #343a40; text-align: justify; }
    .agro-label { font-weight: 700; color: #198754; font-size: 1.05rem; margin-bottom: 5px; display: block; }
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

# --- 4. LOGIN ---
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""<div class="filter-card" style="text-align:center;"><h2>🔐 Agro Intel Enterprise</h2><p>Acesso Restrito ao Sistema de Gestão</p></div>""", unsafe_allow_html=True)
        kw = st.text_input("Chave Meteorológica", type="password")
        kg = st.text_input("Chave Inteligência (IA)", type="password")
        if st.button("ENTRAR", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw; st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# --- 5. CABEÇALHO ---
st.markdown("""
<div class="hero-container">
    <h1 style="margin:0; font-weight:800;">Agro Intel Cockpit</h1>
    <p style="opacity:0.8;">Sistema de Apoio à Decisão Agronômica de Alta Precisão</p>
</div>
""", unsafe_allow_html=True)

# --- 6. FILTROS ---
st.markdown('<div class="filter-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])
with c1:
    city = st.text_input("📍 Unidade Produtiva (GPS)", placeholder="Ex: Lucas do Rio Verde")
    if st.button("🔄 Atualizar Clima") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: 
            st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon
            st.rerun()
with c2:
    if BANCO_MASTER:
        cult_sel = st.selectbox("🚜 Cultura", sorted(list(BANCO_MASTER.keys())))
        try:
            vars_disponiveis = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
            fases_disponiveis = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
            var_sel = st.selectbox("🧬 Variedade/Híbrido", vars_disponiveis)
        except: st.error("Erro dados cultura."); st.stop()
    else: st.warning("Banco de dados vazio."); st.stop()
with c3:
    fase_sel = st.selectbox("📊 Estádio Fenológico", fases_disponiveis)
with c4:
    st.session_state['d_plantio'] = st.date_input("📆 Plantio", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
st.markdown('</div>', unsafe_allow_html=True)

# --- 7. PROCESSAMENTO ---
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # Lógica de Semáforo (Traffic Light)
    temp = hoje['Temp']
    st_t, cr_t = ("Ótima ✅", "#198754") if 18 <= temp <= 32 else ("Crítica 🔥", "#dc3545")
    
    delta_t = hoje['Delta T']
    if 2 <= delta_t <= 8: st_d, cr_d = "APTO ✅", "#198754"
    elif 8 < delta_t <= 10: st_d, cr_d = "Atenção ⚠️", "#ffc107"
    else: st_d, cr_d = "PARE 🛑", "#dc3545"

    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card"><div class="kpi-header">🌡️ Temperatura</div><div class="kpi-body"><span class="kpi-value">{temp:.1f}</span>°C</div><div class="kpi-footer" style="background:{cr_t}">{st_t}</div></div>
        <div class="kpi-card"><div class="kpi-header">💧 Umidade</div><div class="kpi-body"><span class="kpi-value">{hoje['Umid']}</span>%</div><div class="kpi-footer" style="background:#0d6efd">Relativa</div></div>
        <div class="kpi-card" style="border:2px solid {cr_d}"><div class="kpi-header" style="color:{cr_d}">🛡️ Delta T (Aplicação)</div><div class="kpi-body"><span class="kpi-value" style="color:{cr_d}">{delta_t}</span>°C</div><div class="kpi-footer" style="background:{cr_d}">{st_d}</div></div>
        <div class="kpi-card"><div class="kpi-header">☀️ GDA Acumulado</div><div class="kpi-body"><span class="kpi-value">{gda_acum:.0f}</span></div><div class="kpi-footer" style="background:#212529">Meta: {info.get('gda_meta', 1500)}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- 8. ABAS (Foco no Conteúdo) ---
    tabs = st.tabs(["TÉCNICO 🧬", "CLIMA ☁️", "RADAR 📡", "IA 👁️", "CUSTOS 💰", "MAPA 🗺️", "LAUDO 📄"])

    with tabs[0]: # ABA TÉCNICA - CORRIGIDA E ROBUSTA
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.progress(progresso)
        
        # Bloco de Imagem (Com Proteção contra Erro)
        try:
            if "Soja" in str(cult_sel): st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Soybean.jpg/800px-Soybean.jpg", width=300)
            elif "Milho" in str(cult_sel): st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Maize_ear.jpg/800px-Maize_ear.jpg", width=300)
        except: pass # Se falhar, segue sem imagem, sem erro.

        # --- AQUI ESTAVA O PROBLEMA: RESTAURANDO INFORMAÇÕES ---
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<span class="agro-label">🧬 CARACTERIZAÇÃO GENÉTICA ({var_sel})</span>', unsafe_allow_html=True)
            # Busca 'info' OU 'descricao' OU 'detalhes' (Inteligência de chaves)
            info_text = info.get('info') or info.get('desc') or info.get('descricao') or "Informação técnica não disponível no banco de dados."
            st.markdown(f'<div class="agro-text">{info_text}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<span class="agro-label">🌱 FISIOLOGIA DO ESTÁDIO</span>', unsafe_allow_html=True)
            fisio_text = dados_fase.get('fisiologia') or dados_fase.get('Fisiologia') or "Dados fisiológicos não cadastrados."
            st.markdown(f'<div class="agro-text">{fisio_text}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<span class="agro-label">🛡️ ESTRATÉGIAS DE MANEJO TÉCNICO</span>', unsafe_allow_html=True)
        manejo_text = dados_fase.get('manejo') or dados_fase.get('Manejo') or dados_fase.get('recomendacao') or "Consulte um engenheiro agrônomo."
        st.warning(manejo_text)

        st.subheader("🧪 Protocolo Avançado (Químico/Biológico)")
        if isinstance(dados_fase.get('quimica'), list):
            for q in dados_fase['quimica']:
                # LÓGICA ANTI-NONE (O Segredo da Correção)
                # O código agora tenta 3 chaves diferentes antes de desistir.
                alvo = q.get('Alvo') or q.get('Doenca') or q.get('Praga') or "Alvo Geral"
                ativo = q.get('Ativo') or q.get('Produto') or "Não especificado"
                # Aqui corrigimos o erro do "None" na Estratégia
                estrategia = q.get('Estrategia') or q.get('Obs') or q.get('Nota') or q.get('Manejo') or ""
                
                tipo = q.get('Tipo', 'Geral')
                cor_left = "#dc3545" if "Químico" in tipo else "#198754" if "Biológico" in tipo else "#0d6efd"

                st.markdown(f"""
                <div style="background:#fff; border-left:5px solid {cor_left}; padding:15px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.05); margin-bottom:10px;">
                    <div style="font-weight:700; font-size:1.1rem; color:#212529;">{alvo} 
                        <span style="font-size:0.75rem; background:{cor_left}; color:white; padding:4px 8px; border-radius:12px; margin-left:10px; vertical-align:middle;">{tipo}</span>
                    </div>
                    <div style="margin-top:8px; color:#495057;">🧪 <b>Ingrediente Ativo:</b> {ativo}</div>
                    <div style="margin-top:5px; color:#0d6efd; font-style:italic; font-size:0.95rem;">💡 {estrategia}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum protocolo cadastrado para esta fase.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]: # CLIMA
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#0d6efd'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Evapo (mm)', line=dict(color='#dc3545', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]: # RADAR
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#e8f5e9"
                with cols[i]: st.markdown(f"""<div style="background:{bg}; padding:15px; border-radius:8px; text-align:center;"><b>{r["Direcao"]}</b><br><h3>{r["Temp"]:.0f}°</h3>{r["Chuva"]}</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]: # IA
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: img = st.camera_input("📸 Foto do Problema")
        with c2:
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("Analisando..."):
                    try:
                        prompt = f"Agrônomo Expert. Cultura: {cult_sel}, Fase: {fase_sel}. Identifique a praga/doença e dê manejo."
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        res = model.generate_content([prompt, Image.open(img)])
                        st.markdown(res.text)
                    except: st.error("Erro IA.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[4]: # CUSTOS
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item")
        v = c2.number_input("Valor", min_value=0.0)
        if c3.button("➕") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']:
            df = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df, use_container_width=True)
            st.metric("Total", f"R$ {df['Valor'].sum():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[5]: # MAPA
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Ponto")
            if st.button("📍") and st.session_state.get('last'): 
                st.session_state['pontos_mapa'].append({"n": nm, "lat": st.session_state['last'][0], "lon": st.session_state['last'][1]}); st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"🚩 {p['n']}")
        with c2:
            m = folium.Map([st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Sat').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            out = st_folium(m, height=400, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[6]: # LAUDO
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        st.subheader("📝 Laudo Técnico")
        obs = st.text_area("Observações")
        if st.button("🖨️ Gerar PDF"):
            st.markdown(f"""
            <div style="border:1px solid #000; padding:30px; background:white; font-family:serif;">
                <h2 style="text-align:center;">RECEITUÁRIO AGRONÔMICO</h2>
                <p><b>Data:</b> {date.today()} | <b>Local:</b> {city or 'Não informado'}</p>
                <hr>
                <h4>1. IDENTIFICAÇÃO</h4>
                <p>Cultura: {cult_sel} | Variedade: {var_sel}</p>
                <p>Estádio: {fase_sel}</p>
                <h4>2. DIAGNÓSTICO</h4>
                <p>{dados_fase.get('desc')}</p>
                <h4>3. PRESCRIÇÃO TÉCNICA</h4>
                <p>{dados_fase.get('manejo')}</p>
                <hr>
                <p><b>Nota Técnica:</b> {obs}</p>
                <br><br>
                <p style="text-align:center;">_______________________________________<br>Engenheiro Agrônomo Responsável</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
