# vector_search_demo

This repository was created as an introductory to vector search in real-time using OpenAI for vector embedding and Rockset as a real-time engine. Below is a step-by-step guide on how to get started! You will need to create an account on both OpenAI and Rockset to get an API key for both platforms. Thankfully, API keys are available on the free versions. To create an account on OpenAI go (here)[https://platform.openai.com/signup?] and to create an account on Rockset go (here)[https://rockset.com/create/].

This Vector Search demo will cover 3 examples:
1. Vector Search over IMDb movie titles & descriptions using keywords as the search query
2. Vector Search over IMDb movie titles & descriptions using keywords as the search query & applying metadata filtering
3. Generating movie recomendations using a watchlist of previously watched movies and Vector Search

## Data Collection
The unembedded dataset can be found on (Kaggle)[https://www.kaggle.com/datasets/rajugc/imdb-movies-dataset-based-on-genre?select=action.csv].
The embedded dataset can be found on (AWS S3)[s3://rockset-community-datasets/public/imdb-movies/]

## Step 1: Embed Vectors
*This step can be skipped if you download the embedded dataset on AWS S3. Below are the steps I took to embed the vectors in case you would like to replicate it for your own dataset.*

First the dataset needs to be extracted into smaller subsets. Refer to `extract_subsets.py`



https://rockset.com/blog/introducing-vector-search-on-rockset/
https://rockset.com/blog/5-use-cases-for-vector-search/
https://rockset.com/videos/how-to-build-real-time-machine-learning-at-scale/
