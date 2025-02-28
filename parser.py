import os
import argparse
from typing import any

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Cache Simulator')
        self.parser.add_argument('nsets',          type=int, help='Número de conjuntos')
        self.parser.add_argument('bsize',          type=int, help='Tamanho do bloco')
        self.parser.add_argument('assoc',          type=int, help='Associatividade')
        self.parser.add_argument('subst',          type=str, choices=['R', 'F', 'L'], help='Algoritmo de substituição')
        self.parser.add_argument('flagOut',        type=int, choices=[0, 1],          help='Flag de saída')
        self.parser.add_argument('arquivoEntrada', type=str, help='Arquivo de entrada')

    def parse(self) -> any:
        args = self.parser.parse_args()
        self.validate_args(args)
        return args
    
    def validate_args(self, args: any) -> None:
        if args.nsets <= 0 or args.bsize <= 0 or args.assoc <= 0: 
            self.parser.error("nsets, bsize e assoc devem ser maiores que zero.")
        if not os.path.isfile(args.arquivoEntrada):
            self.parser.error(f"Arquivo de entrada '{args.arquivoEntrada}' não encontrado.")