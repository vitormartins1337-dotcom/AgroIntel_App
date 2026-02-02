# ARQUIVO: data_engine.py
# VERSÃO: V6 - THE INTEGRATOR (Lê TUDO e funde as informações)

import json
import streamlit as st
import os
from pathlib import Path
import collections.abc

# --- FUNÇÃO DE FUSÃO INTELIGENTE (DEEP MERGE) ---
def deep_merge(dic_destino, dic_origem):
    """
    Funde dois dicionários. Se a chave já existe, entra nela e atualiza.
    Se é uma lista (como quimica), substitui pela nova (mais atualizada).
    """
    for k, v in dic_origem.items():
        if (k in dic_destino and 
            isinstance(dic_destino[k], dict) and 
            isinstance(v, collections.abc.Mapping)):
            deep_merge(dic_destino[k], v)
        else:
            # Aqui a mágica acontece: se o novo arquivo tem informação, ele grava.
            dic_destino[k] = v
    return dic_destino

@st.cache_data(show_spinner=False)
def get_database():
    combined_data = {}
    
    # Define o caminho da pasta database
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    db_folder = base_dir / "database"

    if not db_folder.exists():
        print("⚠️ Pasta database não encontrada.")
        return {}

    print(f"🚜 Data Engine V6: Iniciando Varredura em {db_folder}...")

    # 1. BUSCA UNIVERSAL: Encontra TODO arquivo .json, onde quer que esteja
    # rglob("*") procura em todas as subpastas
    todos_arquivos = list(db_folder.rglob("*.json"))
    
    # Ordena para garantir consistência (arquivos 'master' costumam ficar por último se nomeados assim)
    todos_arquivos.sort()

    count = 0
    for arquivo in todos_arquivos:
        try:
            # Ignora arquivos ocultos ou de sistema
            if arquivo.name.startswith("."): continue
            
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo_novo = json.load(f)
                
                # Validação básica: O JSON precisa ser um dicionário
                if isinstance(conteudo_novo, dict):
                    # FUSÃO: Mistura o que acabou de ler com o que já tinha
                    deep_merge(combined_data, conteudo_novo)
                    count += 1
                    
        except json.JSONDecodeError:
            print(f"❌ Erro de sintaxe JSON no arquivo: {arquivo.name}")
        except Exception as e:
            print(f"⚠️ Erro ao processar {arquivo.name}: {e}")

    print(f"✅ Fusão Concluída! {count} arquivos processados e integrados.")
    return combined_data
