import os
import json

# Define o caminho da pasta database
BASE_DB = "database"

# Função para gravar o arquivo atualizado
def atualizar_arquivo(nome_arquivo, dados):
    # Garante que a pasta existe
    os.makedirs(BASE_DB, exist_ok=True)
    
    caminho_completo = os.path.join(BASE_DB, nome_arquivo)
    
    with open(caminho_completo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"✅ Arquivo {nome_arquivo} atualizado com Estratégias Master!")

# ==============================================================================
# 1. ALGODÃO (COM AS ESTRATÉGIAS QUE VOCÊ QUER)
# ==============================================================================
algodao_master = {
  "Algodão (Gossypium hirsutum)": {
    "t_base": 15,
    "vars": {
      "FiberMax 985 GLTP": { "kc": 1.2, "gda_meta": 1650, "info": "Tecnologia TwinLink Plus. Ciclo Médio. Alta exigência de regulador." },
      "TMG 44 B2RF": { "kc": 1.15, "gda_meta": 1580, "info": "Precoce. Monitorar Ramulária no final de ciclo." }
    },
    "fases": {
      "B1 - Botão Floral": {
        "desc": "Primeiros botões florais (Pinhead).",
        "fisiologia": "Início reprodutivo. Planta sensível a abortamento.",
        "manejo": "Monitoramento de Bicudo (Bordadura) e Regulador.",
        "quimica": [
          {
            "Alvo": "Bicudo (Monitoramento/Borda)",
            "Ativo": "Malationa",
            "Grupo": "Organofosforado",
            "Tipo": "Químico Choque",
            "Estrategia": "Realizar bateria de 3 aplicações com intervalo de 3 a 5 dias APENAS nas bordaduras. Foco em eliminar fêmeas migrantes."
          },
          {
            "Alvo": "Regulador de Crescimento",
            "Ativo": "Cloreto de Mepiquat",
            "Grupo": "Inibidor Giberelina",
            "Tipo": "Fisiológico",
            "Estrategia": "Sistema Pix: Doses baixas (50-70ml) e frequentes baseadas na taxa de crescimento diário."
          }
        ]
      },
      "F1 - Primeira Flor": {
        "desc": "Abertura da primeira flor branca.",
        "fisiologia": "Pico de demanda hídrica.",
        "manejo": "Manejo de Ramulária e Lagartas.",
        "quimica": [
          {
            "Alvo": "Ramulária (Preventivo)",
            "Ativo": "Azoxistrobina + Difenoconazol",
            "Grupo": "Estrob + Triazol",
            "Tipo": "Químico Sistêmico",
            "Estrategia": "Aplicação preventiva mandatória. Obrigatória adição de multissítio (Mancozebe) para proteção."
          }
        ]
      }
    }
  }
}

# ==============================================================================
# 2. SOJA (COM ESTRATÉGIAS MASTER)
# ==============================================================================
soja_master = {
  "Soja (Glycine max)": {
    "t_base": 10,
    "vars": {
      "Intacta 2 Xtend": { "kc": 1.15, "gda_meta": 1380, "info": "Plataforma I2X. Resistente a Dicamba. Monitorar Spodoptera." },
      "Brasmax": { "kc": 1.15, "gda_meta": 1350, "info": "Alto teto produtivo." }
    },
    "fases": {
      "V3 - Vegetativo": {
        "desc": "Terceiro trifólio aberto.",
        "fisiologia": "Início da Fixação Biológica (FBN).",
        "manejo": "Controle de lagartas e ervas.",
        "quimica": [
          {
            "Alvo": "Lagartas (Spodoptera)",
            "Ativo": "Benzoato de Emamectina",
            "Tipo": "Químico Ingestão",
            "Estrategia": "Aplicar apenas se houver >2 lagartas/metro ou desfolha >20%. Rotacionar com fisiológicos."
          }
        ]
      },
      "R1 - Início Floração": {
        "desc": "Uma flor aberta.",
        "fisiologia": "Parada de crescimento de raiz.",
        "manejo": "Fungicida Zero.",
        "quimica": [
          {
            "Alvo": "Ferrugem Asiática",
            "Ativo": "Protioconazol + Trifloxistrobina",
            "Tipo": "Químico Sistêmico",
            "Estrategia": "Aplicação preventiva. Momento chave para definir sanidade do baixeiro."
          }
        ]
      }
    }
  }
}

# ==============================================================================
# EXECUÇÃO DA ATUALIZAÇÃO
# ==============================================================================
if __name__ == "__main__":
    print("🚜 Injetando inteligência nos arquivos JSON...")
    
    # Atualiza Algodão
    atualizar_arquivo("algodao.json", algodao_master)
    
    # Atualiza Soja
    atualizar_arquivo("soja.json", soja_master)
    
    # Se tiver outros (Milho, Tomate), basta adicionar aqui seguindo o modelo acima.
    
    print("="*40)
    print("🎉 DADOS ATUALIZADOS!")
    print("Agora vá no App -> Limpe o Cache (C) -> Recarregue (R).")
    print("O texto 'Seguir recomendação de bula' será substituído.")
