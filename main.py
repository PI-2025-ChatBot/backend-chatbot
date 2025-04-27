from supabase import create_client, Client
# Substitua pela URL do seu projeto
SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"  # Substitua pela chave de API pública/anon
TABLE_NAME = "Pedidos"  # Nome da tabela no Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

menu_pratos = {
    "1": "R$ 26,99 - Salada com file de frango",
    "2": "R$ 26,99 - Salada com atum",
    "3": "R$ 31,99 - Salada com kibe vegano ou quiche",
    "4": "R$ 27,99 - Salada ceaser",
    "5": "R$ 26,99 - Salada com omelete"
}

menu_bebidas = {
    "1": "R$ 5,99 - Cola-Cola",
    "2": "R$ 5,99 - Cola-Cola Zero",
    "3": "R$ 7,99 - Suco de laranja",
    "4": "R$ 7,99 - Suco de uva",
    "5": "R$ 6,99 - Água com gás",
    "6": "R$ 4,99 - Água sem gás"
}
cancelado = False
estado = "inicio"
pedido = {}
total = 0

while True:
    if estado == "inicio":
        print("bot: Olá, aqui é o bot de atendimento do restaurante Comida Boa.")
        print("bot: Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n")
        estado = "menu"

    elif estado == "menu":
        print("bot: Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n")
        msg = input("usuario: \n").strip()
        if msg == "1":
            print("\nbot: Escolha o prato que deseja:")
            print("0 - Voltar")
            for key, value in menu_pratos.items():
                print(f"{key} - {value}")
            estado = "escolhendo_prato"
        elif msg == "2":
            print("0 - Voltar")
            print("\nbot: Escolha a bebida que deseja:")
            for key, value in menu_bebidas.items():
                print(f"{key} - {value}")
            estado = "escolhendo_bebida"
        else:
            print("\nbot: Opção inválida. Digite 1 ou 2.")

    elif estado == "escolhendo_prato":
        msg = input("usuario: \n").strip()
        if msg in menu_pratos:
            prato_escolhido = menu_pratos[msg]
            total += float(prato_escolhido.split("R$ ")
                           [1].split(" - ")[0].replace(",", "."))
            print(f"\nbot: Você escolheu: {prato_escolhido}")
            print("bot: Confirmar este prato?\n1 - Sim\n2 - Não, quero escolher outro\n0 - Voltar ao menu principal")
            estado = "confirmar_prato"
        elif msg == "0":
            estado = "inicio"
        else:
            print("\nbot: Escolha inválida. Tente novamente.")

    elif estado == "confirmar_prato":
        msg = input("usuario: \n").strip()
        if msg == "1":
            pedido["prato"] = prato_escolhido
            print(f"\nbot: Prato confirmado: {pedido['prato']}")
            print('\nbot: deseja escolher sua bebida?\n0 - voltar\n1 - sim\n2 - não')
            estado = "pergunta_bebida"
        elif msg == "2":
            print('\nbot: Escolha o prato que deseja:')
            print('0 - voltar')
            for key, value in menu_pratos.items():
                print(f'{key} - {value}')
            estado = "escolhendo_prato"
        elif msg == "0":
            estado = "inicio"
        else:
            print('\nbot : Opção inválida. Digite 1, 2 ou 0.')

    elif estado == "pergunta_bebida":
        msg = input("usuario: \n").strip()
        if msg == "1":
            print("\nbot: Escolha a bebida que deseja:")
            for key, value in menu_bebidas.items():
                print(f"{key} - {value}")
            estado = "escolhendo_bebida"
        elif msg == "2":
            pedido["bebida"] = "nenhuma"
            estado = "resumo"
        elif msg == "0":
            estado = "inicio"
        else:
            print("\nbot: Opção inválida. Digite 1 ou 2.")

    elif estado == "escolhendo_bebida":
        msg = input("usuario: \n").strip()
        if msg in menu_bebidas:
            bebida_escolhida = menu_bebidas[msg]
            total += float(bebida_escolhida.split("R$ ")
                           [1].split(" - ")[0].replace(",", "."))
            print(f'\nbot: Você escolheu: {bebida_escolhida}')
            print('bot: Confirmar esta bebida?\n1 - Sim\n2 - Não, quero escolher outra\n0 - Voltar ao menu principal')
            estado = "confirmar_bebida"
        else:
            print("\nbot: Vi que você não escolheu nenhuma das opções acima.\nEscolha uma das opções para eu te ajudar!")

    elif estado == "confirmar_bebida":
        msg = input("usuario: \n").strip()
        if msg == "1":
            pedido["bebida"] = bebida_escolhida
            print(f'\nbot: Bebida confirmada: {pedido["bebida"]}')
            estado = "resumo"
        elif msg == "2":
            print('\nbot: Escolha a bebida que deseja:')
            for key, value in menu_bebidas.items():
                print(f'{key} - {value}')
            estado = "escolhendo_bebida"
        elif msg == "0":
            estado = "inicio"
        else:
            print('\nbot: Opção inválida. Digite 1, 2 ou 0.')

    elif estado == "resumo":
        print("\nbot: resumo do pedido:")
        print(f"prato: {pedido.get('prato', 'nenhum')}")
        print(f"bebida: {pedido.get('bebida', 'nenhuma')}")
        print(f"Total: R$ {total:.2f}")
        print("\nbot: deseja alterar ou confirmar o pedido?\n0 - cancelar pedido\n1 - alterar\n2 - confirmar pedido")
        estado = "confirmacao"

    elif estado == "confirmacao":
        msg = input("usuario: \n").strip()
        if msg == "1":
            estado = "menu"
        elif msg == "2":
            # Variável que será enviada para o banco de dados
            prato = pedido.get('prato', 'nenhum')
            bebida = pedido.get('bebida', 'nenhuma')

            # Insere os dados na tabela
            if cancelado == False:
                try:
                    response = supabase.table(TABLE_NAME).insert({
                        "prato": prato,
                        "bebida": bebida,
                        "total": total
                    }).execute()
                    print("Pedido armazenado com sucesso!")
                    # print("Resposta do Supabase:", response)
                except Exception as e:
                    print("Erro ao inserir dados no Supabase:", e)
            numero_pedido = response.data[0]['id']
            print("\nbot: pedido confirmado")
            print(f"\nbot: número do pedido: {numero_pedido}")
            break
        elif msg == "0":
            print("Até mais!")
            cancelado = True
            break
        else:
            print("\nbot: Opção inválida. Digite 0, 1 ou 2.")
