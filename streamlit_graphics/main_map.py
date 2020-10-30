#---------------------------------------------------------------------------------------------------- DEPENDENCIES
# for viz
import folium
import folium.folium
from folium.plugins import Fullscreen
#---------------------------------------------------------------------------------------------------- DEPENDENCIES

MAP_SAVE_PATH = 'streamlit_graphics/'  # three files (there should be only two: catastro and arturo). DIFFERENT SHAPES

def get_main_map(gfd, center_location, tile, color_palette):
    """
    :param gfd: GeoDataframe with filters to show or not in map
    :param center_location: list with central coordinates
    :param tile: string with basemap raster tile to show
    :param color_palette: color_palette to render
    :return: enables html
    """
    # All layers to add MUST BE EPSG3857 for proyection compatibility
    print(
        f"\n-- Rendering Main Map ----------------------------------------------------------------------------------------------")

    m = folium.Map(
        location=center_location,
        zoom_start=14, max_zoom=16, min_zoom=13,
        min_lat=40.15, max_lat=40.75, min_lon=-3.25, max_lon=-3.95, max_bounds=True,
        control_scale=False,
        prefer_canvas=True,
        tiles=tile,
    )

    for i, val in enumerate(gfd.index.tolist()):
        fillColor = color_palette[i]

        gjson_popup = folium.features.GeoJsonTooltip(
            fields=['value', 'currentUse', 'centuryOfConstr', 'nFloors_AG', 'nFloors_BG'],
            aliases=['Voting_Mean', 'Main_Use', 'Construction_Age', 'numFloors_aboveGr', 'numFloors_belowGr'],
            localize=True,
            sticky=True)

        gjson = folium.GeoJson(gfd[gfd.index == val],
                               name=f"cluster_{val}",
                               tooltip=gjson_popup,
                               style_function=lambda x, fillColor=fillColor: {
                                   'fillColor': fillColor,
                                   'color': fillColor,
                                   'weight': 0.2,
                                   'fillOpacity': 0.90}
                               ).add_to(m)

    Fullscreen().add_to(m)
    print(
        f"\t MAIN MAP \tRENDERED --------------------------------------------------------------------------------")
    m.save(f'{MAP_SAVE_PATH}map_to_render.html')