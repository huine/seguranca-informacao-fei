import argparse
import sys
import modulos.conversor as conv

parser = argparse.ArgumentParser(description="Conversor de base.")

parser.add_argument(
    '-c', '--converter', action="store_true",
    help="Converte o arquivo 'output.txt'.")

parser.add_argument(
    '-v', '--validar', action="store_true",
    help="Valida o conteúdo do arquivo 'base-output.txt'. " +
    "(O arquivo deve ter sido gerado com a flag -p)")

parser.add_argument(
    '-p', '--plain', action="store_true", default=False,
    help="Converte o arquivo 'output.txt', mantendo a senha em plain text " +
    "para validação.")

parser.add_argument(
    '-l', '--limite', type=int, default=0,
    help="Limita a quantidade de linhas a serem lidas do" +
    " arquivo. Afeta tanto a conversão quanto a validação.")

parser.add_argument(
    '-r', '--repeticoes', type=int, default=1,
    help="Número de vezes que a conversão/validação devem rodar.")

parser.add_argument(
    '-u', '--user', type=str, default='',
    help="Usuário a ter a senha validada.")

parser.add_argument(
    '-pwd', '--password', type=str, default='',
    help="Senha do usuário à validar.")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if __name__ == '__main__':
    if args.converter:
        conv.converter(args.limite, args.plain, args.repeticoes)
    elif args.validar:
        conv.testar(args.limite, args.repeticoes)
    elif args.user and args.password:
        check = conv.validar_user(args.user, args.password)
        if check ==  1:
            print("Login e senha válido")
        elif check == 0:
            print("Senha invalida")
        else:
            print("Login não encontrado")
    else:
        parser.print_help()
