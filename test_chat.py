import requests
import json

response = requests.post(
    'http://localhost:8000/chat/message/',
    json={'message': 'Tell me about prison movies'}
)

print("TEST 1: Global Chat")
print(json.dumps(response.json(), indent=2))



response2 = requests.post(
    'http://localhost:8000/chat/message/',
    json={'message': 'What is the main theme', 'movie_id': 1}
)

print("TEST 2: Movie specific chat")
print(json.dumps(response2.json(), indent=2))