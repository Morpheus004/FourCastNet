# import cdsapi
#
# c = cdsapi.Client()
#
# c.retrieve(
#     'reanalysis-era5-single-levels',
#     {
#         'product_type': 'reanalysis',
#         'format': 'netcdf',
#         'variable': [
#             '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
#             'mean_sea_level_pressure', 'surface_pressure', 'total_column_water_vapour',
#         ],
#         'year': '2021',
#         'month': '10',
#         'day': [
#             '19', '20', '21',
#             '22', '23', '24',
#             '25', '26', '27',
#             '28', '29', '30',
#             '31',
#         ],
#         'time': [
#             '00:00', '06:00', '12:00',
#             '18:00',
#         ],
#     },
#     '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_sfc.nc')
#

#    '/project/projectdirs/dasrepo/ERA5/oct_2021_19_31_pl.nc')
#    my required request
import cdsapi

dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "2m_temperature",
        "mean_sea_level_pressure",
        "surface_pressure",
        "total_column_water_vapour",
    ],
    "year": ["2022"],
    "month": ["01"],
    "day": [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
    ],
    "time": ["00:00", "06:00", "12:00", "18:00"],
    "data_format": "netcdf",
    "download_format": "unarchived",
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
