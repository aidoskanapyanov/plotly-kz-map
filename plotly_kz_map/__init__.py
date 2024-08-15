import os
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd
import plotly.express as px


def capture(func):
    if func.__name__ == "plotly.express.data":

        def kazakhstan_population():
            df = pd.DataFrame(
                {
                    "AST": 1472027.0,
                    "ALA": 2258253.0,
                    "SHY": 1238969.0,
                    "ALR": 1545564.0,
                    "AKT": 944610.0,
                    "ATY": 708529.0,
                    "AKM": 789015.0,
                    "WKR": 695018.0,
                    "EKR": 726077.0,
                    "JMB": 1223670.0,
                    "KGD": 1134776.0,
                    "KST": 827899.0,
                    "KZY": 844914.0,
                    "MNG": 795923.0,
                    "NKR": 526185.0,
                    "PVD": 753215.0,
                    "TRK": 2150796.0,
                    "ABY": 605872.0,
                    "JTS": 696783.0,
                    "ULY": 221612.0,
                }.items(),
                columns=["region", "population"],
            )
            return df

        func.kazakhstan_population = kazakhstan_population
        return func

    if func.__module__ != "plotly.express._chart_types":
        return func

    if func.__name__ != "choropleth":
        return func

    def wrapped(*args, **kwargs):
        if "locationmode" not in kwargs:
            return func(*args, **kwargs)

        if "locations" not in kwargs:
            return func(*args, **kwargs)

        if kwargs["locationmode"] != "KZ-regions":
            return func(*args, **kwargs)

        regions_cities = {
            "Abay Region": "ABY",
            "Akmola Region": "AKM",
            "Aktobe Region": "AKT",
            "Almaty Region": "ALR",
            "Atyrau Region": "ATY",
            "East Kazakhstan Region": "EKR",
            "Jambyl Region": "JMB",
            "Jetisu Region": "JTS",
            "Karaganda Region": "KGD",
            "Kostanay Region": "KST",
            "Kyzylorda Region": "KZY",
            "Mangystau Region": "MNG",
            "North Kazakhstan Region": "NKR",
            "Pavlodar Region": "PVD",
            "Turkistan Region": "TRK",
            "Ulytau Region": "ULY",
            "West Kazakhstan Region": "WKR",
            "Almaty": "ALA",
            "Astana": "AST",
            "Shymkent": "SHY",
        }

        path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "kz-adm1.geojson",
        )

        value = []
        if "color" in kwargs:
            value = kwargs["color"]
        if "z" in kwargs:
            value = kwargs["z"]

        locations = kwargs["locations"]
        mapping = dict(zip(locations, value))

        SENTIENT_VALUE = -10000
        gdf = (
            gpd.read_file(path)
            .assign(
                geometry=lambda _df: _df.geometry.buffer(0).simplify(0.05),
                region_code=lambda _df: _df.ADM1_EN.map(regions_cities),
                region_name=lambda _df: _df.ADM1_EN,
            )
            .drop("ADM1_EN", axis=1)
            .assign(color=lambda _df: _df.region_code.map(mapping))
            .assign(color=lambda _df: _df.color.fillna(SENTIENT_VALUE))
            .assign(value=lambda _df: _df.color.replace(SENTIENT_VALUE, ""))
        )

        def generateColorScale(colors, naColor):
            colorArray = []
            colorArray.append([0, naColor])
            for grenze, color in zip(np.linspace(0.01, 1, len(colors)), colors):
                colorArray.append([grenze, color])
            return colorArray

        colors = None
        if gdf.color.dtype == "object":
            n_colors = gdf.color.nunique()
            colors = px.colors.sample_colorscale(
                "viridis", [n / (n_colors - 1) for n in range(n_colors)]
            )

        fig = px.choropleth(
            gdf,
            geojson=gdf,
            color="color",
            hover_data={
                "region_name": True,
                "value": True,
                # hide these
                "color": False,
                "region_code": False,
            },
            locations="region_code",
            featureidkey="properties.region_code",
            projection="mercator",
            color_continuous_scale=generateColorScale(
                colors=px.colors.sequential.Viridis,
                naColor="#e5ecf6",
            )
            if (gdf.color == -10000).any()
            else "Viridis",
            range_color=(
                np.unique(gdf["color"])[1] * 0.99,
                np.max(gdf["color"]),
            )
            if (gdf.color == -10000).any()
            else None,
            color_discrete_sequence=colors,
        )
        fig.update_geos(
            fitbounds="locations",
            visible=False,
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig

    return wrapped


def __getattr__(name: str) -> Any:
    px_name = getattr(px, name)
    return capture(px_name)
