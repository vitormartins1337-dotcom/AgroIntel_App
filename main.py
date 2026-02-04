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

                                
                    # 5. GESTÃO (SIMULADOR DE VIABILIDADE ECONÔMICA)
    with tabs[4]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        # --- 1. CÉREBRO AGRONÔMICO (DADOS DE REFERÊNCIA) ---
        # Aqui está a inteligência. O sistema sabe a média de produção por nível tecnológico.
        AGRO_INTELLIGENCE = {
            "Soja":    {"unidade": "ha", "prod": [50, 65, 85], "medida": "Sacas", "preco": 128.00, "custo_perc": 0.65}, # Custo 65% da receita
            "Milho":   {"unidade": "ha", "prod": [100, 140, 180], "medida": "Sacas", "preco": 58.00, "custo_perc": 0.70},
            "Café":    {"unidade": "ha", "prod": [25, 35, 55], "medida": "Sacas", "preco": 1150.00, "custo_perc": 0.60},
            "Algodão": {"unidade": "ha", "prod": [250, 320, 400], "medida": "@", "preco": 145.00, "custo_perc": 0.75},
            
            # Fruticultura / Perenes (Cálculo por PLANTA/PÉ) - Ideal para pequenos/médios
            "Citros":  {"unidade": "pé", "prod": [2.0, 3.5, 5.0], "medida": "Cx 40kg", "preco": 45.00, "custo_perc": 0.40},
            "Mirtilo": {"unidade": "pé", "prod": [1.5, 3.0, 5.0], "medida": "Kg", "preco": 45.00, "custo_perc": 0.50},
            "Uva":     {"unidade": "pé", "prod": [8.0, 12.0, 20.0], "medida": "Kg", "preco": 9.00, "custo_perc": 0.55},
            "Tomate":  {"unidade": "pé", "prod": [4.0, 7.0, 10.0], "medida": "Cx 20kg", "preco": 70.00, "custo_perc": 0.60},
            "Banana":  {"unidade": "pé", "prod": [15, 25, 40], "medida": "Kg", "preco": 3.00, "custo_perc": 0.40},
        }

        # Carrega inteligência da cultura selecionada
        # Se não tiver, usa padrão genérico
        ref = AGRO_INTELLIGENCE.get(cult_sel, {"unidade": "ha", "prod": [1, 2, 3], "medida": "Unid", "preco": 10.0, "custo_perc": 0.5})

        st.markdown(f"### 📈 Simulador de Viabilidade: **{cult_sel}**")
        st.caption("Planejamento financeiro baseado no seu nível tecnológico.")

        # --- 2. INPUTS SIMPLIFICADOS (O USUÁRIO SÓ INFORMA O BÁSICO) ---
        
        c_in1, c_in2 = st.columns([1, 2])
        
        with c_in1:
            # Pergunta 1: Quanto você tem?
            txt_label = "Área Total (Hectares)" if ref["unidade"] == "ha" else "Nº de Plantas/Pés"
            qtd = st.number_input(txt_label, min_value=1.0, value=100.0 if ref["unidade"] == "pé" else 50.0, step=1.0)

        with c_in2:
            # Pergunta 2: Qual seu nível de tecnologia? (Isso muda a produtividade automaticamente)
            nivel_tec = st.select_slider(
                "Nível Tecnológico / Manejo", 
                options=["Baixo (Tradicional)", "Médio (Tecnificado)", "Alto (Precisão)"],
                value="Médio (Tecnificado)"
            )
            
            # Define o índice da lista de produtividade (0, 1 ou 2)
            idx_tec = 0 if "Baixo" in nivel_tec else 1 if "Médio" in nivel_tec else 2
            prod_estimada = ref["prod"][idx_tec]

        st.divider()

        # --- 3. O CÁLCULO MÁGICO (MOTOR FINANCEIRO) ---
        
        # Produção Total
        total_colheita = qtd * prod_estimada
        
        # Receita Bruta (Entrada de Dinheiro)
        receita_bruta = total_colheita * ref["preco"]
        
        # Custo Estimado (Baseado na margem setorial)
        custo_operacional = receita_bruta * ref["custo_perc"]
        
        # Lucro (O que sobra)
        lucro_estimado = receita_bruta - custo_operacional
        margem_lucro = (lucro_estimado / receita_bruta) * 100

        # --- 4. APRESENTAÇÃO DE RESULTADOS (VISUAL ESTRATÉGICO) ---
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            # CARTÃO PRODUÇÃO
            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:15px; text-align:center;">
                <div style="color:#64748b; font-size:0.75rem; font-weight:bold;">EXPECTATIVA DE COLHEITA</div>
                <div style="color:#0f172a; font-size:1.8rem; font-weight:800;">{total_colheita:,.0f}</div>
                <div style="background:#e2e8f0; color:#475569; font-size:0.7rem; padding:2px; border-radius:4px; margin-top:5px;">
                    {prod_estimada} {ref['medida']} por {ref['unidade']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res2:
            # CARTÃO CUSTO (ALERTA)
            st.markdown(f"""
            <div style="background:#fff1f2; border:1px solid #fda4af; border-radius:10px; padding:15px; text-align:center;">
                <div style="color:#9f1239; font-size:0.75rem; font-weight:bold;">CUSTO ESTIMADO</div>
                <div style="color:#be123c; font-size:1.4rem; font-weight:800;">R$ {custo_operacional/1000:,.1f} k</div>
                <div style="color:#9f1239; font-size:0.7rem; margin-top:5px;">
                    ~{ref['custo_perc']*100:.0f}% da Receita
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res3:
            # CARTÃO LUCRO (SUCESSO)
            st.markdown(f"""
            <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:10px; padding:15px; text-align:center;">
                <div style="color:#166534; font-size:0.75rem; font-weight:bold;">LUCRO LÍQUIDO</div>
                <div style="color:#16a34a; font-size:1.4rem; font-weight:800;">R$ {lucro_estimado/1000:,.1f} k</div>
                <div style="color:#15803d; font-size:0.7rem; margin-top:5px;">
                    Margem: {margem_lucro:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # --- 5. FERRAMENTAS DE MERCADO (O "BUSCADOR") ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🔎 Inteligência Comercial")
        st.caption(f"Preço base utilizado: R$ {ref['preco']:.2f} / {ref['medida']}. Pesquise compradores reais abaixo:")
        
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            # Botão Inteligente 1: Busca Preço no Google
            link_preco = f"https://www.google.com/search?q=preço+{cult_sel}+hoje+cotacao"
            st.link_button(f"💰 Ver Cotação Atual ({cult_sel})", link_preco, use_container_width=True)
            
        with c_b2:
            # Botão Inteligente 2: Busca Compradores na Região
            # Se tiver cidade definida, busca lá. Se não, busca geral.
            local_busca = city if city else "na minha região"
            link_comprador = f"https://www.google.com/search?q=compradores+de+{cult_sel}+{local_busca}"
            st.link_button(f"🤝 Encontrar Compradores", link_comprador, use_container_width=True)

        st.info("💡 **Dica Profissional:** O Lucro real depende do seu controle de custos. Use a Aba **Alertas** para monitorar riscos climáticos que podem causar quebra de safra.")
        
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
