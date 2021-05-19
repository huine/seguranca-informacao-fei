# seguranca-informacao-fei
Script para conversão das senhas gravadas no arquivo ``base.txt``.
As senhas são criptografadas usando o algoritmo [Scrypt].

O *paper* original pode ser encontrado aqui: [scrypt_paper]

A página oficial do algoritmo pode ser encontrada aqui: [RFC7914]

## Requisitos

 - Python 3.8
 - Cython

## Instalação
Instalar as dependências
```Bash
pip install -r requirements
```
Compilar os módulos com o ``Cython``
```Bash
cd modulos
python setup.py build_ext --inplace
```

## Como usar
Basta executar o arquivo ``orquestrador.py``.

### Conversão
Para realizar a conversão do arquivo de base, basta executar com o parâmetro ``-c``.
```Bash
python orquestrador.py -c [-l Linhas, -p PlainText, -r Repetições]
```
Outros parâmetros disponíveis na conversão são:
```
[-l , --limite] INT -> Um número inteiro positivo para indicar a quantidade de linhas a processar do arquivo.
[-p , --plain] -> Flag que determina se a conversão deve manter a senha em plaintext no arquivo de saída. (Para a validação da saída esse parâmetro é obrigatório).
[-r, --repeticoes] INT -> Determina a quantidade de vezes que a operação deve ser executada. (Para validar o tempo de execução).
```
Essa função gera o arquivo ``base-output.txt`` com a senha criptografada usando o algoritmo [Scrypt].

### Validação
Para realizar a conversão do arquivo de base, basta executar com o parâmetro ``-v``.
O arquivo ``base-output.txt`` deve ter sido gerado com a flag ``-p`` no processo de conversão para que a validação funcione corretamente.
```Bash
python orquestrador.py -v [-l Linhas, -r Repetições]
```
Outros parâmetros disponíveis na conversão são:
```
[-l , --limite] INT -> Um número inteiro positivo para indicar a quantidade de linhas a processar do arquivo.
[-r, --repeticoes] INT -> Determina a quantidade de vezes que a operação deve ser executada. (Para validar o tempo de execução).
```
Caso alguma senha falhe na validação, acontecerá uma exceção no processo e a validação será interrompida com um erro.

[rfc7914]: https://datatracker.ietf.org/doc/html/rfc7914 "RFC7914"
[scrypt_paper]: https://www.tarsnap.com/scrypt/scrypt.pdf "Scrypt Paper"
[scrypt]: https://www.tarsnap.com/scrypt.html "Scrypt"
