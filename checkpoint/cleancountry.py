import re
import pycountry
import plotly.express as px
def clean_title1(country):
    if country == 'USA':
        return 'US'
    if country.endswith('usa'):
        return 'US'
    if country.startswith('usa'):
        return 'US'
    return re.sub("[^a-zA-Z0-9]"," ",country).upper()

def get_iso_alpha3(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None

def visualize_book_distribution(maindata):
    maindata.dropna(subset=['country'], inplace=True)
    maindata['cleancountry'] = maindata['country'].apply(clean_title1)
    maindata['iso_alpha3_code'] = maindata['cleancountry'].apply(get_iso_alpha3)
    country_count = maindata['iso_alpha3_code'].value_counts()
    iso_counts = maindata['iso_alpha3_code'].value_counts()
    filtered_iso_counts = iso_counts[iso_counts > 5]
    valid_iso_codes = filtered_iso_counts.index
    filtered_data = maindata[maindata['iso_alpha3_code'].isin(valid_iso_codes)]
    iso_counts_valid = filtered_data['iso_alpha3_code'].value_counts()
    fig = px.choropleth(iso_counts_valid, 
                        locations=iso_counts_valid.index,
                        locationmode='ISO-3',
                        color=iso_counts_valid,
                        range_color=(500, 20000),
                        title="Book Distribution by Country",
                        color_continuous_scale=px.colors.sequential.Viridis,
                    )
    return fig