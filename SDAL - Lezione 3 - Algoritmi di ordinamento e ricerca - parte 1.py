# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 3
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 3 
# =================================================
# Prof. Andrea Cigliano
# =================================================

# ========================================
# 1. LINEAR SEARCH
# ========================================
def linear_search(arr, target):
    """
    Linear Search:
    Scorre la lista da sinistra a destra fino a trovare il target.
    Complessità: O(n) nel caso medio/peggiore, O(1) nel migliore.
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i   # ritorna l'indice se trovato
    return -1          # -1 indica che non è presente


# ========================================
# 2. BINARY SEARCH
# ========================================
def binary_search(arr, target):
    """
    Binary Search:
    Funziona SOLO se l'array è ordinato.
    Divide l'intervallo a metà ad ogni passo.
    Complessità: O(log n) in tutti i casi non banali.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2  # indice centrale
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1   # cerca a destra
        else:
            right = mid - 1  # cerca a sinistra
    return -1


# ========================================
# 3. MERGE SORT
# ========================================
def merge_sort(arr):
    """
    Merge Sort:
    Algoritmo 'divide et impera':
    - divide la lista in due metà,
    - ordina ricorsivamente,
    - unisce i risultati.
    Complessità: O(n log n) in tutti i casi.
    Spazio: O(n) (usa array ausiliari).
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def merge(left, right):
    """ Funzione di supporto per unire due liste ordinate """
    merged = []
    i = j = 0

    # confronta gli elementi delle due liste
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # aggiunge eventuali restanti
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


# ========================================
# 4. HEAP SORT
# ========================================
def heapify(arr, n, i):
    """
    Funzione di supporto per mantenere la proprietà di max-heap.
    - arr: array da ordinare
    - n: dimensione dell'heap
    - i: indice della radice del sottoalbero
    """
    largest = i
    left = 2 * i + 1     # figlio sinistro
    right = 2 * i + 2    # figlio destro

    # confronta con figlio sinistro
    if left < n and arr[left] > arr[largest]:
        largest = left

    # confronta con figlio destro
    if right < n and arr[right] > arr[largest]:
        largest = right

    # se il nodo radice non è il più grande, scambia e ricorsione
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    """
    Heap Sort:
    - Costruisce un max-heap
    - Estrae uno per volta il massimo e ricostruisce l'heap.
    Complessità: O(n log n) in tutti i casi.
    Spazio: O(1) (in-place).
    """
    n = len(arr)

    # costruisce l'heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # estrae elementi uno a uno
    for i in range(n - 1, 0, -1):
        # scambia radice (massimo) con ultimo elemento
        arr[i], arr[0] = arr[0], arr[i]
        # ripristina heap sulla parte rimanente
        heapify(arr, i, 0)

    return arr


# ========================================
# ESEMPIO DI UTILIZZO
# ========================================
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]

    print("Array originale:", data)

    # Ricerca lineare
    print("Linear Search (22):", linear_search(data, 22))
    print("Linear Search (100):", linear_search(data, 100))

    # Ricerca binaria (serve array ordinato!)
    sorted_data = sorted(data)
    print("Array ordinato:", sorted_data)
    print("Binary Search (25):", binary_search(sorted_data, 25))
    print("Binary Search (100):", binary_search(sorted_data, 100))

    # Merge Sort
    print("Merge Sort:", merge_sort(data.copy()))

    # Heap Sort
    print("Heap Sort:", heap_sort(data.copy()))

