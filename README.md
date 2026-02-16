# 🧠 Friday Local (macOS Edition)

> Um assistente virtual inteligente, privado e offline, projetado para rodar nativamente em Apple Silicon (M1/M2/M3/m4).

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange)
![Whisper](https://img.shields.io/badge/ASR-Whisper-green)
![Status](https://img.shields.io/badge/Status-Functional-brightgreen)

## 📖 Sobre o Projeto

O **Friday Local** é uma implementação moderna de assistente de voz que prioriza privacidade e performance. Diferente de soluções como Alexa ou Google Assistant, todo o processamento — desde o reconhecimento de fala até a geração de resposta — acontece **localmente** no seu Mac, aproveitando a Neural Engine dos chips Apple Silicon.

### ✨ Funcionalidades Principais
* **🗣️ Interação Híbrida:** Suporta comandos por voz (Hands-free) ou texto.
* **🔒 Privacidade Total:** Nenhum áudio ou dado é enviado para a nuvem.
* **🧠 IA Generativa Local:** Utiliza o **Llama 3** via Ollama para processamento de linguagem natural.
* **👂 Transcrição de Alta Fidelidade:** Integração com **OpenAI Whisper** para entender fala mesmo em ambientes ruidosos.
* **⚡ Controle do SO:** Capaz de abrir aplicativos e executar comandos do sistema nativamente.
* **🗣️ Text-to-Speech:** Responde vocalmente utilizando o motor de síntese nativo do macOS.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**: Linguagem base.
* **Ollama**: Orquestrador de LLMs locais (rodando Llama 3).
* **OpenAI Whisper**: Modelo SOTA (State of the Art) para Automatic Speech Recognition (ASR).
* **SoundDevice & SciPy**: Captura e processamento de áudio em tempo real.
* **Subprocess**: Automação e execução de comandos shell.

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
* macOS (Recomendado Apple Silicon M1/M2/M3/M4 para melhor performance).
* Python 3 instalado.
* [Ollama](https://ollama.com) instalado e rodando.
* **FFmpeg** instalado (essencial para o Whisper).

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/JoaoPaulo121212/ia-local.git](https://github.com/JoaoPaulo121212/ia-local.git)
    cd jarvis-local
    ```

2.  **Prepare o ambiente:**
    ```bash
    # Instale o FFmpeg (via Homebrew)
    brew install ffmpeg

    # Baixe o modelo Llama 3 no Ollama
    ollama run llama3
    ```

3.  **Configure o Python:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install ollama openai-whisper sounddevice scipy numpy
    ```

4.  **Execute:**
    ```bash
    python3 main.py
    ```

---

## 🎮 Exemplos de Uso

| Comando de Voz | Ação do Jarvis |
| :--- | :--- |
| *"Open Spotify"* | Abre o aplicativo Spotify nativamente. |
| *"Start Visual Studio Code"* | Inicia o seu editor de código. |
| *"What is the capital of France?"* | Responde: *"Paris is the capital of France"* (falado e escrito). |
| *[Enter sem falar]* | Ativa o modo de escuta para comandos rápidos. |

---

## 🧠 Como Funciona (Pipeline)

1.  **Input:** O usuário fala no microfone ou digita um comando.
2.  **Processamento de Áudio:** Se for voz, o `sounddevice` grava e normaliza o áudio.
3.  **Transcrição:** O `Whisper` converte o áudio (.wav) em texto (String).
4.  **Intenção (Intent Recognition):** O script verifica se é um comando de sistema (ex: "Open X").
    * *Se for app:* A IA extrai o nome do app e o `subprocess` executa `open -a "App Name"`.
5.  **Raciocínio:** Se não for comando, o texto vai para o `Ollama (Llama 3)` que gera uma resposta curta.
6.  **Output:** A resposta é lida em voz alta pelo `say` do macOS.

---

## 📄 Licença

Este projeto está sob a licença MIT - sinta-se livre para usar e modificar.
