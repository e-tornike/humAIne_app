import sys
sys.path.append(".")
import os
import json
import copy
import pathlib
import requests
import numpy as np
import pandas as pd
import gensim.downloader as api
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA

import streamlit as st
import plotly.express as px

from src.models import get_3D_coordinates
from src.debias_Lauscher2020 import debias_model
from src.metrics import get_terms, get_metric


# MODEL_PATH = "glove-twitter-25"
MODEL_PATH = "w2b_bitlevel2_size400_vocab400K"

@st.cache(allow_output_mutation=True)
def load_models():
    # model = api.load(MODEL_PATH)
    model = KeyedVectors.load_word2vec_format(MODEL_PATH, binary=False, limit=50000)
    model_deb = copy.deepcopy(model)
    model_deb.init_sims(replace=True)
    return {"GloVe": model, "GloVe debiased": model_deb}

headers_1 = {'accept': 'application/json'}
headers_2 = {'accept': 'application/json', 'Content-Type': 'application/json'}

st.title("Visualizer")

st.sidebar.title("Parameters")
st.sidebar.title("Choose Model")

model_choice = st.sidebar.selectbox("Choose a model:", ['GloVe'])

LOOKUP = load_models()  # load models

model = LOOKUP[model_choice]

# =====================================================================
st.sidebar.title("Visualize in 3D")
# Visualize 3D 
hosp_list = st.sidebar.selectbox("1. Select term list with a property", ['female_terms', 'male_terms', 'female_names', 'male_names', 'young_people_names', 'old_people_names', 'european_american_names_5', 'african_american_names_5'])
terms_1 = get_terms(hosp_list)
text_1 = st.sidebar.text_input("Terms 1", ", ".join(terms_1))
viz_terms_1 = text_1.split(", ")

hosp_list = st.sidebar.selectbox("2. Select term list with a different property", ['male_terms', 'female_terms', 'male_names', 'female_names', 'young_people_names', 'old_people_names', 'european_american_names_5', 'african_american_names_5'])
terms_2 = get_terms(hosp_list)
text_2 = st.sidebar.text_input("Terms 2", ", ".join(terms_2))
viz_terms_2 = text_2.split(", ")

hosp_list = st.sidebar.selectbox("3. Select term list for neutral words", ['family', 'career', 'math', 'arts', 'science', 'pleasant', 'unpleasant', 'instruments', 'weapons', 'mental_disease', 'physical_disease', 'professions_Bommasani'])
terms_3 = get_terms(hosp_list)
text_3 = st.sidebar.text_input("Terms 3", ", ".join(terms_3))
viz_neutral_terms = text_3.split(", ")

terms = [viz_terms_1, viz_terms_2, viz_neutral_terms]

button_viz = st.sidebar.button("Visualize")

if button_viz:
    coordinates = get_3D_coordinates(model, terms)

    st.markdown("GloVe Model")
    st.markdown("Word embeddings are vectors of numbers that are used to represent words. GloVe (Grave et al., 2018) word embeddings were trained on the text on Common Crawl and Wikipedia, which contain many millions of websites. The model learns vectors for words, which are called word embeddings, by prediction a word according to its context. For example, when looking at a sequence of 5 words, the middle word in the sequence is predicted taking the surrounding words into account.")

    _t1_coords = [coordinates[t] for t in viz_terms_1]
    _t2_coords = [coordinates[t] for t in viz_terms_2]
    _t3_coords = [coordinates[t] for t in viz_neutral_terms]

    col1 = viz_terms_1+viz_terms_2+viz_neutral_terms
    col2 = ["1"]*len(viz_terms_1)+["2"]*len(viz_terms_2)+["3"]*len(viz_neutral_terms)
    x,y,z = [], [], []
    for term, (_x,_y,_z) in zip(viz_terms_1+viz_terms_2+viz_neutral_terms, _t1_coords+_t2_coords+_t3_coords):
        x.append(_x)
        y.append(_y)
        z.append(_z)

    df = pd.DataFrame.from_dict({"x": x, "y": y, "z": z, "text": col1,"type": col2})

    fig = px.scatter_3d(df, x='x', y='y', z='z', color='type', text='text', width=800, height=800, hover_name='text', hover_data={'x':False, 'y':False, 'z':False, 'text':False, 'type':False})
    fig.update_layout(
        scene=dict(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False),
        ),
        showlegend=False
    )
    fig.update_traces(marker=dict(size=5), hoverinfo='skip')
    st.plotly_chart(fig)

# =====================================================================
st.sidebar.title("Debias Model")
deb_choice = st.sidebar.selectbox("Choose a debiasing method:", ['GBDD'])
# Debiasing method
hosp_list = st.sidebar.selectbox("4. Select term list with a property", ['family', 'career', 'math', 'arts', 'science', 'pleasant', 'unpleasant', 'instruments', 'weapons', 'mental_disease', 'physical_disease', 'professions_Bommasani'])
terms_4 = get_terms(hosp_list)
text_4 = st.sidebar.text_input("Terms 4", ", ".join(terms_4))
deb_terms_1 = text_4.split(", ")

hosp_list = st.sidebar.selectbox("5. Select term list with a different property", ['career', 'family', 'math', 'arts', 'science', 'pleasant', 'unpleasant', 'instruments', 'weapons', 'mental_disease', 'physical_disease', 'professions_Bommasani'])
terms_5 = get_terms(hosp_list)
text_5 = st.sidebar.text_input("Terms 5", ", ".join(terms_5))
deb_terms_2 = text_5.split(", ")

button_deb = st.sidebar.button("Run debiasing")

if button_deb:
    LOOKUP["GloVe debiased"] = debias_model(LOOKUP["GloVe debiased"], deb_choice, deb_terms_1, deb_terms_2)
    model = LOOKUP["GloVe debiased"]
    coordinates = get_3D_coordinates(model, terms)

    st.markdown("GBDD Debiasing")
    st.markdown("The Generalized Bias-Direction Debiasing (GBDD) model by Lauscher et al. (2020), removes a bias from word embeddings. To do this, pairs of opposing terms are created from two lists of terms, each with a property that the other does not have. For example, female and male terms like “mother” and “father”. The bias embedding can be found by collecting all differences between all pairs and applying a mathematical operation to remove it.")
    
    _t1_coords = [coordinates[t] for t in viz_terms_1]
    _t2_coords = [coordinates[t] for t in viz_terms_2]
    _t3_coords = [coordinates[t] for t in viz_neutral_terms]

    col1 = viz_terms_1+viz_terms_2+viz_neutral_terms
    col2 = ["1"]*len(viz_terms_1)+["2"]*len(viz_terms_2)+["3"]*len(viz_neutral_terms)
    x,y,z = [], [], []
    for term, (_x,_y,_z) in zip(viz_terms_1+viz_terms_2+viz_neutral_terms, _t1_coords+_t2_coords+_t3_coords):
        x.append(_x)
        y.append(_y)
        z.append(_z)

    df = pd.DataFrame.from_dict({"x": x, "y": y, "z": z, "text": col1,"type": col2})

    fig = px.scatter_3d(df, x='x', y='y', z='z', color='type', text='text', width=800, height=800, hover_name='text', hover_data={'x':False, 'y':False, 'z':False, 'text':False, 'type':False})
    fig.update_layout(
        scene=dict(
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False),
        ),
        showlegend=False
    )
    fig.update_traces(
        hoverinfo='skip'
        )
    fig.update_traces(marker=dict(size=5))
    st.plotly_chart(fig)

# =====================================================================
st.sidebar.title("Evaluate on Metric")
metric_choice = st.sidebar.selectbox("Choose an evalaution metric:", ['WEAT'])
# Metric lists
hosp_list = st.sidebar.selectbox("6. Select term list with a property", ['female_terms', 'male_terms', 'female_names', 'male_names', 'young_people_names', 'old_people_names', 'european_american_names_5', 'african_american_names_5'])
terms_6 = get_terms(hosp_list)
text_6 = st.sidebar.text_input("Terms 6", ", ".join(terms_6))
metric_terms_1 = text_6.split(", ")

hosp_list = st.sidebar.selectbox("7. Select term list with a different property", ['male_terms', 'female_terms', 'male_names', 'female_names', 'young_people_names', 'old_people_names', 'european_american_names_5', 'african_american_names_5'])
terms_7 = get_terms(hosp_list)
text_7 = st.sidebar.text_input("Terms 7", ", ".join(terms_7))
metric_terms_2 = text_7.split(", ")

hosp_list = st.sidebar.selectbox("8. Select attribute list with a property", ['family', 'career', 'math', 'arts', 'science', 'pleasant', 'unpleasant', 'instruments', 'weapons', 'mental_disease', 'physical_disease', 'professions_Bommasani'])
terms_8 = get_terms(hosp_list)
text_8 = st.sidebar.text_input("Terms 8", ", ".join(terms_8))
metric_attr_1 = text_8.split(", ")

hosp_list = st.sidebar.selectbox("9. Select attribute list with a different property", ['career', 'family', 'math', 'arts', 'science', 'pleasant', 'unpleasant', 'instruments', 'weapons', 'mental_disease', 'physical_disease', 'professions_Bommasani'])
terms_9 = get_terms(hosp_list)
text_9 = st.sidebar.text_input("Terms 9", ", ".join(terms_9))
metric_attr_2 = text_9.split(", ")

button_metric = st.sidebar.button("Run metric")

data_3 = {"property_terms_1": metric_terms_1, "property_terms_2": metric_terms_2, "attribute_terms_1": metric_attr_1, "attribute_terms_1": metric_attr_2}

if button_metric:
    result = get_metric(metric_choice, model, metric_terms_1, metric_terms_2, metric_attr_1, metric_attr_2)

    st.markdown("WEAT Metric")
    st.markdown("The Word Embedding Association Test (WEAT) (Caliskan et al., 2017) calculates a score that measures how much bias a word embedding contains based on the words used to evaluate it. The choice of words thus affects the outcome. The metric requires two sets of target and attribute terms.")
    
    st.markdown(f"WEAT score: {str(result)}")
    

