# TDD

TDD é uma prática de desenvolvimento de software que é baseada em escrevermos testes antes mesmo do código em produção, desta maneira garantindo que o código produzido sempre estará testado.
A ideia é termos duas classes ("select_banco" e "criar_menu") em que devemos garantir que os selects no banco de dados e a criação dos menus funcionem de maneira correta.

## Passo 1 - Começando, obviamente, pelos testes

Criaremos em uma pasta "tests" dois arquivos Python: "select_banco.py" e "criar_menu". Neles definiremos todos os testes:

class test_criar_menu.py:
  ```
  import pytest
from src.criar_menu import CriarMenu

class TestCriarMenu:

    def test_criar_menu_com_dados_validos(self):
        dados = [
            {"id": 1, "nome": "Prato A", "preco": 10.5},
            {"id": 2, "nome": "Prato B", "preco": 20.0},
            {"id": 3, "nome": "Prato C", "preco": 5.75}
        ]

        menu = CriarMenu(dados).menu

        esperado = {
            1: "R$ 10.50 - Prato A",
            2: "R$ 20.00 - Prato B",
            3: "R$ 5.75 - Prato C"
        }

        assert menu == esperado

    def test_criar_menu_com_lista_vazia_retorna_dicionario_vazio(self):
        dados = []
        menu = CriarMenu(dados).menu
        assert menu == {}
  ```

class test_select_banco.py:
```
from src.select_banco import SelectBanco

class TestSelectBanco:
    def test_select_pratos(self):
        select = SelectBanco("Cardapio_Pratos")
        dados = select.get_dados()
        assert isinstance(dados, list)
        assert all("id" in item and "nome" in item for item in dados)

    def test_select_bebidas(self):
        select = SelectBanco("Cardapio_Bebidas")
        dados = select.get_dados()
        assert isinstance(dados, list)
        assert all("id" in item and "nome" in item for item in dados)
```

Estes testes não rodarão pois estão com erros, afinal não criamos as classes "criar_menu" e "select_banco" ainda, porém é importante entender que todos as possíveis operações/funcionalidades dessa classe estão garatidamente testadas.

## Passo 2 - Criando a classe
  ```
  class CriarMenu:
    def __init__(self, dados):
        self.menu = self._criar_menu(dados)

    def _criar_menu(self, dados):
        menu = {}
        for item in dados:
            menu[item["id"]] = f"R$ {item['preco']:.2f} - {item['nome']}"
        return menu
  ```

  ```
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
  ```

## Passo 3 - Executando os testes
  ```
  pytest tests/test_criar_menu.py
  ```

  ```
  pytest tests/test_select_banco.py
  ```

## Passo 4 - Analisando o resultado dos testes
test_criar_menu: 
<img src="imanges_testes/print_criar_menu.png">

test_select_banco:  
<img src="imanges_testes/print_select_banco.png">