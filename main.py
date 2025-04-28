from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"  # Substitua por segurança
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
    "1": "R$ 5,99 - Cola-Cola",
    "2": "R$ 5,99 - Cola-Cola Zero",
    "3": "R$ 7,99 - Suco de laranja",
    "4": "R$ 7,99 - Suco de uva",
    "5": "R$ 6,99 - Água com gás",
    "6": "R$ 4,99 - Água sem gás"
}

usuarios = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    numero = request.form.get("From")
    numero_limpo = numero.replace("whatsapp:","")
    msg = request.form.get("Body").strip()
    response = MessagingResponse()
    reply = response.message()

    if numero not in usuarios:
        usuarios[numero] = {
            "estado": "inicio",
            "pedido": {},
            "cancelado": False,
            "total": 0
        }

    user = usuarios[numero]
    estado = user["estado"]
    pedido = user["pedido"]
    total = user["total"]

    if estado == "inicio":
        reply.body("Olá, aqui é o bot de atendimento do restaurante Comida Boa. 🤖\nDigite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida")
        user["estado"] = "menu"

    elif estado == "menu":
        if msg == "1":
            texto = "Escolha o prato que deseja:\n0 - Voltar\n"
            for key, value in menu_pratos.items():
                texto += f"{key} - {value}\n"
            reply.body(texto)
            user["estado"] = "escolhendo_prato"
        elif msg == "2":
            texto = "Escolha a bebida que deseja:\n0 - Voltar\n"
            for key, value in menu_bebidas.items():
                texto += f"{key} - {value}\n"
            reply.body(texto)
            user["estado"] = "escolhendo_bebida"
        else:
            reply.body("Opção inválida. Tente novamente.")

    elif estado == "escolhendo_prato":
        if msg in menu_pratos:
            prato_escolhido = menu_pratos[msg]
            total += float(prato_escolhido.split("R$ ")
                           [1].split(" - ")[0].replace(",", "."))
            pedido["prato"] = menu_pratos[msg]
            reply.body(f"Você escolheu: {prato_escolhido}")
            reply.body("Confirmar este prato?\n1 - Sim\n2 - Não, quero escolher outro\n0 - Voltar ao menu principal")
            user["estado"] = "confirmar_prato"
        elif msg == "0":
            user["estado"] = "inicio"
            reply.body("Voltando ao menu inicial.")
        else:
            reply.body("Escolha inválida. Tente novamente.")
        
    elif estado == "confirmar_prato":
        if msg == "1":
            pedido["prato"] = prato_escolhido
            reply.body(f"Prato confirmado: {pedido['prato']}")
            reply.body('Deseja escolher sua bebida?\n0 - voltar\n1 - sim\n2 - não')
            estado = "pergunta_bebida"
        elif msg == "2":
            reply.body("Escolha o prato que deseja:\n")
            reply.body('0 - voltar\n')
            for key, value in menu_pratos.items():
                reply.body(f'{key} - {value}\n')
            estado = "menu"
        elif msg == "0":
            estado = "inicio"
        else:
            print('Opção inválida. Tente novamente.')


    elif estado == "pergunta_bebida":
        if msg == "1":
            texto = "Escolha a bebida que deseja:\n"
            for key, value in menu_bebidas.items():
                texto += f"{key} - {value}\n"
            reply.body(texto)
            user["estado"] = "escolhendo_bebida"
        elif msg == "2":
            pedido["bebida"] = "nenhuma"
            user["estado"] = "confirmacao"
            reply.body(f"Resumo do pedido:\nPrato: {pedido.get('prato', 'nenhum')}\nBebida: nenhuma\n0 - cancelar\n1 - alterar\n2 - confirmar")
        elif msg == "0":
            user["estado"] = "inicio"
            reply.body("Voltando ao início.")
        else:
            reply.body("Opção inválida. Tente novamente.")

    elif estado == "escolhendo_bebida":
        if msg in menu_bebidas:
            bebida_escolhida = menu_bebidas[msg]
            total += float(bebida_escolhida.split("R$ ")
                           [1].split(" - ")[0].replace(",", "."))
            pedido["bebida"] = menu_bebidas[msg]
            user["estado"] = "confirmacao"
            reply.body(f'Você escolheu: {bebida_escolhida}')
            reply.body('Confirmar esta bebida?\n1 - Sim\n2 - Não, quero escolher outra\n0 - Voltar ao menu principal')
            estado = "confirmar_bebida"
        else:
            reply.body("Escolha inválida. Tente novamente.")

    elif estado == "confirmar_bebida":
        if msg == "1":
            pedido["bebida"] = bebida_escolhida
            reply.body(f'bot: Bebida confirmada: {pedido["bebida"]}')
            estado = "resumo"
        elif msg == "2":
            reply.body('Escolha a bebida que deseja:')
            for key, value in menu_bebidas.items():
                reply.body(f'{key} - {value}')
            estado = "escolhendo_bebida"
        elif msg == "0":
            estado = "inicio"
        else:
            reply.body('Opção inválida. Tente novamente')
    
    elif estado == "resumo":
        reply.body("Resumo do pedido:")
        reply.body(f"Prato: {pedido.get('prato', 'nenhum')}")
        reply.body(f"Bebida: {pedido.get('bebida', 'nenhuma')}")
        reply.body(f"Total: R$ {total:.2f}")
        reply.body("Deseja alterar ou confirmar o pedido?\n0 - cancelar pedido\n1 - alterar\n2 - confirmar pedido")
        estado = "confirmacao"

    elif estado == "confirmacao":
        if msg == "1":
            pedido = {}
            reply.body("Você pode alterar seu pedido agora.")
            user["estado"] = "menu"
        elif msg == "2":
            try:
                result = supabase.table(TABLE_NAME).insert({
                    "prato": pedido.get('prato', 'nenhum'),
                    "bebida": pedido.get('bebida', 'nenhuma'),
                    "total": total,
                    "numero": numero_limpo
                }).execute()

                # print("✅ Supabase resultado:", result)

                if result.data:
                    numero_pedido = result.data[0]['id']
                    reply.body(f"Pedido confirmado! ✅\nNúmero do pedido: {numero_pedido}")
                usuarios.pop(numero)
            except Exception as e:
                reply.body("Erro ao registrar o pedido. Tente novamente.")
        elif msg == "0":
            reply.body("Pedido cancelado. Até mais! 👋")
            usuarios.pop(numero)
        else:
            reply.body("Opção inválida. Tente novamente.")

    # Resposta padrão se nenhuma condição foi atendida
    if not reply.body:
        reply.body("Opção inválida. Tente novamente.")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)