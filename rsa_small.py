#!/usr/bin/env python3
"""
RSA com N pequeno demais (vulneravel a fatoracao).

Uso:
    1. Preencha N, e, c com os valores do arquivo `values` do desafio.
    2. Rode o script. Ele tenta fatorar sozinho (Fermat, depois sympy).
    3. Se o N for grande demais para fatorar localmente, ele avisa:
       cole o N em factordb.com, copie p e q, e preencha as variaveis
       p e q abaixo antes de rodar de novo.
"""
from math import isqrt

# ── Preencha com os valores do arquivo `values` ──
N = 0   # TODO: cole o N
e = 0   # TODO: cole o e
c = 0   # TODO: cole o c

# Se ja tiver p e q (por exemplo, do factordb.com), preencha aqui
# e o script pula direto para a decifragem.
p = 0   # TODO (opcional)
q = 0   # TODO (opcional)


def fatorar_fermat(n, tentativas=1_000_000):
    """Funciona bem quando p e q sao proximos um do outro."""
    a = isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(tentativas):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1
    return None, None


def fatorar_sympy(n):
    from sympy import factorint
    fatores = factorint(n)
    primos = list(fatores.keys())
    if len(primos) != 2:
        raise SystemExit(f"Esperava 2 primos, veio: {fatores}")
    return primos[0], primos[1]


def main():
    global p, q

    if N == 0 or e == 0 or c == 0:
        raise SystemExit("Preencha N, e e c antes de rodar.")

    print("Bits do N:", N.bit_length())

    if p == 0 or q == 0:
        print("Tentando fatorar por Fermat (rapido se p e q forem proximos)...")
        p, q = fatorar_fermat(N)

        if p is None:
            if N.bit_length() > 110:
                raise SystemExit(
                    "N grande demais para fatorar localmente.\n"
                    "Cole o N no factordb.com, copie p e q, e preencha "
                    "as variaveis p e q no topo do script."
                )
            print("Fermat nao encontrou, tentando sympy (pode demorar)...")
            p, q = fatorar_sympy(N)

    assert p * q == N, "p * q != N, confira os valores"
    print("p =", p)
    print("q =", q)

    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, N)

    mensagem = m.to_bytes((m.bit_length() + 7) // 8, "big")
    try:
        print("Mensagem:", mensagem.decode())
    except UnicodeDecodeError:
        print("Bytes brutos:", mensagem)


if __name__ == "__main__":
    main()