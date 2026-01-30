# ARQUIVO: data_engine.py
# FUNÇÃO: Leitor de Banco de Dados JSON
import json
import os
import streamlit as st

def get_database():
    """
    Carrega o banco de dados agronômico do arquivo externo JSON.
    Isso permite que o banco cresça indefinidamente sem pesar no código.
    """
    # Caminho para o arquivo na pasta database
    file_path = os.path.join("database", "agro_db.json")
    
    try:
        # Tenta abrir o arquivo com codificação UTF-8 (para acentos)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
        
    except FileNotFoundError:
        st.error(f"ERRO CRÍTICO: O arquivo de dados '{file_path}' não foi encontrado.")
        return {}
    except json.JSONDecodeError as e:
        st.error(f"ERRO NO ARQUIVO DE DADOS: O JSON está mal formatado. Detalhe: {e}")
        return {}
