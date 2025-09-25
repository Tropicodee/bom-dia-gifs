import os
import json
import unicodedata
import re

def padronizar_nome(nome):
    """Remove acentos, espaços e caracteres especiais de nomes"""
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    nome = nome.replace(" ", "_").replace("-", "_")
    nome = re.sub(r'[^\w_.]', '', nome)  # mantém apenas letras, números, underscore e ponto
    return nome.lower()

# Caminho raiz onde estão as pastas gif/ e imagens/
ROOT_PATH = "C:\\Users\\91mar\\Downloads\\bom-dia-gifs"  # ALTERE para seu caminho local

# 🔧 Configurações principais
GITHUB_USER = "Tropicodee"
REPO_NAME = "bom-dia-gifs"
BRANCH = "master"  # Alterado para master

BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}"

FOLDERS = ["gif", "imagens"]  # Se a pasta se chama imagens

manifest = {
    "version": "1",
    "gif": {},
    "imagens": {}
}

for folder in FOLDERS:
    folder_path = os.path.join(ROOT_PATH, folder)
    if not os.path.exists(folder_path):
        print(f"Pasta não encontrada: {folder_path}")
        continue

    for category in os.listdir(folder_path):
        category_path = os.path.join(folder_path, category)
        if os.path.isdir(category_path):
            files = []
            nome_categoria = padronizar_nome(category)

            for file in os.listdir(category_path):
                if not file.startswith("."):
                    arquivo_padronizado = padronizar_nome(file)
                    antigo = os.path.join(category_path, file)
                    novo = os.path.join(category_path, arquivo_padronizado)

                    # Renomeia o arquivo localmente se necessário
                    if antigo != novo and not os.path.exists(novo):
                        print(f"Renomeando {antigo} → {novo}")
                        os.rename(antigo, novo)
                    elif antigo != novo and os.path.exists(novo):
                        print(f"Arquivo já existe, não renomeando: {novo}")

                    # Sempre usa o nome padronizado para gerar URL
                    url = f"{BASE_URL}/{folder}/{nome_categoria}/{arquivo_padronizado}"
                    files.append(url)

            manifest[folder][nome_categoria] = files

# Salva o arquivo JSON com URLs completas
with open(os.path.join(ROOT_PATH, "conteudo.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("conteudo.json gerado com sucesso ✅")
