# ARQUIVO: data_engine.py
# VERSÃO: V4 - DEEP SEARCH (Lê qualquer estrutura de pastas recursivamente)

import json
import streamlit as st
from pathlib import Path

@st.cache_data(show_spinner=False)
def get_database():
    """
    Varre o Data Lake (pasta database) procurando por culturas.
    Não importa se está em 'database/01_Graos/Soja' ou 'database/03_Frutas/Uva',
    ele vai encontrar e montar o objeto agronômico completo.
    """
    combined_data = {}
    
    # 1. Localiza a pasta raiz do banco de dados
    base_dir = Path(__file__).parent.resolve()
    db_folder = base_dir / "database"
    
    # Se a pasta não existir, retorna vazio sem erro
    if not db_folder.exists():
        return {}

    # 2. A MÁGICA: rglob("1_genetica.json")
    # Ele procura recursivamente em TODAS as subpastas por esse arquivo.
    # Onde ele achar um '1_genetica.json', ele sabe que ali existe uma cultura.
    for genetica_file in db_folder.rglob("1_genetica.json"):
        try:
            # A pasta pai do arquivo é a pasta da cultura (Ex: 01_Soja)
            cultura_dir = genetica_file.parent
            
            # Estrutura temporária da cultura
            dados_cultura = {
                "vars": {},
                "fases": {},
                "t_base": 10
            }
            
            # A. LER GENÉTICA (Garante o nome e variedades)
            with open(genetica_file, 'r', encoding='utf-8') as f:
                d = json.load(f)
                nome_cultura = d.get("cultura", "Desconhecida")
                dados_cultura["vars"] = d.get("variedades", {})
                dados_cultura["t_base"] = d.get("t_base", 10)

            # B. LER FENOLOGIA (Se existir na mesma pasta)
            f_fen = cultura_dir / "2_fenologia.json"
            if f_fen.exists():
                with open(f_fen, 'r', encoding='utf-8') as f:
                    dados_cultura["fases"] = json.load(f).get("fases", {})

            # C. LER PROTOCOLOS (Se existir e cruza com as fases)
            f_pro = cultura_dir / "3_protocolos.json"
            if f_pro.exists():
                with open(f_pro, 'r', encoding='utf-8') as f:
                    d_prot = json.load(f)
                    # Injeta a química dentro da fase correspondente
                    for cod_fase, lista_prods in d_prot.items():
                        if cod_fase in dados_cultura["fases"]:
                            dados_cultura["fases"][cod_fase]["quimica"] = lista_prods
            
            # Adiciona ao dicionário mestre se tiver nome válido
            if nome_cultura:
                combined_data[nome_cultura] = dados_cultura
                
        except Exception as e:
            # Blindagem: Se um arquivo falhar, ele apenas ignora e tenta o próximo
            print(f"⚠️ Erro ao processar cultura em {genetica_file}: {e}")
            continue

    # Retorna o dicionário completo e organizado
    return combined_data
