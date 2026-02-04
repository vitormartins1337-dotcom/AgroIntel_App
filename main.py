# ARQUIVO: main.py
# SISTEMA: AGRO SDI | ENTERPRISE EDITION
# VERSÃO: V-GESTÃO-360 (Estimativa de Safra + Financeiro Real)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, datetime
import folium
from folium.plugins import LocateControl, Fullscreen, Draw
from streamlit_folium import st_folium
import os
import json

# --- 1. SETUP & SEGURANÇA ---
try:
    from data_engine import get_database
    from calc_engine import AgroPhysics, WeatherConn
    from styles import load_css
    from agro_utils import AgroBrain
    from notification_engine import NotificationSystem
    import market_engine 
except ImportError as e:
    st.error(f"⚠️ Erro Crítico de Sistema: {e.name} não encontrado.")
    st.stop()

st.set_page_config(page_title="Agro SDI", page_icon="🌱", layout="wide")
load_css() 

# --- 2. VARIÁVEIS DE SESSÃO (PERSISTÊNCIA) ---
if 'loc_lat' not in st.session_state: st.session_state['loc_lat'] = -13.414
if 'loc_lon' not in st.session_state: st.session_state['loc_lon'] = -41.285
if 'pontos_mapa' not in st.session_state: st.session_state['pontos_mapa'] = [] # MIP
if 'custos_safra' not in st.session_state: st.session_state['custos_safra'] = [] # Gestão
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
            <h1 style="color:#064e3b; margin:0; font-size:2.5rem;">AGRO SDI</h1>
            <p style="color:#6b7280; font-weight:bold; margin-top:10px; letter-spacing:1px;">PLATAFORMA INTEGRADA DE GESTÃO</p>
        </div>""", unsafe_allow_html=True)
        kw = st.text_input("CHAVE OPENWEATHER", type="password")
        kg = st.text_input("CHAVE GEMINI (Opcional)", type="password") # Deixei opcional pois tiramos a aba IA
        if st.button("ACESSAR PAINEL", type="primary", use_container_width=True):
            if kw: 
                st.query_params["w_key"] = kw
                st.query_params["g_key"] = kg
                st.rerun()
    st.stop()

# ==============================================================================
# 💎 HEADER & TICKER
# ==============================================================================
ticker_html = market_engine.MarketData.get_ticker_real()

st.markdown(f"""
<div class="header-wrapper">
    <div>
        <h1 style="margin:0; font-family:sans-serif; font-weight:900; font-size:1.8rem; letter-spacing:-1px;">
            AGRO <span style="color:#34d399;">SDI</span>
        </h1>
        <div style="font-size:0.7rem; letter-spacing:2px; opacity:0.9; margin-top:5px; font-weight:bold;">
            SISTEMA DE DECISÃO INTEGRADA
        </div>
    </div>
    <div class="status-badge">
        <span class="status-dot"></span>
        ONLINE
    </div>
</div>
<div class="ticker-container">
    <div class="ticker-text">{ticker_html}</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 💎 FILTROS GLOBAIS
# ==============================================================================
st.markdown('<div class="app-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 2, 1.5, 1])

with c1:
    st.markdown("### 📍 Unidade")
    city = st.text_input("GPS", placeholder="Fazenda...", label_visibility="collapsed")
    if st.button("📡 Sincronizar GPS", use_container_width=True) and city:
        lat, lon = WeatherConn.get_coords(city, url_w)
        if lat: st.session_state['loc_lat'], st.session_state['loc_lon'] = lat, lon; st.rerun()

with c2:
    st.markdown("### 🚜 Cultura")
    if BANCO_MASTER:
        cult_sel = st.selectbox("Cultura", sorted(list(BANCO_MASTER.keys())), label_visibility="collapsed")
        vars_disp = list(BANCO_MASTER[cult_sel].get('vars', {}).keys())
        fases_disp = list(BANCO_MASTER[cult_sel].get('fases', {}).keys())
        var_sel = st.selectbox("Genética", vars_disp)
    else: st.error("Banco de Dados Offline"); st.stop()

with c3:
    st.markdown("### 📊 Fase")
    fase_sel = st.selectbox("Estádio", fases_disp, label_visibility="collapsed")

with c4:
    st.markdown("### 📆 Safra")
    st.session_state['d_plantio'] = st.date_input("Plantio", st.session_state['d_plantio'], label_visibility="collapsed")
    dias = (date.today() - st.session_state['d_plantio']).days

st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESSAMENTO PRINCIPAL ---
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
    with c3: st.markdown(AgroBrain.gerar_cartao_kpi("💨 VPD (Pressão)", f"{vpd:.2f}", "kPa", v_st, v_cor), unsafe_allow_html=True)
    with c4: st.markdown(AgroBrain.gerar_cartao_kpi("☀️ GDA Acumulado", f"{gda_acum:.0f}", "°GD", f"Ciclo: {dias}d", "#1e293b"), unsafe_allow_html=True)

    # ==============================================================================
    # 💎 ABAS DE NAVEGAÇÃO (NOVA ORDEM)
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    # Removemos IA e Laudo, adicionamos Gestão em destaque
    tabs = st.tabs(["🧬 TÉCNICO", "☁️ CLIMA", "📡 RADAR", "🗺️ MAPA", "💰 GESTÃO", "🔔 ALERTAS"])

    # 1. TÉCNICO
    with tabs[0]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.caption(f"Evolução do Ciclo: {progresso*100:.1f}%")
        st.progress(progresso)

        # Imagem da Cultura
        nome_cultura = str(cult_sel).lower()
        mapa_img = {"soja": "soja", "milho": "milho", "algodão": "algodao", "algodao": "algodao", "café": "cafe", "cafe": "cafe", "feijão": "feijao", "feijao": "feijao", "trigo": "trigo", "tomate": "tomate", "batata": "batata", "uva": "uva", "banana": "banana", "citros": "citros", "manga": "manga"}
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
            if img_path: st.image(img_path, caption=f"Fase: {fase_sel}", use_container_width=True)
            else: st.image("https://images.unsplash.com/photo-1625246333195-58197bd47d26?q=80&w=1000&auto=format&fit=crop", caption="Imagem Ilustrativa", use_container_width=True)

        st.divider()
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
        st.markdown('<div class="section-title">🛡️ MANEJO</div>', unsafe_allow_html=True)
        manejo_txt = AgroBrain.get_info_segura(dados_fase, ['manejo'])
        st.warning(f"🎯 **Recomendação:** {manejo_txt}")
        
        st.markdown("### 🧪 Defensivos Sugeridos")
        AgroBrain.render_protocolo_quimico(dados_fase.get('quimica')) 
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. CLIMA
    with tabs[1]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 📅 Tendência Semanal")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Consumo (ETc)', line=dict(color='#ef4444', width=3)))
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        df_hora = WeatherConn.get_hourly_forecast(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        if not df_hora.empty:
            st.markdown("### 🕒 Detalhe 24 Horas")
            fig_h = go.Figure()
            fig_h.add_trace(go.Scatter(x=df_hora['HoraSimples'], y=df_hora['Temp'], name='Temp', mode='lines+markers+text', text=[f"{t:.0f}°" for t in df_hora['Temp']], textposition="top center", line=dict(color='#f97316', width=3), fill='tozeroy', fillcolor='rgba(249, 115, 22, 0.1)'))
            fig_h.update_layout(title="Variação Térmica", height=250, margin=dict(l=20, r=20, t=40, b=20), yaxis=dict(showgrid=False))
            st.plotly_chart(fig_h, use_container_width=True)

            st.markdown("#### 🚜 Janela Delta T")
            cores_dt = ["#16a34a" if 2 <= dt <= 8 else "#ca8a04" if 8 < dt <= 10 else "#dc2626" for dt in df_hora['Delta T']]
            fig_dt = go.Figure()
            fig_dt.add_trace(go.Bar(x=df_hora['HoraSimples'], y=df_hora['Delta T'], marker_color=cores_dt, text=df_hora['Delta T'], textposition='auto'))
            fig_dt.add_hrect(y0=2, y1=8, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Ideal")
            fig_dt.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_dt, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. RADAR (VISUAL MASTER)
    with tabs[2]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 📡 Monitoramento Regional")
        st.caption("Dados em tempo real das estações meteorológicas vizinhas.")
        
        df_r = WeatherConn.get_radar_simulation(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        
        if not df_r.empty:
            cols = st.columns(4)
            for i, r in df_r.iterrows():
                # Lógica Visual
                if r['Chuva'] == "Sim":
                    cor_fundo, cor_borda, icon, txt, cor_txt = "#fef2f2", "#fca5a5", "🌧️", "Chuva", "#991b1b"
                else:
                    cor_fundo, cor_borda, icon, txt, cor_txt = "#f0fdf4", "#86efac", "☀️", "Limpo", "#166534"

                html_radar = f"""
                <div style="background-color:{cor_fundo}; border:1px solid {cor_borda}; border-radius:12px; padding:15px; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
                    <div style="font-size:0.7rem; font-weight:700; text-transform:uppercase; color:#64748b; margin-bottom:5px;">📍 {r['Direcao']}</div>
                    <div style="font-size:2rem; font-weight:800; color:#0f172a; line-height:1;">{r['Temp']:.0f}°</div>
                    <div style="margin-top:8px; font-size:0.8rem; font-weight:700; color:{cor_txt}; background:rgba(255,255,255,0.5); padding:4px; border-radius:6px;">{icon} {txt}</div>
                </div>"""
                with cols[i]: st.markdown(html_radar, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. MAPA (MIP SYNGENTA STYLE)
    with tabs[3]:
        # Carrega histórico
        DB_FILE = "monitoramento_campo.json"
        def carregar_dados_mip():
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f: return json.load(f)
            return []
        def salvar_dados_mip(novo):
            d = carregar_dados_mip()
            d.append(novo)
            with open(DB_FILE, "w") as f: json.dump(d, f)
            return d

        historico_real = carregar_dados_mip()
        DB_IMAGENS = {
            "Lagarta-do-cartucho": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Spodoptera_frugiperda_back.jpg/320px-Spodoptera_frugiperda_back.jpg",
            "Percevejo-marrom": "https://live.staticflickr.com/65535/49086326938_5f470375e8_w.jpg",
            "Ferrugem Asiática": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Phakopsora_pachyrhizi_on_Soybean_02.jpg/320px-Phakopsora_pachyrhizi_on_Soybean_02.jpg",
            "Cigarrinha-do-milho": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Dalbulus_maidis.jpg/320px-Dalbulus_maidis.jpg"
        }

        st.markdown('<div class="app-card" style="padding:0px; overflow:hidden;">', unsafe_allow_html=True)
        c_h1, c_h2 = st.columns([3, 1])
        with c_h1:
            st.markdown(f"### 🎯 MIP: **{cult_sel}**")
            st.caption(f"Pontos Coletados: {len(historico_real)}")
        with c_h2: st.button("🔄 Sync", use_container_width=True)

        m = folium.Map(location=[st.session_state['loc_lat'], st.session_state['loc_lon']], zoom_start=18, tiles=None, control_scale=True)
        folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite HD', overlay=False).add_to(m)
        
        if len(historico_real) > 1:
            caminho = [[p['lat'], p['lon']] for p in historico_real if p.get('Cultura') == str(cult_sel)]
            if caminho: folium.PolyLine(caminho, color="#fbbf24", weight=3, opacity=0.8, dash_array='10').add_to(m)

        for p in historico_real:
            cor_icon = "red" if p['Nivel'] == "Alto" else "orange" if p['Nivel'] == "Médio" else "#4ade80"
            folium.Marker([p['lat'], p['lon']], popup=f"<b>{p['Praga']}</b><br>{p['Nivel']}", icon=folium.Icon(color="black", icon_color=cor_icon, icon="bug", prefix="fa")).add_to(m)

        LocateControl(auto_start=True).add_to(m)
        map_data = st_folium(m, height=480, returned_objects=["last_clicked"])

        st.divider()

        lat_f = map_data["last_clicked"]["lat"] if map_data and map_data["last_clicked"] else None
        lon_f = map_data["last_clicked"]["lng"] if map_data and map_data["last_clicked"] else None

        if lat_f:
            st.markdown(f"<div style='background:#f0fdf4; padding:10px; border-radius:8px; margin-bottom:15px;'>📍 <b>PONTO CAPTURADO!</b></div>", unsafe_allow_html=True)
            with st.form("form_mip_master"):
                c_sel, c_foto = st.columns([1.5, 1])
                with c_sel:
                    tipo = st.radio("Categoria", ["🐛 Praga", "🍄 Doença", "🌿 Daninha"], horizontal=True)
                    sugestoes = ["Lagarta-do-cartucho", "Percevejo-marrom", "Ferrugem Asiática"] if str(cult_sel) == "Soja" else ["Cigarrinha-do-milho", "Pulgão"] if str(cult_sel) == "Milho" else ["Outro"]
                    praga_sel = st.selectbox("Agente", sugestoes + ["Outro..."])
                    nivel = st.select_slider("Severidade", ["Baixo", "Médio", "Alto"], value="Médio")
                with c_foto:
                    img_url = DB_IMAGENS.get(praga_sel, "https://via.placeholder.com/150?text=Sem+Foto")
                    st.image(img_url, caption="Referência", use_container_width=True)
                
                if st.form_submit_button("✅ SALVAR", type="primary", use_container_width=True):
                    novo_registro = {"Data": date.today().strftime("%d/%m/%Y"), "Cultura": str(cult_sel), "Tipo": tipo, "Praga": praga_sel, "Nivel": nivel, "lat": lat_f, "lon": lon_f}
                    salvar_dados_mip(novo_registro)
                    st.rerun()
        else:
            st.info("👆 Toque no mapa para identificar uma ocorrência.")
        st.markdown('</div>', unsafe_allow_html=True)

                                
                    # 5. GESTÃO (SIMULADOR DE NEGÓCIO - CORRIGIDO E PRÁTICO)
    with tabs[4]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        # --- 1. BANCO DE DADOS INTELIGENTE (CORRIGIDO) ---
        # input_type: 'area' (Hectares) ou 'planta' (Pés/Unidades)
        # prod_factors: [Baixa Tec, Média Tec, Alta Tec] -> Quanto rende por unidade de entrada
        
        AGRO_PLAN = {
            # GRÃOS (Extensivos -> Hectares)
            "Soja":      {"input": "area", "label": "Hectares", "prod": [50, 65, 85],   "medida_final": "Sacas", "preco": 128.00},
            "Milho":     {"input": "area", "label": "Hectares", "prod": [100, 140, 180], "medida_final": "Sacas", "preco": 58.00},
            "Algodão":   {"input": "area", "label": "Hectares", "prod": [250, 320, 400], "medida_final": "@",     "preco": 145.00},
            "Trigo":     {"input": "area", "label": "Hectares", "prod": [40, 60, 80],    "medida_final": "Sacas", "preco": 85.00},
            
            # PERENES E FRUTAS (Intensivos -> Pés/Plantas)
            # Café: Pede PÉS -> Entrega SACAS (Conversão automática: ~0.01 a 0.02 sacas/pé)
            "Café":      {"input": "planta", "label": "Pés/Plantas", "prod": [0.010, 0.015, 0.025], "medida_final": "Sacas (60kg)", "preco": 1150.00},
            
            # Frutas Pequenas: Pede PÉS -> Entrega KG
            "Framboesa": {"input": "planta", "label": "Pés/Mudas",   "prod": [0.5, 1.2, 2.5],    "medida_final": "Kg",      "preco": 60.00}, # Alto valor
            "Mirtilo":   {"input": "planta", "label": "Pés/Mudas",   "prod": [1.0, 2.5, 4.0],    "medida_final": "Kg",      "preco": 45.00},
            "Uva":       {"input": "planta", "label": "Pés/Videiras","prod": [8.0, 15.0, 25.0],  "medida_final": "Kg",      "preco": 9.50},
            
            # Frutas Grandes: Pede PÉS -> Entrega CAIXAS/KG
            "Citros":    {"input": "planta", "label": "Árvores",     "prod": [2.0, 3.5, 5.0],    "medida_final": "Cx 40.8kg", "preco": 45.00},
            "Tomate":    {"input": "planta", "label": "Pés",         "prod": [4.0, 7.0, 10.0],   "medida_final": "Cx 20kg",   "preco": 70.00},
            "Banana":    {"input": "planta", "label": "Touceiras",   "prod": [15.0, 30.0, 50.0], "medida_final": "Kg",        "preco": 3.00},
        }

        # Carrega dados ou usa genérico se a cultura não estiver na lista
        dados = AGRO_PLAN.get(cult_sel, {"input": "area", "label": "Unidades", "prod": [1, 1, 1], "medida_final": "Unid", "preco": 1.0})

        st.markdown(f"### 📊 Calculadora de Potencial: **{cult_sel}**")
        st.caption("Estimativa de colheita baseada no seu volume de plantio.")

        # --- 2. INPUT INTUITIVO (Pergunta o que faz sentido) ---
        
        c_i1, c_i2, c_i3 = st.columns([1.2, 1.5, 1])
        
        with c_i1:
            # Pergunta Dinâmica: "Quantos Pés?" ou "Quantos Hectares?"
            qtd_input = st.number_input(
                f"Quantos {dados['label']} você tem?", 
                min_value=1.0, 
                value=1000.0 if dados['input'] == 'planta' else 50.0, 
                step=1.0 if dados['input'] == 'planta' else 0.5,
                help="Quantidade total plantada."
            )

        with c_i2:
            # Nível Tecnológico (Define a produtividade unitária)
            tec = st.select_slider(
                "Nível Tecnológico", 
                options=["Baixo (Simples)", "Médio (Padrão)", "Alto (Intensivo)"],
                value="Médio (Padrão)"
            )
            # Pega o índice 0, 1 ou 2
            idx = 0 if "Baixo" in tec else 1 if "Médio" in tec else 2
            fator_prod = dados['prod'][idx]

        with c_i3:
            # Mostra o fator usado para educação do usuário
            st.metric(f"Rendimento Esp.", f"{fator_prod:.3f}", f"{dados['medida_final']}/{dados['label'][:-1]}")

        st.divider()

        # --- 3. RESULTADO DIRETO (POTENCIAL BRUTO) ---
        # O usuário pediu "Dado bruto aproximado"
        
        producao_potencial = qtd_input * fator_prod
        receita_bruta = producao_potencial * dados['preco']

        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            # BALÃO DE PRODUÇÃO (O que importa pro produtor)
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                border: 1px solid #bae6fd; 
                border-radius: 12px; 
                padding: 20px; 
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            ">
                <div style="color:#0284c7; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">POTENCIAL PRODUTIVO</div>
                <div style="color:#0369a1; font-size:2.2rem; font-weight:900; line-height:1.2;">
                    {producao_potencial:,.1f}
                </div>
                <div style="background:#0ea5e9; color:white; font-size:0.8rem; font-weight:bold; padding:4px 10px; border-radius:15px; display:inline-block; margin-top:5px;">
                    {dados['medida_final'].upper()} TOTAIS
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
            # BALÃO FINANCEIRO (Estimativa Bruta)
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                border: 1px solid #86efac; 
                border-radius: 12px; 
                padding: 20px; 
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            ">
                <div style="color:#16a34a; font-size:0.8rem; font-weight:bold; letter-spacing:1px;">VALOR BRUTO ESTIMADO</div>
                <div style="color:#15803d; font-size:2.2rem; font-weight:900; line-height:1.2;">
                    R$ {receita_bruta/1000:,.1f} k
                </div>
                <div style="color:#166534; font-size:0.8rem; margin-top:10px;">
                    Baseado em R$ {dados['preco']:.2f} / {dados['medida_final']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Nota: Este cálculo considera o **Potencial Produtivo** da planta. Fatores climáticos, pragas e manejo podem alterar o resultado real.")

        # --- 4. LINKS DE AÇÃO RÁPIDA (GOOGLE) ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🌍 Inteligência de Mercado")
        
        c_btn1, c_btn2 = st.columns(2)
        local_user = city if city else "na minha região"
        
        with c_btn1:
            # Botão 1: Buscar Compradores
            termos_busca = f"compradores de {cult_sel} {local_user} atacado"
            st.link_button(f"🤝 Quem compra {cult_sel}?", f"https://www.google.com/search?q={termos_busca}", use_container_width=True)
            
        with c_btn2:
            # Botão 2: Buscar Preço
            termos_preco = f"preço kg {cult_sel} hoje {local_user} ceasa"
            st.link_button(f"💰 Cotação Hoje no Google", f"https://www.google.com/search?q={termos_preco}", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. ALERTAS (CENTRAL DE CONFIGURAÇÃO)
    with tabs[5]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("### 🔔 Central de Automação")
        st.info("Configure aqui os alertas automáticos. No App Mobile, estas notificações chegarão como Push Notification.")
        
        with st.form("form_notificacao_pro"):
            st.markdown("#### 👤 Perfil do Assinante")
            col_n1, col_n2 = st.columns(2)
            nome_user = col_n1.text_input("Nome Responsável", value="Produtor")
            email_user = col_n2.text_input("E-mail Principal")
            
            st.markdown("#### ⚙️ Regras de Disparo")
            c_chk1, c_chk2 = st.columns(2)
            chk_chuva = c_chk1.checkbox("Alertar Chuva (>10mm)", value=True)
            chk_praga = c_chk1.checkbox("Alertar Risco de Pragas", value=True)
            chk_temp = c_chk2.checkbox("Alertar Alta Temperatura (>35°C)")
            chk_mercado = c_chk2.checkbox("Alertar Variação de Preço (>2%)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("💾 SALVAR CONFIGURAÇÃO", type="primary"):
                NotificationSystem.salvar_assinatura(nome_user, email_user, [cult_sel])
                st.success("✅ Configurações salvas no servidor!")
        
        st.divider()
        st.markdown("#### 🧪 Teste de Workflow")
        c_t1, c_t2 = st.columns([3,1])
        with c_t1: st.markdown("Disparar relatório imediato para validar o servidor de e-mail.")
        with c_t2:
            if st.button("📧 Enviar Agora"):
                if email_user:
                    dados_simulados = {str(cult_sel): f"Estimativa: {prod_liquida:.0f} sc | Preço: R$ {preco_venda}"}
                    ok, msg = NotificationSystem.enviar_email_agora(nome_user, email_user, [cult_sel], dados_simulados)
                    if ok: st.toast("E-mail enviado com sucesso!")
                    else: st.error(msg)
                else: st.warning("Preencha o e-mail acima.")
        st.markdown('</div>', unsafe_allow_html=True)
