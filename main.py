# ARQUIVO: main.py
# SISTEMA: AGRO SDI (Sistema de Decisão Integrada)
# VERSÃO: V21 - FINAL STABLE (Clean Code)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
from PIL import Image
import google.generativeai as genai
import os  # <--- OBRIGATÓRIO PARA AS IMAGENS FUNCIONAREM
from notification_engine import NotificationSystem

# --- 1. IMPORTAÇÃO DOS MOTORES ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
    from styles import load_css
    from agro_utils import AgroBrain
except ImportError as e:
    st.error(f"🚨 FALHA CRÍTICA: Módulo {e.name} não encontrado.")
    st.stop()

# --- 2. CONFIGURAÇÃO ---
st.set_page_config(page_title="Agro SDI | Enterprise", page_icon="🛰️", layout="wide")
load_css()

# Estado da Sessão
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = []
if 'custos' not in st.session_state: st.session_state['custos'] = []
if 'd_plantio' not in st.session_state: st.session_state['d_plantio'] = date(2025, 11, 25)

BANCO_MASTER = get_database()
url_w = st.query_params.get("w_key", None)
url_g = st.query_params.get("g_key", None)

# --- 3. LOGIN ---
if not url_w:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
        <div class="app-card" style="text-align:center; padding:40px;">
            <h1 style="color:#064e3b; font-family:'Montserrat'; font-weight:900; font-size:3rem; margin:0;">AGRO SDI</h1>
            <p style="text-transform:uppercase; color:#6b7280; font-weight:600; letter-spacing:2px; margin-top:5px;">Enterprise Portal</p>
        </div>""", unsafe_allow_html=True)
        kw = st.text_input("CHAVE OPENWEATHER", type="password")
        kg = st.text_input("CHAVE GEMINI AI", type="password")
        if st.button("ACESSAR", type="primary", use_container_width=True):
            if kw and kg: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# --- 4. HEADER ---
st.markdown("""
<div class="brand-container">
    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div>
            <h1 class="brand-title">AGRO <span class="brand-accent">SDI</span></h1>
            <div class="brand-subtitle">SISTEMA DE DECISÃO INTEGRADA | v21.0</div>
        </div>
        <div style="text-align:right; font-size:0.85rem; opacity:0.9;">
            <b>STATUS:</b> ONLINE 🟢
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. FILTROS ---
st.markdown('<div class="app-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])
with c1:
    st.markdown("### 📍 Unidade")
    city = st.text_input("GPS Busca", placeholder="Fazenda...", label_visibility="collapsed")
    if st.button("📡 Sincronizar") and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()
with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())), label_visibility="collapsed")
        vars_disp = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
        fases_disp = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
        var_sel = st.selectbox("Genética", vars_disp)
    else: st.error("Banco vazio."); st.stop()
with c3:
    st.markdown("### 📊 Fase")
    fase_sel = st.selectbox("Estádio", fases_disp, label_visibility="collapsed")
with c4:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Plantio", st.session_state['d_plantio'], label_visibility="collapsed")
    dias = (date.today() - st.session_state['d_plantio']).days
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PROCESSAMENTO ---
info = BANCO_MASTER[cult_sel]['vars'][var_sel]
dados_fase = BANCO_MASTER[cult_sel]['fases'][fase_sel]
df_clima = WeatherConn.get_forecast_dataframe(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'], info.get('kc', 1.0), BANCO_MASTER[cult_sel].get('t_base', 10))

if not df_clima.empty:
    hoje = df_clima.iloc[0]
    gda_acum = dias * df_clima['GDA'].mean()
    progresso = min(1.0, gda_acum / info.get('gda_meta', 1500))
    temp, umid, delta_t = hoje['Temp'], hoje['Umid'], hoje['Delta T']
    vpd = AgroBrain.calcular_vpd(temp, umid)
    
    # Cores KPI
    t_st, t_cor = ("Ótima ✅", "#16a34a") if 18 <= temp <= 32 else ("Crítica 🔥", "#dc2626")
    d_st, d_cor = ("APTO ✅", "#16a34a") if 2 <= delta_t <= 8 else ("PARE 🛑", "#dc2626")
    v_st, v_cor = ("Ideal 💧", "#2563eb") if 0.5 <= vpd <= 1.5 else ("Estresse 🌵", "#dc2626")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(AgroBrain.gerar_cartao_kpi("🌡️ Temperatura", f"{temp:.1f}", "°C", t_st, t_cor), unsafe_allow_html=True)
    with c2: st.markdown(AgroBrain.gerar_cartao_kpi("🛡️ Delta T", f"{delta_t}", "°C", d_st, d_cor), unsafe_allow_html=True)
    with c3: st.markdown(AgroBrain.gerar_cartao_kpi("💨 VPD", f"{vpd:.2f}", "kPa", v_st, v_cor), unsafe_allow_html=True)
    with c4: st.markdown(AgroBrain.gerar_cartao_kpi("☀️ GDA", f"{gda_acum:.0f}", "°GD", f"Ciclo: {dias}d", "#1f2937"), unsafe_allow_html=True)

    # --- 7. ABAS DE CONTEÚDO ---
    tabs = st.tabs(["🧬 TÉCNICO", "☁️ CLIMA", "📡 RADAR", "👁️ IA", "💰 GESTÃO", "🗺️ MAPA", "📄 LAUDO", "🔔 ALERTAS"])
    # ABA 1: TÉCNICO (SINGLE PASS - SEM DUPLICAÇÃO)
    with tabs[0]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.progress(progresso)

        # Imagens Inteligentes
        nome_cultura = str(cult_sel).lower()
        mapa_img = {
            "soja": "soja", "milho": "milho", "algodão": "algodao", "algodao": "algodao",
            "café": "cafe", "cafe": "cafe", "feijão": "feijao", "feijao": "feijao",
            "trigo": "trigo", "tomate": "tomate", "batata": "batata", "uva": "uva",
            "banana": "banana", "citros": "citros", "manga": "manga"
        }
        
        # Tenta achar o nome do arquivo
        arquivo_base = next((v for k, v in mapa_img.items() if k in nome_cultura), None)
        img_path = None
        
        if arquivo_base:
            p_jpg = os.path.join("images", f"{arquivo_base}.jpg")
            p_png = os.path.join("images", f"{arquivo_base}.png")
            if os.path.exists(p_jpg): img_path = p_jpg
            elif os.path.exists(p_png): img_path = p_png

        st.markdown("<br>", unsafe_allow_html=True)
        c_i1, c_i2, c_i3 = st.columns([1,2,1])
        with c_i2:
            if img_path:
                st.image(img_path, caption=cult_sel, use_container_width=True)
            else:
                st.image("https://images.unsplash.com/photo-1625246333195-58197bd47d26?q=80&w=1000&auto=format&fit=crop", caption="Imagem Ilustrativa", use_container_width=True)

        st.divider()

        # Detalhes Técnicos
        c_t1, c_t2 = st.columns(2)
        with c_t1:
            st.markdown('<div class="section-title">🧬 GENÉTICA</div>', unsafe_allow_html=True)
            info_txt = AgroBrain.get_info_segura(info, ['info', 'desc'])
            st.markdown(f'<div class="info-text"><b>{var_sel}</b><br>{info_txt}</div>', unsafe_allow_html=True)
        with c_t2:
            st.markdown('<div class="section-title">🌱 FISIOLOGIA</div>', unsafe_allow_html=True)
            fisio_txt = AgroBrain.get_info_segura(dados_fase, ['fisiologia'])
            st.markdown(f'<div class="info-text">{fisio_txt}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-title">🛡️ MANEJO TÉCNICO</div>', unsafe_allow_html=True)
        manejo_txt = AgroBrain.get_info_segura(dados_fase, ['manejo'])
        st.warning(f"🎯 **Ação:** {manejo_txt}")

        st.markdown("### 🧪 Protocolo de Defesa")
        # ESTA LINHA SÓ PODE APARECER UMA VEZ NO CÓDIGO INTEIRO
        AgroBrain.render_protocolo_quimico(dados_fase.get('quimica')) 
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 2: CLIMA
    with tabs[1]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Evapo', line=dict(color='#ef4444')))
        st.plotly_chart(fig, use_container_width=True)
        status_ap, cor_ap, alertas = AgroBrain.analisar_risco_aplicacao(temp, umid, delta_t)
        st.markdown(f"**Condição:** <span style='color:{cor_ap}'>{status_ap}</span>", unsafe_allow_html=True)
        for t, d in alertas: st.error(f"{t}: {d}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 3: RADAR
    with tabs[2]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                with cols[i]:
                    bg = "#fee2e2" if r['Chuva']=="Sim" else "#ecfdf5"
                    st.markdown(f"<div style='background:{bg}; padding:10px; text-align:center;'>{r['Direcao']}<br><b>{r['Temp']:.0f}°</b></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 4: IA
    with tabs[3]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        img = st.camera_input("Foto")
        if img and url_g:
            genai.configure(api_key=url_g)
            try: st.markdown(genai.GenerativeModel('gemini-1.5-flash').generate_content(["Diagnóstico agro", Image.open(img)]).text)
            except: st.error("Erro AI")
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 5: GESTÃO
    with tabs[4]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2,1,1])
        i = c1.text_input("Item")
        v = c2.number_input("Valor", min_value=0.0)
        if c3.button("➕") and i: st.session_state['custos'].append({"Data": date.today(), "Item": i, "Valor": v}); st.rerun()
        if st.session_state['custos']: st.dataframe(pd.DataFrame(st.session_state['custos']), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 6: MAPA
    with tabs[5]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            nm = st.text_input("Ponto")
            if st.button("Gravar") and st.session_state.get('last'): 
                st.session_state['pontos_mapa'].append({"n": nm, "lat": st.session_state['last'][0], "lon": st.session_state['last'][1]}); st.rerun()
            for p in st.session_state['pontos_mapa']: st.markdown(f"📍 {p['n']}")
        with c2:
            m = folium.Map([st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=15)
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Sat').add_to(m)
            LocateControl().add_to(m); Draw(export=True).add_to(m)
            for p in st.session_state['pontos_mapa']: folium.Marker([p['lat'], p['lon']], popup=p['n']).add_to(m)
            out = st_folium(m, height=500, returned_objects=["last_clicked"])
            if out["last_clicked"]: st.session_state['last'] = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])
        st.markdown('</div>', unsafe_allow_html=True)

    # ABA 7: LAUDO
    with tabs[6]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        obs = st.text_area("Notas")
        if st.button("Gerar PDF"):
            diag = AgroBrain.get_info_segura(dados_fase, ['desc', 'diagnostico'])
            man = AgroBrain.get_info_segura(dados_fase, ['manejo'])
            st.markdown(f"<div style='background:white; color:black; padding:20px;'><h1>LAUDO</h1><p><b>{cult_sel}</b></p><p>{diag}</p><p>{man}</p><p>{obs}</p></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ABA 8: NOTIFICAÇÕES
    with tabs[7]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 🔔 Central de Notificações")
        st.markdown("Receba análises diárias de clima e manejo agronômico direto no seu e-mail.")
        
        with st.form("form_notificacao"):
            col_n1, col_n2 = st.columns(2)
            nome_user = col_n1.text_input("Seu Nome")
            email_user = col_n2.text_input("Seu E-mail")
            
            # Pega as culturas do banco de dados
            opcoes_culturas = sorted(list(BANCO_MASTER.keys())) if BANCO_MASTER else []
            culturas_subs = st.multiselect("Quais culturas você quer monitorar?", options=opcoes_culturas, default=[cult_sel] if cult_sel in opcoes_culturas else None)
            
            c_btn1, c_btn2 = st.columns([1,3])
            salvar = c_btn1.form_submit_button("💾 Salvar Assinatura")
            
            if salvar:
                if nome_user and email_user and culturas_subs:
                    NotificationSystem.salvar_assinatura(nome_user, email_user, culturas_subs)
                    st.success(f"✅ Perfeito, {nome_user}! Você receberá relatórios sobre: {', '.join(culturas_subs)}.")
                else:
                    st.error("Preencha todos os campos.")

        st.divider()
        st.markdown("#### 🚀 Teste de Envio Instantâneo")
        st.caption("Use este botão para testar se o sistema está funcionando agora mesmo.")
        
        if st.button("📧 Enviar Relatório Agora"):
            if not email_user:
                st.warning("Preencha o e-mail acima primeiro.")
            else:
                with st.spinner("Compilando dados climáticos e agronômicos..."):
                    # SIMULAÇÃO DA INTELIGÊNCIA (Aqui entraria seu código de clima real)
                    dados_simulados = {}
                    for c in culturas_subs:
                        dados_simulados[c] = f"Previsão de 15mm de chuva. Fase fenológica requer atenção com fungos. Delta T favorável pela manhã."
                    
                    sucesso, msg = NotificationSystem.enviar_email_agora(nome_user, email_user, culturas_subs, dados_simulados)
                    
                    if sucesso: st.balloons(); st.success(msg)
                    else: st.error(msg)
                    
        st.markdown('</div>', unsafe_allow_html=True)
