from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client

app = Flask(__name__)

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

usuarios = {}


@app.route("/mensagem", methods=["POST"])
def whatsapp():
    numero = request.form.get("From")
    numero_limpo = numero.replace("whatsapp:", "")
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
        reply.body("Olá, aqui é o bot de atendimento do restaurante Comida Boa.\nDigite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n0 - Cancelar pedido")
        user["estado"] = "menu"

    elif estado == "menu":
        if msg == "1":
            texto = "Escolha o prato que deseja:\n"
            for key, value in menu_pratos.items():
                texto += f"{key} - {value}\n"
            texto += "0 - Voltar ao menu principal\n"
            reply.body(texto)
            user["estado"] = "escolhendo_prato"
        elif msg == "2":
            texto = "Escolha a bebida que deseja:\n0 - Voltar ao menu principal\n"
            for key, value in menu_bebidas.items():
                texto += f"{key} - {value}\n"
            reply.body(texto)
            user["estado"] = "escolhendo_bebida"
        elif msg == "0":
            reply.body("Pedido cancelado. Até mais! 👋")
            usuarios.pop(numero)
        else:
            reply.body("Opção inválida. Digite 1 ou 2.")

    elif estado == "escolhendo_prato":
        if msg in menu_pratos:
            prato_escolhido = menu_pratos[msg]
            if "prato" in pedido:
                total -= float(pedido["prato"].split("R$ ")
                               [1].split(" - ")[0].replace(",", "."))
            pedido["prato"] = prato_escolhido
            total += float(prato_escolhido.split("R$ ")
                           [1].split(" - ")[0].replace(",", "."))
            user["total"] = total
            reply.body(
                f"Você escolheu: {prato_escolhido}\nConfirmar este prato?\n1 - Sim\n2 - Não, quero escolher outro\n0 - Voltar ao menu principal")
            user["estado"] = "confirmar_prato"
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n0 - Cancelar pedido\n1 - Escolher prato\n2 - Escolher bebida")
            user["estado"] = "menu"
        else:
            reply.body("Escolha inválida. Tente novamente.")

    elif estado == "confirmar_prato":
        if msg == "1":
            reply.body(
                f"Prato confirmado: {pedido['prato']}\nDeseja escolher sua bebida?\0 - Voltar ao menu principal\n1 - Sim\n2 - Não\n")
            user["estado"] = "pergunta_bebida"
        elif msg == "2":
            texto = "Escolha o prato que deseja:\n0 - Voltar ao menu principal\n"
            for key, value in menu_pratos.items():
                texto += f"{key} - {value}\n"
            reply.body(texto)
            user["estado"] = "escolhendo_prato"
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n0 - Cancelar pedido\n1 - Escolher prato\n2 - Escolher bebida")
            user["estado"] = "menu"
        else:
            reply.body("Opção inválida. Tente novamente.")

    elif estado == "pergunta_bebida":
        if msg == "1":
            texto = "Escolha a bebida que deseja:\n"
            for key, value in menu_bebidas.items():
                texto += f"{key} - {value}\n"
            texto += "0 - Voltar ao menu principal\n"
            reply.body(texto)
            user["estado"] = "escolhendo_bebida"
        elif msg == "2":
            if "bebida" in pedido and "R$ " in pedido["bebida"]:
                total -= float(pedido["bebida"].split("R$ ")
                               [1].split(" - ")[0].replace(",", "."))
            pedido["bebida"] = "nenhuma"
            user["total"] = total
            user["estado"] = "confirmacao"
            reply.body(f"Resumo do pedido:\nPrato: {pedido.get('prato', 'nenhum')}\nBebida: nenhuma\nTotal: R$ {total:.2f}".replace(
                ".", ",") + "\n1 - Confirmar\n2 - Alterar\n0 - Cancelar")
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n0 - Cancelar pedido\n1 - Escolher prato\n2 - Escolher bebida")
            user["estado"] = "menu"
        else:
            reply.body("Opção inválida. Tente novamente.")

    elif estado == "escolhendo_bebida":
        if msg in menu_bebidas:
            bebida_escolhida = menu_bebidas[msg]
            if "bebida" in pedido and "R$ " in pedido["bebida"]:
                total -= float(pedido["bebida"].split("R$ ")
                               [1].split(" - ")[0].replace(",", "."))
            pedido["bebida"] = bebida_escolhida
            total += float(bebida_escolhida.split("R$ ")
                           [1].split(" - ")[0].replace(",", "."))
            user["total"] = total
            reply.body(
                f"Você escolheu: {bebida_escolhida}\nConfirmar esta bebida?\n1 - Sim\n2 - Não, quero escolher outra\n0 - Voltar ao menu principal")
            user["estado"] = "confirmar_bebida"
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n0 - Cancelar pedido\n1 - Escolher prato\n2 - Escolher bebida")
            user["estado"] = "menu"
        else:
            reply.body("Escolha inválida. Tente novamente.")

    elif estado == "confirmar_bebida":
        if msg == "1":
            total_formatado = f"{total:.2f}".replace(".", ",")
            reply.body(f"Bebida confirmada: {pedido['bebida']}\nResumo do pedido:\nPrato: {pedido.get('prato', 'nenhum')}\nBebida: {pedido.get('bebida', 'nenhuma')}\nTotal: R$ {total_formatado}\n1 - Confirmar\n2 - Alterar\n0 - Cancelar")
            user["estado"] = "confirmacao"
        elif msg == "2":
            texto = "Escolha a bebida que deseja:\n0 - Voltar ao menu principal\n"
            for key, value in menu_bebidas.items():
                texto += f"{key} - {value}\n"
            reply.body(texto)
            user["estado"] = "escolhendo_bebida"
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n0 - Cancelar pedido\n1 - Escolher prato\n2 - Escolher bebida")
            user["estado"] = "menu"
        else:
            reply.body("Opção inválida. Tente novamente.")

    elif estado == "confirmacao":
        if msg == "2":
            reply.body(
                "Digite o número da opção desejada:\n0 - Cancelar pedido\n1 - Escolher prato\n2 - Escolher bebida")
            user["estado"] = "menu"
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
                    reply.body(
                        f"Pedido confirmado! ✅\nNúmero do pedido: {numero_pedido}\nObrigado pela preferência! Até a próxima! 👋")
                usuarios.pop(numero)
            except Exception as e:
                reply.body("Erro ao registrar o pedido. Tente novamente.")
        elif msg == "0":
            reply.body("Pedido cancelado. Até mais! 👋")
            usuarios.pop(numero)
        else:
            reply.body("Opção inválida. Tente novamente.")

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
