# RSA com N pequeno — ataque por fatoração

Este script quebra uma chave RSA cujo módulo `N` é pequeno demais (pouco
mais de 100 bits, em vez dos 2048+ bits usados na prática), explorando o
fato de que fatorar `N = p × q` deixa de ser inviável nesse tamanho.

---

## 1. A ideia por trás do ataque

Toda a segurança do RSA depende de ninguém conseguir recuperar `p` e `q`
só a partir de `N`. Com `N` de milhares de bits, a fatoração levaria mais
tempo que a idade do universo com os métodos conhecidos. Com um `N` de
~100 bits, computadores comuns (ou bancos de dados como o factordb.com)
fatoram em segundos.

Uma vez com `p` e `q` em mãos:

```
φ(N) = (p - 1) × (q - 1)
d = inverso modular de e, mod φ(N)
mensagem = c^d mod N
```

---

## 2. Estrutura do código

### `fatorar_fermat(n, tentativas=1_000_000)`

Implementa o **método de fatoração de Fermat**, que funciona muito bem
quando os dois fatores primos são **próximos um do outro** (uma fraqueza
comum em chaves RSA mal geradas).

A ideia: se `N = p × q` e `p`, `q` são próximos, então existe um `a` tal
que `a² - N` é um quadrado perfeito (`b²`), e `p = a - b`, `q = a + b`. O
código começa com `a = raiz quadrada de N (arredondada para cima)` e vai
incrementando até achar esse `b`.

- É extremamente rápido quando aplicável (frequentemente menos de um
  segundo), mas **não funciona** se `p` e `q` forem bem diferentes em
  tamanho — nesse caso, retorna `(None, None)`.

### `fatorar_sympy(n)`

Usa a função `factorint` da biblioteca `sympy`, uma fatoração de propósito
geral (usa Pollard's rho, entre outros algoritmos). Mais lenta que Fermat,
mas funciona mesmo quando os primos não são próximos — desde que `N` não
seja grande demais (na prática, até uns 100-110 bits em tempo razoável).

### `main()`

Orquestra o processo:

1. Confere se `N`, `e`, `c` foram preenchidos.
2. Se `p` e `q` não foram fornecidos manualmente (por exemplo, copiados do
   factordb.com), tenta fatorar sozinho: primeiro Fermat (rápido, mas só
   funciona em certos casos), depois sympy (mais lento, mas mais geral).
3. Se `N` for grande demais (mais de 110 bits) e Fermat falhar, o script
   para e orienta o uso do **factordb.com** em vez de tentar fatorar
   localmente (que travaria por tempo indefinido).
4. Com `p` e `q` confirmados (`assert p * q == N`), calcula `φ(N)`, a
   chave privada `d`, e decifra a mensagem.
5. Converte o número decifrado em bytes e tenta decodificar como texto.

---

## 3. Como usar

1. Abra o arquivo `values` do desafio e identifique `N`, `e`, `c`.
2. Preencha essas três variáveis no topo do script.
3. Rode: `python3 rsa_small_n.py`.
4. **Se parar pedindo para usar o factordb**: acesse factordb.com, cole o
   `N`, copie os dois fatores (`p` e `q`) do resultado, preencha-os no
   topo do script, e rode de novo — dessa vez ele pula direto para a
   decifragem.

---

## 4. Limitações e cuidados

- **Fermat só serve para primos próximos.** Chaves RSA geradas
  corretamente evitam isso de propósito; o fato de funcionar aqui já é
  parte da "pista" de que a chave foi gerada de forma fraca.
- **`sympy.factorint` não escala**: para números muito maiores que ~110
  bits, essa fatoração pode travar por horas ou dias. O script detecta
  esse caso e avisa, em vez de deixar rodando indefinidamente.
- **Conversão número → texto**: o script assume que o resultado decifrado
  é texto UTF-8 simples. Se a mensagem usar outro formato (base64,
  hexadecimal dentro do texto, etc.), pode ser necessário um passo extra
  de decodificação depois.
