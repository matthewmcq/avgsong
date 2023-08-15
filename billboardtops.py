import billboard

# Get the chart

years_all = {"2022":[], "2021":[], "2020":[], "2019":[], "2018":[], "2017":[], "2016":[], "2015":[]}

years_recent = {"2022":[], "2021":[]}

def get_top_albums(years):
    for year in years:
        albums = list()
        chart = billboard.ChartData('top-billboard-200-albums', year=year)
        for album in chart:
            albums.append((album.rank, album.title, album.artist))
        years[year] = albums


test_chart = billboard.ChartData('alternative-songs', year=2020)
def get_years_all():
    get_top_albums(years_all)
    return years_all

def get_years_recent():
    get_top_albums(years_recent)
    return years_recent

def get_year(year):
    albums = list()
    chart = billboard.ChartData('top-billboard-200-albums', year=year)
    for album in chart:
        albums.append((album.rank, album.title, album.artist))
    return {str(year):albums}