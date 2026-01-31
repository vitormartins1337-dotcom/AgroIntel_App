# ARQUIVO: data_engine.py
# FUNÇÃO: Leitor Inteligente com Diagnóstico de Erros
import json
import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner=False)
def get_database():
    combined_data = {}
    
    # Localiza a pasta database
    base_dir = Path(__file__).parent.resolve()
    db_folder = base_dir / "database"
    
    # Verifica se a pasta existe
    if not db_folder.exists():
        st.error(f"❌ ERRO CRÍTICO: Pasta database não encontrada em {db_folder}")
        return {}

    # Busca recursiva em todas as subpastas
    json_files = list(db_folder.rglob("*.json"))
    
    if not json_files:
        st.warning("⚠️ Nenhum arquivo .json encontrado dentro da pasta database.")
        return {}

    # Itera sobre os arquivos
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                # Tenta carregar o JSON
                data = json.load(f)
                combined_data.update(data)
                
        except json.JSONDecodeError as e:
            # AQUI ESTÁ A MÁGICA: Ele mostra onde o erro está!
            st.error(f"""
            ❌ ERRO NO ARQUIVO: {json_file.name}
            linha: {e.lineno} | coluna: {e.colno}
            O que aconteceu: {e.msg}
            """)
        except Exception as e:
            st.error(f"Erro desconhecido ao ler {json_file.name}: {e}")

    return combined_data
