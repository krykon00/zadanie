"""Streamlit main app file"""
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Zadanie - Analiza gier Steam",
    layout="wide",
    initial_sidebar_state="expanded",
)

df: pd.DataFrame = pd.read_csv("steam.csv", sep=';')
df_steam_media: pd.DataFrame = pd.read_csv("steam_media_data.csv", sep=';')
genres: list[str] = list(pd.read_csv("genres.csv")["genres"])
categories: list[str] = list(pd.read_csv("categories.csv")["categories"])
popularity: list[str] = list(df["owners"].unique())

with st.sidebar:
    st.image("https://icons.iconarchive.com/icons/icons8/windows-8/48/Logos-Steam-icon.png")
    st.divider()
    st.header("Filters:")
    options_genres = st.multiselect(label="Rodzaj", options=genres, placeholder="Wybierz rodzaje gry")
    options_categories = st.multiselect(label="Kategorie", options=categories, placeholder="Wybierz kategorię gier")
    options_popularity = st.multiselect(label="Poularność", options=popularity, placeholder="Wybierz przedizał popularności")
    
if options_genres:
    genres = options_genres
if options_categories:
    categories = options_categories
if options_popularity:
    popularity = options_popularity
    
filtered_df: pd.DataFrame = df[
            (df["owners"].isin(popularity)) 
            & (df["genres"].str.contains('|'.join(genres)))
            & (df["categories"].str.contains('|'.join(categories)))
        ].reset_index()


# Charsts calculations
charts_df: pd.DataFrame = filtered_df[["name", "positive_ratings", "negative_ratings"]].groupby(by="name", as_index=False).sum()
charts_df["diff"] = charts_df["positive_ratings"] - charts_df["negative_ratings"]

with st.container(): # Main body container
    with st.expander(label="Sterowanie wizualizacjami"):
            top_n_rows: int = st.slider(label="Ilość top gier", min_value=1, value=10, step=1)
            charts_top_df = charts_df[:top_n_rows]
    with st.container():
        col_chart_pos_neg, col_chart_diff = st.columns([2, 1], gap="small")
        with col_chart_pos_neg:
            charts_top_df = charts_top_df.sort_values(by="positive_ratings")
            print(charts_top_df)
            st.bar_chart(data=charts_top_df, x="name", y=("positive_ratings", "negative_ratings"), color=("#A7C957", "#BC4749"))
        with col_chart_diff:
            charts_top_df.sort_values(by="diff")
            st.bar_chart(data=charts_top_df, x="name", y="diff", color=["#0A9396"])
    with st.container(): # DF and image container
        col_df, col_game_img = st.columns([2, 1], gap="medium")
        with col_df:
            st.dataframe(
                    filtered_df[
                        ["name", "release_date", "developer", "publisher", "owners"]
                        ][:top_n_rows], 
                    use_container_width=True
            )
        with col_game_img:
            try:
                appid: str = filtered_df.at[0, "appid"]
                header_img_url: str = df_steam_media[df_steam_media["steam_appid"] == appid].reset_index().at[0, "header_image"]
            except:
                header_img_url = "https://cdn-icons-png.flaticon.com/512/16/16096.png"
            st.image(header_img_url)

