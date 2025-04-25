from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from supabase import create_client, Client

app = Flask(__name__)

SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"  # Substitua por segurança
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

usuarios = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    numero = request.form.get("From")
    msg = request.form.get("Body").strip()
    response = MessagingResponse()
    reply = response.message()

    if numero not in usuarios:
        usuarios[numero] = {
            "estado": "inicio",
            "pedido": {},
            "cancelado": False
        }

    user = usuarios[numero]
    estado = user["estado"]
    pedido = user["pedido"]

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
            reply.body("Opção inválida. Digite 1 ou 2.")

    elif estado == "escolhendo_prato":
        if msg in menu_pratos:
            pedido["prato"] = menu_pratos[msg]
            reply.body(f"Prato escolhido: {pedido['prato']}\nDeseja escolher uma bebida?\n0 - voltar\n1 - sim\n2 - não")
            user["estado"] = "pergunta_bebida"
        elif msg == "0":
            user["estado"] = "inicio"
            reply.body("Voltando ao menu inicial.")
        else:
            reply.body("Escolha inválida. Tente novamente.")

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
            reply.body("Opção inválida. Digite 1 ou 2.")

    elif estado == "escolhendo_bebida":
        if msg in menu_bebidas:
            pedido["bebida"] = menu_bebidas[msg]
            user["estado"] = "confirmacao"
            reply.body(f"Bebida escolhida: {pedido['bebida']}\nResumo do pedido:\nPrato: {pedido.get('prato', 'nenhum')}\nBebida: {pedido['bebida']}\n0 - cancelar\n1 - alterar\n2 - confirmar")
        else:
            reply.body("Escolha inválida. Tente novamente.")

    elif estado == "confirmacao":
        if msg == "1":
            user["estado"] = "menu"
            reply.body("Você pode alterar seu pedido agora.")
        elif msg == "2":
            try:
                result = supabase.table(TABLE_NAME).insert({
                    "prato": pedido.get('prato', 'nenhum'),
                    "bebida": pedido.get('bebida', 'nenhuma')
                }).execute()

                print("✅ Supabase resultado:", result)

                if result.data:
                    numero_pedido = result.data[0]['id']
                    reply.body(f"Pedido confirmado! ✅\nNúmero do pedido: {numero_pedido}")
                else:
                    reply.body("Pedido confirmado! ✅ (sem número retornado)")

                usuarios.pop(numero)
            except Exception as e:
                print("❌ Erro ao inserir no Supabase:", e)
                reply.body("Erro ao registrar o pedido. Tente novamente.")
        elif msg == "0":
            reply.body("Pedido cancelado. Até mais! 👋")
            usuarios.pop(numero)
        else:
            reply.body("Opção inválida. Digite 0, 1 ou 2.")

    # Resposta padrão se nenhuma condição foi atendida
    if not reply.body:
        reply.body("Não entendi sua resposta. Por favor, digite uma das opções.")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
