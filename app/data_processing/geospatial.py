import geopandas as gpd
from shapely.geometry import Polygon

def generate_geojson(shp_path: str):
    """Converte Shapefile in GeoJSON e calcola metriche spaziali."""
    gdf = gpd.read_file(shp_path)
    gdf = gdf.to_crs(epsg=4326)  # WGS84
    
    # Calcola area effettiva
    gdf['area_ettari'] = gdf.geometry.area * 1e-4  # m² → Ettari
    
    # Filtra geometrie non valide
    gdf = gdf[gdf.geometry.is_valid]
    
    return gdf.__geo_interface__
