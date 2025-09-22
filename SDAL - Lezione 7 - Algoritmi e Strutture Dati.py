# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 7
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 7
# =================================================
# Prof. Andrea Cigliano
# =================================================

# ===============================================
# 1) HASH TABLE (con separate chaining + resize)
# ===============================================
class HashTable:
    """
    Implementazione minimale di una tabella hash con:
    - hashing tramite built-in hash()
    - gestione collisioni con separate chaining (liste)
    - ridimensionamento automatico quando il load factor supera una soglia
    Metodi: put, get, delete, __contains__, __len__, keys, values, items
    """

    def __init__(self, initial_capacity=8, load_factor_threshold=0.75):
        # Numero di "bucket" (liste) iniziali: potenza di 2 aiuta la distribuzione
        self._capacity = max(8, int(initial_capacity))
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0  # numero di coppie (chiave, valore) attualmente memorizzate
        self._load_factor_threshold = load_factor_threshold

    # ---------------------------
    # Funzioni di supporto interne
    # ---------------------------
    def _bucket_index(self, key):
        # Converte l'hash (che può essere negativo) in indice di bucket [0..capacity-1]
        return hash(key) & (self._capacity - 1) if (self._capacity & (self._capacity - 1)) == 0 \
               else hash(key) % self._capacity

    def _should_resize(self):
        # Load factor = size / capacity
        return self._size / self._capacity > self._load_factor_threshold

    def _resize(self, new_capacity=None):
        # Raddoppia (o imposta) la capacità e reinserisce tutti gli elementi (re-hash)
        old_items = list(self.items())
        self._capacity = new_capacity if new_capacity is not None else self._capacity * 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for k, v in old_items:
            self.put(k, v)

    # ---------------------------
    # API pubblica
    # ---------------------------
    def put(self, key, value):
        """
        Inserisce/aggiorna (key -> value).
        Se la chiave esiste, aggiorna il valore.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]

        # Cerca se la chiave esiste già nel bucket
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # update in place
                return

        # Nuovo inserimento
        bucket.append((key, value))
        self._size += 1

        # Controlla se serve il resize
        if self._should_resize():
            self._resize()

    def get(self, key, default=None):
        """
        Restituisce il valore associato a key oppure default se non presente.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return default

    def delete(self, key):
        """
        Rimuove la coppia associata a key.
        Solleva KeyError se la chiave non esiste.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return
        raise KeyError(f"Key not found: {key}")

    def __contains__(self, key):
        return self.get(key, default=None) is not None or any(k == key for k, _ in self._buckets[self._bucket_index(key)])

    def __len__(self):
        return self._size

    def keys(self):
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def values(self):
        for bucket in self._buckets:
            for _, v in bucket:
                yield v

    def items(self):
        for bucket in self._buckets:
            for k, v in bucket:
                yield (k, v)

    def __repr__(self):
        pairs = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashTable({{{pairs}}})"


# =========================================================
# 2) INSIEMI DISGIUNTI (UNION-FIND con path compression)
# =========================================================
class DisjointSetUnion:
    """
    Struttura dati per insiemi disgiunti (Union-Find):
    - find(x): trova il rappresentante (radice) dell'insieme di x, con path compression
    - union(a, b): unisce gli insiemi contenenti a e b, con union by rank
    - connected(a, b): True se a e b appartengono allo stesso insieme
    Complessità quasi-ammortizzata ~ O(alpha(n)) per operazione, dove alpha è la funzione di Ackermann inversa.
    """

    def __init__(self, elements=None):
        # Se "elements" è fornito, inizializza ogni elemento come insieme singoletto
        self.parent = {}
        self.rank = {}
        self._components = 0

        if elements is not None:
            for x in elements:
                self.make_set(x)

    def make_set(self, x):
        """Crea un nuovo insieme contenente solo x, se non esiste già."""
        if x not in self.parent:
            self.parent[x] = x  # padre di se stesso
            self.rank[x] = 0    # altezza stimata dell'albero
            self._components += 1

    def find(self, x):
        """
        Restituisce la radice (rappresentante) dell'insieme di x.
        Applica path compression per appiattire l'albero e velocizzare le chiamate successive.
        """
        if x not in self.parent:
            # opzionale: auto-registrazione del nuovo elemento
            self.make_set(x)

        # Path compression ricorsiva
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        """
        Unisce gli insiemi contenenti 'a' e 'b' usando union by rank.
        Se sono già nello stesso insieme, non fa nulla.
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False  # nessuna unione effettuata

        # Attacca l'albero con rank minore sotto quello con rank maggiore
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            # rank uguali: scegli uno come radice e incrementa il suo rank
            self.parent[rb] = ra
            self.rank[ra] += 1

        self._components -= 1
        return True

    def connected(self, a, b):
        """Ritorna True se a e b appartengono allo stesso insieme."""
        return self.find(a) == self.find(b)

    def components(self):
        """Numero di insiemi disgiunti correnti."""
        return self._components

    def groups(self):
        """
        Restituisce un dizionario {radice: [elementi]} con la partizione corrente.
        Utile per ispezione/debug.
        """
        from collections import defaultdict
        g = defaultdict(list)
        for x in self.parent:
            g[self.find(x)].append(x)
        return dict(g)

    def __repr__(self):
        return f"DSU(groups={self.groups()})"


# =========================
# ESEMPIO DI UTILIZZO
# =========================
if __name__ == "__main__":
    # ---- HashTable ----
    ht = HashTable()
    ht.put("alice", 30)
    ht.put("bob", 25)
    ht.put("charlie", 35)
    ht.put("bob", 26)  # update
    print("HashTable items:", list(ht.items()))
    print("bob in ht?", "bob" in ht)
    ht.delete("alice")
    print("Dopo delete('alice'):", list(ht.items()), "size =", len(ht))

    # ---- Disjoint Set Union ----
    dsu = DisjointSetUnion(elements=[1, 2, 3, 4, 5])
    dsu.union(1, 2)
    dsu.union(3, 4)
    print("1 connesso a 2?", dsu.connected(1, 2))
    print("1 connesso a 3?", dsu.connected(1, 3))
    dsu.union(2, 3)  # ora {1,2,3,4} sono collegati
    print("Componenti:", dsu.components())
    print("Gruppi:", dsu.groups())
