from encoder import processar_lista, slice_list
from collections import namedtuple
from os import sched_getaffinity
from threading import Thread
from timeit import default_timer


def open_file(filename, limite=0):
    """Abre o arquivo e particiona a lista para processamento paralelo."""
    with open(filename, 'r') as f:
        if limite:
            tmp = f.read().splitlines()[:limite]
        else:
            tmp = f.read().splitlines()
        f.close()

    user = namedtuple('User', ['login', 'pwd', 'hash'])
    base = map(user._make, (i.split('|')[1:4] for i in tmp))

    if not limite:
        limite = len(tmp)

    return (base, limite)


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
    while [item for item in threads if item.is_alive()]:
        # pass
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
    for i in range(30):
        print('Rodada: {}'.format(i + 1))

        base, tamanho_file = open_file('base.txt')
        file = slice_list(base, (tamanho_file//len(sched_getaffinity(0))))

        start = default_timer()
        file_proc = processar_arquivo(file=file, tamanho=tamanho_file)
        execucao = default_timer() - start

    times.append(execucao)

    with open('base-output.txt', 'w') as f:
        f.writelines(file_proc)
        f.close()

    print("Tempo de execução: %.10f s" % (sum(times)/len(times)))
