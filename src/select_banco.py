from supabase import create_client, Client

SUPABASE_URL = "https://zunahsztxrsteancdzkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1bmFoc3p0eHJzdGVhbmNkemtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU1MTQxMjEsImV4cCI6MjA2MTA5MDEyMX0.Wndqn0SjlLfPDPQeSbg0NDijxW4jIH_Yq523wVOQS94"

class SelectBanco:
    def __init__(self, tabela: str):
        self.tabela = tabela
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_dados(self):
        resposta = self.supabase.table(self.tabela).select("*").order("id", desc=False).execute()
        return resposta.data