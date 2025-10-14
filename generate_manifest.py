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

ROOT_PATH = "C:\\Users\\91mar\\Downloads\\bom-dia-gifs"  # ALTERE para seu caminho local
GITHUB_USER = "Tropicodee"
REPO_NAME = "bom-dia-gifs"
BRANCH = "master"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}"
FOLDERS = ["gif", "imagens"]

# ✅ Lê o conteudo.json existente, se existir
conteudo_path = os.path.join(ROOT_PATH, "conteudo.json")
if os.path.exists(conteudo_path):
    with open(conteudo_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
else:
    manifest = {"version": "2", "gif": {}, "imagens": {}}

for folder in FOLDERS:
    folder_path = os.path.join(ROOT_PATH, folder)
    if not os.path.exists(folder_path):
        print(f"Pasta não encontrada: {folder_path}")
        continue

    for category in os.listdir(folder_path):
        category_path = os.path.join(folder_path, category)
        if not os.path.isdir(category_path):
            continue

        nome_categoria = padronizar_nome(category)
        if nome_categoria not in manifest[folder]:
            manifest[folder][nome_categoria] = []

        # Cria um set para checar duplicados rapidamente
        urls_existentes = set(manifest[folder][nome_categoria])

        for file in os.listdir(category_path):
            if file.startswith("."):
                continue

            arquivo_padronizado = padronizar_nome(file)
            antigo = os.path.join(category_path, file)
            novo = os.path.join(category_path, arquivo_padronizado)

            # Se já existe arquivo com esse nome, adiciona (1), (2), ...
            contador = 1
            nome_base, ext = os.path.splitext(arquivo_padronizado)
            while os.path.exists(novo) and novo != antigo:
                arquivo_padronizado = f"{nome_base}({contador}){ext}"
                novo = os.path.join(category_path, arquivo_padronizado)
                contador += 1

            # Renomeia localmente apenas se mudou o nome
            if antigo != novo:
                print(f"Renomeando {antigo} → {novo}")
                os.rename(antigo, novo)

            url = f"{BASE_URL}/{folder}/{nome_categoria}/{arquivo_padronizado}"

            # Adiciona apenas se não existir no JSON
            if url not in urls_existentes:
                manifest[folder][nome_categoria].append(url)

# Salva o arquivo JSON atualizado
with open(conteudo_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("conteudo.json atualizado com sucesso ✅")
