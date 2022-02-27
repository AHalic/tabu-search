from typing import List

def sort_with_key(nodes: List[dict], key: str, reverse:bool=True) -> List[dict]:
    """
    Ordena lista de dicionario de forma descresncete com base no string utilizada
    Caso reverse=False, os valores estarao em ordem crescente.
    """
    return sorted(nodes, key=lambda item: item[key], reverse=reverse) 