class SateliteImagem:
    def __init__(self, data, metadata):
        """
        Inicializa uma instância da classe com os dados da imagem e metadados associados.

        Args:
            data: DataArray contendo as bandas espectrais (vermelho, verde, nir).
            metadata: dicionário com os metadados do item.
        """
        self.data = data #DataArray (red, green, nir)
        self.metadata = metadata #dict com metadados do item