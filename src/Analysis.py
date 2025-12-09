import xarray as xr

class Analysis:

    """
    Atributos de Classe:
        WATER_THRESHOLD (float): Limiar para classificação de água. Pixels com NDWI acima deste valor são classificados como água.
        SOIL_THRESHOLD (float): Limiar para classificação de solo exposto/vegetação. Pixels com NDVI abaixo deste valor (e que não são água) são classificados como solo exposto/lama.

    """

    WATER_THRESHOLD = 0.0 #limite de água
    SOIL_THRESHOLD = 0.25 #limiar do solo

    
    def __init__(self, ndvi: xr.DataArray, ndwi: xr.DataArray):
        
        """
        Inicializa a instância da classe de análise.

        Args:
            ndvi (xr.DataArray): Array de dados contendo o Índice de Vegetação por Diferença Normalizada (NDVI).
            ndwi (xr.DataArray): Array de dados contendo o Índice de Água por Diferença Normalizada (NDWI).

        Attributes:
            ndvi (xr.DataArray): Índice de Vegetação por Diferença Normalizada.
            ndwi (xr.DataArray): Índice de Água por Diferença Normalizada.
            class_map (None): Mapa de classificação (inicializado como None).
            stats (None): Estatísticas da análise (inicializado como None).
        """

        self.ndvi = ndvi
        self.ndwi = ndwi
        self.class_map = None
        self.stats = None

    def classify_cover(self):
        """
        Classifica a cobertura do solo com base nos índices NDWI e NDVI.
        Retorna um mapa de classes onde:
            0 - Água (quando NDWI > WATER_THRESHOLD)
            1 - Solo (quando NDWI <= WATER_THRESHOLD e NDVI < SOIL_THRESHOLD)
            2 - Vegetação (quando NDWI <= WATER_THRESHOLD e NDVI >= SOIL_THRESHOLD)
        Returns:
            xarray.DataArray: Mapa de classificação das coberturas.
        """
        
        # Lógica: Se é água, é 0. Se não, verifica se é solo (1) ou veg (2)
        self.class_map = xr.where(
            self.ndwi > self.WATER_THRESHOLD, 
            0, 
            xr.where(self.ndvi < self.SOIL_THRESHOLD, 1, 2)
        )

        return self.class_map

    def calculate_stats(self):
        """
            Calcula as estatísticas percentuais de cada classe (água, solo, vegetação) no mapa de classes.
            Retorna:
            dict: Um dicionário contendo as porcentagens de pixels classificados como água ('perc_water'), solo ('perc_solo') e vegetação ('perc_veg').
            Levanta:
            ValueError: Se o mapa de classes ainda não foi gerado (self.class_map é None).
        """
       
        if self.class_map is None:
            raise ValueError("O mapa de classes ainda não foi gerado.") #tem que executar classify_cover primeiro

        total_pixels = self.ndvi.size
        pixels_water = int((self.class_map == 0).sum())
        pixels_solo = int((self.class_map == 1).sum())
        pixels_veg = int((self.class_map == 2).sum())

        self.stats= {
            "perc_water": (pixels_water / total_pixels) * 100,
            "perc_solo": (pixels_solo / total_pixels) * 100,
            "perc_veg": (pixels_veg / total_pixels) * 100
        }
    
        return self.stats

"""Como usar a classe: 
    analise = Analysis(ndvi, ndwi)
    mapa = analise.classify_cover()
    estatisticas = analise.calculate_stats()
    print(estatisticas)
"""