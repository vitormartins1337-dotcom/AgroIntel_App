# ARQUIVO: notification_engine.py
# VERSÃO: V-DIRECT (Sem travas de segurança)

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
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="background-color: #064e3b; color: white; padding: 20px;">
                <h1 style="margin: 0;">AGRO SDI</h1>
            </div>
            <div style="padding: 20px;">
                <p>Olá, <strong>{nome}</strong>!</p>
                <hr>
        """
        for cultura, texto in relatorios_cultura.items():
            html_content += f"""
            <div style="margin-bottom: 15px; background-color: #f0fdf4; padding: 10px; border-left: 5px solid #16a34a;">
                <h3 style="margin:0; color: #166534;">{cultura}</h3>
                <p>{texto}</p>
            </div>
            """
        html_content += "</div></body></html>"
        return html_content

    @staticmethod
    def enviar_email_agora(nome, email_destinatario, culturas_selecionadas, weather_data_simulado):
        
        # --- PREENCHA AQUI E SALVE O ARQUIVO ---
        MEU_EMAIL = "vitormartins1337@gmail.com"  
        MINHA_SENHA = "ikkv obvi xzle gzvf"
        # ---------------------------------------

        # Verifica se você esqueceu de preencher (só pra avisar no log)
        if "SEU_EMAIL" in MEU_EMAIL or "SUA SENHA" in MINHA_SENHA:
            return False, "⚠️ Erro: Você precisa editar o arquivo notification_engine.py e colocar seu email real nas linhas 58 e 59."

        try:
            msg = MIMEMultipart()
            msg['From'] = f"Agro SDI <{MEU_EMAIL}>"
            msg['To'] = email_destinatario
            msg['Subject'] = f"Agro SDI: Relatório {date.today().strftime('%d/%m')}"

            corpo = NotificationSystem.gerar_html_email(nome, weather_data_simulado)
            msg.attach(MIMEText(corpo, 'html'))

            # Conexão
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(MEU_EMAIL, MINHA_SENHA)
            server.sendmail(MEU_EMAIL, email_destinatario, msg.as_string())
            server.quit()
            
            return True, f"✅ E-mail enviado com sucesso para {email_destinatario}!"
            
        except Exception as e:
            return False, f"❌ Erro Técnico: {str(e)}"
