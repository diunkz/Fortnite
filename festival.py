import os
import time
import pydirectinput
import keyboard
from threading import Thread, Event
import psutil

def desligar_computador():
    os.system('shutdown /s /t 0')

def fechar_processo(nome_processo):
    for processo in psutil.process_iter(['pid', 'name']):
        if processo.info['name'] == nome_processo:
            pid = processo.info['pid']
            processo = psutil.Process(pid)
            processo.terminate()
            print(f'Processo {nome_processo} encerrado com sucesso.')
            return True
    print(f'Processo do Fortnite não encontrado. Não foi possível fechar.')

    return False

# Função para pressionar uma tecla com uma duração específica
def press_key(key, duration):
    pydirectinput.keyDown(key)
    time.sleep(duration)
    pydirectinput.keyUp(key)

def display_remaining_time(stop_event, t_seconds):
    # Função para exibir o tempo restante no formato "faltam X minutos e X segundos"
    start_time = time.time()
    while time.time() - start_time < t_seconds and not stop_event.is_set():
        remaining_seconds = int(t_seconds - (time.time() - start_time))
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa o terminal
        print("Aperte repetidamente a tecla P para parar o programa.")
        print()
        print(f"\tFaltam {minutes} minutos e {seconds} segundos!")
        print()
        print("\t\t\t\tFeito por Noah Diunkz! ;)")
        print("\t\t\t\tgithub.com/diunkz")
        print()
        time.sleep(1)

def main():
    # Solicita a entrada do tempo em minutos
    t_minutes = int(input("Digite o tempo de execução em minutos: "))
    t_seconds = t_minutes * 60  # converte minutos para segundos

    # Solicita a entrada para a ação após o tempo acabar
    print()
    print("Escolha o que fazer após o tempo acabar:")
    print("1 - Fechar Fortnite após finalizar o tempo")
    print("2 - Desligar o PC após finalizar o tempo")
    print("3 - Nada")
    print()
    opcao = input("Escolha uma opção (1/2/3): ")

    # Espera pela tecla "I" ser pressionada para começar 
    print("")
    print("Abra a Janela do Fortnite (no fortnite festival)\ne pressione a tecla 'I' para começar...\n\nLembrando que você pode parar o programa a\nqualquer momento pressionando P repetidamente.")
    keyboard.wait('i')

    print("Iniciando simulação... Pressione 'P' para parar.")

    # Flag de evento para indicar que a simulação deve parar
    stop_event = Event()

    # Thread para exibir o tempo restante paralelamente
    timer_thread = Thread(target=display_remaining_time, args=(stop_event, t_seconds))
    timer_thread.start()

    # Loop para simular os pressionamentos até a tecla "P" ser pressionada ou o tempo acabar
    start_time = time.time()
    while True:
        press_key(' ', 1)
        keys_to_press = ['w', 'd', 's', 'a', 'd', 'w', 'a', 's']
        for key in keys_to_press:
            press_key(key, 0.5)
            if keyboard.is_pressed('p'):  # Verifica se a tecla "P" foi pressionada
                stop_event.set()  # Define o evento para parar a thread do temporizador
                print("Simulação interrompida. Pressione enter para sair.")
                return

        time_elapsed = time.time() - start_time
        if time_elapsed >= t_seconds:
            stop_event.set()  # Define o evento para parar a thread do temporizador
            print("Tempo de execução atingido. Simulação encerrada.")
            break

    timer_thread.join()  # Aguarda a thread do temporizador terminar

    # Realiza a ação escolhida após o tempo acabasar
    if opcao == '1':
        fechar_processo("FortniteClient-Win64-Shipping.exe")
    elif opcao == '2':
        desligar_computador()

if __name__ == "__main__":
    main()
    input('Pressione enter para sair.')
