# ARQUIVO: core_logic.py
from agro_database import get_agro_db

class AgroEngine:
    def __init__(self):
        self.db = get_agro_db()

    def listar_culturas(self):
        """Retorna lista de culturas disponíveis"""
        return list(self.db.keys())

    def get_fases(self, cultura):
        """Retorna as fases fenológicas da cultura"""
        if cultura in self.db:
            return self.db[cultura]['fases_fenologicas']
        return {}

    def buscar_problema(self, cultura, termo_busca=None, tipo="Pragas"):
        """
        Busca pragas ou doenças.
        Se termo_busca for vazio, retorna todas.
        """
        if cultura not in self.db:
            return []
        
        todos_problemas = self.db[cultura]['problemas'].get(tipo, {})
        
        if not termo_busca:
            return todos_problemas # Retorna o dicionário inteiro
        
        # Filtro simples (Case insensitive)
        resultado = {}
        for nome, dados in todos_problemas.items():
            if termo_busca.lower() in nome.lower():
                resultado[nome] = dados
        
        return resultado

    def get_detalhe_tecnico(self, cultura, tipo, nome_problema):
        """Retorna a ficha técnica completa para o App exibir"""
        try:
            return self.db[cultura]['problemas'][tipo][nome_problema]
        except KeyError:
            return None
