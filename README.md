# vector_search_demo

This repository was created as an introductory to vector search in real-time using OpenAI for vector embedding and Rockset as a real-time engine. Below is a step-by-step guide on how to get started! You will need to create an account on both OpenAI and Rockset to get an API key for both platforms. Thankfully, API keys are available on the free versions. To create an account on OpenAI go [here](https://platform.openai.com/signup?) and to create an account on Rockset go [here](https://rockset.com/create/).<br /><br />


## Data Collection
This Vector Search demo will showcase how to run a Vector Search query over IMDb movie titles & descriptions using keywords as the search query. The unembedded dataset can be found on [Kaggle](https://www.kaggle.com/datasets/rajugc/imdb-movies-dataset-based-on-genre?select=action.csv). The embedded dataset can be found in this public AWS S3 bucket: s3://rockset-community-datasets/public/imdb-movies/ <br /><br />

## Step 1: Embed Vectors using OpenAI's API
*This step can be skipped if you choose to use the embedded dataset on AWS S3. Below are the steps I took to embed the vectors in case you would like to replicate it for your own dataset.*

First the Kaggle dataset needs to be extracted into smaller subsets. Refer to `extract_subsets.py`

Now we can send API requests to OpenAI's embedding endpoint. Refer to `vector_embedding.py`. In this file, I create embeddings using OpenAI's second generation vector embedding model `text-embedding-ada-002`. For more information on this and other embedding models, check out OpenAI's [docs](https://platform.openai.com/docs/guides/embeddings). For the IMDb movie dataset, I embedded the `movie_name` and the `description` fields:

```
values = [row['movie_name']+' '+row['description'] for row in rows]
embeddings = [generate_embeddings(value) for value in values]
```

The vector embeddings for `text-embedding-ada-002` contain 1536 elements so expect a significant storage size increase. The embeddings are appended onto the original subset files.<br /><br />

## Step 2: Upload Data to Rockset
In order to execute a Vector Search query over the dataset, we will need a real-time database to host our collection. With a larger dataset, I recommend dropping the files in an AWS S3 bucket and then ingesting it into Rockset using these [docs](https://rockset.com/docs/amazon-s3/). If you are using the embedded dataset I shared above, you can ingest right away by following these steps:
  1. In the Rockset Console, go to the "Collections" tab and then select "Create a Collection"
  2. Select "Amazon S3" then " — public bucket — "
  3. Click "Start" then select "CSV/TSV" for File Format
  4. Enter "s3://rockset-community-datasets/public/imdb-movies/" in the S3 Path then click "Next"
  5. Do NOT use the default ingest transformation. You will need to use VECTOR_ENFORCE to ensure all the vector embeddings are the same size & type (this will ensure the data is perfectly compacted during query execution). Copy and paste the ingest transformation below:

  ```
  SELECT
    _input.movie_id as _id, -- by setting _id to the movie_id we ensure that we are not ingesting any duplicates
    _input.movie_name,
    _input.description,
    TRY_CAST(_input.year as int) as year,
    TRY_CAST(SPLIT(_input.runtime, ' ') [1] as int) as runtime, -- removing ' min' from runtime and casting as integer
    TRY_CAST(_input.rating as float) as rating,
    _input.certificate,
    TRY_CAST(_input."gross(in $)" as int) as gross_profit,
    SPLIT(_input.genre, ', ') as genre, -- ingesting genre as an array of strings instead of one string
    SPLIT(_input.director, CONCAT(', ',CHR(10))) as director, -- removing CHR(10) the newline character
    SPLIT(_input.star, CONCAT(', ',CHR(10))) as stars,
    VECTOR_ENFORCE(JSON_PARSE(_input.embedding), 1536, 'float') as embedding -- enforcing all the vectors are the same size & type
  FROM
    _input
  ```

  6. In the next page, type a workspace name and collection name. I used workspace=`movies` and collection=`imdb_movies`
  7. Final step is to click "Create" and wait for the data to bulk ingest into your Rockset collection. This will take anywhere from 5-10min with embedded IMDb dataset. The final dataset will be ~243k docs and ~8.2 GiB.<br /><br />

## Step 3: Execute a Vector Search Query using Rockset's API

Refer to `vector_search.py` for this step. This python file takes a search_query as an input, runs a vector search SQL, then prints the results. In this example, the search query is:
```
search_query = "medieval, knights, castles, dragons"
```
You can change the search query to be any movie keywords. We then embed the search query in the following lines using OpenAI again and then pass the embedded search query vector as a string `embedding_str` in the following request to the RocksetClient:

```
response = rs.sql(query="SELECT movie_name FROM movies.imdb_movies \
                        WHERE ARRAY_CONTAINS(genre, 'History') \
                        ORDER BY COSINE_SIM(embedding,["+embedding_str+"]) desc LIMIT 5")
```
In the above query we are applying a metadata filter on the genre. This will speed up our query. Perhaps this search function is set-up on the 'History movies' webpage of your site. If you want to search through the entire dataset, remove the line containing the WHERE clause. The query is ordered by a distance function (in this case that is COSINE_SIM). This calculates the distance between the search query and the movies in our dataset. We want to output the 5 movies that are the closest in distance (also known as the 5 Nearest Neighbors! The LIMIT is the 'k' in kNN also known as k-Nearest Neighbors).

Note that in the query above, I am reading from workspace `movies` and collection `imdb_movies`. Adjust according to the names you used!<br /><br />

### Want more information?
Check out this recording of a workshop I hosted on Vector Search: <br />
*coming soon*

Check out this awesome talk on vector search at scale in real-time: <br />
https://rockset.com/videos/how-to-build-real-time-machine-learning-at-scale/

Check out these cool blogs: <br />
https://rockset.com/blog/introducing-vector-search-on-rockset/ <br />
https://rockset.com/blog/5-use-cases-for-vector-search/
