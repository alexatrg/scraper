import ast

# Modul-modul bawaan Python (tidak perlu dimasukkan ke requirements.txt)
# Daftar ini bisa ditambah kalau kamu mau
BUILTIN_MODULES = {
    'os', 'sys', 're', 'json', 'csv', 'argparse', 'datetime', 'logging',
    'io', 'typing', 'urllib', 'xml', 'time', 'pathlib', 'subprocess',
    'shutil', 'math', 'itertools', 'functools', 'collections', 'dataclasses'
}

# Pemetaan nama import -> nama paket di pip
PACKAGE_MAP = {
    'bs4': 'beautifulsoup4',
    'PIL': 'pillow',
    'dotenv': 'python-dotenv',
    'cv2': 'opencv-python',
}

def get_imports_from_file(filename):
    """Parse file .py dan ambil semua import module"""
    with open(filename, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filename)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return sorted(imports)

def filter_external_modules(modules):
    """Filter modul non-bawaan dan ubah ke nama paket pip"""
    external = set()
    for mod in modules:
        if mod in BUILTIN_MODULES:
            continue
        pkg_name = PACKAGE_MAP.get(mod, mod)
        external.add(pkg_name)
    return sorted(external)

def main(source_file, output_file="requirements.txt"):
    modules = get_imports_from_file(source_file)
    external = filter_external_modules(modules)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(external))

    print(f"[+] requirements.txt berhasil dibuat dari {source_file}")
    print("Isi file:")
    for pkg in external:
        print(" -", pkg)

if __name__ == "__main__":
    # Ganti 'script_kamu.py' dengan nama file Python yang mau dibaca
    main("scraper.py")
