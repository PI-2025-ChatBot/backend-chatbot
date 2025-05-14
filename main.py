from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

menu_pratos = {}
menu_bebidas = {}

select_pratos = supabase.table("Cardapio").select("*").eq("tipo", "prato").execute()
select_pratos.data

select_bebidas = supabase.table("Cardapio").select("*").eq("tipo", "bebida").execute()
select_bebidas.data

for prato in select_pratos.data:
    menu_pratos[prato["id"]] = f"R$ {prato['preco']} - {prato['nome']}"

for bebida in select_bebidas.data:
    menu_bebidas[bebida["id"]] = f"R$ {bebida['preco']} - {bebida['nome']}"

usuarios = {}

@app.route("/mensagem", methods=["POST"])
def whatsapp():
    email = request.form.get("From")
    msg = request.form.get("Body").strip()
    response = MessagingResponse()
    reply = response.message()

    if email not in usuarios:
        usuarios[email] = {
            "estado": "inicio",
            "pedido": {},
            "cancelado": False,
            "total": 0
        }

    user = usuarios[email]
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
            usuarios.pop(email)
        else:
            reply.body("Opção inválida. Digite 1 ou 2.")

    elif estado == "escolhendo_prato":
        if msg in menu_pratos:
            prato_escolhido = menu_pratos[msg]
            if "prato" in pedido:
                total -= float(pedido["prato"].split("R$ ")
                               [1].split(" - ")[0].replace(",", "."))
            pedido["prato"] = prato_escolhido
            descricao_prato = supabase.table("Cardapio").select("Descricao").eq("id", msg).execute()
            total += float(prato_escolhido.split("R$ ")
                           [1].split(" - ")[0].replace(",", "."))
            user["total"] = total
            reply.body(
                f"Você escolheu: {prato_escolhido}\n\n{descricao_prato.data[0]["descricao"]}Confirmar este prato?\n1 - Sim\n2 - Não, quero escolher outro\n0 - Voltar ao menu principal")
            user["estado"] = "confirmar_prato"
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n0 - Cancelar pedido")
            user["estado"] = "menu"
        else:
            reply.body("Escolha inválida. Tente novamente.")

    elif estado == "confirmar_prato":
        if msg == "1":
            reply.body(
                f"Prato confirmado: {pedido['prato']}\nDeseja escolher sua bebida?\n1 - Sim\n2 - Não\n0 - Voltar ao menu principal")
            user["estado"] = "pergunta_bebida"
        elif msg == "2":
            texto = "Escolha o prato que deseja:\n0 - Voltar ao menu principal\n"
            for key, value in menu_pratos.items():
                texto += f"{key} - {value}\n"
            reply.body(texto)
            user["estado"] = "escolhendo_prato"
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n0 - Cancelar pedido")
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
                "Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n0 - Cancelar pedido")
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
                "Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n0 - Cancelar pedido")
            user["estado"] = "menu"
        else:
            reply.body("Escolha inválida. Tente novamente.")

    elif estado == "confirmar_bebida":
        if msg == "1":
            total_formatado = f"{total:.2f}".replace(".", ",")
            reply.body(f"Bebida confirmada: {pedido['bebida']}\nResumo do pedido:\nPrato: {pedido.get('prato', 'nenhum')}\nBebida: {pedido.get('bebida', 'nenhuma')}\nTotal: R$ {total_formatado}\n1 - Confirmar\n2 - Alterar\n0 - Cancelar")
            user["estado"] = "confirmacao"
        elif msg == "2":
            texto = "Escolha a bebida que deseja:\n"
            for key, value in menu_bebidas.items():
                texto += f"{key} - {value}\n"
                texto+="\n0 - Voltar ao menu principal"
            reply.body(texto)
            user["estado"] = "escolhendo_bebida"
        elif msg == "0":
            reply.body(
                "Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n0 - Cancelar pedido")
            user["estado"] = "menu"
        else:
            reply.body("Opção inválida. Tente novamente.")

    elif estado == "confirmacao":
        if msg == "2":
            reply.body(
                "Digite o número da opção desejada:\n1 - Escolher prato\n2 - Escolher bebida\n0 - Cancelar pedido")
            user["estado"] = "menu"
        elif msg == "1":
            try:
                result = supabase.table("Pedidos").insert({
                    "prato": pedido.get('prato', 'nenhum'),
                    "bebida": pedido.get('bebida', 'nenhuma'),
                    "total": total,
                    "email": email
                }).execute()
                if result.data:
                    email_pedido = result.data[0]['id']
                    reply.body(
                        f"Pedido confirmado! ✅\nNúmero do pedido: {email_pedido}\nObrigado pela preferência! Até a próxima! 👋")
                usuarios.pop(email)
            except Exception as e:
                reply.body("Erro ao registrar o pedido. Tente novamente.")
        elif msg == "0":
            reply.body("Pedido cancelado. Até mais! 👋")
            usuarios.pop(email)
        else:
            reply.body("Opção inválida. Tente novamente.")

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
