from bcrypt import hashpw, checkpw, gensalt
from hashlib import sha256, scrypt
from base64 import b64encode, b64decode
from secrets import token_bytes, compare_digest
from itertools import islice


def encrypt(string):
    """Criptografa uma string com o algoritmo blowfish."""
    if not string or not isinstance(string, (str, bytes)):
        print(type(string))
        raise Exception('Tipo inválido no parâmetro string.')

    # Verifica se é uma string, se for tem que converter para bytes.
    if isinstance(string, str):
        string = string.encode()

    # O algoritmo blowfish no python aceita no máximo 72 caracteres
    # então geramos uma hash com o sha256, o que resulta em uma hash de 72
    # caracteres e encodamos a hash em base64 para evitar problemas com
    # bytes nulos na hash.
    string256_b64 = b64encode(sha256(string).digest())
    return hashpw(string256_b64, gensalt()).decode()


def encrypt_s(string, n=16384, r=8, p=1, salt=None):
    """Criptografa uma string com o algoritmo blowfish."""
    if not string or not isinstance(string, (str, bytes)):
        print(type(string))
        raise Exception('Tipo inválido no parâmetro string.')

    # Verifica se é uma string, se for tem que converter para bytes.
    if isinstance(string, str):
        string = string.encode()

    if not salt:
        salt = token_bytes()

    string256_b64 = b64encode(sha256(string).digest())
    hs = scrypt(string256_b64, salt=salt, n=int(n), r=int(r), p=int(p),
                dklen=64).hex()

    return '{n}${r}${p}${salt}${hash}'.format(
        n=n, r=r, p=p, salt=b64encode(salt).decode(), hash=hs)


def check_s(pwd, hash_pwd):
    """Verifica se a senha(pwd) é o valor criptografado(hash)."""
    if not pwd or not isinstance(pwd, str):
        raise Exception('Tipo inválido no parâmetro pwd.')

    if not hash_pwd or not isinstance(hash_pwd, str):
        raise Exception('Tipo inválido no parâmetro hash_pwd.')

    n, r, p, salt_b64, hash_hex = hash_pwd.split('$')

    return compare_digest(
        encrypt_s(pwd, n, r, p, b64decode(salt_b64)), hash_pwd)


def check(pwd, hash_pwd):
    """Verifica se a senha(pwd) é o valor criptografado(hash)."""
    if not pwd or not isinstance(pwd, (str, bytes)):
        raise Exception('Tipo inválido no parâmetro pwd.')

    if not hash_pwd or not isinstance(hash_pwd, (str, bytes)):
        raise Exception('Tipo inválido no parâmetro hash_pwd.')

    if isinstance(hash_pwd, str):
        hash_pwd = hash_pwd.encode()

    if isinstance(pwd, str):
        pwd = pwd.encode()

    string256_b64 = b64encode(sha256(pwd).digest())
    return checkpw(string256_b64, hash_pwd)


def processar_lista(user_list, fila):
    """Processa uma lista de usuarios para conversao."""
    s = '|{login}|{plain}|{pwd}|\n'
    for user in user_list:
        fila.append(
            s.format(login=user.login, pwd=encrypt_s(user.pwd), plain=user.pwd)
        )
    return


def slice_list(base, tamanho):
    """Divide uma lista 'base' em n iterators com tamanho 'tamanho'"""
    return iter(lambda: tuple(islice(base, tamanho)), ())
