# ARQUIVO: agro_utils.py
import streamlit as st

class AgroBrain:
    """
    Classe responsável por processar dados brutos e transformar em
    informação agronômica profissional (Anti-Erro).
    """
    
    @staticmethod
    def get_info_segura(dicionario, lista_chaves, padrao="Informação não disponível no banco de dados."):
        """Busca valor usando múltiplas chaves possíveis (Sinônimos)."""
        if not dicionario: return padrao
        for chave in lista_chaves:
            valor = dicionario.get(chave) or dicionario.get(chave.lower()) or dicionario.get(chave.capitalize())
            if valor: return valor
        return padrao

    @staticmethod
    def analisar_risco_climatico(temp, delta_t, umid):
        """Gera alertas agronômicos automáticos baseados no clima."""
        alertas = []
        
        # Análise Térmica
        if temp > 32: alertas.append(("🔥 Estresse Térmico", "Alto risco de abortamento floral. Evite aplicações."))
        elif temp < 15: alertas.append(("❄️ Metabolismo Lento", "Absorção de sistêmicos reduzida."))
        
        # Análise Delta T
        if delta_t < 2: alertas.append(("🛑 Risco de Deriva", "Gota não chega no alvo. Pare a aplicação."))
        elif delta_t > 8: alertas.append(("💧 Risco de Evaporação", "Use adjuvante óleo/super espalhante."))
        elif 2 <= delta_t <= 8: alertas.append(("✅ Condição Ideal", "Janela de aplicação aberta."))
        
        return alertas

    @staticmethod
    def gerar_cartao_kpi(titulo, valor, unidade, status_texto, cor_status):
        """Gera o HTML do cartão de KPI padronizado."""
        return f"""
        <div class="kpi-box">
            <div class="kpi-header">{titulo}</div>
            <div class="kpi-value">{valor}<span class="kpi-unit">{unidade}</span></div>
            <div class="kpi-footer" style="background-color: {cor_status};">{status_texto}</div>
        </div>
        """

    @staticmethod
    def render_protocolo_quimico(lista_produtos):
        """Renderiza os cards de produtos químicos com blindagem visual."""
        if not lista_produtos:
            return st.info("ℹ️ Nenhum produto cadastrado para esta fase.")
            
        for prod in lista_produtos:
            # Inteligência de Chaves (Nunca mais 'None')
            alvo = AgroBrain.get_info_segura(prod, ['Alvo', 'Doenca', 'Praga'], "Alvo Geral")
            ativo = AgroBrain.get_info_segura(prod, ['Ativo', 'Ingrediente', 'Produto'], "Consultar Bula")
            estrategia = AgroBrain.get_info_segura(prod, ['Estrategia', 'Obs', 'Manejo', 'Nota'], "Seguir recomendação do fabricante.")
            tipo = prod.get('Tipo', 'Geral')
            
            # Cores
            cor = "#2563eb" # Azul Padrão
            icone = "🧪"
            if "Químico" in tipo: cor, icone = "#dc2626", "☠️"
            elif "Biológico" in tipo: cor, icone = "#16a34a", "🦠"
            elif "Nutri" in tipo: cor, icone = "#ca8a04", "⚡"

            st.markdown(f"""
            <div style="border-left: 4px solid {cor}; background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #e2e8f0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; color:#334155; font-size:1.05rem;">{icone} {alvo}</span>
                    <span class="tag-chem" style="background:{cor};">{tipo}</span>
                </div>
                <div style="margin-top:8px; font-size:0.95rem; color:#475569;">
                    <b>Ingrediente:</b> {ativo}
                </div>
                <div style="margin-top:6px; font-size:0.9rem; color:#64748b; background:white; padding:8px; border-radius:4px;">
                    💡 {estrategia}
                </div>
            </div>
            """, unsafe_allow_html=True)
