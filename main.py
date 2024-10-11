import logging
from typing import Dict, Optional
import frontmatter
from pathlib import Path

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constantes
MARKDOWN_EXTENSION = '.md'


def get_metadata(path: Path) -> dict:
    """
    Extrai metadados de um arquivo Markdown com frontmatter.

    Args:
        path (Path): Caminho do arquivo.

    Returns:
        Dict: Dicionário com os metadados do arquivo.
    """
    try:
        with path.open(encoding='utf-8') as file:
            post = frontmatter.load(file)
            return post.metadata
    except FileNotFoundError:
        print(f'Arquivo não encontrado: {path}')
    except frontmatter.ParseException:
        print(f'Erro ao analisar metadados em: {path}')
    except Exception as e:
        logging.error(f'Erro inesperado ao processar {path}: {e}')
    return {}


def metadata_check(metadata_obj: dict, key: str, target: str) -> Optional[bool]:
    """
    Verifica se um par chave-valor específico está nos metadados.

    Args:
        metadata (Dict): Dicionário com metadados do arquivo.
        key (str): Chave a ser verificada.
        target (str): Valor alvo para a chave.

    Returns:
        Optional[bool]: True se encontrar a chave e o valor corresponder,
                        False se a chave existir, mas o valor não corresponder,
                        None se a chave não existir.
    """
    value = metadata_obj.get(key)
    if value is None:
        logging.warning(f'Campo alvo "{key}" não encontrado.')
        return None
    return value == target


def move_file(root_folder: Path, meta_value: str, file: Path) -> None:
    """
    Move um arquivo para uma pasta de destino.

    Args:
        root_folder (Path): Pasta raiz.
        meta_value (str): Valor do metadado usado como nome da pasta de destino.
        file (Path): Arquivo a ser movido.
    """
    pasta_destino = root_folder / meta_value
    pasta_destino.mkdir(parents=True, exist_ok=True)
    """O método .rename move o arquivo para o local desejado."""
    file.rename(root_folder / meta_value / file.name)
    logging.info(f'Arquivo movido com sucesso: {file.name} -> {pasta_destino}.')


def process_file(root_folder: Path, meta_key: str, meta_value: str) -> None:
    """
        Processa arquivos Markdown em uma pasta, movendo-os se atenderem a um critério de metadados.

        Args:
            root_folder (Path): Pasta raiz para procurar arquivos.
            meta_key (str): Chave do metadado a ser verificada.
            meta_value (str): Valor do metadado para comparação.
        """
    for file in root_folder.glob(f'*{MARKDOWN_EXTENSION}'):
        metadata = get_metadata(file)
        if metadata_check(metadata, meta_key, meta_value):
            move_file(root_folder, meta_value, file)
            print('Arquivo movido com sucesso!')
        else:
            logging.info(f'Arquivo não atende ao critério: {file.name}')


def get_input(message: str) -> str:
    result = str(input(message))
    return result


def main() -> None:
    """
    root_folder é a pasta raiz. Esse valor pode ser alterado quando precisar usar esse script em outra pasta.
    meta_key pede num input ao usuário o campo do frontmatter que vai usar como referência na busca.
    meta_value pede num input qual é o valor que o script vau usar para criar uma nova pasta se necessário e
    mover o arquivo em questão.
    """
    root_folder = Path(r'D:\Google Drive - Lucas\OBSIDIAN Lucas\Lucas\005_TEOCRÁTICO\Discursos')
    meta_key = get_input('Digite o campo que deseja procurar: (Por exemplo "Parte" ou "Orador") ')
    meta_value = get_input('Digite o valor que quer usar como referência: Por exemplo "Tesouros" ou "Lucas") ')

    if not root_folder.exists():
        logging.error(f'O diretório especificado não existe: {root_folder}')
        return

    logging.info(f'Iniciando processamento na pasta: {root_folder}')
    process_file(root_folder, meta_key, meta_value)
    logging.info(f'Processamento concluído.')


if __name__ == '__main__':
    main()
