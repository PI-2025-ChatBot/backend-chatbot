import uuid

menu_pratos = {
    "1": "arroz, feijão e fritas",
    "2": "arroz e frango à parmegiana",
    "3": "frango à milanesa"
}

menu_bebidas = {
    "1": "coca",
    "2": "coca zero",
    "3": "suco de laranja",
    "4": "suco de uva"
}
cancelado = False
estado = "inicio"
pedido = {}

while True:
    if estado == "inicio":
        print("bot: Olá, aqui é o bot de atendimento do restaurante Comida Boa. 🤖")
        print("bot: Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n")
        estado = "menu"

    elif estado == "menu":
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
            pedido["prato"] = menu_pratos[msg]
            print(f"\nbot: o prato escolhido foi: {pedido['prato']}")
            print("\nbot: deseja escolher sua bebida?\n0 - voltar\n1 - sim\n2 - não")
            estado = "pergunta_bebida"
        elif msg == "0":
            estado ="inicio"
        else:
            print("\nbot: Escolha inválida. Tente novamente.")

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
            pedido["bebida"] = menu_bebidas[msg]
            print(f"\nbot: a bebida escolhida foi: {pedido['bebida']}")
            estado = "resumo"
        else:
            print("\nbot: Vi que você não escolheu nenhuma das opções acima.\nEscolha uma das opções para eu te ajudar!")

    elif estado == "resumo":
        print("\nbot: resumo do pedido:")
        print(f"prato: {pedido.get('prato', 'nenhum')}")
        print(f"bebida: {pedido.get('bebida', 'nenhuma')}")
        print("\nbot: deseja alterar ou confirmar o pedido?\n0 - cancelar pedido\n1 - alterar\n2 - confirmar pedido")
        estado = "confirmacao"

    elif estado == "confirmacao":
        msg = input("usuario: \n").strip()
        if msg == "1":
            estado = "menu"
        elif msg == "2":
            numero_pedido = str(uuid.uuid4())
            print("\nbot: pedido confirmado")
            print(f"\nbot: número do pedido: {numero_pedido}")
            break
        elif msg =="0":
            print("Até mais!")
            cancelado = True
            break
        else:
            print("\nbot: Opção inválida. Digite 0, 1 ou 2.")

from supabase import create_client, Client

SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"  # Substitua pela URL do seu projeto
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"  # Substitua pela chave de API pública/anon
TABLE_NAME = "Pedidos"  # Nome da tabela no Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# Variável que será enviada para o banco de dados
prato = pedido.get('prato', 'nenhum')
bebida = pedido.get('bebida', 'nenhuma')

# Insere os dados na tabela
if cancelado == False:
    try:
        response = supabase.table(TABLE_NAME).insert({"prato": prato, "bebida": bebida}).execute()
        print("Dados inseridos com sucesso!")
        print("Resposta do Supabase:", response)
    except Exception as e:
        print("Erro ao inserir dados no Supabase:", e)