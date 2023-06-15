import openai
from rockset import RocksetClient

### EDIT BELOW
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
ROCKSET_API_KEY = 'YOUR_ROCKSET_API_KEY'
host_url = 'https://api.usw2a1.rockset.com' # use the Base URL associated with your region found here: https://rockset.com/docs/rest-api/

search_query = "medieval, knights, castles, dragons"
### STOP

# set openai api key
openai.api_key = OPENAI_API_KEY

# initialize RocksetClient
rs = RocksetClient(api_key=ROCKSET_API_KEY, host=host_url)

# embed search query
search_query_embedding = openai.Embedding.create(input=search_query, model="text-embedding-ada-002")["data"][0]["embedding"]  

# convert list to string
embedding_str = ",".join([str(num) for num in search_query_embedding])

# vector search on Rockset (can remove WHERE clause to search over entire dataset)
response = rs.sql(query="SELECT movie_name FROM movies.imdb_movies \
                        WHERE ARRAY_CONTAINS(genre, 'History') \
                        ORDER BY COSINE_SIM(embedding,["+embedding_str+"]) desc LIMIT 5")

# print results
print()
[print(movie['movie_name']) for movie in response.results]
print()
