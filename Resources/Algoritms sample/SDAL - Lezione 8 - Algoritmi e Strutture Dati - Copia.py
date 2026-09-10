# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 8
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 8
# =================================================
# Prof. Andrea Cigliano
# =================================================

# ============================================
# ALBERO DI RICERCA BINARIO (BST)
# ============================================

class BSTNode:
    """Nodo di un albero di ricerca binario."""
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    """
    Implementazione classica di BST:
      - Inserimento: O(h)
      - Ricerca:     O(h)
      - Cancellazione: O(h)
    dove h è l'altezza (O(n) nel peggiore dei casi, O(log n) se l'albero è bilanciato).
    """

    def __init__(self):
        self.root = None

    # ---------- INSERIMENTO ----------
    def insert(self, key):
        """Inserisce key mantenendo l'ordinamento BST."""
        def _insert(node, key):
            if node is None:
                return BSTNode(key)
            if key < node.key:
                node.left = _insert(node.left, key)
            elif key > node.key:
                node.right = _insert(node.right, key)
            # Se key == node.key non inseriamo duplicati (politica semplice)
            return node

        self.root = _insert(self.root, key)

    # ---------- RICERCA ----------
    def search(self, key):
        """Ritorna True se key è presente, altrimenti False."""
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    # ---------- MIN / MAX ----------
    def min_value(self):
        """Ritorna la chiave minima (solleva ValueError se albero vuoto)."""
        if not self.root:
            raise ValueError("Albero vuoto")
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.key

    def max_value(self):
        """Ritorna la chiave massima (solleva ValueError se albero vuoto)."""
        if not self.root:
            raise ValueError("Albero vuoto")
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.key

    # ---------- CANCELLAZIONE ----------
    def delete(self, key):
        """Cancella key, se presente, mantenendo la proprietà BST."""
        def _delete(node, key):
            if node is None:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                # Caso 1: nessun figlio o un solo figlio
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                # Caso 2: due figli -> sostituisci con il successore (min nel sottoalbero destro)
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.right = _delete(node.right, succ.key)
            return node

        self.root = _delete(self.root, key)

    # ---------- VISITE ----------
    def inorder(self):
        """Visita in-order: restituisce le chiavi in ordine crescente."""
        res = []
        def _in(node):
            if not node: return
            _in(node.left)
            res.append(node.key)
            _in(node.right)
        _in(self.root)
        return res

    def preorder(self):
        res = []
        def _pre(node):
            if not node: return
            res.append(node.key)
            _pre(node.left)
            _pre(node.right)
        _pre(self.root)
        return res

    def postorder(self):
        res = []
        def _post(node):
            if not node: return
            _post(node.left)
            _post(node.right)
            res.append(node.key)
        _post(self.root)
        return res


# ============================================
# ALBERO AVL (Autobilanciato con rotazioni)
# ============================================

class AVLNode:
    """Nodo di un albero AVL con campo altezza per bilanciamento."""
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # altezza del nodo (foglia = 1)


class AVLTree:
    """
    Albero AVL:
      - Inserimento: O(log n)
      - Ricerca:     O(log n)
      - Cancellazione: O(log n)
    Mantiene |balance| <= 1 per ogni nodo (balance = h(left) - h(right)).
    """

    def __init__(self):
        self.root = None

    # ---------- UTILITIES ----------
    @staticmethod
    def _height(node):
        return node.height if node else 0

    @staticmethod
    def _balance(node):
        # fattore di bilanciamento = altezza(sx) - altezza(dx)
        return (AVLTree._height(node.left) - AVLTree._height(node.right)) if node else 0

    @staticmethod
    def _update_height(node):
        node.height = 1 + max(AVLTree._height(node.left), AVLTree._height(node.right))

    # ---------- ROTAZIONI ----------
    def _rotate_right(self, y):
        """
        Rotazione destra:
               y                  x
              / \                / \
             x   T3    ->       T1  y
            / \                    / \
           T1 T2                  T2 T3
        """
        x = y.left
        T2 = x.right

        # rotazione
        x.right = y
        y.left = T2

        # aggiorna altezze
        self._update_height(y)
        self._update_height(x)

        return x  # nuova radice del sottoalbero

    def _rotate_left(self, x):
        """
        Rotazione sinistra:
           x                       y
          / \                     / \
         T1  y        ->         x  T3
            / \                 / \
           T2 T3               T1 T2
        """
        y = x.right
        T2 = y.left

        # rotazione
        y.left = x
        x.right = T2

        # aggiorna altezze
        self._update_height(x)
        self._update_height(y)

        return y  # nuova radice del sottoalbero

    # ---------- INSERIMENTO ----------
    def insert(self, key):
        """Inserisce key riequilibrando tramite rotazioni se necessario."""
        def _insert(node, key):
            # Inserimento BST standard
            if node is None:
                return AVLNode(key)
            if key < node.key:
                node.left = _insert(node.left, key)
            elif key > node.key:
                node.right = _insert(node.right, key)
            else:
                # niente duplicati
                return node

            # Aggiorna altezza
            self._update_height(node)

            # Controlla squilibri
            balance = self._balance(node)

            # 4 casi classici:

            # Caso LL: sbilanciato a sinistra e key < node.left.key -> rotazione destra
            if balance > 1 and key < node.left.key:
                return self._rotate_right(node)

            # Caso RR: sbilanciato a destra e key > node.right.key -> rotazione sinistra
            if balance < -1 and key > node.right.key:
                return self._rotate_left(node)

            # Caso LR: sbilanciato a sinistra ma key > node.left.key -> rotazione sinistra su left, poi destra
            if balance > 1 and key > node.left.key:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            # Caso RL: sbilanciato a destra ma key < node.right.key -> rotazione destra su right, poi sinistra
            if balance < -1 and key < node.right.key:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            # Se bilanciato, ritorna il nodo così com'è
            return node

        self.root = _insert(self.root, key)

    # ---------- MIN NEL SOTTOALBERO ----------
    @staticmethod
    def _min_node(node):
        cur = node
        while cur.left:
            cur = cur.left
        return cur

    # ---------- CANCELLAZIONE ----------
    def delete(self, key):
        """Cancella key mantenendo l'albero bilanciato tramite rotazioni."""
        def _delete(node, key):
            if node is None:
                return None

            # Cancellazione tipo BST
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                # Nodo trovato: gestisci i casi 0/1/2 figli
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                # Due figli: prendi successore in-order
                succ = self._min_node(node.right)
                node.key = succ.key
                node.right = _delete(node.right, succ.key)

            # Aggiorna altezza
            self._update_height(node)

            # Riequilibrio
            balance = self._balance(node)

            # 4 casi di squilibrio dopo delete:

            # Caso LL
            if balance > 1 and self._balance(node.left) >= 0:
                return self._rotate_right(node)

            # Caso LR
            if balance > 1 and self._balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)

            # Caso RR
            if balance < -1 and self._balance(node.right) <= 0:
                return self._rotate_left(node)

            # Caso RL
            if balance < -1 and self._balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)

            return node

        self.root = _delete(self.root, key)

    # ---------- RICERCA ----------
    def search(self, key):
        """Ritorna True se key è presente, altrimenti False (O(log n))."""
        cur = self.root
        while cur:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    # ---------- VISITE ----------
    def inorder(self):
        res = []
        def _in(n):
            if not n: return
            _in(n.left)
            res.append(n.key)
            _in(n.right)
        _in(self.root)
        return res

    def preorder(self):
        res = []
        def _pre(n):
            if not n: return
            res.append(n.key)
            _pre(n.left)
            _pre(n.right)
        _pre(self.root)
        return res

    def postorder(self):
        res = []
        def _post(n):
            if not n: return
            _post(n.left)
            _post(n.right)
            res.append(n.key)
        _post(self.root)
        return res


# ============================================
# ESEMPIO D'USO RAPIDO
# ============================================
if __name__ == "__main__":
    print("=== BST ===")
    bst = BST()
    for x in [10, 5, 15, 2, 7, 12, 20]:
        bst.insert(x)
    print("InOrder:", bst.inorder())        # [2, 5, 7, 10, 12, 15, 20]
    print("Search 7:", bst.search(7))       # True
    bst.delete(10)
    print("InOrder (senza 10):", bst.inorder())

    print("\n=== AVL ===")
    avl = AVLTree()
    for x in [10, 20, 30, 40, 50, 25]:
        avl.insert(x)
    # L'AVL si riequilibra automaticamente
    print("InOrder:", avl.inorder())        # Ordinato crescente
    print("PreOrder:", avl.preorder())      # Utile per vedere la struttura bilanciata
    avl.delete(40)
    print("InOrder (senza 40):", avl.inorder())
