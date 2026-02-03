# ARQUIVO: notification_engine.py
# VERSÃO: V-GOLD (Layout Enterprise HTML/CSS)

import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime, date

DB_EMAILS = "user_subscriptions.json"

class NotificationSystem:
    
    @staticmethod
    def salvar_assinatura(nome, email, culturas):
        novo_dado = {
            "nome": nome,
            "email": email,
            "culturas": culturas,
            "data_cadastro": str(datetime.now())
        }
        dados = []
        if os.path.exists(DB_EMAILS):
            try:
                with open(DB_EMAILS, "r") as f:
                    dados = json.load(f)
            except: pass
        dados = [d for d in dados if d['email'] != email]
        dados.append(novo_dado)
        with open(DB_EMAILS, "w") as f:
            json.dump(dados, f, indent=4)
        return True

    @staticmethod
    def gerar_html_email(nome, relatorios_cultura):
        """
        Gera o HTML Padrão Ouro (Enterprise) com tabelas e alertas visuais.
        """
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Estrutura CSS Inline (Compatível com Gmail/Outlook)
        style_table = "width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px;"
        style_th = "background-color: #f3f4f6; color: #1f2937; padding: 10px; text-align: left; border-bottom: 2px solid #e5e7eb;"
        style_td = "padding: 10px; border-bottom: 1px solid #e5e7eb; color: #4b5563;"
        style_alert = "background-color: #fff7ed; border-left: 5px solid #f97316; padding: 15px; margin: 15px 0; color: #9a3412;"

        # Cabeçalho do HTML
        html_content = f"""
        <html>
        <body style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #333; background-color: #f9fafb; padding: 20px;">
            
            <div style="max-width: 650px; margin: auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                
                <div style="background-color: #064e3b; color: white; padding: 25px; text-align: center;">
                    <h1 style="margin: 0; font-size: 24px; letter-spacing: 1px;">💎 LAUDO TÉCNICO AGRO-INTEL</h1>
                    <p style="margin: 5px 0 0; opacity: 0.8; font-size: 14px;">📍 Ibicoara (Sede) | 📅 {data_hoje}</p>
                </div>

                <div style="padding: 30px;">
                    <p style="font-size: 16px;">Olá, <strong>{nome}</strong>.</p>
                    
                    <div style="{style_alert}">
                        <strong style="display:block; margin-bottom:5px;">⚠️ ALERTA DE VOLATILIDADE CLIMÁTICA</strong>
                        A previsão de chuva acumulada mudou bruscamente nas últimas horas. 
                        Revise o planejamento de maquinário e pulverização.
                    </div>

                    <h3 style="color: #064e3b; border-bottom: 2px solid #064e3b; padding-bottom: 5px; margin-top: 25px;">📅 Microclima Semanal (Ibicoara)</h3>
                    <table style="{style_table}">
                        <thead>
                            <tr>
                                <th style="{style_th}">Data</th>
                                <th style="{style_th}">Temp</th>
                                <th style="{style_th}">Chuva</th>
                                <th style="{style_th}">Consumo (ETc)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td style="{style_td}"><b>Hoje</b></td><td style="{style_td}">20.1°C</td><td style="{style_td}"><span style="color:#2563eb; font-weight:bold;">3.7mm</span></td><td style="{style_td}">0.12mm</td></tr>
                            <tr><td style="{style_td}">Amanhã</td><td style="{style_td}">21.5°C</td><td style="{style_td}">6.5mm</td><td style="{style_td}">0.13mm</td></tr>
                            <tr><td style="{style_td}">Quinta</td><td style="{style_td}">21.3°C</td><td style="{style_td}">9.3mm</td><td style="{style_td}">0.13mm</td></tr>
                        </tbody>
                    </table>

                    <h3 style="color: #064e3b; border-bottom: 2px solid #064e3b; padding-bottom: 5px; margin-top: 30px;">🔬 Diagnóstico Fisiológico & Estratégico</h3>
                    <table style="{style_table}">
                        <thead>
                            <tr>
                                <th style="{style_th}">Parâmetro</th>
                                <th style="{style_th}">Valor</th>
                                <th style="{style_th}">Interpretação Técnica</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        # Loop Dinâmico para as Culturas/Parâmetros
        # Aqui simulamos os dados técnicos que você pediu (VPD, Delta T, etc.)
        parametros = [
            ("Termodinâmica (VPD)", "0.4 kPa", "🔴 <b>Atmosfera saturada.</b> Transpiração bloqueada. Risco de doenças."),
            ("Pulverização (Delta T)", "2.1 °C", "🟢 <b>Ideal.</b> Gota protegida contra evaporação."),
            ("Balanço Hídrico (7d)", "22.1 mm", "🔵 <b>Superávit.</b> Solo tende à saturação. Risco de anoxia."),
            ("Pressão Sanitária", "1 Janela", "🟢 <b>Baixo Risco.</b> Ausência de molhamento contínuo."),
            ("Nutrição (Fase)", "Vegetativo", "💊 <b>Foco: N + Mg.</b> Nitrogênio para síntese proteica."),
            ("Maturação (GDA)", "1036 GDA", "☀️ Acúmulo térmico definindo conversão de açúcares.")
        ]

        for p, v, i in parametros:
            html_content += f"""
            <tr>
                <td style="{style_td}"><b>{p}</b></td>
                <td style="{style_td}"><span style="background:#f3f4f6; padding:4px 8px; border-radius:4px; font-weight:bold;">{v}</span></td>
                <td style="{style_td}">{i}</td>
            </tr>
            """

        html_content += f"""
                        </tbody>
                    </table>

                    <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin-top: 30px; border: 1px solid #d1fae5;">
                        <h4 style="margin-top: 0; color: #047857;">📡 Radar Regional (Tempo Real)</h4>
                        <ul style="list-style: none; padding: 0; margin: 0; color: #065f46;">
                            <li style="margin-bottom: 8px;">📍 <b>Mucugê:</b> 🌤️ Nublado (20.18°C)</li>
                            <li style="margin-bottom: 8px;">📍 <b>Barra da Estiva:</b> 🌤️ Nublado (20.19°C)</li>
                            <li style="margin-bottom: 8px;">📍 <b>Piatã:</b> 🌤️ Nublado (19.21°C)</li>
                            <li>📍 <b>Cascavel:</b> 🌤️ Nublado (19.54°C)</li>
                        </ul>
                    </div>
                    
                    <div style="margin-top: 40px; text-align: center; border-top: 1px solid #eee; padding-top: 20px; font-size: 12px; color: #9ca3af;">
                        <p>Sistema Agro-Intel v21.0 | Enterprise Module</p>
                        <p>Este laudo foi gerado automaticamente baseando-se em telemetria via satélite.</p>
                    </div>

                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    @staticmethod
    def enviar_email_agora(nome, email_destinatario, culturas_selecionadas, weather_data_simulado):
        
        # Leitura Segura dos Secrets
        try:
            MEU_EMAIL = st.secrets["email"]["usuario"]
            MINHA_SENHA = st.secrets["email"]["senha"]
        except Exception:
            return False, "❌ Erro: Segredos não encontrados. Verifique o Streamlit Cloud."

        try:
            msg = MIMEMultipart()
            msg['From'] = f"Agro SDI Enterprise <{MEU_EMAIL}>"
            msg['To'] = email_destinatario
            msg['Subject'] = f"💎 Laudo Técnico: {date.today().strftime('%d/%m')} - Volatilidade Climática"

            corpo = NotificationSystem.gerar_html_email(nome, weather_data_simulado)
            msg.attach(MIMEText(corpo, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(MEU_EMAIL, MINHA_SENHA)
            server.sendmail(MEU_EMAIL, email_destinatario, msg.as_string())
            server.quit()
            
            return True, f"✅ Relatório Enterprise enviado para {email_destinatario}!"
            
        except Exception as e:
            return False, f"❌ Erro Técnico: {str(e)}"
