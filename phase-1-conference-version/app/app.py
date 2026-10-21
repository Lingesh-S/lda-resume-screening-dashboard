"""Resume screening dashboard (ICCCAI 2024 version).

Ranks resumes against a selected job description, then clusters the resumes
into topics with LDA. Run from anywhere:

    streamlit run phase-1-conference-version/app/app.py
"""

import sys
from pathlib import Path

import gensim
import gensim.corpora as corpora
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from wordcloud import WordCloud

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
sys.path.insert(0, str(BASE_DIR / "core"))

import Similar  # noqa: E402

NUM_TOPICS = 6


@st.cache_data
def load_data():
    resumes = pd.read_csv(DATA_DIR / "Resume_Data.csv")
    jobs = pd.read_csv(DATA_DIR / "Job_Data.csv")
    return resumes, jobs


@st.cache_data
def calculate_scores(resume_tokens: tuple, job_tokens: str) -> list:
    """Score every resume against one job description (cached per job)."""
    return [Similar.match(resume, job_tokens) for resume in resume_tokens]


@st.cache_resource
def train_lda(cleaned_documents: tuple):
    """Train the LDA model once per dataset instead of on every widget change."""
    documents = [str(doc).split(" ") for doc in cleaned_documents]
    id2word = corpora.Dictionary(documents)
    corpus = [id2word.doc2bow(text) for text in documents]
    model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=NUM_TOPICS,
        random_state=100,
        update_every=3,
        chunksize=100,
        passes=50,
        alpha="auto",
        per_word_topics=True,
    )
    return model, corpus


def format_topics_sentences(ldamodel, corpus):
    """Return [doc index, dominant topic, % contribution, topic keywords] per document."""
    rows = []
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list
        row = sorted(row, key=lambda x: x[1], reverse=True)
        if not row:
            continue
        topic_num, prop_topic = row[0]
        keywords = ", ".join(word for word, _ in ldamodel.show_topic(topic_num))
        rows.append([i, int(topic_num), round(prop_topic, 4) * 100, keywords])
    return rows


st.image(Image.open(BASE_DIR / "Images" / "logo.png"), width="stretch")
st.title("Resume Screening")

Resumes, Jobs = load_data()

# ----------------------------- Job description -----------------------------
if len(Jobs) <= 1:
    st.write("There is only 1 Job Description present. It will be used to create scores.")
else:
    st.write("There are ", len(Jobs), "Job Descriptions available. Please select one.")

if len(Jobs) > 1:
    show_names = st.selectbox("Show the Job Description names?", options=["YES", "NO"])
    if show_names == "YES":
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(values=["Job No.", "Job Desc. Name"], line_color="darkslategray", fill_color="lightskyblue"),
                    cells=dict(values=[list(range(len(Jobs))), Jobs["Name"]], line_color="darkslategray", fill_color="black"),
                )
            ]
        )
        fig.update_layout(width=700, height=400)
        st.write(fig)

jd_index = st.slider("Slide to select the JD:", 0, max(len(Jobs) - 1, 0), min(1, len(Jobs) - 1))

if st.selectbox("Do you want the Job Description to be displayed?", options=["YES", "NO"]) == "YES":
    st.markdown("---")
    st.markdown("### Job Description:")
    st.write(Jobs["Context"][jd_index])
    st.markdown("---")

# ------------------------------- Scoring -----------------------------------
Resumes["Scores"] = calculate_scores(tuple(Resumes["TF_Based"].fillna("")), str(Jobs["TF_Based"][jd_index]))
Ranked_resumes = Resumes.sort_values(by=["Scores"], ascending=False).reset_index(drop=True)
Ranked_resumes["Rank"] = range(1, len(Ranked_resumes) + 1)

st.dataframe(Ranked_resumes[["Rank", "Name", "Scores"]], hide_index=True)
st.markdown("---")

fig2 = px.bar(
    Ranked_resumes,
    x="Name",
    y="Scores",
    color="Scores",
    color_continuous_scale="haline",
    title="Score and Rank Distribution",
)
st.write(fig2)
st.markdown("---")

# ------------------------------ LDA topics ---------------------------------
lda_model, corpus = train_lda(tuple(Resumes["Cleaned"].fillna("")))

st.markdown("## Topics and Topic Related Keywords")
st.markdown(
    "This word cloud shows each topic number and the top keywords that make it up. "
    "The topics are then used to cluster the resumes."
)

cols = list(mcolors.TABLEAU_COLORS.values())
topics = lda_model.show_topics(num_topics=NUM_TOPICS, formatted=False)

fig, axes = plt.subplots(2, 3, figsize=(10, 10), sharex=True, sharey=True)
for i, ax in enumerate(axes.flatten()):
    if i >= len(topics):
        ax.axis("off")
        continue
    cloud = WordCloud(
        background_color="white",
        width=2500,
        height=1800,
        max_words=10,
        collocations=False,
        color_func=lambda *args, _c=cols[i % len(cols)], **kwargs: _c,  # noqa: B008
        prefer_horizontal=1.0,
    )
    cloud.generate_from_frequencies(dict(topics[i][1]), max_font_size=300)
    ax.imshow(cloud)
    ax.set_title(f"Topic {i}", fontdict=dict(size=16))
    ax.axis("off")
plt.subplots_adjust(wspace=0, hspace=0)
plt.tight_layout()
st.pyplot(fig)
st.markdown("---")

df = pd.DataFrame(
    format_topics_sentences(lda_model, corpus),
    columns=["Document No", "Dominant Topic", "Topic % Contribution", "Keywords"],
)
df["Names"] = Resumes["Name"].iloc[df["Document No"]].values

st.markdown("## Topic Modeling with Resume using LDA")
st.markdown("LDA groups the resumes into topics, creating clusters of resumes that share a topic.")
fig3 = px.sunburst(
    df,
    path=["Dominant Topic", "Names"],
    values="Topic % Contribution",
    color="Dominant Topic",
    color_continuous_scale="viridis",
    width=800,
    height=800,
    title="Topic Distribution Graph",
)
st.write(fig3)

# ----------------------------- Resume viewer -------------------------------
if st.selectbox("Do you want to see the Best Resumes?", options=["YES", "NO"]) == "YES":
    rank = st.slider("Which resume to display?", 1, Ranked_resumes.shape[0], 1)
    row = Ranked_resumes.iloc[rank - 1]

    st.write("Displaying Resume with Rank: ", rank)
    st.markdown("---")
    st.markdown("## **Resume**")
    st.markdown("#### The Word Cloud For Resume")
    resume_cloud = WordCloud(
        width=800, height=800, background_color="black", colormap="viridis", collocations=False, min_font_size=10
    ).generate(str(row["Cleaned"]))
    cloud_fig = plt.figure(figsize=(7, 7))
    plt.imshow(resume_cloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(cloud_fig)

    st.write("With a Match Score of:", round(float(row["Scores"]), 2))
    st.write(str(row["Context"]))
    st.markdown("---")
