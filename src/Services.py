import pystac_client
import stackstac
import numpy as np
import streamlit as st
from SateliteImagem import SateliteImagem

class Services:
    """
    Classe responsável por fornecer serviços relacionados à busca e carregamento de dados de satélite Sentinel-2 (L2A)
    utilizando STAC e Stackstac.
    Atributos de classe:
        STAC_URL (str): URL do catálogo público STAC para busca dos dados Sentinel-2.
    Métodos:
        fetch_sentinel_data(bbox, date_range="2023-08-01/2023-11-30", max_cloud=20):
            Busca e carrega dados Sentinel-2 (L2A) para uma área geográfica definida por 'bbox' e intervalo de datas.
            Permite filtrar por cobertura de nuvens máxima ('max_cloud').
            Retorna um objeto contendo as bandas selecionadas e metadados do item.
            Em caso de erro na conexão ou ausência de dados, retorna None.
    """

    
    # URL do catálogo público
    STAC_URL = "https://earth-search.aws.element84.com/v1"

    @st.cache_data(ttl=3600)
    def fetch_sentinel_data(bbox, date_range="2023-08-01/2023-11-30", max_cloud=20):

        """
        Busca e carrega dados do Sentinel-2 (L2A) utilizando STAC e Stackstac.
        Parâmetros:
            bbox (list ou tuple): Caixa delimitadora (bounding box) no formato [min_lon, min_lat, max_lon, max_lat].
            date_range (str, opcional): Intervalo de datas no formato "YYYY-MM-DD/YYYY-MM-DD". Padrão: "2023-08-01/2023-11-30".
            max_cloud (int, opcional): Percentual máximo de cobertura de nuvens permitido. Padrão: 20.
        Retorna:
            sat (objeto): DataArray contendo as bandas 'red', 'nir' e 'green', além dos metadados do item selecionado.
            None: Caso não sejam encontrados itens ou ocorra algum erro na conexão.
        Exceções:
            Em caso de erro na conexão ou busca, retorna None e exibe mensagem de erro via Streamlit.
        """
        
        #Busca e carrega dados Sentinel-2 (L2A) usando STAC e Stackstac.
        #Retorna: DataArray com as bandas raw e metadados do item.
        
        try:
            catalog = pystac_client.Client.open(Services.STAC_URL)

            search = catalog.search(
                collections=["sentinel-2-l2a"],
                bbox=bbox,
                datetime=date_range,
                query={"eo:cloud_cover": {"lt": max_cloud}}
            )
            
            items = search.item_collection()
            
            if not len(items):
                return None

            selected_item = items[0]

            # Configuração do Stackstac (Lazy Loading)
            # Importante: Sem dtype="float32" para evitar erro de escala
            da = stackstac.stack(
                selected_item,
                assets=["red", "nir", "green"], 
                bounds=bbox,
                epsg=4326, 
                resolution=0.0001, # ~10m
                fill_value=np.nan
            )

            
            
            #Criando o objeto com os dados necessário
            sat = SateliteImagem (
                data = da,
                metadata = selected_item.to_dict()
            )


            return sat
        
        except Exception as e:
            st.error(f"Erro na conexão com satélite: {e}")
            return None