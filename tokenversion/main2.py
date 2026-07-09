"""
Simple FastAPI REST Backend
============================
FastAPI is a modern Python web framework for building APIs quickly.
It automatically generates interactive docs at http://127.0.0.1:8000/docs

Run with:
    uvicorn main:app --reload

Then set Postman baseUrl environment variable to: http://127.0.0.1:8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI() creates the application instance - this is the core of your API
app = FastAPI(title="Posts API", description="A simple posts API for testing with Postman")

# Pydantic model defines the shape/validation of incoming request data
class Post(BaseModel):
    title: str
    body: str
    userId: int

# In-memory storage seeded with 20 posts matching JSONPlaceholder structure
posts: dict = {
    1:  {"userId": 1, "id": 1,  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit", "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"},
    2:  {"userId": 1, "id": 2,  "title": "qui est esse", "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"},
    3:  {"userId": 1, "id": 3,  "title": "ea molestias quasi exercitationem repellat qui ipsa sit aut", "body": "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"},
    4:  {"userId": 1, "id": 4,  "title": "eum et est occaecati", "body": "ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"},
    5:  {"userId": 1, "id": 5,  "title": "nesciunt quas odio", "body": "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"},
    6:  {"userId": 1, "id": 6,  "title": "dolorem eum magni eos aperiam quia", "body": "ut aspernatur corporis harum nihil quis provident sequi\nmollitia nobis aliquid molestiae\nperspiciatis et ea nemo ab reprehenderit accusantium quas\nvoluptate dolores velit et doloremque molestiae"},
    7:  {"userId": 1, "id": 7,  "title": "magnam facilis autem", "body": "dolore placeat quibusdam ea quo vitae\nmagni quis enim qui quis quo nemo aut saepe\nquidem repellat excepturi ut quia\nsunt ut sequi eos ea sed quas"},
    8:  {"userId": 1, "id": 8,  "title": "dolorem dolore est ipsam", "body": "dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"},
    9:  {"userId": 1, "id": 9,  "title": "nesciunt iure omnis dolorem tempora et accusantium", "body": "consectetur animi nesciunt iure dolore\nenim quia ad\nveniam autem ut quam aut nobis\net est aut quod aut provident voluptas autem voluptas"},
    10: {"userId": 1, "id": 10, "title": "optio molestias id quia eum", "body": "quo et expedita modi cum officia vel magni\ndoloribus qui repudiandae\nvero nisi sit\nquos veniam quod sed accusamus veritatis error"},
    11: {"userId": 2, "id": 11, "title": "et ea vero quia laudantium autem", "body": "delectus reiciendis molestiae occaecati non minima eveniet qui voluptatibus\naccusamus in eum beatae sit\nvel qui neque voluptates ut commodi qui incidunt\nut animi commodi"},
    12: {"userId": 2, "id": 12, "title": "in quibusdam tempore odit est dolorem", "body": "itaque id aut magnam\npraesentium quia et ea odit et ea voluptas et\nsapiente quia nihil amet occaecati quia id voluptatem\nincidunt ea est distinctio odio"},
    13: {"userId": 2, "id": 13, "title": "dolorum ut in voluptas mollitia et saepe quo animi", "body": "aut dicta possimus sint mollitia voluptas commodi quo doloremque\niste corrupti reiciendis voluptatem eius rerum\nsit cumque quod eligendi laborum minima\nperferendis recusandae assumenda consectetur porro architecto ipsum ipsam"},
    14: {"userId": 2, "id": 14, "title": "voluptatem eligendi optio", "body": "fuga et accusamus dolorum perferendis illo voluptas\nnon doloremque neque facere\nad qui dolorum molestiae beatae\nsed aut voluptas totam sit illum"},
    15: {"userId": 2, "id": 15, "title": "eveniet quod temporibus", "body": "reprehenderit quos placeat\nvelit minima officia dolores impedit repudiandae molestiae nam\nvoluptas recusandae quis delectus\nofficiis harum fugiat vitae"},
    16: {"userId": 2, "id": 16, "title": "sint suscipit perspiciatis velit dolorum rerum ipsa laboriosam odio", "body": "suscipit nam nisi quo aperiam aut\nasperiores eos fugit maiores voluptatibus quia\nvoluptatem quis ullam qui in alias quia est\nconsequatur magni mollitia accusamus ea nisi voluptate dicta"},
    17: {"userId": 2, "id": 17, "title": "fugit voluptas sed molestias voluptatem provident", "body": "eos voluptas et aut odit natus earum\naspernatur fuga molestiae ullam\ndeserunt ratione qui eos\nqui nihil ratione nemo velit ut aut id quo"},
    18: {"userId": 2, "id": 18, "title": "voluptate et itaque vero tempora molestiae", "body": "eveniet quo quis\nlaborum totam consequatur non dolor\nut et est repudiandae\nest voluptatem vel debitis et magnam"},
    19: {"userId": 2, "id": 19, "title": "adipisci placeat illum aut reiciendis qui", "body": "illum quis cupiditate provident sit magnam\nea sed aut omnis\nveniam maiores ullam consequatur atque\nadipisci quo iste expedita sit quos voluptas"},
    20: {"userId": 2, "id": 20, "title": "doloribus ad provident suscipit at", "body": "qui consequuntur ducimus possimus quisquam amet similique\nsuscipit porro ipsam amet\neos veritatis officiis exercitationem vel fugit aut necessitatibus totam\nomnis rerum consequatur expedita quidem cumque explicabo"},
}
next_id = 21  # tracks the next available ID for new posts


# GET /posts/{post_id} - retrieves a single post by its ID
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in posts:
        # HTTPException sends a proper HTTP error response back to the client
        raise HTTPException(status_code=404, detail="Post not found")
    return posts[post_id]


# POST /posts - creates a new post and returns it with a generated ID
@app.post("/posts", status_code=201)
def create_post(post: Post):
    global next_id
    new_post = {"id": next_id, **post.model_dump()}
    posts[next_id] = new_post
    next_id += 1
    return new_post


# PUT /posts/{post_id} - replaces an existing post entirely with new data
@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    posts[post_id] = {"id": post_id, **post.model_dump()}
    return posts[post_id]


# DELETE /posts/{post_id} - removes a post and returns an empty response
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[post_id]
    return {}
