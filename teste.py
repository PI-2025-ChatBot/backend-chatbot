from supabase import create_client, Client

SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"
TABLE_NAME = "Pedidos"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

menu_pratos = {
    "1": "R$ 26,99 - Salada com file de frango",
    "2": "R$ 26,99 - Salada com atum",
    "3": "R$ 31,99 - Salada com kibe vegano ou quiche",
    "4": "R$ 27,99 - Salada ceaser",
    "5": "R$ 26,99 - Salada com omelete",
    "6": "R$ 28,99 - Filé de frango grelhado",
    "7": "R$ 28,99 - Linguiça calabresa acebolada",
    "8": "R$ 28,99 - Linguiça toscana grelhada",
    "9": "R$ 28,99 - Nuggets de frango"
}

menu_bebidas = {
    "1": "R$ 5,99 - Coca-Cola",
    "2": "R$ 5,99 - Coca-Cola Zero",
    "3": "R$ 7,99 - Suco de laranja",
    "4": "R$ 7,99 - Suco de uva",
    "5": "R$ 6,99 - Água com gás",
    "6": "R$ 4,99 - Água sem gás"
}

usuario = {
    "estado": "inicio",
    "pedido": {},
    "cancelado": False,
    "total": 0
}
numero = input("Digite seu número de WhatsApp: ")
numero_limpo = numero.strip()


def mostrar_menu(dicionario):
    for key, value in dicionario.items():
        print(f"{key} - {value}")


while True:
    estado = usuario["estado"]
    pedido = usuario["pedido"]
    total = usuario["total"]

    if estado == "inicio":
        print("Olá, aqui é o bot de atendimento do restaurante Comida Boa.")
        print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
        usuario["estado"] = "menu"

    elif estado == "menu":
        msg = input(">> ")
        if msg == "1":
            print("Escolha o prato que deseja:")
            mostrar_menu(menu_pratos)
            print("0 - Voltar ao menu principal")
            usuario["estado"] = "escolhendo_prato"
        elif msg == "2":
            print("Escolha a bebida que deseja:")
            mostrar_menu(menu_bebidas)
            print("0 - Voltar ao menu principal")
            usuario["estado"] = "escolhendo_bebida"
        else:
            print("Opção inválida. Digite 1 ou 2.")

    elif estado == "escolhendo_prato":
        msg = input(">> ")
        if msg in menu_pratos:
            prato_escolhido = menu_pratos[msg]
            if "prato" in pedido:
                total -= float(pedido["prato"].split("R$ ")[1].split(" - ")[0].replace(",", "."))
            pedido["prato"] = prato_escolhido
            total += float(prato_escolhido.split("R$ ")[1].split(" - ")[0].replace(",", "."))
            usuario["total"] = total
            print(f"Você escolheu: {prato_escolhido}")
            print("Confirmar este prato?\n1 - Sim\n2 - Não, quero escolher outro\n0 - Voltar ao menu principal")
            usuario["estado"] = "confirmar_prato"
        elif msg == "0":
            print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
            usuario["estado"] = "menu"
        else:
            print("Escolha inválida. Tente novamente.")

    elif estado == "confirmar_prato":
        msg = input(">> ")
        if msg == "1":
            print(f"Prato confirmado: {pedido['prato']}")
            print("Deseja escolher sua bebida?\n1 - Sim\n2 - Não\n0 - Voltar ao menu principal")
            usuario["estado"] = "pergunta_bebida"
        elif msg == "2":
            print("Escolha o prato que deseja:")
            mostrar_menu(menu_pratos)
            print("0 - Voltar ao menu principal")
            usuario["estado"] = "escolhendo_prato"
        elif msg == "0":
            print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
            usuario["estado"] = "menu"
        else:
            print("Opção inválida. Tente novamente.")

    elif estado == "pergunta_bebida":
        msg = input(">> ")
        if msg == "1":
            print("Escolha a bebida que deseja:")
            mostrar_menu(menu_bebidas)
            print("0 - Voltar ao menu principal")
            usuario["estado"] = "escolhendo_bebida"
        elif msg == "2":
            if "bebida" in pedido and "R$ " in pedido["bebida"]:
                total -= float(pedido["bebida"].split("R$ ")[1].split(" - ")[0].replace(",", "."))
            pedido["bebida"] = "nenhuma"
            usuario["total"] = total
            usuario["estado"] = "confirmacao"
            total_formatado = f"{total:.2f}".replace(".", ",")
            print(f"Resumo do pedido:\nPrato: {pedido.get('prato', 'nenhum')}\nBebida: nenhuma\nTotal: R$ {total_formatado}")
            print("1 - Confirmar\n2 - Alterar\n0 - Cancelar")
        elif msg == "0":
            print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
            usuario["estado"] = "menu"
        else:
            print("Opção inválida. Tente novamente.")

    elif estado == "escolhendo_bebida":
        msg = input(">> ")
        if msg in menu_bebidas:
            bebida_escolhida = menu_bebidas[msg]
            if "bebida" in pedido and "R$ " in pedido["bebida"]:
                total -= float(pedido["bebida"].split("R$ ")[1].split(" - ")[0].replace(",", "."))
            pedido["bebida"] = bebida_escolhida
            total += float(bebida_escolhida.split("R$ ")[1].split(" - ")[0].replace(",", "."))
            usuario["total"] = total
            print(f"Você escolheu: {bebida_escolhida}")
            print("Confirmar esta bebida?\n1 - Sim\n2 - Não, quero escolher outra\n0 - Voltar ao menu principal")
            usuario["estado"] = "confirmar_bebida"
        elif msg == "0":
            print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
            usuario["estado"] = "menu"
        else:
            print("Escolha inválida. Tente novamente.")

    elif estado == "confirmar_bebida":
        msg = input(">> ")
        if msg == "1":
            total_formatado = f"{total:.2f}".replace(".", ",")
            print(f"Bebida confirmada: {pedido['bebida']}")
            print(f"Resumo do pedido:\nPrato: {pedido.get('prato', 'nenhum')}\nBebida: {pedido.get('bebida', 'nenhuma')}\nTotal: R$ {total_formatado}")
            print("1 - Confirmar\n2 - Alterar\n0 - Cancelar")
            usuario["estado"] = "confirmacao"
        elif msg == "2":
            print("Escolha a bebida que deseja:")
            mostrar_menu(menu_bebidas)
            print("0 - Voltar ao menu principal")
            usuario["estado"] = "pergunta_bebida"
        elif msg == "0":
            print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
            usuario["estado"] = "menu"
        else:
            print("Opção inválida. Tente novamente.")

    elif estado == "confirmacao":
        msg = input(">> ")
        if msg == "2":
            print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
            usuario["estado"] = "menu"
        elif msg == "1":
            try:
                result = supabase.table(TABLE_NAME).insert({
                    "prato": pedido.get('prato', 'nenhum'),
                    "bebida": pedido.get('bebida', 'nenhuma'),
                    "total": total,
                    "numero": numero_limpo
                }).execute()
                if result.data:
                    numero_pedido = result.data[0]['id']
                    print(f"Pedido confirmado! ✅\nNúmero do pedido: {numero_pedido}\nObrigado pela preferência! Até a próxima! 👋")
                break
            except Exception as e:
                print("Erro ao registrar o pedido. Tente novamente.")
        elif msg == "0":
            print("Pedido cancelado. Até mais! 👋")
            break
        else:
            print("Opção inválida. Tente novamente.")
