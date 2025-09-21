# Projeto de Reconhecimento Facial em Tempo Real

Gustavo Kawamura RM: 99679
Manoella Hererrias RM: 98906
Felipe Capriotti RM: 98460
Victor Hugo RM: 550996

Este projeto utiliza Python, OpenCV e a biblioteca `face_recognition` (baseada no dlib) para realizar a detecção e o reconhecimento de rostos em tempo real através de uma webcam. O sistema é capaz de identificar pessoas previamente cadastradas e rotular indivíduos desconhecidos.

## Funcionalidades

-   **Detecção em Tempo Real**: Localiza rostos no feed de vídeo da webcam.
-   **Identificação de Pessoas**: Compara os rostos detectados com um banco de imagens de rostos conhecidos.
-   **Cadastro Simplificado**: Para cadastrar uma nova pessoa, basta adicionar um arquivo de imagem na pasta `rostos_conhecidos`.
-   **Feedback Visual**: Exibe um retângulo ao redor dos rostos detectados (verde para conhecidos, vermelho para desconhecidos) e um rótulo com o nome.
-   **Parâmetros Configuráveis**: Permite ajustar facilmente a tolerância do reconhecimento e o modelo de detecção de rostos.

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado em seu sistema:

1.  **Python 3.8 ou superior**:
    -   Faça o download em [python.org](https://www.python.org/).
    -   **Importante (para Windows):** Durante a instalação, marque a caixa "Add Python to PATH".

2.  **Compilador C++ (Crítico para Windows)**:
    -   A biblioteca `dlib`, uma dependência chave, precisa ser compilada durante a instalação. Para isso, é necessário o "Build Tools para Visual Studio".
    -   Acesse a [página de downloads do Visual Studio](https://visualstudio.microsoft.com/pt-br/downloads/).
    -   Role até **"Ferramentas para Visual Studio"** e baixe o **"Build Tools para Visual Studio"**.
    -   Execute o instalador e, na aba "Cargas de Trabalho", selecione **"Desenvolvimento para desktop com C++"**.
    -   Após a instalação, **reinicie o seu computador**.

## Instalação e Configuração

Siga estes passos para configurar o ambiente do projeto.

**1. Clone ou Baixe este Repositório**

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```
*(Se não estiver usando Git, apenas crie a pasta do projeto manualmente)*

**2. Crie a Estrutura de Pastas**

Certifique-se de que a estrutura do seu projeto está assim:

```
Projeto_Reconhecimento_Facial/
|
├── codigo_reconhecimento.py
|
└── rostos_conhecidos/
    ├── pessoa_1.jpg
    └── pessoa_2.png
```

**3. Adicione as Imagens de Referência**

-   Coloque uma imagem de cada pessoa que você deseja reconhecer dentro da pasta `rostos_conhecidos`.
-   **Importante:** O nome do arquivo será usado como o nome da pessoa. Por exemplo, um arquivo chamado `ana_silva.jpg` será identificado como "Ana Silva".

**4. Crie e Ative o Ambiente Virtual (`venv`)**

É uma boa prática isolar as dependências do projeto.

```bash
# Crie a venv
python -m venv venv_facial

# Ative a venv
# No Windows:
venv_facial\Scripts\activate
# No macOS/Linux:
source venv_facial/bin/activate
```

**5. Instale as Dependências**

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias usando o arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```
*(A instalação do `dlib` pode demorar vários minutos. Isso é normal.)*

## Como Usar

1.  Certifique-se de que seu ambiente virtual (`venv_facial`) está ativo.
2.  Execute o script principal a partir do terminal:
    ```bash
    python codigo_reconhecimento.py
    ```
3.  Uma janela com o feed da sua webcam será aberta. Posicione os rostos em frente à câmera.
4.  Para fechar o programa, clique na janela da webcam e pressione a tecla **'q'**.

## Parâmetros Configuráveis

Dentro do arquivo `codigo_reconhecimento.py`, você pode ajustar os seguintes parâmetros para otimizar o desempenho:

-   `TOLERANCIA`: Um valor entre `0.0` e `1.0` que define o quão estrito é o reconhecimento.
    -   **Valores menores (ex: `0.5`)** tornam o sistema mais rigoroso (menos falsos positivos).
    -   **Valores maiores (ex: `0.7`)** tornam o sistema mais flexível.
-   `MODELO_DETECCAO`: O algoritmo para encontrar rostos.
    -   **`'hog'` (padrão)**: Rápido e ideal para CPU.
