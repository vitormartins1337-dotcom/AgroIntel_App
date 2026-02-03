# ARQUIVO: notification_engine.py
# VERSÃO: V-DIAMOND (Layout Expandido e Tabela Corrigida)

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
        Gera o HTML Padrão Diamante com tabelas expandidas e cultura em destaque.
        """
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        hora_hoje = datetime.now().strftime("%H:%M")
        
        # --- ESTILOS CSS (INLINE) ---
        # Tabela forçada a 100% de largura
        style_table = "width: 100%; min-width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; background-color: white;"
        style_th = "background-color: #f1f5f9; color: #334155; padding: 12px 8px; text-align: center; border-bottom: 2px solid #cbd5e1; font-weight: bold; font-size: 12px; text-transform: uppercase;"
        style_td = "padding: 12px 8px; text-align: center; border-bottom: 1px solid #e2e8f0; color: #475569;"
        
        # Container Principal
        html_content = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; background-color: #f0f2f5; margin: 0; padding: 20px;">
            
            <div style="max-width: 700px; margin: auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                
                <div style="background: linear-gradient(135deg, #064e3b 0%, #065f46 100%); color: white; padding: 30px 20px; text-align: center;">
                    <div style="text-transform: uppercase; font-size: 10px; letter-spacing: 2px; opacity: 0.8; margin-bottom: 5px;">Sistema de Inteligência Agronômica</div>
                    <h1 style="margin: 0; font-size: 26px; font-weight: 800; letter-spacing: 0.5px;">AGRO SDI | ENTERPRISE</h1>
                    <div style="margin-top: 10px; font-size: 14px; background: rgba(255,255,255,0.1); display: inline-block; padding: 5px 15px; border-radius: 20px;">
                        📍 Ibicoara, BA • 📅 {data_hoje} • ⏰ {hora_hoje}
                    </div>
                </div>

                <div style="padding: 30px;">
                    <p style="font-size: 16px; color: #374151;">Prezado(a) <strong>{nome}</strong>,</p>
                    <p style="color: #6b7280; font-size: 14px;">O sistema processou os dados de satélite e estações meteorológicas locais. Abaixo encontra-se o laudo técnico consolidado.</p>
                    
                    <div style="background-color: #fff7ed; border-left: 6px solid #f97316; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <strong style="color: #c2410c; display:block; margin-bottom:5px; font-size: 14px;">⚠️ ALERTA DE VOLATILIDADE CLIMÁTICA</strong>
                        <span style="color: #9a3412; font-size: 14px;">A previsão de chuva acumulada sofreu alteração (+12mm) nas últimas 4 horas. Ajuste o manejo de irrigação e entrada de máquinas.</span>
                    </div>

                    <div style="margin-top: 30px; margin-bottom: 30px;">
                        <h3 style="color: #1e293b; margin-bottom: 10px; font-size: 16px; border-left: 4px solid #3b82f6; padding-left: 10px;">☁️ Microclima Semanal (Ibicoara)</h3>
                        
                        <table style="{style_table}" width="100%">
                            <thead>
                                <tr>
                                    <th style="{style_th}">DATA</th>
                                    <th style="{style_th}">TEMP (Média)</th>
                                    <th style="{style_th}">CHUVA (mm)</th>
                                    <th style="{style_th}">ETc (mm)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="background-color: #f8fafc;">
                                    <td style="{style_td}"><b>Hoje</b></td>
                                    <td style="{style_td}"><b>20.2°C</b></td>
                                    <td style="{style_td}"><span style="background:#dbeafe; color:#1e40af; padding:2px 6px; border-radius:4px; font-weight:bold;">3.7 mm</span></td>
                                    <td style="{style_td}">0.12</td>
                                </tr>
                                <tr><td style="{style_td}">Amanhã</td><td style="{style_td}">21.5°C</td><td style="{style_td}">6.5 mm</td><td style="{style_td}">0.13</td></tr>
                                <tr><td style="{style_td}">05/02</td><td style="{style_td}">21.3°C</td><td style="{style_td}">9.3 mm</td><td style="{style_td}">0.13</td></tr>
                                <tr><td style="{style_td}">06/02</td><td style="{style_td}">20.0°C</td><td style="{style_td}" style="color:#94a3b8;">1.6 mm</td><td style="{style_td}">0.12</td></tr>
                            </tbody>
                        </table>
                        <div style="font-size: 11px; color: #94a3b8; text-align: right; margin-top: 5px;">*ETc: Evapotranspiração da Cultura (Demanda Hídrica)</div>
                    </div>
        """

        # 4. LOOP DAS CULTURAS (Com destaque Visual Máximo)
        for cultura, texto in relatorios_cultura.items():
            html_content += f"""
                    <div style="margin-top: 40px; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">
                        
                        <div style="background-color: #166534; color: white; padding: 12px 20px; font-size: 16px; font-weight: bold; letter-spacing: 0.5px; display: flex; align-items: center;">
                            🌱 CULTURA MONITORADA: {cultura.upper()}
                        </div>
                        
                        <div style="padding: 20px; background-color: #fcfcfc;">
                            
                            <h4 style="margin-top: 0; color: #166534; font-size: 14px; text-transform: uppercase;">🔬 Diagnóstico Técnico</h4>
                            <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 20px;">
                                <tr style="border-bottom: 1px solid #eee;">
                                    <td style="padding: 8px 0; color: #64748b;">Fase Atual:</td>
                                    <td style="padding: 8px 0; font-weight: bold; color: #334155; text-align: right;">Reprodutivo (R1)</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #eee;">
                                    <td style="padding: 8px 0; color: #64748b;">Risco Fúngico:</td>
                                    <td style="padding: 8px 0; font-weight: bold; color: #16a34a; text-align: right;">🟢 Baixo</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #eee;">
                                    <td style="padding: 8px 0; color: #64748b;">Janela de Pulverização:</td>
                                    <td style="padding: 8px 0; font-weight: bold; color: #ca8a04; text-align: right;">🟡 Atenção (Vento)</td>
                                </tr>
                            </table>

                            <div style="background-color: #f0fdf4; border-radius: 6px; padding: 15px; color: #14532d; font-size: 14px; line-height: 1.5;">
                                <b>Parecer Agronômico:</b><br>
                                {texto}
                            </div>
                        </div>
                    </div>
            """

        # 5. FOOTER
        html_content += f"""
                    <div style="margin-top: 40px; background-color: #f8fafc; padding: 20px; border-radius: 8px; border: 1px dashed #cbd5e1;">
                        <h4 style="margin: 0 0 10px 0; color: #475569; font-size: 14px;">📡 Radar Regional (Tempo Real)</h4>
                        <div style="font-size: 13px; color: #64748b;">
                            📍 <b>Mucugê:</b> 20°C 🌤️ &nbsp;|&nbsp; 
                            📍 <b>Barra da Estiva:</b> 21°C 🌧️ &nbsp;|&nbsp; 
                            📍 <b>Cascavel:</b> 19°C 🌤️
                        </div>
                    </div>

                    <div style="margin-top: 40px; text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px;">
                        <p style="font-size: 12px; color: #9ca3af; margin: 0;">
                            <b>Agro SDI Enterprise v21.0</b><br>
                            Inteligência de Dados para o Agronegócio.<br>
                            Este e-mail é automático e confidencial.
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    @staticmethod
    def enviar_email_agora(nome, email_destinatario, culturas_selecionadas, weather_data_simulado):
        try:
            MEU_EMAIL = st.secrets["email"]["usuario"]
            MINHA_SENHA = st.secrets["email"]["senha"]
        except Exception:
            return False, "❌ Erro: Segredos não encontrados (Settings -> Secrets)."

        try:
            msg = MIMEMultipart()
            msg['From'] = f"Agro SDI Enterprise <{MEU_EMAIL}>"
            msg['To'] = email_destinatario
            msg['Subject'] = f"💎 Laudo {culturas_selecionadas[0].upper()}: {date.today().strftime('%d/%m')}"

            corpo = NotificationSystem.gerar_html_email(nome, weather_data_simulado)
            msg.attach(MIMEText(corpo, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(MEU_EMAIL, MINHA_SENHA)
            server.sendmail(MEU_EMAIL, email_destinatario, msg.as_string())
            server.quit()
            
            return True, f"✅ Relatório Enterprise enviado para {email_destinatario}!"
            
        except smtplib.SMTPAuthenticationError:
            return False, "❌ Erro de Login: Verifique senha/email nos Secrets."
        except Exception as e:
            return False, f"❌ Erro Técnico: {str(e)}"
