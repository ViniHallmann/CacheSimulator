import os
import argparse
from typing import Any

class Parser:
    """
    Parser de argumentos para o simulador de cache.
    Processa e valida os argumentos da linha de comando.
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Cache Simulator')
        self.parser.add_argument('nsets',          type=int, help='Número de conjuntos')
        self.parser.add_argument('bsize',          type=int, help='Tamanho do bloco')
        self.parser.add_argument('assoc',          type=int, help='Associatividade')
        self.parser.add_argument('subst',          type=str, choices=['R', 'F', 'L'], help='Algoritmo de substituição')
        self.parser.add_argument('flagOut',        type=int, choices=[0, 1],          help='Flag de saída')
        self.parser.add_argument('arquivoEntrada', type=str, help='Arquivo de entrada')
        self.parser.add_argument("-d", "--debug", action="store_true", help="Ativa o modo debug")

    def parse(self) -> Any:
        """
        Processa os argumentos da linha de comando.
        """
        args = self.parser.parse_args()
        self.validate_args(args)
        return args
    
    def validate_args(self, args: Any) -> None:
        """
        Valida os argumentos processados.
        """
        if args.nsets <= 0:
            self.parser.error("nsets deve ser maior que zero.")
        if args.bsize <= 0:
            self.parser.error("bsize deve ser maior que zero.")
        if args.assoc <= 0:
            self.parser.error("assoc deve ser maior que zero.")
        
        if not os.path.isfile(args.arquivoEntrada):
            self.parser.error(f"Arquivo de entrada '{args.arquivoEntrada}' não encontrado.")