# ARQUIVO: data_engine.py
# FUNÇÃO: Leitor Recursivo Enterprise (Lê subpastas automaticamente)
import json
import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner=False)
def get_database():
    """
    Varre a pasta 'database' e TODAS as suas subpastas.
    Lê qualquer arquivo .json e unifica em um único super-dicionário.
    """
    combined_data = {}
    
    try:
        base_dir = Path(__file__).parent.resolve()
        db_folder = base_dir / "database"
        
        if not db_folder.exists():
            return {}

        # O comando rglob('*/*.json') busca em todas as subpastas
        json_files = list(db_folder.rglob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    combined_data.update(data)
            except Exception as e:
                st.error(f"Erro ao ler {json_file.name}: {e}")

        return combined_data

    except Exception as e:
        st.error(f"Erro Crítico: {e}")
        return {}
