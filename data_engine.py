# ARQUIVO: data_engine.py
import json
import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner=False)
def get_database():
    """
    Motor de Dados Enterprise V2.
    Lê recursivamente todas as pastas dentro de 'database'.
    """
    combined_data = {}
    
    try:
        # Pega a pasta onde o script está
        base_dir = Path(__file__).parent.resolve()
        db_folder = base_dir / "database"
        
        # Cria a pasta se não existir
        if not db_folder.exists():
            db_folder.mkdir()
            return {}

        # Busca arquivos JSON em TODAS as subpastas (soja.json, milho.json, etc)
        # O padrão "**/*.json" garante que ele olhe dentro de subpastas
        json_files = list(db_folder.glob("**/*.json"))
        
        for json_file in json_files:
            try:
                # Pula arquivos vazios para não dar erro
                if json_file.stat().st_size == 0:
                    continue
                    
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    combined_data.update(data)
            except Exception as e:
                st.warning(f"Aviso: Não foi possível ler {json_file.name}. Verifique a formatação.")

        return combined_data

    except Exception as e:
        st.error(f"Erro Crítico no Banco de Dados: {e}")
        return {}
