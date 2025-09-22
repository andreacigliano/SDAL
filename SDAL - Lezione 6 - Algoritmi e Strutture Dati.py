# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 6
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 6
# =================================================
# Prof. Andrea Cigliano
# =================================================

# ============================================
# 1) ARRAY DINAMICO (facciata su list di Python)
# ============================================

class DynamicArray:
    """
    Array dinamico stile Python.
    Sotto il cofano usa 'list', che ridimensiona automaticamente la capacità
    con costo amortizzato O(1) per append.
    """
    def __init__(self, iterable=None):
        self._a = list(iterable) if iterable is not None else []

    def __len__(self):
        return len(self._a)

    def __getitem__(self, idx):
        return self._a[idx]  # indicizzazione O(1)

    def __setitem__(self, idx, value):
        self._a[idx] = value

    def append(self, value):
        self._a.append(value)  # O(1) amortizzato

    def insert(self, idx, value):
        self._a.insert(idx, value)  # O(n) per lo shift a destra

    def remove_at(self, idx):
        """Rimuove l'elemento all'indice dato (O(n) per lo shift a sinistra)."""
        return self._a.pop(idx)

    def to_list(self):
        return list(self._a)

    def __repr__(self):
        return f"DynamicArray({self._a!r})"


# ============================================
# 2) LISTA COLLEGATA (Singly Linked List)
# ============================================

class SinglyLinkedListNode:
    def __init__(self, value, next_=None):
        self.value = value
        self.next = next_

class SinglyLinkedList:
    """
    Lista collegata semplice:
    - Inserimento in testa: O(1)
    - Inserimento in coda: O(n) (senza tail); O(1) mantenendo tail
    - Ricerca: O(n)
    - Indicizzazione casuale: O(n) (non come l'array)
    """
    def __init__(self):
        self.head = None
        self.tail = None  # manteniamo una coda per append O(1)
        self._size = 0

    def __len__(self):
        return self._size

    def prepend(self, value):
        node = SinglyLinkedListNode(value, self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def append(self, value):
        node = SinglyLinkedListNode(value)
        if self.tail is None:
            # lista vuota
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def find(self, predicate):
        """Ritorna il primo valore che soddisfa predicate(value), altrimenti None."""
        cur = self.head
        while cur:
            if predicate(cur.value):
                return cur.value
            cur = cur.next
        return None

    def remove_first(self, value):
        """Rimuove la prima occorrenza (se presente)."""
        prev = None
        cur = self.head
        while cur:
            if cur.value == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur is self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def __repr__(self):
        return "SinglyLinkedList([" + ", ".join(repr(x) for x in self) + "])"


# ============================================
# 3) STACK (LIFO) con list
# ============================================

class Stack:
    """
    Stack LIFO:
    - push/pop in cima: O(1) amortizzato usando list.append / list.pop()
    """
    def __init__(self):
        self._data = []

    def push(self, x):
        self._data.append(x)

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if not self._data:
            return None
        return self._data[-1]

    def is_empty(self):
        return not self._data

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack({self._data!r})"


# ============================================
# 4) QUEUE / CODA (FIFO) con deque
# ============================================

from collections import deque

class Queue:
    """
    Coda FIFO:
    - enqueue (push in coda): O(1)
    - dequeue (pop da testa): O(1)
    Implementata con collections.deque per avere operazioni O(1) agli estremi.
    """
    def __init__(self):
        self._q = deque()

    def enqueue(self, x):
        self._q.append(x)

    def dequeue(self):
        if not self._q:
            raise IndexError("dequeue from empty queue")
        return self._q.popleft()

    def peek(self):
        return self._q[0] if self._q else None

    def is_empty(self):
        return not self._q

    def __len__(self):
        return len(self._q)

    def __repr__(self):
        return f"Queue({list(self._q)!r})"


# ============================================
# 5) STRUTTURA GERARCHICA GENERICA (Albero N-ario)
# ============================================

class NaryTreeNode:
    """
    Nodo di un albero N-ario (struttura gerarchica generica).
    Ogni nodo può avere 0..N figli.
    """
    def __init__(self, value):
        self.value = value
        self.children = []  # lista di figli

    def add_child(self, child_node):
        self.children.append(child_node)

    def dfs(self):
        """Visita in profondità (pre-ordine): nodo -> figli."""
        yield self.value
        for c in self.children:
            yield from c.dfs()

    def bfs(self):
        """Visita in ampiezza (per livelli)."""
        q = deque([self])
        while q:
            node = q.popleft()
            yield node.value
            for c in node.children:
                q.append(c)

    def __repr__(self):
        return f"NaryTreeNode({self.value!r})"


# ============================================
# 6) ALBERO BINARIO (nodo + traversali)
# ============================================

class BinaryTreeNode:
    """
    Nodo di un albero binario.
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left: 'BinaryTreeNode | None' = left
        self.right: 'BinaryTreeNode | None' = right

    # Traversale in-order: sinistra -> nodo -> destra
    def inorder(self):
        if self.left:
            yield from self.left.inorder()
        yield self.value
        if self.right:
            yield from self.right.inorder()

    # Traversale pre-order: nodo -> sinistra -> destra
    def preorder(self):
        yield self.value
        if self.left:
            yield from self.left.preorder()
        if self.right:
            yield from self.right.preorder()

    # Traversale post-order: sinistra -> destra -> nodo
    def postorder(self):
        if self.left:
            yield from self.left.postorder()
        if self.right:
            yield from self.right.postorder()
        yield self.value

    # BFS per livelli
    def level_order(self):
        q = deque([self])
        while q:
            node = q.popleft()
            yield node.value
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

    def __repr__(self):
        return f"BinaryTreeNode({self.value!r})"


# ============================================
# 7) HEAP BINARIO (MIN-HEAP) implementato da zero
# ============================================

class MinHeap:
    """
    Min-heap binario implementato con array (lista).
    Proprietà: il minimo è alla radice (indice 0).
    Operazioni:
      - push: O(log n)
      - pop_min: O(log n)
      - peek: O(1)
    """
    def __init__(self, iterable=None):
        self._a = []
        if iterable:
            self._a = list(iterable)
            self._heapify()  # costruzione O(n)

    # ----------------- Helpers di indicizzazione -----------------
    def _parent(self, i): return (i - 1) // 2
    def _left(self, i):   return 2 * i + 1
    def _right(self, i):  return 2 * i + 2

    # ----------------- Ripristino proprietà heap -----------------
    def _sift_up(self, i):
        """Risale finché il nodo è >= del padre (heap min)."""
        while i > 0:
            p = self._parent(i)
            if self._a[i] < self._a[p]:
                self._a[i], self._a[p] = self._a[p], self._a[i]
                i = p
            else:
                break

    def _sift_down(self, i):
        """Scende scambiando col più piccolo dei figli se viola la proprietà."""
        n = len(self._a)
        while True:
            l = self._left(i)
            r = self._right(i)
            smallest = i

            if l < n and self._a[l] < self._a[smallest]:
                smallest = l
            if r < n and self._a[r] < self._a[smallest]:
                smallest = r

            if smallest != i:
                self._a[i], self._a[smallest] = self._a[smallest], self._a[i]
                i = smallest
            else:
                break

    def _heapify(self):
        """Costruisce l'heap da un array arbitrario. O(n)."""
        for i in range((len(self._a) // 2) - 1, -1, -1):
            self._sift_down(i)

    # ----------------- API pubblica -----------------
    def push(self, x):
        """Inserisce un nuovo elemento (O(log n))."""
        self._a.append(x)
        self._sift_up(len(self._a) - 1)

    def peek(self):
        """Ritorna il minimo senza rimuoverlo."""
        if not self._a:
            return None
        return self._a[0]

    def pop_min(self):
        """Rimuove e ritorna il minimo (O(log n))."""
        if not self._a:
            raise IndexError("pop from empty heap")
        n = len(self._a)
        self._a[0], self._a[n - 1] = self._a[n - 1], self._a[0]
        min_val = self._a.pop()
        if self._a:
            self._sift_down(0)
        return min_val

    def __len__(self):
        return len(self._a)

    def __bool__(self):
        return bool(self._a)

    def __repr__(self):
        return f"MinHeap({self._a!r})"


# ============================================
# ESEMPIO D'USO RAPIDO
# ============================================

if __name__ == "__main__":
    # Array
    arr = DynamicArray([3, 1, 4])
    arr.append(2)
    arr.insert(1, 9)
    _ = arr.remove_at(0)  # rimuove 3
    print("DynamicArray:", arr)

    # Lista collegata
    ll = SinglyLinkedList()
    ll.append(10); ll.append(20); ll.prepend(5)
    ll.remove_first(20)
    print("LinkedList:", ll, "-> elementi:", list(ll))

    # Stack
    st = Stack()
    st.push(1); st.push(2); st.push(3)
    print("Stack top:", st.peek(), "pop:", st.pop(), "resta:", st)

    # Queue
    q = Queue()
    q.enqueue("a"); q.enqueue("b"); q.enqueue("c")
    print("Queue front:", q.peek(), "dequeue:", q.dequeue(), "resta:", q)

    # Albero N-ario
    root = NaryTreeNode("root")
    c1, c2 = NaryTreeNode("c1"), NaryTreeNode("c2")
    root.add_child(c1); root.add_child(c2)
    c1.add_child(NaryTreeNode("c1.1"))
    print("N-ary DFS:", list(root.dfs()))
    print("N-ary BFS:", list(root.bfs()))

    # Albero binario (manuale) e traversali
    bt = BinaryTreeNode(2,
            left=BinaryTreeNode(1),
            right=BinaryTreeNode(3))
    print("BT inorder:", list(bt.inorder()))
    print("BT preorder:", list(bt.preorder()))
    print("BT postorder:", list(bt.postorder()))
    print("BT level-order:", list(bt.level_order()))

    # Min-Heap
    h = MinHeap([5, 3, 8, 1, 2])
    print("Heap dopo heapify:", h, "min:", h.peek())
    h.push(0)
    print("Heap push(0):", h, "pop_min():", h.pop_min(), "->", h)
