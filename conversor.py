from encoder import encrypt, check, processar_lista
from collections import namedtuple
from itertools import islice
from os import sched_getaffinity
from threading import Thread
from timeit import default_timer


def open_file(limite=0):
    """Abre o arquivo e particiona a lista para processamento paralelo."""
    with open('base.txt', 'r') as f:
        if limite:
            tmp = f.read().splitlines()[:limite]
        else:
            tmp = f.read().splitlines()
        f.close()

    user = namedtuple('User', ['login', 'pwd'])
    base = map(user._make, (i.split('|')[1:3] for i in tmp))

    if not limite:
        limite = len(tmp)

    tamanho = limite//len(sched_getaffinity(0))

    return (iter(lambda: tuple(islice(base, tamanho)), ()), limite)


def processar_arquivo(file, tamanho):
    """Processa o arquivo lido e retorna o output."""
    threads = []
    fila = []
    for item in file:
        threads.append(
            Thread(target=processar_lista, args=(item, fila), daemon=True))

    for item in threads:
        item.start()

    last_print = 0
    while True:
        if not [item for item in threads if item.is_alive()]:
            break
        last_print = print_log(last_print, len(fila), tamanho)

    for item in threads:
        item.join()

    return fila

def print_log(last, tam_fila, tam_file):
    """."""
    offset = (tam_file * 0.01)
    if last + offset <= tam_fila:
        last = tam_fila

        print('Faltam:\t{}'.format(tam_file - tam_fila))
    return last


if __name__ == '__main__':
    times = []
    
    # for i in range(100):
    file, tamanho = open_file()
    start = default_timer()
    file_proc = processar_arquivo(file=file, tamanho=tamanho)
    execucao = default_timer() - start

    times.append(execucao)

    with open('base-output.txt', 'w') as f:
        f.writelines(file_proc)
        f.close()

    print("Tempo de execução: %.10f s" % (sum(times)/len(times)))
