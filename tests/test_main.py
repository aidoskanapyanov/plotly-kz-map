import plotly_kz_map as px


def test_continuous_data():
    df = px.data.kazakhstan_population()

    fig = px.choropleth(
        locations=df.region,
        locationmode="KZ-regions",
        color=df.population,
    )

    assert fig


def test_kazakhstan_population_data():
    df = px.data.kazakhstan_population()
    assert not df.empty


def test_dicrete_data():
    df = px.data.kazakhstan_population()

    fig = px.choropleth(
        locations=df.region,
        locationmode="KZ-regions",
        color=df.region,
    )

    assert fig
