from parser import Parser
from cache import Cache

def main():
    p = Parser()
    args = p.parse()

    cache = Cache(nsets=args.nsets, bsize=args.bsize,assoc=args.assoc, subst=args.subst, flagOut=args.flagOut, arquivoEntrada=args.arquivoEntrada)
    cache.simulate()


if __name__ == '__main__':
    main()