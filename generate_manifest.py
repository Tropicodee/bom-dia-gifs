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

ROOT_PATH = "C:\\Users\\91mar\\Downloads\\bom-dia-gifs"  # <-- ajuste conforme o seu PC
GITHUB_USER = "Tropicodee"
REPO_NAME = "bom-dia-gifs"
BRANCH = "master"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}"
FOLDERS = ["gif", "imagens"]

conteudo_path = os.path.join(ROOT_PATH, "conteudo.json")

# ✅ Carrega o JSON atual (original)
if os.path.exists(conteudo_path):
    with open(conteudo_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
else:
    manifest = {"version": "2", "gif": {}, "imagens": {}}

# 🔍 Listas para relatório
novos_arquivos = []
arquivos_removidos = []

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

        # Conjunto de URLs já existentes no JSON
        urls_existentes = set(manifest[folder][nome_categoria])

        # Obter arquivos realmente existentes na pasta
        arquivos_pasta = [
            padronizar_nome(f)
            for f in os.listdir(category_path)
            if not f.startswith(".")
        ]

        # 🔹 Detecta imagens no JSON que sumiram da pasta
        for url_antiga in list(urls_existentes):
            nome_arquivo_json = url_antiga.split("/")[-1]
            if nome_arquivo_json not in arquivos_pasta:
                arquivos_removidos.append(url_antiga)
                manifest[folder][nome_categoria].remove(url_antiga)

        # 🔹 Detecta e adiciona novos arquivos que ainda não estão no JSON
        for file in os.listdir(category_path):
            if file.startswith("."):
                continue

            arquivo_padronizado = padronizar_nome(file)
            url = f"{BASE_URL}/{folder}/{nome_categoria}/{arquivo_padronizado}"

            if url not in urls_existentes:
                manifest[folder][nome_categoria].append(url)
                novos_arquivos.append(url)

# Salva o JSON atualizado
with open(conteudo_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# 🧾 Exibe relatório final
print("\n✅ Atualização concluída com segurança!")
print(f"→ Novos arquivos adicionados: {len(novos_arquivos)}")
print(f"→ Arquivos removidos: {len(arquivos_removidos)}")

if novos_arquivos:
    print("\n📥 Novos arquivos detectados:")
    for a in novos_arquivos[:10]:
        print("  -", a)
    if len(novos_arquivos) > 10:
        print(f"  ... e mais {len(novos_arquivos)-10} arquivos.")

if arquivos_removidos:
    print("\n🗑️ Arquivos ausentes (removidos da pasta):")
    for a in arquivos_removidos[:10]:
        print("  -", a)
    if len(arquivos_removidos) > 10:
        print(f"  ... e mais {len(arquivos_removidos)-10} arquivos.")
