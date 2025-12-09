import xarray as xr
import numpy as np
from dataclasses import dataclasses
from typing import Dict

class Indices:
    """
    Classe Indices para cálculo de índices espectrais a partir de um xr.DataArray.
    Parâmetros
    ----------
    da : xr.DataArray
        DataArray contendo as bandas espectrais, recuperado do banco de dados.
    Métodos
    -------
    pegar_banda(band_name: str) -> xr.DataArray
        Retorna a banda especificada convertida para float32.
    calcular_ndvi() -> xr.DataArray
        Calcula o índice de vegetação por diferença normalizada (NDVI) usando as bandas 'nir' e 'red'.
    calcular_ndwi() -> xr.DataArray
        Calcula o índice de água por diferença normalizada (NDWI) usando as bandas 'nir' e 'green'.
    todos_indices() -> Dict[str, xr.DataArray]
        Retorna um dicionário com todos os índices calculados ('ndvi' e 'ndwi').
    """


    #Recebe o DataArray bruto e calcula NDVI e NDWI.
    
    #Converte para float32 para economizar memória nos cálculos
    #nir = da.sel(band="nir").astype("float32")
    #red = da.sel(band="red").astype("float32")
    #green = da.sel(band="green").astype("float32")

    
    
    def __init__(self, da: xr.DataArray):
        self.da = da #recuperado do banco

    def pegar_banda(self, band_name: str) -> xr.DataArray:
        return self.da.sel(band=band_name).astype("float32") 
    

    def calcular_ndvi(self) -> xr.DataArray:
        nir = self.pegar_banda("nir")
        red = self.pegar_banda("red")

        den = nir + red
        ndvi= xr.where(den == 0, np.nan, (nir - red)/den)
        return ndvi
    
    def calcular_ndwi(self) -> xr.DataArray:
        nir = self.pegar_banda("nir")
        green = self.pegar_banda("green")

        den = nir + green
        ndwi= xr.where(den == 0, np.nan, (nir - green)/den)
        return ndwi
    
    def todos_indices(self) -> Dict[str, xr.DataArray]:
        return {
            "ndvi": self.calcular_ndvi(),
            "ndwi": self.calcular_ndwi()
        }

    #NDVI
    #den_ndvi = nir + red
    #ndvi = xr.where(den_ndvi == 0, np.nan, (nir - red) / den_ndvi)

    #NDWI
    #den_ndwi = green + nir
    #ndwi = xr.where(den_ndwi == 0, np.nan, (green - nir) / den_ndwi)
    
    # O .compute() é chamado aqui para trazer os resultados para a memória
    #return ndvi.compute(), ndwi.compute()
    #return ndvi, ndwi