import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Cache.parser   import Parser
from Cache.cache    import Cache

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