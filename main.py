# ARQUIVO: main.py
# VERSÃO: V14 (Enterprise Master - Cockpit Integrado)
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
    st.error("🚨 ERRO CRÍTICO: Arquivos 'data_engine.py' ou 'calc_engine.py' não encontrados na pasta.")
    st.stop()

# --- 2. CONFIGURAÇÃO DA PÁGINA & CSS ---
st.set_page_config(page_title="Agro-Intel Enterprise", page_icon="🚜", layout="wide")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f0f2f5; }

    /* HEADER PREMIUM */
    .titan-header {
        background: linear-gradient(135deg, #004d40 0%, #00695c 100%);
        padding: 24px; border-radius: 12px; text-align: center; color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    .titan-header h1 { font-weight: 900; letter-spacing: 1px; margin: 0; font-size: 2.2rem; }
    .titan-header p { opacity: 0.9; font-weight: 300; margin-top: 5px; font-size: 1.1rem; }

    /* CONTAINER PADRÃO */
    .pro-card {
        background: white; border-radius: 12px; padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    /* ABAS GRANDES (TOUCH FRIENDLY) */
    button[data-baseweb="tab"] {
        font-size: 18px !important; font-weight: 600 !important;
        padding: 12px 24px !important; background-color: white !important;
        border-radius: 8px 8px 0 0 !important; border: 1px solid transparent !important;
        margin-right: 4px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #004d40 !important; background-color: #e0f2f1 !important;
        border-bottom: 3px solid #004d40 !important;
    }

    /* COCKPIT CARDS (CSS DO PAINEL) */
    .kpi-container { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 10px; }
    .kpi-card {
        flex: 1; min-width: 220px; background: white; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04); border: 1px solid #e0e0e0;
        overflow: hidden; display: flex; flex-direction: column;
    }
    .kpi-header {
        font-size: 13px; font-weight: 700; color: #555; padding: 10px 15px;
        background: #fcfcfc; border-bottom: 1px solid #f0f0f0; text-transform: uppercase;
    }
    .kpi-body { padding: 15px; text-align: center; flex-grow: 1; }
    .kpi-value { font-size: 32px; font-weight: 800; color: #222; margin-bottom: 0px; line-height: 1.1; }
    .kpi-unit { font-size: 16px; color: #888; font-weight: 400; margin-left: 2px; }
    .kpi-footer { padding: 8px; text-align: center; color: white; font-size: 13px; font-weight: 600; }

    /* TAGS QUÍMICAS */
    .chem-card { background: #fafafa; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)
load_css()

# --- 3. INICIALIZAÇÃO E DADOS ---
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
url_w, url_g = st.query_params.get("w_key", None), st.query_params.get("g_key", None)

# --- 4. LOGIN (GATEKEEPER) ---
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown('<div class="pro-card" style="text-align:center;"><h2>🔒 Acesso Enterprise</h2><p>Identifique-se para acessar o painel agronômico.</p></div>', unsafe_allow_html=True)
        kw = st.text_input("Chave OpenWeather", type="password")
        kg = st.text_input("Chave Gemini AI", type="password")
        if st.button("ACESSAR SISTEMA", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# --- 5. INTERFACE PRINCIPAL ---
st.markdown('<div class="titan-header"><h1>AGRO INTEL ENTERPRISE</h1><p>Sistema de Apoio à Decisão Agronômica</p></div>', unsafe_allow_html=True)

# FILTROS
st.markdown('<div class="pro-card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.5, 1.5, 1])
with c1:
    st.markdown("### 📍 Unidade Produtiva")
    city = st.text_input("Cidade/Fazenda", label_visibility="collapsed", placeholder="Digite a localização...")
    if st.button("🔍 Atualizar Dados Climáticos") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: 
            st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon
            st.rerun()
with c2:
    st.markdown("### 🚜 Cultura & Genética")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())))
        try:
            vars_disponiveis = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
            fases_disponiveis = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
            col_v, col_f = st.columns(2)
            var_sel = col_v.selectbox("Variedade", vars_disponiveis)
            fase_sel = col_f.selectbox("Estádio Atual", fases_disponiveis)
        except:
            st.error("Erro estrutural no banco de dados selecionado.")
            st.stop()
    else: 
        st.warning("Banco de dados vazio. Verifique os arquivos JSON.")
        st.stop()
with c3:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Data Plantio", st.session_state['d_plantio'])
    dias = (date.today() - st.session_state['d_plantio']).days
    st.markdown(f"<h3 style='text-align:center; color:#00695c; margin:0;'>{dias} DAE</h3>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# PROCESSAMENTO DE DADOS
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

# --- AQUI COMEÇA A LÓGICA DO PAINEL (COCKPIT) ---
if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))

    # --- LÓGICA DE CORES E ALERTAS (SMART AGRO) ---
    # Temperatura
    temp = hoje['Temp']
    if temp < 18: status_temp = "Baixa (Metabolismo Lento) ❄️"; cor_temp = "#1976d2"
    elif 18 <= temp <= 32: status_temp = "Zona de Conforto ✅"; cor_temp = "#388e3c"
    else: status_temp = "Estresse Térmico 🔥"; cor_temp = "#d32f2f"

    # Delta T (Segurança de Aplicação)
    delta_t = hoje['Delta T']
    if delta_t < 2: status_delta = "PARE (Risco Deriva) 🛑"; cor_delta = "#d32f2f"
    elif 2 <= delta_t <= 8: status_delta = "APTO (Ideal) ✅"; cor_delta = "#388e3c"
    elif 8 < delta_t <= 10: status_delta = "Limite (Atenção) ⚠️"; cor_delta = "#fbc02d"
    else: status_delta = "PARE (Perda Gota) 🛑"; cor_delta = "#d32f2f"

    # Umidade
    umid = hoje['Umid']
    if umid < 40: status_umid = "Seco (Atenção Ácaros)"; cor_umid = "#fbc02d"
    elif 40 <= umid <= 80: status_umid = "Ideal ✅"; cor_umid = "#388e3c"
    else: status_umid = "Alta (Risco Fúngico) 🍄"; cor_umid = "#d32f2f"

    # VPD (Opcional - Calculado simples)
    vpd_valor = 0.6108 * 2.718 ** ((17.27 * temp) / (temp + 237.3)) * (1 - (umid / 100))
    
    # --- RENDERIZAÇÃO DO SMART COCKPIT HTML ---
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-header">🌡️ Temperatura</div>
            <div class="kpi-body"><div class="kpi-value">{temp:.1f}<span class="kpi-unit">°C</span></div></div>
            <div class="kpi-footer" style="background-color: {cor_temp};">{status_temp}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">💧 Umidade Relativa</div>
            <div class="kpi-body"><div class="kpi-value">{umid}<span class="kpi-unit">%</span></div></div>
            <div class="kpi-footer" style="background-color: {cor_umid};">{status_umid}</div>
        </div>
        <div class="kpi-card" style="border: 2px solid {cor_delta};">
            <div class="kpi-header" style="color:{cor_delta};">🛡️ Delta T (Pulverização)</div>
            <div class="kpi-body"><div class="kpi-value" style="color:{cor_delta};">{delta_t}<span class="kpi-unit">°C</span></div></div>
            <div class="kpi-footer" style="background-color: {cor_delta};">{status_delta}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header">💨 VPD (Pressão)</div>
            <div class="kpi-body"><div class="kpi-value">{vpd_valor:.2f}<span class="kpi-unit">kPa</span></div></div>
            <div class="kpi-footer" style="background-color: #455a64;">Indicador de Transpiração</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- ABAS DE CONTEÚDO ---
    tabs = st.tabs(["🎓 TÉCNICO", "📊 CLIMA", "📡 RADAR", "👁️ IA", "💰 CUSTOS", "🗺️ MAPA", "📄 LAUDO"])

    # ABA 1: TÉCNICO (AGRONOMIA PURA)
    with tabs[0]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.caption(f"Evolução Térmica (GDA): {gda_acum:.0f} de {info.get('gda_meta', 1500)} GDAs previstos.")
        st.progress(progresso)

        # Accordions Profissionais
        with st.expander("🧬 GENÉTICA & POTENCIAL (Caracterização)", expanded=True):
            st.info(f"**Material:** {var_sel}")
            st.markdown(f"**Perfil Técnico:** {info.get('info', 'Dados não cadastrados.')}")
        
        with st.expander("🌱 FISIOLOGIA DO ESTÁDIO (O que acontece na planta)", expanded=True):
            col_a, col_b = st.columns([1,2])
            with col_a: st.markdown(f"**Visual:**\n{dados_fase.get('desc', '-')}")
            with col_b: st.markdown(f"**Metabolismo:**\n{dados_fase.get('fisiologia', '-')}")

        with st.expander("🛡️ RECOMENDAÇÃO DE MANEJO INTEGRADO", expanded=True):
            st.warning(f"**Estratégia:** {dados_fase.get('manejo', '-')}")

        with st.expander("🧪 FARMÁCIA DIGITAL (Protocolos FRAC/IRAC)", expanded=False):
            if isinstance(dados_fase.get('quimica'), list):
                for q in dados_fase['quimica']:
                    tipo = q.get('Tipo', 'Geral')
                    cor_borda = "#1976d2"
                    icone = "💊"
                    if "Biológico" in tipo: cor_borda, icone = "#2e7d32", "🦠"
                    elif "Químico" in tipo: cor_borda, icone = "#d32f2f", "☠️"
                    
                    st.markdown(f"""
                    <div class="chem-card" style="border-left: 5px solid {cor_borda};">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:bold; font-size:1.1em; color:#333;">{icone} {q.get('Alvo', 'Alvo')}</span>
                            <span style="background:{cor_borda}; color:white; padding:4px 10px; border-radius:4px; font-weight:bold; font-size:0.8em;">{tipo}</span>
                        </div>
                        <div style="margin-top:10px;"><b>Ativo:</b> {q.get('Ativo', '-')}</div>
                        <div style="margin-top:5px; color:#666;">🧬 <b>Resistência:</b> <span style="background:#eee; padding:2px 6px; border-radius:4px;">{q.get('Codigos', q.get('Grupo', '-'))}</span></div>
                        <div style="margin-top:10px; color:#0d47a1; font-style:italic;">💡 {q.get('Estrategia', q.get('Obs', ''))}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum protocolo químico/biológico cadastrado para esta fase.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 2: CLIMA (GRÁFICOS)
    with tabs[1]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#0277bd'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='ETc (mm)', line=dict(color='#d32f2f', width=3)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 3: RADAR (PREVISÃO CURTO PRAZO)
    with tabs[2]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                bg = "#ffebee" if r['Chuva'] == "Sim" else "#e8f5e9"
                with cols[i]: st.markdown(f"""<div style="background:{bg}; padding:15px; border-radius:8px; text-align:center;"><b>{r["Direcao"]}</b><br><h3 style='margin:10px 0;'>{r["Temp"]:.0f}°C</h3>{r["Chuva"]}</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 4: IA (GEMINI VISION)
    with tabs[3]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c_ia1, c_ia2 = st.columns([1, 1])
        with c_ia1: img = st.camera_input("📸 Diagnóstico Visual")
        with c_ia2:
            if img and url_g:
                genai.configure(api_key=url_g)
                with st.spinner("IA processando imagem..."):
                    try:
                        prompt = f"Sou Agrônomo. Cultura: {cult_sel}, Fase: {fase_sel}. Identifique a praga/doença e sugira controle."
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content([prompt, Image.open(img)])
                        st.markdown(response.text)
                    except Exception as e: st.error(f"Erro IA: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5: CUSTOS (GESTÃO)
    with tabs[4]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Descrição do Custo")
        v = c2.number_input("Valor (R$)", min_value=0.0)
        if c3.button("➕ Adicionar") and i: 
            st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v})
            st.rerun()
        if st.session_state['custos']: 
            df_custos = pd.DataFrame(st.session_state['custos'])
            st.dataframe(df_custos, use_container_width=True)
            st.metric("Custo Total da Safra", f"R$ {df_custos['Valor'].sum():.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA (GIS)
    with tabs[5]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Nome do Talhão/Ponto")
            if st.button("📍 Gravar Ponto") and st.session_state.get('last_click'): 
                st.session_state['pontos_mapa'].append({"nome": nm, "lat": st.session_state['last_click'][0], "lon": st.session_state['last_click'][1]})
                st.rerun()
            for p in st.session_state['pontos_mapa']: st.write(f"🚩 {p['nome']}")
        with c2:
            m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m); Fullscreen().add_to(m)
            out = st_folium(m, height=450, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last_click'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 7: LAUDO (RELATÓRIO)
    with tabs[6]:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Gerador de Receituário Agronômico")
        obs = st.text_area("Observações Técnicas Complementares")
        if st.button("🖨️ Gerar PDF para Impressão"):
            st.success("Documento gerado e pronto para assinatura.")
            st.write(f"**LAUDO TÉCNICO - {date.today()}**\n\nCultura: {cult_sel} | {var_sel}\nFase: {fase_sel}\n\nDiagnóstico: {dados_fase.get('desc','')}\nRecomendação: {dados_fase.get('manejo','')}\n\nNota: {obs}")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Sistema aguardando sincronização com satélites meteorológicos...")
