class CriarMenu:
    def __init__(self, dados):
        self.menu = self._criar_menu(dados)

    def _criar_menu(self, dados):
        menu = {}
        for item in dados:
            menu[item["id"]] = f"R$ {item['preco']:.2f} - {item['nome']}"
        return menu
