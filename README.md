# Outrora

RPG interativo onde as escolhas do jogador moldam o desenvolvimento da história.

![Tela Inicial](assets/images/tela_inicial_outrora.jpg)

## Tecnologias / Framework

- Python
- Kivy
- KivyMD

## Pré-requisitos

- **Python 3.8 a 3.13** (recomendado no Windows: **3.12** ou **3.13**)
- Dependências instaladas via `requirements.txt`

## Estrutura do projeto

```text
.
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── data/
│   ├── __init__.py
│   └── story.py
└── assets/
    ├── images/
    ├── audio/
    └── video/
```

## Como executar (Windows / Linux / macOS)

### 1) Clonar o repositório

```bash
git clone https://github.com/diegobrnrd/outrora.git
cd outrora
```

### 2) Criar e ativar um ambiente virtual (recomendado)

Criar:

```bash
python -m venv .venv
```

Ativar:

- Windows (PowerShell):
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Windows (cmd):
  ```bat
  .\.venv\Scripts\activate.bat
  ```
- Linux/macOS:
  ```bash
  source .venv/bin/activate
  ```

### 3) Instalar dependências

```bash
pip install -r requirements.txt
```

### 4) Rodar o jogo

```bash
python main.py
```

## Licença

Este projeto está licenciado sob a [Apache License 2.0](LICENSE).
