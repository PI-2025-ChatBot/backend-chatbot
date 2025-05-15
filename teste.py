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
    menu_bebidas[bebida["id"]] = f"R$ {bebida['preco']:.2f} - {bebida['nome']}"

print(menu_bebidas)