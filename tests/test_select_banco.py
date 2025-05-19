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