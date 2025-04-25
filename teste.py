from supabase import create_client, Client

SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"
TABLE_NAME = "Pedidos"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

def main():
    estado = "inicio"
    pedido = {}
    numero = input("Digite o número de telefone (formato +5511999999999): ").strip()
    cancelado = False

    while True:
        if estado == "inicio":
            print("\n🤖 Olá, aqui é o bot de atendimento do restaurante Comida Boa.")
            print("Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
            estado = "menu"

        elif estado == "menu":
            msg = input("Você: ").strip()
            if msg == "1":
                print("\nEscolha o prato que deseja:")
                print("0 - Voltar")
                for key, value in menu_pratos.items():
                    print(f"{key} - {value}")
                estado = "escolhendo_prato"
            elif msg == "2":
                print("\nEscolha a bebida que deseja:")
                print("0 - Voltar")
                for key, value in menu_bebidas.items():
                    print(f"{key} - {value}")
                estado = "escolhendo_bebida"
            else:
                print("Opção inválida. Digite 1 ou 2.")

        elif estado == "escolhendo_prato":
            msg = input("Você: ").strip()
            if msg in menu_pratos:
                pedido["prato"] = menu_pratos[msg]
                print(f"\nPrato escolhido: {pedido['prato']}")
                print("Deseja escolher uma bebida?\n0 - voltar\n1 - sim\n2 - não")
                estado = "pergunta_bebida"
            elif msg == "0":
                estado = "inicio"
            else:
                print("Escolha inválida. Tente novamente.")

        elif estado == "pergunta_bebida":
            msg = input("Você: ").strip()
            if msg == "1":
                print("\nEscolha a bebida que deseja:")
                for key, value in menu_bebidas.items():
                    print(f"{key} - {value}")
                estado = "escolhendo_bebida"
            elif msg == "2":
                pedido["bebida"] = "nenhuma"
                estado = "resumo"
            elif msg == "0":
                estado = "inicio"
            else:
                print("Opção inválida. Digite 1 ou 2.")

        elif estado == "escolhendo_bebida":
            msg = input("Você: ").strip()
            if msg in menu_bebidas:
                pedido["bebida"] = menu_bebidas[msg]
                estado = "resumo"
            elif msg == "0":
                estado = "inicio"
            else:
                print("Escolha inválida. Tente novamente.")

        elif estado == "resumo":
            print("\nResumo do pedido:")
            print(f"Prato: {pedido.get('prato', 'nenhum')}")
            print(f"Bebida: {pedido.get('bebida', 'nenhuma')}")
            print("Deseja alterar ou confirmar o pedido?\n0 - cancelar\n1 - alterar\n2 - confirmar")
            estado = "confirmacao"

        elif estado == "confirmacao":
            msg = input("Você: ").strip()
            if msg == "1":
                pedido = {}  # limpa os dados anteriores
                estado = "inicio"  # reinicia o fluxo do zero
            elif msg == "2":
                try:
                    response = supabase.table(TABLE_NAME).insert({
                        "numero": numero,
                        "prato": pedido.get("prato", "nenhum"),
                        "bebida": pedido.get("bebida", "nenhuma")
                    }).execute()
                    numero_pedido = response.data[0]['id']
                    print(f"\n✅ Pedido confirmado! Número do pedido: {numero_pedido}")
                except Exception as e:
                    print("❌ Erro ao salvar no banco:", e)
                break
            elif msg == "0":
                print("Pedido cancelado. Até mais! 👋")
                cancelado = True
                break
            else:
                print("Opção inválida. Digite 0, 1 ou 2.")

if __name__ == "__main__":
    main()
