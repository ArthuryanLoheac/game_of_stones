import re

def is_valid_format(line: str):
    """
    Vérifie si la ligne correspond au format : "<pers> is friends with <pers>"
    et retourne la paire [pers1, pers2] si valide.
    """
    pattern = r'^(\S.*) is friends with (\S.*)$'
    match = re.match(pattern, line)
    if match:
        return [match.group(1).strip(), match.group(2).strip()]
    return None

def is_valid_plot_format(line: str):
    """
    Vérifie si la ligne correspond au format : "<pers> is plotting against <pers>"
    et retourne la paire [pers1, pers2] si valide.
    """
    pattern = r'^(\S.*) is plotting against (\S.*)$'
    match = re.match(pattern, line)
    if match:
        return [match.group(1).strip(), match.group(2).strip()]
    return None

def read_file(file_path: str) -> list:
    """Lit un fichier et retourne la liste des lignes."""
    try:
        with open(file_path, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")

def get_list_pair_friend(lines: list):
    """Extrait les paires d'amitié à partir des lignes du fichier."""
    pairs = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        pair = is_valid_format(line)
        if pair is not None:
            pairs.append(pair)
        else:
            raise ValueError(f"Invalid format in friendship file: {line}")
    return pairs

def get_list_pair_conspiracy(lines: list):
    """Extrait les paires de complot à partir des lignes du fichier."""
    pairs = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        pair = is_valid_plot_format(line)
        if pair is not None:
            pairs.append(pair)
        else:
            raise ValueError(f"Invalid format in conspiracy file: {line}")
    return pairs
