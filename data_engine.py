# ARQUIVO: data_engine.py
# FUNÇÃO: Multi-File Database Loader (Leitor de Múltiplos Arquivos)
import json
import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner=False)
def get_database():
    """
    Carrega e unifica TODOS os arquivos .json encontrados na pasta 'database'.
    Isso permite dividir as culturas em arquivos separados (graos, frutas, hf...).
    """
    combined_data = {}
    
    try:
        # 1. Localiza a pasta database
        base_dir = Path(__file__).parent.resolve()
        db_folder = base_dir / "database"
        
        if not db_folder.exists():
            st.error(f"ERRO CRÍTICO: Pasta '{db_folder}' não encontrada.")
            return {}

        # 2. Busca TODOS os arquivos .json dentro da pasta
        json_files = list(db_folder.glob("*.json"))
        
        if not json_files:
            st.warning("Nenhum arquivo .json encontrado na pasta database.")
            return {}

        # 3. Lê cada arquivo e adiciona ao dicionário mestre
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    combined_data.update(data) # Junta os dados
            except json.JSONDecodeError as e:
                st.error(f"Erro no arquivo {json_file.name}: {e}")

        return combined_data

    except Exception as e:
        st.error(f"ERRO GERAL DE LEITURA: {e}")
        return {}
