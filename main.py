# ... (código anterior onde calcula gda_acum e progresso) ...

    # ==============================================================================
    # 📟 SMART COCKPIT (VISUAL PROFISSIONAL)
    # ==============================================================================
    
    # 1. Lógica de Cores e Status (Inteligência Agronômica)
    # Temperatura
    temp = hoje['Temp']
    if temp < 18: status_temp = "Baixa ❄️"; cor_temp = "#1e88e5" # Azul
    elif 18 <= temp <= 30: status_temp = "Ideal ✅"; cor_temp = "#2e7d32" # Verde
    else: status_temp = "Estresse Térmico 🔥"; cor_temp = "#d32f2f" # Vermelho

    # Umidade
    umid = hoje['Umid']
    if umid < 30: status_umid = "Crítico (Seco) ⚠️"; cor_umid = "#d32f2f"
    elif 30 <= umid <= 50: status_umid = "Atenção ⚠️"; cor_umid = "#fbc02d" # Amarelo
    else: status_umid = "Ideal 💧"; cor_umid = "#2e7d32"

    # Delta T (O mais importante para pulverização)
    delta_t = hoje['Delta T']
    if delta_t < 2: 
        status_delta = "PARE (Risco Deriva) 🛑"; cor_delta = "#d32f2f" # Vermelho
    elif 2 <= delta_t <= 8: 
        status_delta = "APTO (Pulverizar) ✅"; cor_delta = "#2e7d32" # Verde
    elif 8 < delta_t <= 10: 
        status_delta = "Atenção (Evaporação) ⚠️"; cor_delta = "#f9a825" # Laranja
    else: 
        status_delta = "PARE (Perda Gota) 🛑"; cor_delta = "#d32f2f" # Vermelho

    # ETc
    etc = hoje['ETc']
    
    # 2. Renderização dos Cartões HTML
    st.markdown(f"""
    <style>
        .kpi-container {{
            display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px;
        }}
        .kpi-card {{
            flex: 1; min-width: 200px; background: white; 
            border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #e0e0e0; overflow: hidden;
            display: flex; flex-direction: column;
        }}
        .kpi-header {{
            font-size: 14px; font-weight: 600; color: #666; 
            padding: 12px 15px; background: #f8f9fa; border-bottom: 1px solid #eee;
            text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .kpi-body {{
            padding: 15px; text-align: center; flex-grow: 1;
        }}
        .kpi-value {{
            font-size: 28px; font-weight: 800; color: #333; margin-bottom: 5px;
        }}
        .kpi-unit {{ font-size: 14px; color: #888; font-weight: 400; }}
        .kpi-footer {{
            padding: 8px; text-align: center; color: white; font-size: 13px; font-weight: 600;
        }}
    </style>

    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-header">🌡️ Temperatura</div>
            <div class="kpi-body">
                <div class="kpi-value">{temp:.1f}<span class="kpi-unit">°C</span></div>
            </div>
            <div class="kpi-footer" style="background-color: {cor_temp};">
                {status_temp}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-header">💧 Umidade Relativa</div>
            <div class="kpi-body">
                <div class="kpi-value">{umid}<span class="kpi-unit">%</span></div>
            </div>
            <div class="kpi-footer" style="background-color: {cor_umid};">
                {status_umid}
            </div>
        </div>

        <div class="kpi-card">
            <div class="kpi-header">💦 Evapotranspiração</div>
            <div class="kpi-body">
                <div class="kpi-value">{etc}<span class="kpi-unit">mm/dia</span></div>
            </div>
            <div class="kpi-footer" style="background-color: #1565c0;">
                Demanda Hídrica
            </div>
        </div>

        <div class="kpi-card" style="border: 2px solid {cor_delta};">
            <div class="kpi-header" style="color:{cor_delta}; font-weight:900;">🛡️ Delta T (Aplicação)</div>
            <div class="kpi-body">
                <div class="kpi-value" style="color:{cor_delta};">{delta_t}<span class="kpi-unit">°C</span></div>
            </div>
            <div class="kpi-footer" style="background-color: {cor_delta};">
                {status_delta}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ... (Continua o código das Abas tabs = st.tabs...) ...
