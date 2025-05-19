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
