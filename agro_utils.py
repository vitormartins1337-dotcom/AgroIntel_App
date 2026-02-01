# ARQUIVO: agro_utils.py
# VERSÃO: GEMINI MASTER INTELLIGENCE (VPD + Fisiologia Avançada)

import streamlit as st
import math

class AgroBrain:
    """
    Motor de Inteligência Agronômica.
    Responsável por transformar dados brutos em decisões de campo.
    """
    
    # --- 1. INTELIGÊNCIA DE DADOS (ANTI-FALHA) ---
    @staticmethod
    def get_info_segura(dicionario, lista_chaves, padrao="Consulte a bula ou Engenheiro Agrônomo."):
        """
        Busca inteligente: tenta encontrar a informação por vários sinônimos.
        Se não achar nada, retorna um texto padrão seguro.
        """
        if not dicionario: return padrao
        
        # Normaliza chaves para busca insensível a maiúsculas/minúsculas
        chaves_norm = {k.lower(): v for k, v in dicionario.items()}
        
        for chave in lista_chaves:
            if chave.lower() in chaves_norm:
                valor = chaves_norm[chave.lower()]
                if valor and str(valor).strip() != "":
                    return valor
        return padrao

    # --- 2. CÁLCULOS FISIOLÓGICOS AVANÇADOS (VPD) ---
    @staticmethod
    def calcular_vpd(temp, umid):
        """
        Calcula o Déficit de Pressão de Vapor (VPD) em kPa.
        O VPD é o indicador mais preciso de estresse hídrico na planta.
        """
        try:
            # Fórmula de Tetens para Pressão de Saturação de Vapor (es)
            es = 0.6108 * math.exp((17.27 * temp) / (temp + 237.3))
            
            # Pressão Atual de Vapor (ea)
            ea = es * (umid / 100.0)
            
            # VPD
            vpd = es - ea
            return max(0.0, vpd)
        except:
            return 0.0

    # --- 3. ANÁLISE CLIMÁTICA PARA PULVERIZAÇÃO (DELTA T + MODO DE AÇÃO) ---
    @staticmethod
    def analisar_risco_aplicacao(temp, umid, delta_t, tipo_produto="Sistêmico"):
        """
        Analisa a janela de aplicação cruzando dados climáticos com o tipo de produto.
        """
        alertas = []
        status_geral = "APTO"
        cor_status = "#16a34a" # Verde

        # A. Análise de Delta T (Padrão Ouro para Gota)
        if delta_t < 2:
            alertas.append(("🛑 Risco de Deriva/Inversão", "Gotas muito finas podem não decantar ou evaporar muito lentamente."))
            status_geral = "PARE"
            cor_status = "#dc2626"
        elif delta_t > 8:
            if delta_t > 10:
                alertas.append(("🔥 Evaporação Crítica", "Perda imediata da gota. Aplicação proibida."))
                status_geral = "PARE"
                cor_status = "#dc2626"
            else:
                alertas.append(("⚠️ Alta Evaporação", "Obrigatório uso de óleo/adjuvante redutor de deriva."))
                status_geral = "ATENÇÃO"
                cor_status = "#ca8a04"

        # B. Análise Fisiológica (Para Sistêmicos)
        # Sistêmicos precisam que a planta esteja com estômatos abertos para absorver.
        if "Sistêmico" in tipo_produto:
            vpd = AgroBrain.calcular_vpd(temp, umid)
            if vpd > 2.0 or temp > 32:
                alertas.append(("🌵 Estresse Fisiológico", "Planta fechando estômatos. Produto sistêmico não será absorvido."))
                if status_geral == "APTO": 
                    status_geral = "EVITAR"
                    cor_status = "#ca8a04"

        return status_geral, cor_status, alertas

    # --- 4. RENDERIZADORES VISUAIS (HTML/CSS) ---
    @staticmethod
    def gerar_cartao_kpi(titulo, valor, unidade, status_texto, cor_status, tooltip=""):
        """Gera o HTML do cartão de KPI do Cockpit."""
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
        Renderiza os cards de produtos químicos com blindagem visual e inteligência de cor.
        """
        if not lista_produtos:
            return st.warning("⚠️ Nenhum produto cadastrado especificamente para esta fase no banco de dados.")
            
        for prod in lista_produtos:
            # Busca Inteligente de Dados
            alvo = AgroBrain.get_info_segura(prod, ['Alvo', 'Doenca', 'Praga'], "Alvo Biológico")
            ativo = AgroBrain.get_info_segura(prod, ['Ativo', 'Ingrediente', 'Produto'], "Ingrediente não informado")
            estrategia = AgroBrain.get_info_segura(prod, ['Estrategia', 'Obs', 'Manejo', 'Nota'], "Seguir recomendação de bula.")
            grupo = AgroBrain.get_info_segura(prod, ['Grupo', 'Codigos', 'Mecanismo'], "")
            tipo = prod.get('Tipo', 'Geral')
            
            # Lógica de Cores Semântica
            if "Químico" in tipo: 
                cor_borda = "#ef4444"; bg_icon = "#fee2e2"; icone = "☠️" # Vermelho
            elif "Biológico" in tipo: 
                cor_borda = "#22c55e"; bg_icon = "#dcfce7"; icone = "🦠" # Verde
            elif "Nutri" in tipo: 
                cor_borda = "#eab308"; bg_icon = "#fef9c3"; icone = "⚡" # Amarelo
            else:
                cor_borda = "#3b82f6"; bg_icon = "#dbeafe"; icone = "🧪" # Azul
            
            # HTML Robusto
            html_grupo = f'<span style="background:#f1f5f9; color:#64748b; padding:2px 6px; border-radius:4px; font-size:0.75rem; margin-left:10px;">🧬 {grupo}</span>' if grupo else ""
            
            st.markdown(f"""
            <div style="
                background: white; 
                border-left: 5px solid {cor_borda}; 
                border-radius: 8px; 
                padding: 16px; 
                margin-bottom: 12px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
                border: 1px solid #e2e8f0;">
                
                <div style="display:flex; align-items:flex-start; gap:15px;">
                    <div style="
                        background:{bg_icon}; 
                        min-width: 45px; height: 45px; 
                        border-radius: 50%; 
                        display:flex; align-items:center; justify-content:center; 
                        font-size:1.4rem;">
                        {icone}
                    </div>
                    
                    <div style="flex-grow:1;">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                            <span style="font-weight:700; font-size:1.05rem; color:#1e293b;">{alvo}</span>
                            <span style="background:{cor_borda}; color:white; padding:3px 8px; border-radius:12px; font-size:0.7rem; font-weight:700; text-transform:uppercase;">{tipo}</span>
                        </div>
                        
                        <div style="margin-top:6px; color:#475569; font-size:0.95rem;">
                            <b>Princípio Ativo:</b> {ativo} {html_grupo}
                        </div>
                        
                        <div style="margin-top:10px; background:#f8fafc; padding:10px; border-radius:6px; border:1px dashed #cbd5e1;">
                            <div style="font-size:0.85rem; color:#334155; line-height:1.5;">
                                💡 <b>Estratégia Técnica:</b> {estrategia}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
