# Plotly Kazakhstan Map

`plotly_kz_map` — is a Python package that provides a simple interface to create
Kazakhstan maps using [Plotly](https://github.com/plotly/plotly.py).

## Installation

```bash
pip install plotly-kz-map
```

## Features

- Drop in replacement for Plotly `choropleth` function, but with Kazakhstan regions support.

## Example

Here is an example using `plotly_kz_map` to visualize the population
of Kazakhstan by regions.

```python
import plotly_kz_map as px

# load a sample dataset as a pandas DataFrame
df = px.data.kazakhstan_population()

fig = px.choropleth(
    locations=df.region,
    locationmode="KZ-regions",
    color=df.population,
)

fig.show()
```

![Plotly Kazakhstan Map continuous](https://github.com/aidoskanapyanov/plotly-kz-map/blob/main/images/plotly-kz-map-continuous.png?raw=true)

Or you can use a discrete color scale:

```python
import plotly_kz_map as px

# load a sample dataset as a pandas DataFrame
df = px.data.kazakhstan_population()

fig = px.choropleth(
    locations=df.region,
    locationmode="KZ-regions",
    color=df.region,
)

fig.show()
```

![Plotly Kazakhstan Map discrete](https://github.com/aidoskanapyanov/plotly-kz-map/blob/main/images/plotly-kz-map-discrete.png?raw=true)

## License

[MIT](LICENSE)
