# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 2
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 2 
# =================================================
# Prof. Andrea Cigliano
# =================================================


# =========================
# 1. SELECTION SORT
# =========================
def selection_sort(arr):
    """
    Selection Sort: trova il minimo a ogni iterazione e lo scambia in posizione corretta.
    Complessità: O(n^2)
    """
    n = len(arr)
    for i in range(n):
        # Supponiamo che il minimo sia in posizione i
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j  # aggiornamento indice del minimo
        # Scambio tra arr[i] e arr[min_idx]
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# =========================
# 2. INSERTION SORT
# =========================
def insertion_sort(arr):
    """
    Insertion Sort: costruisce l'array ordinato inserendo ogni elemento
    nella posizione corretta rispetto ai precedenti.
    Complessità: O(n^2), ma O(n) nel caso migliore (array già ordinato).
    """
    for i in range(1, len(arr)):
        key = arr[i]       # elemento da inserire
        j = i - 1
        # sposta a destra tutti gli elementi maggiori di key
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key     # inserisce key nella posizione giusta
    return arr


# =========================
# 3. BUBBLE SORT
# =========================
def bubble_sort(arr):
    """
    Bubble Sort: confronta coppie adiacenti e scambia se fuori ordine.
    Complessità: O(n^2)
    """
    n = len(arr)
    for i in range(n):
        # flag per vedere se ci sono stati scambi
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # se non ci sono stati scambi, array già ordinato
        if not swapped:
            break
    return arr


# =========================
# 4. QUICK SORT
# =========================
def quick_sort(arr):
    """
    Quick Sort: divide l'array in due sottoarray rispetto a un pivot,
    ricorsivamente ordina i due sottoarray.
    Complessità media: O(n log n), peggiore: O(n^2).
    """

    # Caso base: array con 0 o 1 elementi è già ordinato
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]  # scegliamo pivot centrale
    left = [x for x in arr if x < pivot]      # elementi < pivot
    middle = [x for x in arr if x == pivot]   # elementi == pivot
    right = [x for x in arr if x > pivot]     # elementi > pivot

    # ricorsione su left e right
    return quick_sort(left) + middle + quick_sort(right)


# =========================
# ESEMPIO DI UTILIZZO
# =========================
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]

    print("Originale:", data)
    print("Selection Sort:", selection_sort(data.copy()))
    print("Insertion Sort:", insertion_sort(data.copy()))
    print("Bubble Sort:", bubble_sort(data.copy()))
    print("Quick Sort:", quick_sort(data.copy()))
