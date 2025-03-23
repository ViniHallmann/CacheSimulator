from Cache.block                        import Block
from Cache.statistics                   import Statistics
from Cache.ReplacementPolicies.random  import Random
from Cache.ReplacementPolicies.fifo    import FIFO
from Cache.ReplacementPolicies.lru     import LRU
from Cache.ReplacementPolicies.base    import ReplacementPolicy
import math
import struct

class Cache:
    def __init__(self, nsets, bsize, assoc, subst, flagOut, arquivoEntrada, debug):
        """
        Inicializa cache
        """
        self.nsets: int             = nsets
        self.bsize: int             = bsize
        self.assoc: int             = assoc
        self.subst: str             = subst
        self.flagOut: int           = flagOut
        self.arquivoEntrada: str    = arquivoEntrada
        self.debug: str             = debug

        self.replacement_policy: ReplacementPolicy = None

        #Na real quando fiz o código inicial isso fazia sentido
        #Faz sentido usar essas funções agora??
        self.offset_bits: int = self.get_offset(bsize)
        self.index_bits:  int = self.get_index(nsets)
        self.tag_bits:    int = self.get_tag(nsets, bsize)

        self.mapping_type: str = ""
        #Se tem mais de um conjunto e somente uma associação -> Mapeamento Direto
        #Se tem mais de um conjunto e mais de uma associação -> Conjunto Associativo
        #Se tem um conjunto e mais de uma associação         -> Totalmente Associativo
        if self.nsets >= 1 and self.assoc == 1:
            self.mapping_type = "direct"
        elif self.nsets > 1 and self.assoc > 1:
            self.mapping_type = "set"
        elif self.nsets == 1 and self.assoc > 1:
            self.mapping_type = "fully"
        else:
            raise ValueError("Tipo de mapeamento inválido.")

        #Inicia estatisticas da cache
        self.stats = Statistics()

        #Cria cache
        self.cache = self.create_cache(nsets, bsize, assoc)

        #So usa politica de substituicao se nao for mapeamento direto
        if self.mapping_type != "direct":
            self.replacement_policy = self.attach_replacement_policy(subst)

    def attach_replacement_policy(self, subst: str = "R"):
        """
        Anexa uma política de substituição à cache.
        Valor default: "R" (Random)
        """
        if subst == "R":
            return Random(self.nsets, self.assoc)
        elif subst == "F":
            return FIFO(self.nsets, self.assoc)
        elif subst == "L":
            return LRU(self.nsets, self.assoc)
        else:
            raise ValueError("Política de substituição inválida.")

    def get_offset(self, bsize: int) -> int:
        """
        Retorna offset
        """
        return int(math.log2(bsize))

    def get_index(self, nsets: int) -> int:
        """
        Retorna index
        """
        return int(math.log2(nsets))

    def get_tag(self, nsets: int, bsize: int) -> int:
        """
        Retorna tag
        """
        return 32 - self.get_offset(bsize) - self.get_index(nsets)
    
    def get_address_components(self, address) -> tuple:
        """
        Retorna tag, index e offset de um endereço
        """
        offset: int = address & ((1 << self.offset_bits) - 1)
        index:  int = (address >> self.offset_bits) & ((1 << self.index_bits) - 1)
        tag:    int = (address >> (self.offset_bits + self.index_bits)) & ((1 << self.tag_bits) - 1)
        return tag, index, offset
    
    def create_cache(self, nsets: int, bsize: int, assoc: int) -> list:
        """
        Cria cache
        """
        cache: list = []
        for _ in range(nsets):
            sets: list = []
            for _ in range(assoc):  
                sets.append(Block())
            cache.append(sets)
        return cache

    def get_info(self) -> None:
        num_sets = self.nsets
        blocks_per_set = self.assoc
        block_size = self.bsize
        total_cache_size = self.nsets * self.assoc * self.bsize
        offset = self.offset_bits
        index = self.index_bits
        tag = self.tag_bits

        print(
            "\n🔹 CONFIGURAÇÃO DA CACHE 🔹\n"
            "============================\n"
            f"📌 Número de Conjuntos    : {num_sets}\n"
            f"📌 Blocos por Conjunto    : {blocks_per_set}\n"
            f"📌 Tamanho do Bloco       : {block_size} bytes\n"
            f"📌 Tamanho Total da Cache : {total_cache_size} bytes\n"
            "----------------------------\n"
            f"🔢 Bits de Offset         : {offset} bits\n"
            f"🔢 Bits de Índice         : {index} bits\n"
            f"🔢 Bits de Tag            : {tag} bits\n"
            "============================\n"
        )
        
    def simulate(self) -> None:
        if (self.debug):
            print("Iniciando leitura do arquivo ...\n")

        with open(self.arquivoEntrada, 'rb') as file:
            addresses: list = []
            while chunk := file.read(4):
                address: int = struct.unpack('>I', chunk)[0] 
                addresses.append(str(address))

                self.stats.increment_access()

                tag, index, offset = self.get_address_components(address)
                if self.debug:
                    print(f"Address: {address} => Tag: {tag}, Index: {index}, Offset: {offset}")
                
                if self.mapping_type == "direct":
                    self.simulate_direct_mapped(address)
                elif self.mapping_type == "set":
                    self.simulate_set_associative(address)
                elif self.mapping_type == "fully":
                    self.simulate_fully_associative(address)
                else:
                    raise ValueError("Tipo de mapeamento inválido.")
        if (self.debug):
            max_width = max(len(num) for num in addresses)
            for i in range(0, len(addresses), 15):
                print("  ".join(f"{num:>{max_width}}" for num in addresses[i:i+15]))
    
    def simulate_direct_mapped(self, address) -> None:
        #ACESSO DIRETO AO BLOCO
        tag, index, offset = self.get_address_components(address)
        
        block = self.cache[index][0]
        
        if block.valid and block.tag == tag:
            self.stats.increment_hit()
            return True
        
        if not block.valid:
            self.stats.increment_compulsory()
        else:
            self.stats.increment_conflict()

        block.tag = tag
        block.valid = True
        block.set_data(address)
        
        return False
    
    def simulate_set_associative(self, address) -> None:
        tag, index, offset = self.get_address_components(address)
        
        #PROCURA POR HIT
        for i in range(self.assoc):
            block = self.cache[index][i]
            if not block.valid:
                # Encontrou um bloco inválido - Miss compulsório
                block.tag = tag
                block.valid = True
                block.set_data(address)
                self.replacement_policy.update_usage(index, i)
                self.stats.increment_compulsory()
                return False
            elif block.tag == tag:
                # Hit - bloco válido com a mesma tag
                self.stats.increment_hit()
                self.replacement_policy.update_usage(index, i)
                return True
        
        # Se chegou aqui, todos os blocos são válidos mas nenhum tem a tag procurada
        # É um miss de conflito ou capacidade
        block_index = self.replacement_policy.select_block(index)
        block = self.cache[index][block_index]
        block.tag = tag
        block.valid = True
        block.set_data(address)
        self.replacement_policy.update_usage(index, block_index)
        
        if self.is_cache_completely_full():
            self.stats.increment_capacity()
        else:
            self.stats.increment_conflict()

        return False

    def simulate_fully_associative(self, address) -> None:
        tag, index, offset = self.get_address_components(address)
    
        # PROCURA POR HIT
        for i in range(self.assoc):
            block = self.cache[0][i]
            if not block.valid:
                # Encontrou um bloco inválido - Miss compulsório
                block.tag = tag
                block.valid = True
                block.set_data(address)
                self.replacement_policy.update_usage(0, i)
                self.stats.increment_compulsory()
                return False
            elif block.tag == tag:
                # Hit - bloco válido com a mesma tag
                self.stats.increment_hit()
                self.replacement_policy.update_usage(0, i)
                return True
        
        # Se chegou aqui, todos os blocos são válidos mas nenhum tem a tag procurada
        # Na cache totalmente associativa, isso é sempre um miss de capacidade
        block_index = self.replacement_policy.select_block(0)
        block = self.cache[0][block_index]
        block.tag = tag
        block.valid = True
        block.set_data(address)
        self.replacement_policy.update_usage(0, block_index)

        self.stats.increment_capacity()
        
        return False

    def is_cache_completely_full(self) -> bool:
        """Verifica se TODA a cache está cheia"""
        return all(all(block.valid for block in set_blocks) for set_blocks in self.cache)
            
    def get_simulation(self) -> None:
        total_accesses = self.stats.access
        total_hits = self.stats.hit
        total_misses = self.stats.get_total_misses()
        compulsory_misses = self.stats.misses["compulsory"]
        conflict_misses = self.stats.misses["conflict"]
        capacity_misses = self.stats.misses["capacity"]

        hit_rate = self.stats.get_hit_rate()
        miss_rate = self.stats.get_miss_rate()
        compulsory_rate = compulsory_misses / total_misses if total_misses > 0 else 0
        conflict_rate = conflict_misses / total_misses if total_misses > 0 else 0
        capacity_rate = capacity_misses / total_misses if total_misses > 0 else 0

        if self.flagOut == 0:
            print(
                "\n🔹 RESULTADOS DA SIMULAÇÃO 🔹\n"
                "============================\n"
                f"📊 Acessos e Hits:\n"
                f"   ├─ Total de acessos : {total_accesses}\n"
                f"   ├─ Total de hits    : {total_hits}\n"
                f"   └─ Total de misses  : {total_misses}\n"
                "----------------------------\n"
                f"📈 Tipos de Misses:\n"
                f"   ├─ Compulsórios     : {compulsory_misses}\n"
                f"   ├─ Capacidade       : {capacity_misses}\n"
                f"   └─ Conflito         : {conflict_misses}\n"
                "----------------------------\n"
                f"📉 Taxas:\n"
                f"   ├─ Taxa de hits     : {hit_rate:.2%}\n"
                f"   ├─ Taxa de misses   : {miss_rate:.2%}\n"
                f"   ├─ Taxa compulsória : {compulsory_rate:.2%}\n"
                f"   ├─ Taxa capacidade  : {capacity_rate:.2%}\n"
                f"   └─ Taxa conflito    : {conflict_rate:.2%}\n"
                "============================\n"
            )
        else:
            print(f"{total_accesses}, {hit_rate:.2f}, {miss_rate:.2f}, {compulsory_rate:.2f}, {capacity_rate:.2f}, {conflict_rate:.2f}")
