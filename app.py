# -*- coding: utf-8 -*-
"""
    Fun Survey Dashboard
    ~~~~~~

"""

import os
from flask import Flask, request, g, redirect, url_for, render_template, flash
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)



# survey data url
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkK73xD192AdP0jZe6ac9cnVPSeqqbYZmSPnhY2hnY8ANROAOCStRFdvjwFoapv3j2rzMtZ91KXPFm/pub?output=csv"

renamelist = ['Timestamp', 'Musicartist', 'height', 'city', 'thirtymin', 'travel', \
              'likepizza', 'deepdish', 'sport', 'spell', 'hangout', 'talk', \
              'year', 'quote', 'areacode', 'pets', 'superpower', 'shoes']

# create data frame from url
df = pd.read_csv(url)

# assign original headers to list
survey_questions = df.columns.to_list()

# replace with column names easier to work with
df.columns = renamelist

# drop duplicates
df = df.drop_duplicates(subset=df.columns[1:])
df.Timestamp = pd.to_datetime(df.Timestamp)

label_dict = {}
for i in range(len(renamelist)):
    label_dict[renamelist[i]] = survey_questions[i]

@app.context_processor
def inject_vars():
    return {'label_dict': label_dict}



def render_count(col_label, horizontal=False, hist=False, big=False, width=9):
    question = col_label
    qtext = label_dict[question]
    series = df[question]

    # Generate descriptive statistics HTML
    descrip_stats = series.describe()
    descrip_df = pd.DataFrame(descrip_stats)
    descrip_df.reset_index(inplace=True)

    # Convert the DataFrame to HTML with minimal formatting, excluding the index
    custom_descrip_html = descrip_df.to_html(index=False, header=False)
    custom_descrip_html = custom_descrip_html.replace('<table border="1" class="dataframe">', '<table class="table table-striped" style="width: auto" >')



    value_counts = series.value_counts(ascending=False)
    value_counts_df = pd.DataFrame(value_counts).head(10)
    value_counts_df.reset_index(inplace=True)
    value_counts_html = value_counts_df.to_html(index=False, header=False)
    value_counts_html = value_counts_html.replace('<table border="1" class="dataframe">', '<table class="table table-striped" style="width: auto">')

    # Generate the histogram
    # plt.figure(figsize=(8, 4))  # Optional, adjust size as needed
    if big:
        top_ten = value_counts[:20]
        barchart = sns.barplot(y=top_ten.index, x=top_ten.values)
        plt.title('Top Twenty')
        plt.gcf().set_size_inches(width, 6)
        plt.xlabel('Count')
    elif horizontal:
        barchart = sns.countplot(y=series)
    elif hist:
        barchart = sns.histplot(x=series)
    else:
        barchart = sns.countplot(x=series)
    image_path = f'static/images/{question}_plot.png'
    plt.savefig(image_path)
    plt.close()

    # Pass the path of the image to the template
    return render_template('numeric.html', title=question, qtext= qtext, descrip=custom_descrip_html,
                           value_counts = value_counts_html,
                           chart_url=url_for('static', filename=f'images/{question}_plot.png'))



@app.route('/')
def home():
    df_descriptives = df.describe().to_html()
    return render_template('index.html',
                           label_dict=label_dict,
                           first=df.Timestamp.min(),
                           last =df.Timestamp.max(),
                           responses=df.shape[0])

@app.route('/Musicartist')
def Musicartist():
    return render_count('Musicartist', horizontal=False, hist=False, big=True, width=10)
@app.route('/height')
def height():
    return render_count('height', horizontal=False, hist=False, big=True)
@app.route('/city')
def city():
    return render_count('city', horizontal=False, hist=False, big=True)
@app.route('/thirtymin')
def thirtymin():
    return render_count('thirtymin', horizontal=False, hist=False, big=True, width=10)
@app.route('/travel')
def travel():
    return render_count('travel', horizontal=False, hist=False, big=True)

@app.route('/likepizza')
def likepizza():
    return render_count('likepizza', horizontal=False, hist= True)

@app.route('/deepdish')
def deepdish():
    return render_count('deepdish', horizontal=False, hist= True)

@app.route('/sport')
def sport():
    return render_count('sport', horizontal=False, hist=False, big=True, width=10)
@app.route('/spell')
def spell():
    return render_count('spell', horizontal=False, hist= True)
@app.route('/hangout')
def hangout():
    return render_count('hangout', horizontal=False, hist=False, big=True)

@app.route('/talk')
def talk():
    return render_count('talk', horizontal=False, hist= True)
@app.route('/year')
def year():
    return render_count('year', horizontal=False, hist=False, big=True)

@app.route('/quote')
def quote():
    return render_count('quote', horizontal=False, hist=False, big=True, width=15)
@app.route('/areacode')
def areacode():
    return render_count('areacode', horizontal=False, hist=False, big=True)
@app.route('/pets')
def pets():
    return render_count('pets', horizontal=False, hist=False, big=True)
@app.route('/superpower')
def superpower():
    return render_count('superpower', horizontal=False, hist=False, big=True)
@app.route('/shoes')
def shoes():
    return render_count('shoes', horizontal=False, hist=False, big=True)

