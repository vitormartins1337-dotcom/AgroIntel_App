# ARQUIVO: agro_utils.py
# VERSÃO: V-DEDUP (Com Filtro Anti-Duplicação)

import streamlit as st
import math

class AgroBrain:
    """
    Motor de Inteligência Agronômica.
    Versão Blindada contra duplicidade de dados.
    """

    # --- 1. INTELIGÊNCIA DE DADOS ---
    @staticmethod
    def get_info_segura(dicionario, lista_chaves, padrao="Consulte Eng. Agrônomo"):
        if not dicionario: return padrao
        chaves_norm = {k.lower(): v for k, v in dicionario.items()}
        for chave in lista_chaves:
            if chave.lower() in chaves_norm:
                return chaves_norm[chave.lower()]
        return padrao

    # --- 2. CÁLCULOS FISIOLÓGICOS (VPD) ---
    @staticmethod
    def calcular_vpd(temp, umid):
        try:
            es = 0.6108 * math.exp((17.27 * temp) / (temp + 237.3))
            ea = es * (umid / 100.0)
            return max(0.0, es - ea)
        except: return 0.0

    # --- 3. ANÁLISE CLIMÁTICA ---
    @staticmethod
    def analisar_risco_aplicacao(temp, umid, delta_t, tipo_produto="Sistêmico"):
        alertas = []
        status_geral = "APTO"
        cor_status = "#16a34a" # Verde

        if delta_t < 2:
            alertas.append(("🛑 Risco de Deriva", "Gota muito leve (inversão térmica)."))
            status_geral = "PARE"
            cor_status = "#dc2626"
        elif delta_t > 8:
            if delta_t > 10:
                alertas.append(("🔥 Evaporação Crítica", "Perda imediata. Proibido aplicar."))
                status_geral = "PARE"
                cor_status = "#dc2626"
            else:
                alertas.append(("⚠️ Alta Evaporação", "Use óleo/adjuvante redutor de deriva."))
                status_geral = "ATENÇÃO"
                cor_status = "#ca8a04"

        if "Sistêmico" in tipo_produto:
            vpd = AgroBrain.calcular_vpd(temp, umid)
            if vpd > 2.0 or temp > 32:
                alertas.append(("🌵 Estresse Fisiológico", "Estômatos fechados. Absorção comprometida."))
                if status_geral == "APTO": 
                    status_geral = "EVITAR"
                    cor_status = "#ca8a04"

        return status_geral, cor_status, alertas

    # --- 4. RENDERIZADORES VISUAIS (NATIVO + FILTRO) ---
    @staticmethod
    def gerar_cartao_kpi(titulo, valor, unidade, status_texto, cor_status, tooltip=""):
        return f"""
        <div class="kpi-box" title="{tooltip}">
            <div class="kpi-header">{titulo}</div>
            <div class="kpi-value">{valor}<span class="kpi-unit">{unidade}</span></div>
            <div class="kpi-footer" style="background-color: {cor_status};">
                {status_texto}
            </div>
        </div>
        """

    @staticmethod
    def render_protocolo_quimico(lista_produtos):
        """
        Renderiza os cards com sistema inteligente que remove duplicatas.
        """
        if not lista_produtos:
            st.warning("⚠️ Nenhum protocolo cadastrado para esta fase.")
            return

        # --- INÍCIO DO FILTRO ANTI-DUPLICIDADE ---
        produtos_unicos = []
        assinaturas_vistas = set() # Memória temporária

        for prod in lista_produtos:
            # Cria uma "impressão digital" do produto (Nome do Alvo + Nome do Ativo)
            alvo_check = AgroBrain.get_info_segura(prod, ['Alvo', 'Doenca', 'Praga'], "").strip().lower()
            ativo_check = AgroBrain.get_info_segura(prod, ['Ativo', 'Ingrediente', 'Produto'], "").strip().lower()
            
            # Cria uma chave única. Ex: "ferrugem-protioconazol"
            chave_unica = f"{alvo_check}|{ativo_check}"

            # Se eu ainda não vi essa chave, adiciono na lista de exibição
            if chave_unica not in assinaturas_vistas:
                assinaturas_vistas.add(chave_unica)
                produtos_unicos.append(prod)
        # --- FIM DO FILTRO ---

        # Agora iteramos SOMENTE sobre a lista limpa (produtos_unicos)
        for i, prod in enumerate(produtos_unicos):
            # 1. Extração de Dados
            alvo = AgroBrain.get_info_segura(prod, ['Alvo', 'Doenca', 'Praga'], "Alvo Biológico")
            ativo = AgroBrain.get_info_segura(prod, ['Ativo', 'Ingrediente', 'Produto'], "Ingrediente não informado")
            estrategia = AgroBrain.get_info_segura(prod, ['Estrategia', 'Obs', 'Manejo'], "Seguir recomendação técnica.")
            grupo = AgroBrain.get_info_segura(prod, ['Grupo', 'Mecanismo'], "Não listado")
            tipo = prod.get('Tipo', 'Geral')

            # 2. Definição Visual
            if any(x in tipo for x in ["Químico", "Sistêmico", "Choque"]):
                icon = "☠️"
                border_color = "red"
            elif "Biológico" in tipo or "FBN" in tipo:
                icon = "🦠"
                border_color = "green"
            elif "Nutri" in tipo or "Fisiológico" in tipo:
                icon = "⚡"
                border_color = "orange"
            elif "TS" in tipo:
                icon = "🟣"
                border_color = "violet"
            else:
                icon = "🛡️"
                border_color = "grey"

            # 3. Construção do Card
            with st.container(border=True):
                c1, c2 = st.columns([0.15, 0.85])
                with c1:
                    st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{alvo}**")
                    st.caption(f"TIPO: {tipo} | GRUPO: {grupo}")
                    st.markdown(f"🧬 **Ativo:** `{ativo}`")

                st.info(f"💡 **Estratégia Técnica:** {estrategia}", icon="👨‍🌾")
