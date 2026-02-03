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
    def enviar_email_agora(nome, email_destinatario, culturas_selecionadas, weather_data_simulado):
        """
        Envia o e-mail usando SMTP do Gmail.
        """
        # --- ÁREA DE CONFIGURAÇÃO (PREENCHA COM SEUS DADOS REAIS) ---
        # 1. Seu E-mail do Gmail (Obrigatório)
        EMAIL_REMETENTE = "vitormartins1337@gmail.com" 
        
        # 2. Sua Senha de App (Gerada lá na segurança do Google)
        # Não é a senha que você usa para entrar no e-mail! É a de 16 letras.
        SENHA_APP = "ikkv obvi xzle gzvf"  
        
        # --- FIM DA CONFIGURAÇÃO ---

        try:
            # Montando o cabeçalho do e-mail
            msg = MIMEMultipart()
            msg['From'] = f"Agro SDI System <{EMAIL_REMETENTE}>"
            msg['To'] = email_destinatario
            msg['Subject'] = f"📊 Relatório Agro SDI: {datetime.now().strftime('%d/%m')}"

            # Gera o conteúdo HTML
            corpo_email = NotificationSystem.gerar_html_email(nome, weather_data_simulado)
            msg.attach(MIMEText(corpo_email, 'html'))

            # Conectando ao Servidor do Google (SMTP)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            # Aqui ele faz o login
            server.login(EMAIL_REMETENTE, SENHA_APP)
            
            # Aqui ele envia
            text = msg.as_string()
            server.sendmail(EMAIL_REMETENTE, email_destinatario, text)
            server.quit()
            
            return True, f"✅ E-mail enviado com sucesso para {email_destinatario}!"
            
        except smtplib.SMTPAuthenticationError:
            return False, "❌ Erro de Login: Verifique se a 'Senha de App' está correta e se a verificação em 2 etapas está ativa no Gmail."
        except Exception as e:
            return False, f"❌ Erro no envio: {str(e)}"
