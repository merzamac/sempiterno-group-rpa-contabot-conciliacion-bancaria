from itertools import islice


def split_operation(lista: tuple, chunk):
    """Generador que divide la lista en chunks (eficiente en memoria)"""
    it = iter(lista)
    while True:
        _slice = list(islice(it, chunk))
        if not _slice:
            return
        yield _slice
