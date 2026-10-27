# Embeddings com Ollama local

Script em Python que se conecta ao **Ollama** rodando na máquina, envia um texto simples e gera o **vetor de embeddings** correspondente, exibindo a dimensão do vetor, os primeiros valores e algumas estatísticas.

Atividade: Avaliação Online 3 (IFRN).

📹 **Vídeo de demonstração:** [COLE AQUI O LINK DO VÍDEO](#)

## Estrutura

```
.
├── gerar_embeddings.py   # script principal
├── requirements.txt      # dependências Python
└── README.md
```

## Pré-requisitos

- Python 3.9 ou superior
- Ollama instalado (instruções abaixo)
- Cerca de 300 MB livres para o modelo `nomic-embed-text`

## 1. Instalar o Ollama

**Linux**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS e Windows:** baixe o instalador em <https://ollama.com/download> e execute.

Confira a instalação:

```bash
ollama --version
```

## 2. Iniciar o serviço e baixar o modelo

Em um terminal, inicie o servidor (no Windows e no macOS ele costuma já iniciar sozinho com o aplicativo; se aparecer erro de porta em uso, ele já está ativo):

```bash
ollama serve
```

Em **outro terminal**, confirme que o serviço está respondendo:

```bash
curl http://localhost:11434
# Resposta esperada: Ollama is running
```

Baixe o modelo de embeddings (modelo aberto, 768 dimensões):

```bash
ollama pull nomic-embed-text
ollama list
```

## 3. Preparar o ambiente Python

```bash
git clone https://github.com/SrKeison/ollama-embeddings.git
cd ollama-embeddings

python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## 4. Executar o script

Com o texto padrão:

```bash
python gerar_embeddings.py
```

Com um texto próprio:

```bash
python gerar_embeddings.py --texto "Hello world"
```

Opções disponíveis:

| Opção | Descrição | Padrão |
|---|---|---|
| `--texto` | Texto a ser convertido em embedding | frase de exemplo em português |
| `--modelo` | Modelo de embeddings do Ollama | `nomic-embed-text` |
| `--host` | Endereço do servidor Ollama | `http://localhost:11434` (ou variável `OLLAMA_HOST`) |
| `--completo` | Exibe o vetor inteiro, e não só o resumo | desativado |

## Exemplo de saída

```
[OK] Conectado ao Ollama em http://localhost:11434
[OK] Modelo 'nomic-embed-text' disponível
[..] Gerando embedding para: 'O Ollama permite executar modelos de linguagem localmente.'

============================================================
RESULTADO
============================================================
Texto de entrada : 'O Ollama permite executar modelos de linguagem localmente.'
Modelo           : nomic-embed-text
Dimensão do vetor: 768
Mínimo / Máximo  : -0.133633 / 0.133648
Média            : 0.000105
Norma (L2)       : 1.000000

Primeiros 10 valores:
  [0]  0.044694
  [1]  0.058168
  [2] -0.116276
  ...
============================================================
```

A norma igual a 1 indica que o Ollama devolve o vetor já normalizado, o que facilita comparar textos por similaridade de cosseno.

## Como funciona

1. `conectar()` cria um `ollama.Client` e chama `list()` para garantir que o servidor está ativo.
2. `verificar_modelo()` confere se o modelo foi baixado com `ollama pull`.
3. `gerar_embedding()` chama `client.embed(model, input)`, que usa o endpoint `/api/embed` do Ollama.
4. `exibir_resumo()` mostra dimensão, valores iniciais, mínimo, máximo, média e norma do vetor.

## Problemas comuns

| Mensagem | Solução |
|---|---|
| `Não foi possível conectar ao Ollama` | Rode `ollama serve` em outro terminal |
| `O modelo '...' não está instalado` | Rode `ollama pull nomic-embed-text` |
| `ModuleNotFoundError: No module named 'ollama'` | Ative o `.venv` e rode `pip install -r requirements.txt` |
