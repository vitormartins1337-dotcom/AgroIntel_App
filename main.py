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
    st.markdown("### 📍 Local")
    city = st.text_input("GPS", placeholder="cidade,estado", label_visibility="collapsed")
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
    tabs = st.tabs(["🧬 TÉCNICO", "🧪 NUTRIÇÃO", "☁️ CLIMA", "📡 RADAR", "🗺️ MAPA", "💰 GESTÃO", "🔔 ALERTAS"])

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


                                                        # 2. NUTRIÇÃO (MARCHA DE ABSORÇÃO & MANEJO ESPECÍFICO - FONTE: MALAVOLTA/EMBRAPA)
    with tabs[1]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        # --- 1. CABEÇALHO ---
        st.markdown(f"### 🧪 Nutrição de Precisão: **{cult_sel}**")
        st.caption("Curvas de Absorção (Marcha) e Estratégias de Adubação.")

        # --- 2. BANCO DE DADOS MASTER (COM MANEJO ESPECÍFICO) ---
        # Adicionei a chave 'manejo_tatico' para cada cultura
        
        DB_NUTRI_MASTER = {
            "Soja": {
                "fases": ["V1", "V4", "R1 (Flor)", "R5 (Grão)", "R8 (Mat)"],
                "macros": {"N": [5, 30, 90, 240, 300], "P": [1, 5, 15, 25, 30], "K": [5, 25, 70, 95, 100], "Ca": [2, 15, 45, 75, 85], "Mg": [1, 5, 15, 25, 30], "S": [1, 5, 10, 18, 20]},
                "micros": {"Mn": [10, 80, 200, 300, 350], "Zn": [5, 40, 120, 200, 250], "B": [2, 10, 40, 80, 100]},
                "manejo_tatico": {
                    "N": "<b>NÃO APLICAR NITROGÊNIO MINERAL.</b> A soja obtém todo o N via Fixação Biológica (FBN). Invista em inoculante de qualidade e Molibdênio.",
                    "P": "Aplicar 100% no sulco de plantio. O Fósforo é imóvel e precisa estar logo abaixo da semente para o arranque.",
                    "K": "Se a dose for > 60kg/ha, aplicar metade no pré-plantio (a lanço) e metade no plantio (sulco, mas separado da semente) para evitar salinidade."
                }
            },
            "Milho": {
                "fases": ["V2", "V6", "VT", "R3", "R6"],
                "macros": {"N": [5, 45, 130, 190, 220], "P": [1, 10, 35, 45, 50], "K": [5, 60, 160, 175, 180], "Ca": [2, 15, 40, 50, 55], "Mg": [1, 8, 25, 35, 40], "S": [1, 5, 15, 25, 30]},
                "micros": {"Zn": [10, 120, 350, 450, 500], "Mn": [10, 90, 250, 320, 350], "B": [5, 20, 60, 90, 100]},
                "manejo_tatico": {
                    "N": "<b>FOME DE NITROGÊNIO:</b> Aplicar 30% no plantio e 70% em cobertura entre V4 e V6. Atrasar além de V8 causa perda irreversível de potencial.",
                    "P": "Total no sulco de plantio. O milho define o tamanho da espiga muito cedo (V4), precisa de P disponível imediatamente.",
                    "K": "Aplicar no plantio. Se solo arenoso, parcelar junto com o N em cobertura para evitar lixiviação."
                }
            },
            "Café": { 
                "fases": ["Veg", "Botão", "Chumbinho", "Expansão", "Maturação"],
                "macros": {"N": [30, 80, 150, 220, 280], "P": [3, 8, 18, 25, 30], "K": [25, 60, 120, 200, 260], "Ca": [20, 40, 70, 90, 100], "Mg": [5, 15, 30, 40, 45], "S": [5, 10, 20, 30, 35]},
                "micros": {"Fe": [200, 800, 1500, 2000, 2500], "B": [50, 200, 400, 550, 600], "Zn": [40, 150, 300, 400, 450]},
                "manejo_tatico": {
                    "N": "Parcelar em 3 ou 4 vezes durante o período chuvoso (Set a Mar). O café demanda N constante para vegetar e encher grão ao mesmo tempo.",
                    "P": "Aplicar fontes de liberação gradual ou termofosfatos. Essencial garantir níveis altos no solo antes da florada.",
                    "K": "Crucial na fase de <b>Expansão (Jan/Fev)</b>. Aplicar na projeção da saia. Cuidado com excesso que inibe absorção de Cálcio/Magnésio."
                }
            },
            "Algodão": {
                "fases": ["Emerg", "Botão", "Flor", "Maçã", "Abertura"],
                "macros": {"N": [5, 35, 95, 140, 160], "P": [1, 8, 25, 35, 40], "K": [5, 45, 110, 145, 155], "Ca": [2, 20, 60, 90, 100], "Mg": [1, 5, 15, 25, 30], "S": [1, 5, 15, 25, 30]},
                "micros": {"B": [10, 60, 180, 280, 320], "Zn": [10, 50, 120, 180, 200]},
                "manejo_tatico": {
                    "N": "Parcelar intensamente. Aplicar regulador de crescimento junto com N para evitar que a planta cresça demais e aborte maçãs.",
                    "P": "Essencial no balanço. Deficiência de P atrasa a maturação e a qualidade da fibra.",
                    "K": "Alta exigência na formação da maçã. Deficiência causa 'Oulakh' (fome de potássio) e fibra fraca."
                }
            },
            "Citros": {
                "fases": ["Brotação", "Flor", "Fruto I", "Fruto II", "Colheita"],
                "macros": {"N": [20, 60, 120, 180, 200], "P": [2, 8, 15, 20, 25], "K": [15, 50, 110, 170, 190], "Ca": [30, 80, 140, 180, 200], "Mg": [5, 15, 30, 40, 45], "S": [5, 15, 25, 35, 40]},
                "micros": {"Mn": [50, 200, 400, 500, 600], "Zn": [50, 200, 400, 500, 600], "B": [20, 80, 150, 200, 250]},
                "manejo_tatico": {
                    "N": "Parcelar em 3x: Brotação (Ago), Verão (Dez) e Final do Verão (Mar).",
                    "P": "Aplicar no sulco em pomares novos. Em produção, aplicar via foliar ou fertirrigação na florada.",
                    "K": "Afeta espessura da casca e acidez. Ajustar dose conforme análise de folha para não perder qualidade de suco."
                }
            },
            "Banana": {
                "fases": ["Cresc", "Flor", "Cacho", "Enchimento", "Colheita"],
                "macros": {"N": [30, 100, 250, 350, 400], "P": [5, 15, 40, 50, 60], "K": [50, 200, 600, 1200, 1500], "Ca": [20, 60, 150, 200, 220], "Mg": [10, 30, 80, 120, 140], "S": [10, 30, 60, 80, 100]},
                "micros": {"Mn": [100, 500, 1500, 2500, 3000], "Zn": [20, 100, 300, 500, 600], "B": [10, 50, 150, 250, 300]},
                "manejo_tatico": {
                    "N": "Aplicar mensalmente ou quinzenalmente. A planta emite folhas novas a cada 10 dias e precisa de N constante.",
                    "P": "Aplicar na cova de plantio. Em produção, usar superfosfato simples para fornecer S e Ca também.",
                    "K": "<b>BOMBA DE POTÁSSIO:</b> A banana extrai muito K. Repor a cada corte do cacho. Sem K, o cacho é pequeno e quebra."
                }
            },
            "Tomate": {
                "fases": ["Veg", "Flor 1", "Fruto 1", "Fruto Total", "Colheita"],
                "macros": {"N": [10, 40, 100, 180, 220], "P": [2, 10, 25, 35, 40], "K": [15, 60, 160, 280, 350], "Ca": [10, 40, 100, 160, 190], "Mg": [5, 15, 35, 50, 60], "S": [5, 15, 30, 45, 50]},
                "micros": {"Mn": [20, 150, 400, 600, 700], "B": [10, 50, 120, 200, 250], "Zn": [10, 60, 150, 250, 300]},
                "manejo_tatico": {
                    "N": "Cuidado com excesso na fase vegetativa (vício). Aumentar dose no enchimento.",
                    "P": "100% no transplante da muda. Raiz do tomate precisa de P abundante para pegar.",
                    "K": "Fundamental na maturação. Relação K/Ca deve ser monitorada para evitar podridão apical (fundo preto)."
                }
            },
            "Batata": {
                "fases": ["Emerg", "Estolon", "Tuber", "Enchimento", "Maturação"],
                "macros": {"N": [10, 50, 100, 140, 160], "P": [2, 10, 25, 35, 40], "K": [15, 60, 150, 250, 280], "Ca": [5, 20, 50, 70, 80], "Mg": [2, 10, 25, 35, 40], "S": [2, 8, 15, 25, 30]},
                "micros": {"Mn": [20, 100, 250, 400, 450], "B": [5, 20, 50, 80, 100], "Zn": [10, 40, 100, 150, 180]},
                "manejo_tatico": {
                    "N": "Aplicar no plantio e amontoa. Excesso atrasa a tuberização.",
                    "P": "Aplicar tudo no sulco. Aumenta o número de tubérculos por planta.",
                    "K": "Usar preferencialmente Sulfato de Potássio (menos cloro). O Cloro do KCl pode reduzir o teor de amido (qualidade de fritura)."
                }
            },
            "Feijão": {
                "fases": ["V2", "V4", "R5", "R7", "R9"],
                "macros": {"N": [5, 25, 60, 100, 120], "P": [1, 5, 12, 18, 20], "K": [5, 20, 50, 80, 90], "Ca": [3, 15, 40, 60, 70], "Mg": [2, 8, 15, 20, 25], "S": [1, 3, 8, 12, 15]},
                "micros": {"Fe": [50, 200, 600, 1000, 1200], "Mn": [20, 80, 200, 300, 350], "Zn": [10, 40, 100, 150, 180]},
                "manejo_tatico": {
                    "N": "Aplicar 1/3 no plantio e 2/3 em cobertura V4 (3ª folha trifoliada). Não atrase! O ciclo é curto demais para recuperar.",
                    "P": "Tudo no sulco. Raiz rasa e sensível.",
                    "K": "No plantio. Atenção ao contato com a semente (salinidade)."
                }
            },
            "Trigo": {
                "fases": ["Emerg", "Perfilho", "Along", "Espiga", "Grão"],
                "macros": {"N": [5, 30, 80, 110, 130], "P": [1, 8, 18, 22, 25], "K": [5, 25, 70, 90, 100], "Ca": [2, 10, 25, 35, 40], "Mg": [1, 5, 10, 15, 18], "S": [1, 4, 10, 15, 18]},
                "micros": {"Mn": [20, 100, 300, 400, 450], "Cu": [2, 10, 25, 35, 40], "Zn": [5, 20, 50, 70, 80]},
                "manejo_tatico": {
                    "N": "Base no plantio + Cobertura no Perfilhamento (define nº espigas) + Reforço no Espigamento (define proteína/glúten).",
                    "P": "No sulco. Essencial para perfilhamento vigoroso.",
                    "K": "No plantio. Ajuda na resistência ao acamamento (tombamento) e doenças."
                }
            },
            "Uva": {
                "fases": ["Brota", "Flor", "Varaison", "Maturação", "Colheita"],
                "macros": {"N": [15, 50, 90, 100, 110], "P": [2, 8, 15, 20, 25], "K": [10, 40, 90, 130, 150], "Ca": [10, 40, 80, 100, 110], "Mg": [5, 15, 30, 40, 45], "S": [2, 10, 20, 30, 35]},
                "micros": {"Fe": [50, 200, 500, 700, 800], "B": [10, 50, 100, 150, 180], "Zn": [10, 40, 100, 150, 200]},
                "manejo_tatico": {
                    "N": "Aplicar na brotação. Suspender N na maturação para não prejudicar cor e açúcar.",
                    "P": "Antes da brotação ou via fertirrigação.",
                    "K": "Aplicar parcelado a partir da 'chumbada' até a mudança de cor (Varaison) para garantir Brix (açúcar)."
                }
            },
            "Manga": {
                "fases": ["Veg", "Flor", "Chumbinho", "Expansão", "Colheita"],
                "macros": {"N": [20, 60, 100, 130, 150], "P": [5, 15, 25, 35, 40], "K": [15, 50, 110, 160, 180], "Ca": [15, 50, 100, 130, 150], "Mg": [5, 20, 40, 60, 70], "S": [5, 15, 30, 40, 50]},
                "micros": {"B": [10, 60, 120, 180, 200], "Fe": [50, 200, 600, 800, 1000], "Zn": [20, 80, 150, 200, 250]},
                "manejo_tatico": {
                    "N": "Estimula vegetação. Deve ser suspenso antes da indução floral para a planta 'estressar' e florir.",
                    "P": "Na poda de produção e florada.",
                    "K": "Junto com Cálcio e Boro na fase de chumbinho para segurar fruto."
                }
            },
            "Morango": {
                "fases": ["Plantio", "Flor", "Fruto Inic", "Pico", "Final"],
                "macros": {"N": [5, 25, 60, 100, 120], "P": [1, 8, 15, 25, 30], "K": [5, 30, 80, 150, 180], "Ca": [5, 25, 60, 90, 110], "Mg": [2, 10, 25, 40, 50], "S": [2, 8, 15, 25, 30]},
                "micros": {"Fe": [20, 100, 300, 500, 600], "Mn": [10, 50, 150, 250, 300], "B": [5, 20, 50, 80, 100]},
                "manejo_tatico": {
                    "N": "Via fertirrigação constante. Equilíbrio N:K de 1:1.5.",
                    "P": "Fundamental na implantação dos canteiros.",
                    "K": "Aumentar dose na frutificação para dar sabor. Cálcio semanalmente para firmeza."
                }
            },
            "Mirtilo": {
                "fases": ["Brota", "Flor", "Verde", "Matur", "Dorm"],
                "macros": {"N": [5, 20, 40, 60, 70], "P": [1, 3, 8, 12, 15], "K": [5, 15, 35, 55, 65], "Ca": [2, 10, 20, 30, 35], "Mg": [1, 5, 10, 15, 18], "S": [2, 8, 15, 20, 25]},
                "micros": {"Fe": [10, 50, 100, 150, 180], "Mn": [5, 20, 50, 80, 100]},
                "manejo_tatico": {
                    "N": "<b>ATENÇÃO:</b> Usar Sulfato de Amônio. O mirtilo prefere N amoniacal e odeia Nitrato em excesso. pH deve ser ácido (4.5-5.5).",
                    "P": "Baixa exigência, mas aplicar na brotação.",
                    "K": "Usar Sulfato de Potássio (livre de Cloro). Mirtilo é sensível a Cloreto."
                }
            },
            "Framboesa": {
                "fases": ["Veg", "Flor", "Verde", "Colheita", "Senesc"],
                "macros": {"N": [10, 30, 60, 80, 90], "P": [2, 8, 15, 20, 25], "K": [10, 35, 70, 100, 110], "Ca": [5, 20, 40, 60, 70], "Mg": [2, 8, 15, 25, 30], "S": [2, 8, 15, 20, 25]},
                "micros": {"Fe": [20, 80, 150, 200, 250], "B": [5, 15, 30, 45, 50]},
                "manejo_tatico": {
                    "N": "Parcelar na primavera/verão. Excesso gera ramos moles sujeitos a doenças.",
                    "P": "Aplicar anualmente no início da primavera.",
                    "K": "Vital para doçura. Aplique potássio durante a formação do fruto."
                }
            },
            "Cebola": {
                "fases": ["Mudas", "Cresc", "Bulbo", "Mat", "Estalo"],
                "macros": {"N": [5, 30, 90, 120, 130], "P": [1, 10, 25, 30, 35], "K": [5, 40, 110, 150, 160], "Ca": [3, 20, 60, 80, 90], "Mg": [2, 8, 20, 30, 35], "S": [2, 10, 30, 45, 50]},
                "micros": {"Mn": [10, 50, 150, 250, 300], "Zn": [5, 30, 80, 120, 150], "B": [2, 10, 30, 50, 60]},
                "manejo_tatico": {
                    "N": "Suspender N na fase de maturação para evitar rebrota e podridão no armazenamento.",
                    "P": "Todo no plantio. Define o sistema radicular.",
                    "K": "Melhora a qualidade da 'casca' e conservação pós-colheita."
                }
            },
            "Alho": {
                "fases": ["Emerg", "Veg", "Bulbo", "Mat", "Colheita"],
                "macros": {"N": [5, 40, 100, 120, 125], "P": [1, 10, 20, 25, 30], "K": [5, 45, 120, 140, 150], "Ca": [3, 25, 60, 70, 75], "Mg": [2, 10, 20, 30, 35], "S": [3, 15, 40, 55, 60]},
                "micros": {"Zn": [5, 40, 100, 130, 150], "B": [2, 15, 40, 60, 70]},
                "manejo_tatico": {
                    "N": "Fundamental no início (folhas). Suspender na diferenciação para não causar 'alho dente de cachorro' (superbrotamento).",
                    "P": "Sulco de plantio.",
                    "K": "Garante peso da cabeça."
                }
            },
            "Pastagens": {
                "fases": ["D0", "D10", "D20", "D30", "D45"],
                "macros": {"N": [5, 40, 100, 180, 250], "P": [2, 8, 18, 25, 30], "K": [5, 30, 90, 160, 220], "Ca": [2, 10, 30, 50, 60], "Mg": [1, 5, 15, 25, 30], "S": [1, 5, 15, 25, 30]},
                "micros": {"Mn": [10, 50, 150, 250, 300], "Zn": [5, 30, 80, 120, 150]},
                "manejo_tatico": {
                    "N": "Aplicar após cada pastejo/corte, com umidade no solo. É o motor da produção.",
                    "P": "Reposição anual. P baixo limita a resposta ao N.",
                    "K": "O gado recicla K (urina), mas em corte (feno) a extração é violenta e precisa repor."
                }
            }
        }

        # --- 3. SELEÇÃO DA CULTURA ---
        dados_nutri = None
        nome_cultura_exibicao = str(cult_sel)
        
        for chave in DB_NUTRI_MASTER:
            if chave.lower() in str(cult_sel).lower() or str(cult_sel).lower() in chave.lower():
                dados_nutri = DB_NUTRI_MASTER[chave]
                nome_cultura_exibicao = chave
                break
        
        if not dados_nutri and ("citrus" in str(cult_sel).lower() or "limão" in str(cult_sel).lower() or "laranja" in str(cult_sel).lower()):
            dados_nutri = DB_NUTRI_MASTER["Citros"]
            nome_cultura_exibicao = "Citros"

        if dados_nutri:
            
            # --- 4. PAINEL QUÍMICO ---
            st.markdown(f"#### ⚛️ Extração Total Estimada ({nome_cultura_exibicao})")
            st.caption("Quantidade total extraída (Grão/Fruto + Restos) para alta produtividade.")

            n_tot = dados_nutri['macros'].get('N', [0])[-1]
            p_tot = dados_nutri['macros'].get('P', [0])[-1]
            k_tot = dados_nutri['macros'].get('K', [0])[-1]
            ca_tot = dados_nutri['macros'].get('Ca', [0])[-1]
            mg_tot = dados_nutri['macros'].get('Mg', [0])[-1]
            s_tot = dados_nutri['macros'].get('S', [0])[-1]

            # CSS CORRIGIDO (LETRA ESCURA)
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(90px, 1fr)); gap: 10px; margin-bottom: 25px;">
                <div style="background:#f0fdf4; border:1px solid #16a34a; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#16a34a; font-size:1.3rem;">N</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{n_tot} kg</div>
                </div>
                <div style="background:#eff6ff; border:1px solid #2563eb; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#2563eb; font-size:1.3rem;">P</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{p_tot} kg</div>
                </div>
                <div style="background:#fef2f2; border:1px solid #dc2626; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#dc2626; font-size:1.3rem;">K</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{k_tot} kg</div>
                </div>
                <div style="background:#fffbeb; border:1px solid #d97706; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#d97706; font-size:1.3rem;">Ca</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{ca_tot} kg</div>
                </div>
                <div style="background:#faf5ff; border:1px solid #9333ea; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#9333ea; font-size:1.3rem;">Mg</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{mg_tot} kg</div>
                </div>
                <div style="background:#fff7ed; border:1px solid #ea580c; border-radius:8px; padding:10px; text-align:center; color:#0f172a;">
                    <div style="font-weight:900; color:#ea580c; font-size:1.3rem;">S</div>
                    <div style="font-size:0.9rem; font-weight:bold;">{s_tot} kg</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- 5. GRÁFICOS ---
            st.markdown("#### 1. Macronutrientes (N, K)")
            fig_big = go.Figure()
            colors_big = {'N': '#16a34a', 'K': '#dc2626'}
            for nutri in ['N', 'K']:
                fig_big.add_trace(go.Scatter(x=dados_nutri['fases'], y=dados_nutri['macros'][nutri], mode='lines+markers', name=nutri, line=dict(width=4, color=colors_big[nutri]), fill='tozeroy'))
            fig_big.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=20), yaxis=dict(title="kg/ha"))
            st.plotly_chart(fig_big, use_container_width=True)

            st.markdown("#### 2. Fósforo e Secundários (P, Ca, Mg, S)")
            fig_mid = go.Figure()
            colors_mid = {'P': '#2563eb', 'Ca': '#eab308', 'Mg': '#9333ea', 'S': '#f97316'}
            for nutri in ['P', 'Ca', 'Mg', 'S']:
                width_l = 5 if nutri == 'P' else 3
                fig_mid.add_trace(go.Scatter(x=dados_nutri['fases'], y=dados_nutri['macros'][nutri], mode='lines+markers', name=nutri, line=dict(width=width_l, color=colors_mid[nutri])))
            fig_mid.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=20), yaxis=dict(title="kg/ha"))
            st.plotly_chart(fig_mid, use_container_width=True)

            st.markdown("#### 3. Micronutrientes (g/ha)")
            fig_mic = go.Figure()
            colors_mic = {'B': '#ec4899', 'Zn': '#06b6d4', 'Mn': '#8b5cf6', 'Cu': '#f59e0b', 'Fe': '#64748b'}
            for nutri, vals in dados_nutri['micros'].items():
                fig_mic.add_trace(go.Scatter(x=dados_nutri['fases'], y=vals, mode='lines+markers', name=nutri, line=dict(width=2, dash='dot', color=colors_mic.get(nutri, '#555'))))
            fig_mic.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=20), yaxis=dict(title="g/ha"))
            st.plotly_chart(fig_mic, use_container_width=True)

            st.divider()

            # --- 6. MANEJO ESPECÍFICO (PROFISSIONAL E DINÂMICO) ---
            st.markdown("### 🚜 Estratégia de Manejo Específica")
            st.caption(f"Recomendações técnicas baseadas na fisiologia do(a) **{nome_cultura_exibicao}**.")
            
            c_ad1, c_ad2, c_ad3 = st.columns(3)
            
            # Recupera as dicas do dicionário ou usa um genérico de segurança
            manejo = dados_nutri.get('manejo_tatico', {
                "N": "Aplicar parcelado para evitar perdas.",
                "P": "Aplicar no plantio (imóvel).",
                "K": "Aplicar conforme análise de solo."
            })

            with c_ad1:
                st.markdown(f"""
                <div style="background:#eff6ff; border-top: 4px solid #2563eb; padding:15px; border-radius:8px; color:#0f172a; height:100%;">
                    <b style="color:#1e3a8a;">FÓSFORO (P)</b><hr style="margin:8px 0;">
                    <div style="font-size:0.85rem;">{manejo['P']}</div>
                </div>""", unsafe_allow_html=True)
                
            with c_ad2:
                st.markdown(f"""
                <div style="background:#f0fdf4; border-top: 4px solid #16a34a; padding:15px; border-radius:8px; color:#0f172a; height:100%;">
                    <b style="color:#14532d;">NITROGÊNIO (N)</b><hr style="margin:8px 0;">
                    <div style="font-size:0.85rem;">{manejo['N']}</div>
                </div>""", unsafe_allow_html=True)

            with c_ad3:
                st.markdown(f"""
                <div style="background:#fef2f2; border-top: 4px solid #dc2626; padding:15px; border-radius:8px; color:#0f172a; height:100%;">
                    <b style="color:#7f1d1d;">POTÁSSIO (K)</b><hr style="margin:8px 0;">
                    <div style="font-size:0.85rem;">{manejo['K']}</div>
                </div>""", unsafe_allow_html=True)

            # --- 7. AVISO LEGAL E FONTE (MANDATÓRIO) ---
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color: #fff7ed; border-left: 5px solid #f97316; padding: 20px; border-radius: 5px;">
                <h4 style="color: #9a3412; margin-top: 0;">⚠️ ALERTA AGRONÔMICO (LEIA COM ATENÇÃO)</h4>
                <p style="color: #7c2d12; font-size: 0.9rem; margin-bottom: 10px;">
                    <b>1. Demanda vs. Recomendação:</b> Estes gráficos mostram a <i>Marcha de Absorção</i> (o que a planta consome), 
                    NÃO a recomendação de adubação (o que você deve aplicar).
                </p>
                <p style="color: #7c2d12; font-size: 0.9rem; margin-bottom: 10px;">
                    <b>2. Lei do Mínimo:</b> O solo já possui reservas de nutrientes. Aplicar a quantidade total absorvida sem descontar 
                    o que já existe no solo pode causar toxicidade, salinidade e prejuízo financeiro.
                </p>
                <p style="color: #7c2d12; font-weight: bold; font-size: 0.95rem;">
                    🧪 RECOMENDAÇÃO OFICIAL: Faça sempre a ANÁLISE DE SOLO antes do plantio. Consulte um Engenheiro Agrônomo 
                    para calcular a dose exata baseada na "Lei de Restituição".
                </p>
                <hr style="border-color: #fdba74;">
                <p style="color: #9a3412; font-size: 0.7rem; margin-top: 5px;">
                    <i>Fontes de Dados: Malavolta (2006), Embrapa Soja/Milho/Café, IPNI Brasil. Dados baseados em média para alta produtividade.</i>
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("Dados em compilação.")

        st.markdown('</div>', unsafe_allow_html=True)
    
    
    # 3. CLIMA (CORRIGIDO E BLINDADO)
    with tabs[2]:
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        
        c_clim1, c_clim2 = st.columns([3, 1])
        with c_clim1:
            st.markdown("### 📅 Planejamento Climático")
        with c_clim2:
            hora_att = datetime.now().strftime("%H:%M")
            st.markdown(f"<div style='text-align:right; font-size:0.7rem; color:#64748b; margin-top:5px;'>🔄 Atualizado às: <b>{hora_att}</b></div>", unsafe_allow_html=True)

        # Gráfico Semanal (Mantido)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_clima['Data'], y=df_clima['Chuva'], name='Chuva (mm)', marker_color='#3b82f6'))
        fig.add_trace(go.Scatter(x=df_clima['Data'], y=df_clima['ETc'], name='Consumo (ETc)', line=dict(color='#ef4444', width=3)))
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=20), legend=dict(orientation="h", y=1.1), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # --- TABELA DE DETALHE HORÁRIO (CORREÇÃO DO ERRO) ---
        df_hora = WeatherConn.get_hourly_forecast(url_w, st.session_state['loc_lat'], st.session_state['loc_lon'])
        
        if not df_hora.empty:
            st.markdown("### 🕒 Detalhe Operacional (Próximas 24h)")
            st.caption("Analise as janelas de aplicação baseadas no Delta T.")

            # 1. Cria a coluna de Condição (Semáforo)
            def get_status_deltat(dt):
                if 2 <= dt <= 8: return "✅ IDEAL"
                elif 8 < dt <= 10: return "⚠️ ATENÇÃO"
                else: return "🚫 PARE"

            # Garante que a coluna Delta T existe antes de aplicar
            if 'Delta T' in df_hora.columns:
                df_hora['Condição'] = df_hora['Delta T'].apply(get_status_deltat)
            else:
                df_hora['Condição'] = "---"

            # 2. Seleção de Colunas Segura (Evita o KeyError)
            # Lista de colunas que QUEREMOS mostrar
            cols_desejadas = ['HoraSimples', 'Temp', 'Chuva', 'Umid', 'Vento', 'Delta T', 'Condição']
            
            # Filtra apenas as que REALMENTE EXISTEM no dataframe
            cols_finais = [c for c in cols_desejadas if c in df_hora.columns]
            
            # Cria a tabela de visualização apenas com o que existe
            df_view = df_hora[cols_finais].copy()
            
            # Renomeia para ficar bonito (se a coluna existir)
            mapa_nomes = {
                'HoraSimples': 'Horário',
                'Temp': 'Temp (°C)',
                'Chuva': 'Chuva (mm)',
                'Umid': 'Umid (%)',
                'Vento': 'Vento (km/h)',
                'Delta T': 'Delta T',
                'Condição': 'Status'
            }
            df_view.rename(columns=mapa_nomes, inplace=True)

            # 3. Exibição da Tabela
            st.dataframe(
                df_view,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Horário": st.column_config.TextColumn("Horário"),
                    "Temp (°C)": st.column_config.ProgressColumn(
                        "Temperatura", format="%.1f°", min_value=0, max_value=45
                    ),
                    "Chuva (mm)": st.column_config.NumberColumn("Chuva", format="%.1f mm"),
                    "Umid (%)": st.column_config.NumberColumn("Umidade", format="%d%%"),
                    "Delta T": st.column_config.NumberColumn("Delta T", format="%.1f", help="Ideal: 2 a 8"),
                    "Status": st.column_config.TextColumn("Janela Aplicação")
                }
            )
            
            # Legenda
            c_leg1, c_leg2 = st.columns(2)
            with c_leg1: st.info("💧 **Chuva:** Acumulado previsto na hora.")
            with c_leg2: st.warning("🛡️ **Delta T:** Ideal entre 2 e 8.")

        else:
            st.error("⚠️ Previsão horária indisponível no momento.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. RADAR (VISUAL MASTER)
    with tabs[3]:
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

    # 5. MAPA (MIP SYNGENTA STYLE - COM MODAL FLUTUANTE)
    with tabs[4]:
        import json
        import base64
        from io import BytesIO

        # --- 1. CONFIGURAÇÃO E BANCO DE DADOS ---
        DB_FILE = "monitoramento_campo.json"
        
        # Banco de Imagens (Simulando App Nativo)
        DB_IMAGENS_MIP = {
            "Soja": {
                "Lagarta-do-cartucho": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Spodoptera_frugiperda_back.jpg/320px-Spodoptera_frugiperda_back.jpg",
                "Percevejo-marrom": "https://live.staticflickr.com/65535/49086326938_5f470375e8_w.jpg",
                "Ferrugem Asiática": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Phakopsora_pachyrhizi_on_Soybean_02.jpg/320px-Phakopsora_pachyrhizi_on_Soybean_02.jpg",
                "Antracnose": "https://content.eol.org/data/media/7f/32/a6/542.1465431668.jpg",
                "Mofo-branco": "https://www.agrolink.com.br/upload/problemas/Sclerotinia_sclerotiorum81.jpg"
            },
            "Milho": {
                "Cigarrinha": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Dalbulus_maidis.jpg/320px-Dalbulus_maidis.jpg",
                "Lagarta-do-cartucho": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Spodoptera_frugiperda_back.jpg/320px-Spodoptera_frugiperda_back.jpg",
                "Pulgão": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Rhopalosiphum_maidis.jpg/320px-Rhopalosiphum_maidis.jpg"
            },
            # Fallback para outras culturas
            "Geral": {
                "Praga Genérica": "https://via.placeholder.com/300x200.png?text=Praga+Detectada",
                "Doença Genérica": "https://via.placeholder.com/300x200.png?text=Doen%C3%A7a+Detectada"
            }
        }

        # Funções de Banco de Dados
        def carregar_dados():
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r") as f: return json.load(f)
            return []

        def salvar_dado(novo):
            d = carregar_dados()
            d.append(novo)
            with open(DB_FILE, "w") as f: json.dump(d, f)
            return d

        # Carrega dados
        historico = carregar_dados()
        cultura_atual = str(cult_sel)
        imgs_cultura = DB_IMAGENS_MIP.get(cultura_atual, DB_IMAGENS_MIP["Geral"])

        # --- 2. MODAL FLUTUANTE (A MÁGICA VISUAL) ---
        # Esta função cria a janela "Pop-up" bonita
        @st.dialog(f"🛡️ Registrar Ocorrência: {cultura_atual}")
        def popup_monitoramento(lat, lon):
            st.markdown(f"<div style='font-size:0.8rem; color:#64748b; margin-bottom:10px;'>📍 Localização Exata: {lat:.5f}, {lon:.5f}</div>", unsafe_allow_html=True)
            
            # Abas dentro do Modal (Praga vs Doença)
            tab_p, tab_d = st.tabs(["🐛 PRAGAS", "🍄 DOENÇAS"])
            
            sel_nome = None
            sel_img = None
            sel_tipo = None

            # Conteúdo Visual (Cards Selecionáveis)
            with tab_p:
                st.caption("Toque na imagem para selecionar")
                cols = st.columns(3)
                idx = 0
                for nome, url in imgs_cultura.items():
                    # Filtro simples (num app real seria mais robusto)
                    if "Ferrugem" not in nome and "Antracnose" not in nome and "Mofo" not in nome: 
                        with cols[idx % 3]:
                            st.image(url, use_container_width=True)
                            if st.button(nome, key=f"btn_p_{nome}", use_container_width=True):
                                st.session_state['temp_sel'] = (nome, url, "Praga")
                        idx += 1
            
            with tab_d:
                st.caption("Toque na imagem para selecionar")
                cols_d = st.columns(3)
                idx_d = 0
                for nome, url in imgs_cultura.items():
                    if "Ferrugem" in nome or "Antracnose" in nome or "Mofo" in nome:
                        with cols_d[idx_d % 3]:
                            st.image(url, use_container_width=True)
                            if st.button(nome, key=f"btn_d_{nome}", use_container_width=True):
                                st.session_state['temp_sel'] = (nome, url, "Doença")
                        idx_d += 1

            st.divider()

            # Área de Confirmação (Só aparece se selecionou algo)
            if 'temp_sel' in st.session_state:
                s_nome, s_url, s_tipo = st.session_state['temp_sel']
                
                st.markdown(f"""
                <div style="background:#f0fdf4; padding:10px; border-radius:8px; border:1px solid #bbf7d0; display:flex; align-items:center; gap:10px;">
                    <img src="{s_url}" style="width:50px; height:50px; border-radius:50%; object-fit:cover;">
                    <div>
                        <div style="font-weight:bold; color:#166534;">{s_nome}</div>
                        <div style="font-size:0.8rem; color:#166534;">{s_tipo} Identificada</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c_qtd, c_sev = st.columns(2)
                with c_qtd:
                    focos = st.number_input("Número de Focos", min_value=1, value=1)
                with c_sev:
                    severidade = st.select_slider("Severidade", ["Leve", "Média", "Alta"], value="Média")
                
                obs = st.text_input("Observação de Campo", placeholder="Ex: Próximo à bordadura...")

                if st.button("✅ CONFIRMAR REGISTRO", type="primary", use_container_width=True):
                    novo = {
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Cultura": cultura_atual,
                        "Tipo": s_tipo,
                        "Nome": s_nome,
                        "Focos": focos,
                        "Severidade": severidade,
                        "Obs": obs,
                        "lat": lat,
                        "lon": lon
                    }
                    salvar_dado(novo)
                    st.toast("💾 Ocorrência Salva com Sucesso!")
                    del st.session_state['temp_sel'] # Limpa seleção
                    st.rerun()

        # --- 3. TELA PRINCIPAL (MAPA FULL) ---
        st.markdown('<div class="app-card" style="padding:0px; overflow:hidden;">', unsafe_allow_html=True)
        
        # Header Flutuante
        c_act1, c_act2 = st.columns([2, 1])
        with c_act1:
            st.markdown(f"### 🛰️ Monitoramento Ativo")
            st.caption(f"Pontos na Sessão: **{len(historico)}**")
        with c_act2:
            # Botão de Exportar
            if st.button("📂 Fechar & Exportar", type="secondary", use_container_width=True):
                 st.session_state['modo_relatorio'] = True
                 st.rerun()

        # O MAPA (GOOGLE EARTH STYLE)
        m = folium.Map(
            location=[st.session_state['loc_lat'], st.session_state['loc_lon']], 
            zoom_start=18,
            tiles=None,
            control_scale=True
        )
        
        # Satélite HD
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri', name='Satélite HD', overlay=False
        ).add_to(m)

        # Pontos Salvos (Ícones Profissionais)
        for p in historico:
            cor = "red" if p['Severidade'] == "Alta" else "orange" if p['Severidade'] == "Média" else "#4ade80"
            folium.Marker(
                [p['lat'], p['lon']],
                popup=f"<b>{p['Nome']}</b><br>{p['Focos']} focos ({p['Severidade']})",
                icon=folium.Icon(color="black", icon_color=cor, icon="bug", prefix="fa")
            ).add_to(m)

        # GPS DO USUÁRIO (BOLINHA AZUL PULSANTE)
        LocateControl(auto_start=True, strings={"title": "Minha Posição"}).add_to(m)
        
        # Captura de Clique
        map_data = st_folium(m, height=500, returned_objects=["last_clicked"])

        # --- GATILHO DO MODAL ---
        # Se clicar no mapa, ABRE O MODAL (Não abre formulário embaixo!)
        if map_data and map_data["last_clicked"]:
            lat_clique = map_data["last_clicked"]["lat"]
            lon_clique = map_data["last_clicked"]["lng"]
            popup_monitoramento(lat_clique, lon_clique)

        st.markdown('</div>', unsafe_allow_html=True)

        # --- 4. ÁREA DE RELATÓRIO / EXPORTAÇÃO (PASTA DIGITAL) ---
        if st.session_state.get('modo_relatorio'):
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📂 RELATÓRIO DE MONITORAMENTO (EXPORTAR)", expanded=True):
                st.markdown("### 📋 Resumo da Inspeção")
                
                if not historico:
                    st.warning("Nenhum dado coletado nesta sessão.")
                else:
                    df = pd.DataFrame(historico)
                    
                    # Métricas
                    c_m1, c_m2, c_m3 = st.columns(3)
                    c_m1.metric("Total de Pontos", len(df))
                    c_m2.metric("Pragas Críticas", len(df[df['Severidade']=='Alta']))
                    c_m3.metric("Focos Totais", df['Focos'].sum())
                    
                    st.dataframe(df[['Data', 'Nome', 'Severidade', 'Focos', 'Obs']], use_container_width=True)
                    
                    # Botão Download Excel
                    c_d1, c_d2 = st.columns(2)
                    with c_d1:
                        # Converte para Excel na memória
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            df.to_excel(writer, index=False, sheet_name='Monitoramento')
                        excel_data = output.getvalue()
                        
                        st.download_button(
                            label="📥 Baixar Planilha (.xlsx)",
                            data=excel_data,
                            file_name=f"Monitoramento_{cultura_atual}_{date.today()}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    with c_d2:
                        if st.button("🔙 Voltar ao Mapa", use_container_width=True):
                            st.session_state['modo_relatorio'] = False
                            st.rerun()

                                
    # 6. GESTÃO (SIMULADOR DE NEGÓCIO - CORRIGIDO E PRÁTICO)
    with tabs[5]:
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

    # 7. ALERTAS (CENTRAL DE CONFIGURAÇÃO)
    with tabs[6]:
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
