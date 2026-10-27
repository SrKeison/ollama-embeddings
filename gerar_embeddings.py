"""
Geração de embeddings com o Ollama local.

O script:
  1. Conecta ao servidor do Ollama rodando na máquina (http://localhost:11434).
  2. Confere se o modelo de embeddings está disponível.
  3. Envia um texto simples e recebe o vetor de embeddings.
  4. Exibe um sumário do vetor (dimensão, primeiros valores e estatísticas).

Uso:
  python gerar_embeddings.py
  python gerar_embeddings.py --texto "Outra frase qualquer"
  python gerar_embeddings.py --modelo mxbai-embed-large --completo
"""

import argparse
import math
import os
import sys

import ollama

# Configurações padrão
HOST_PADRAO = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODELO_PADRAO = "nomic-embed-text"
TEXTO_PADRAO = "O Ollama permite executar modelos de linguagem localmente."
QTD_VALORES_INICIAIS = 10


def conectar(host: str) -> ollama.Client:
    """Cria o cliente e confirma que o servidor do Ollama está respondendo."""
    cliente = ollama.Client(host=host)
    try:
        cliente.list()
    except Exception as erro:
        sys.exit(
            f"[ERRO] Não foi possível conectar ao Ollama em {host}.\n"
            f"       Verifique se o serviço está ativo com: ollama serve\n"
            f"       Detalhe: {erro}"
        )
    print(f"[OK] Conectado ao Ollama em {host}")
    return cliente


def verificar_modelo(cliente: ollama.Client, modelo: str) -> None:
    """Confere se o modelo já foi baixado; se não, orienta o usuário."""
    instalados = [m.model for m in cliente.list().models]
    # Os nomes vêm com tag (ex.: "nomic-embed-text:latest")
    disponivel = any(nome.split(":")[0] == modelo.split(":")[0] for nome in instalados)
    if not disponivel:
        sys.exit(
            f"[ERRO] O modelo '{modelo}' não está instalado.\n"
            f"       Baixe com: ollama pull {modelo}"
        )
    print(f"[OK] Modelo '{modelo}' disponível")


def gerar_embedding(cliente: ollama.Client, modelo: str, texto: str) -> list[float]:
    """Envia o texto ao Ollama e devolve o vetor de embeddings."""
    resposta = cliente.embed(model=modelo, input=texto)
    return list(resposta.embeddings[0])


def exibir_resumo(vetor: list[float], texto: str, modelo: str, completo: bool) -> None:
    """Mostra informações sobre o vetor gerado."""
    norma = math.sqrt(sum(v * v for v in vetor))
    media = sum(vetor) / len(vetor)

    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)
    print(f"Texto de entrada : {texto!r}")
    print(f"Modelo           : {modelo}")
    print(f"Dimensão do vetor: {len(vetor)}")
    print(f"Mínimo / Máximo  : {min(vetor):.6f} / {max(vetor):.6f}")
    print(f"Média            : {media:.6f}")
    print(f"Norma (L2)       : {norma:.6f}")

    print(f"\nPrimeiros {QTD_VALORES_INICIAIS} valores:")
    for i, valor in enumerate(vetor[:QTD_VALORES_INICIAIS]):
        print(f"  [{i}] {valor: .6f}")

    if completo:
        print("\nVetor completo:")
        print(vetor)
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera embeddings de um texto com o Ollama local.")
    parser.add_argument("--texto", default=TEXTO_PADRAO, help="Texto a ser transformado em embedding.")
    parser.add_argument("--modelo", default=MODELO_PADRAO, help="Modelo de embeddings do Ollama.")
    parser.add_argument("--host", default=HOST_PADRAO, help="Endereço do servidor Ollama.")
    parser.add_argument("--completo", action="store_true", help="Exibe o vetor inteiro.")
    args = parser.parse_args()

    cliente = conectar(args.host)
    verificar_modelo(cliente, args.modelo)

    print(f"[..] Gerando embedding para: {args.texto!r}")
    vetor = gerar_embedding(cliente, args.modelo, args.texto)

    exibir_resumo(vetor, args.texto, args.modelo, args.completo)


if __name__ == "__main__":
    main()
