from cache.parser import Parser
from cache.cache import Cache

def main():
    p = Parser()
    args = p.parse()

    cache = Cache(
        nsets=args.nsets,
        bsize=args.bsize,assoc=args.assoc,
        subst=args.subst,
        flagOut=args.flagOut,
        arquivoEntrada=args.arquivoEntrada,
        debug=args.debug
    )

    if (cache.debug):
        cache.get_info()
    cache.simulate()
    cache.get_simulation()

if __name__ == '__main__':
    main()