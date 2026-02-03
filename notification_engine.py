# ARQUIVO: notification_engine.py
# VERSÃO: V-SECRETS (Com importação correta do Streamlit)

import streamlit as st  # <--- ESSA LINHA ERA A QUE FALTAVA!
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
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="background-color: #064e3b; color: white; padding: 20px;">
                <h2 style="margin: 0;">Agro SDI | Boletim</h2>
            </div>
            <div style="padding: 20px; border: 1px solid #ddd;">
                <p>Olá, <strong>{nome}</strong>!</p>
                <hr>
        """
        for cultura, texto in relatorios_cultura.items():
            html_content += f"""
            <div style="margin-bottom: 10px; background-color: #f0fdf4; padding: 10px; border-left: 5px solid #16a34a;">
                <b>🌱 {cultura}</b><br>{texto}
            </div>
            """
        html_content += "</div></body></html>"
        return html_content

    @staticmethod
    def enviar_email_agora(nome, email_destinatario, culturas_selecionadas, weather_data_simulado):
        
        # Leitura Segura das Credenciais (Secrets)
        try:
            MEU_EMAIL = st.secrets["email"]["usuario"]
            MINHA_SENHA = st.secrets["email"]["senha"]
        except Exception:
            return False, "❌ Erro: Segredos não encontrados. Verifique o painel do Streamlit Cloud."

        try:
            msg = MIMEMultipart()
            msg['From'] = f"Agro SDI <{MEU_EMAIL}>"
            msg['To'] = email_destinatario
            msg['Subject'] = f"Relatório Agro SDI: {date.today().strftime('%d/%m')}"

            corpo = NotificationSystem.gerar_html_email(nome, weather_data_simulado)
            msg.attach(MIMEText(corpo, 'html'))

            # Conexão SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(MEU_EMAIL, MINHA_SENHA)
            server.sendmail(MEU_EMAIL, email_destinatario, msg.as_string())
            server.quit()
            
            return True, f"✅ Sucesso! Enviado para {email_destinatario}"
            
        except smtplib.SMTPAuthenticationError:
            return False, "❌ Erro de Login: Senha ou E-mail incorretos nos Secrets."
        except Exception as e:
            return False, f"❌ Erro Técnico: {str(e)}"
