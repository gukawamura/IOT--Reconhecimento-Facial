import cv2
import face_recognition
import os
import numpy as np

# --- PARÂMETROS RELEVANTES ---

# Parâmetro 1: Tolerância da Comparação
# Define o quão estrita a correspondência de rostos deve ser.
# VALOR PADRÃO: 0.6. Valores comuns estão entre 0.50 e 0.65.
TOLERANCIA = 0.6

# Parâmetro 2: Modelo de Detecção de Rosto
# 'hog' é mais rápido e funciona bem na maioria das CPUs. cnn
MODELO_DETECCAO = 'hog'

# Parâmetro 3: Ampliação da Localização do Rosto (Upsampling)
# Quantas vezes fazer o upsample da imagem antes de procurar por rostos.
UPSAMPLE_TIMES = 1

print("Inicializando o sistema...")
print(f"Usando modelo de detecção: {MODELO_DETECCAO}")
print(f"Tolerância de comparação: {TOLERANCIA}")

def carregar_imagens_conhecidas(caminho_pasta):
    """
    Carrega todas as imagens de uma pasta, codifica os rostos e armazena os nomes.
    """
    codificacoes_conhecidas = []
    nomes_conhecidos = []
    print(f"Carregando rostos conhecidos da pasta: {caminho_pasta}")

    if not os.path.exists(caminho_pasta):
        print(f"[ERRO] A pasta '{caminho_pasta}' não foi encontrada. Por favor, crie-a.")
        return [], []

    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        # Ignora subdiretórios e arquivos que não são imagens
        if os.path.isfile(caminho_completo) and nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Extrai o nome da pessoa a partir do nome do arquivo
            nome_pessoa = os.path.splitext(nome_arquivo)[0].replace('_', ' ').title()
            
            print(f"Processando {nome_pessoa}...")
            
            # Carrega a imagem e a converte para RGB (face_recognition usa RGB)
            imagem = face_recognition.load_image_file(caminho_completo)
            
            # Obtém a codificação do rosto na imagem
            # Assumimos que cada imagem contém apenas um rosto
            codificacoes = face_recognition.face_encodings(imagem)
            
            if len(codificacoes) > 0:
                codificacoes_conhecidas.append(codificacoes[0])
                nomes_conhecidos.append(nome_pessoa)
            else:
                print(f"  [AVISO] Nenhum rosto encontrado em {nome_arquivo}. Ignorando.")
                
    print(f"{len(nomes_conhecidos)} rostos conhecidos carregados com sucesso.")
    return codificacoes_conhecidas, nomes_conhecidos

# Carrega os rostos que o sistema deve reconhecer
codificacoes_conhecidas, nomes_conhecidos = carregar_imagens_conhecidas("rostos_conhecidos")

# Inicializa a webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERRO] Não foi possível abrir a câmera. Verifique se ela está conectada.")
    exit()

while True:
    # Captura um único quadro de vídeo
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar quadro. Encerrando...")
        break

    # Redimensiona o quadro para processamento mais rápido (opcional)
    # frame_pequeno = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Converte a imagem de BGR (padrão do OpenCV) para RGB (padrão do face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Encontra todos os rostos e suas codificações no quadro atual
    localizacoes_rosto = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=UPSAMPLE_TIMES, model=MODELO_DETECCAO)
    codificacoes_rosto = face_recognition.face_encodings(rgb_frame, localizacoes_rosto)

    # Itera sobre cada rosto encontrado no quadro
    for (top, right, bottom, left), codificacao_rosto in zip(localizacoes_rosto, codificacoes_rosto):
        # Compara o rosto encontrado com todos os rostos conhecidos
        correspondencias = face_recognition.compare_faces(codificacoes_conhecidas, codificacao_rosto, tolerance=TOLERANCIA)
        nome = "Desconhecido"

        # Calcula a "distância" facial para encontrar a melhor correspondência
        distancias_faciais = face_recognition.face_distance(codificacoes_conhecidas, codificacao_rosto)
        
        # Se houver alguma correspondência, encontra o índice da melhor
        if True in correspondencias:
            melhor_indice = np.argmin(distancias_faciais)
            if correspondencias[melhor_indice]:
                nome = nomes_conhecidos[melhor_indice]

        # --- Exibição em tela ---
        
        # Desenha um retângulo ao redor do rosto
        # A cor será verde para conhecidos e vermelha para desconhecidos
        cor = (0, 255, 0) if nome != "Desconhecido" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), cor, 2)

        # Desenha um rótulo com o nome abaixo do rosto
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), cor, cv2.FILLED)
        fonte = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, nome, (left + 6, bottom - 6), fonte, 0.8, (255, 255, 255), 1)

    # Mostra o resultado final na tela
    cv2.imshow('Reconhecimento Facial (Pressione "q" para sair)', frame)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()
print("Sistema encerrado.")