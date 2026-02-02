# ARQUIVO: data_engine.py
# VERSÃO: RESTORE (Lê qualquer arquivo .json na pasta database e subpastas)

import json
import streamlit as st
import os
from pathlib import Path
import collections.abc

# Função para garantir que dados novos se somem aos antigos sem apagar
def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

@st.cache_data(show_spinner=False)
def get_database():
    """
    Varre a pasta 'database' inteira e carrega TODOS os arquivos .json encontrados.
    Funciona para estruturas antigas (soja.json) e novas.
    """
    combined_data = {}
    
    # 1. Localiza a pasta database de forma absoluta (Blindagem)
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    db_folder = base_dir / "database"
    
    # Se não achar a pasta, não trava o app, só retorna vazio
    if not db_folder.exists():
        print(f"⚠️ A pasta {db_folder} não foi encontrada.")
        return {}

    # 2. O ASPIRADOR: Busca recursiva por qualquer .json (*.json)
    # rglob = Recursive Global search
    arquivos_json = list(db_folder.rglob("*.json"))
    
    print(f"🔄 Data Engine: Encontrados {len(arquivos_json)} arquivos JSON.")

    for arquivo in arquivos_json:
        try:
            # Ignora arquivos de sistema ou vazios
            if arquivo.name.startswith(".") or arquivo.stat().st_size < 5:
                continue

            with open(arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Se o arquivo tiver dados, mistura no caldeirão principal
                if data:
                    combined_data = deep_update(combined_data, data)
                    
        except json.JSONDecodeError:
            print(f"⚠️ Erro de formatação no arquivo: {arquivo.name}")
            continue
        except Exception as e:
            print(f"⚠️ Erro genérico ao ler {arquivo.name}: {e}")
            continue

    return combined_data
