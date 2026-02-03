# ARQUIVO: notification_engine.py
# FUNÇÃO: Gerenciar assinaturas e enviar e-mails HTML profissionais

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime
import streamlit as st

# Arquivo para salvar os e-mails cadastrados (Simulação de Banco de Dados)
DB_EMAILS = "user_subscriptions.json"

class NotificationSystem:
    
    @staticmethod
    def salvar_assinatura(nome, email, culturas):
        """Salva as preferências do usuário em um arquivo JSON local."""
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
            
        # Remove duplicatas de e-mail antigo se houver e adiciona o novo
        dados = [d for d in dados if d['email'] != email]
        dados.append(novo_dado)
        
        with open(DB_EMAILS, "w") as f:
            json.dump(dados, f, indent=4)
            
        return True

    @staticmethod
    def gerar_html_email(nome, relatorios_cultura):
        """
        Gera um HTML Bonito (Enterprise) para o corpo do e-mail.
        'relatorios_cultura' é um dicionário: {'Soja': 'Texto do clima...', 'Milho': 'Texto...'}
        """
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #064e3b; color: white; padding: 20px; text-align: center;">
                    <h1 style="margin: 0;">AGRO SDI</h1>
                    <p style="margin: 5px 0 0; opacity: 0.9;">Boletim Diário de Inteligência</p>
                </div>
                
                <div style="padding: 20px;">
                    <p>Olá, <strong>{nome}</strong>!</p>
                    <p>Aqui está o resumo estratégico das suas culturas para hoje:</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        """
        
        for cultura, texto in relatorios_cultura.items():
            html_content += f"""
            <div style="margin-bottom: 20px; background-color: #f9fafb; padding: 15px; border-left: 4px solid #16a34a; border-radius: 4px;">
                <h3 style="margin-top: 0; color: #064e3b;">🌱 {cultura}</h3>
                <p style="line-height: 1.5; color: #555;">{texto}</p>
            </div>
            """
            
        html_content += """
                    <div style="background-color: #eff6ff; padding: 15px; border-radius: 8px; margin-top: 20px;">
                        <h4 style="margin-top: 0; color: #1e40af;">📡 Radar Regional</h4>
                        <p>Monitoramento indica estabilidade nas próximas 12h. Nuvens carregadas a 40km a Leste.</p>
                    </div>
                    
                    <p style="font-size: 12px; color: #888; margin-top: 30px; text-align: center;">
                        Gerado via Agro SDI Enterprise System.<br>
                        Não responda a este e-mail.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content

    @staticmethod
    def enviar_email_agora(nome, email_destinatario, culturas_selecionadas, weather_data_simulado):
        """
        Envia o e-mail usando SMTP do Gmail.
        """
        # CONFIGURAÇÕES DE ENVIO (Idealmente use st.secrets para isso)
        # Substitua pelos seus dados REAIS para testar
        EMAIL_REMETENTE = "vitormartins1337@gmail" 
        SENHA_APP = "rqyubydyerpioxiu"  
        
        if "seu_email" in EMAIL_REMETENTE:
            return False, "Configure o e-mail e senha no arquivo notification_engine.py"

        try:
            msg = MIMEMultipart()
            msg['From'] = f"Agro SDI System <{EMAIL_REMETENTE}>"
            msg['To'] = email_destinatario
            msg['Subject'] = f"📊 Relatório Agro SDI: {date.today().strftime('%d/%m')}"

            # Gera o conteúdo
            corpo_email = NotificationSystem.gerar_html_email(nome, weather_data_simulado)
            msg.attach(MIMEText(corpo_email, 'html'))

            # Conexão Segura
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA_APP)
            text = msg.as_string()
            server.sendmail(EMAIL_REMETENTE, email_destinatario, text)
            server.quit()
            
            return True, "E-mail enviado com sucesso!"
        except Exception as e:
            return False, f"Erro no envio: {str(e)}"
