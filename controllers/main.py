from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Required
from typing import Union, List
from enum import Enum

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {
        "Hello": "World"
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {
        "item_id": item_id,
        "q": q
    }


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_name": item.name,
        "item_price": item.price,
        "item_id": item_id
    }


@app.get("/users/me")
async def read_user_me():
    return {
        "user_id": "the current user"
    }


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {
        "user_id": user_id
    }


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    print(model_name)
    if model_name is ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }

    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }

    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {
        "file_path": file_path
    }


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get("/items2/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {
        "item_id": item_id,
        "owner_id": user_id
    }
    if q:
        item.update({"q": q})

    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item


@app.get("/items3/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None):
    item = {
        "item_id": item_id,
        "needy": needy,
        "skip": skip,
        "limit": limit
    }
    return item


class Item2(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/items/")
async def creat_item(item: Item2):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items4/{item_id}")
async def create_item(item_id: int, item: Item2, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items5/")
async def read_items(q: Union[str, None] = Query(
    default=None, min_length=3, max_length=50, regex="^fixedquery$"
)):
    results = {
        "items": [
            {"item_id": "Foo"},
            {"item_id": "Bar"}
        ]
    }
    if q:
        results.update({"q": q})
    return results


@app.get("/items6/")
async def read_items(q: str = Query(min_length=3)):
    results = {"items": [
        {"item_id": "Foo"},
        {"item_id": "Bar"}
    ]}
    if q:
        results.update({"q": q})
    return results


# ... => el parámetro es requerido
@app.get("/items7/")
async def read_items(q: str = Query(default=..., min_length=3)):
    results = {"items": [
        {"item_id": "Foo"},
        {"item_id": "Bar"}
    ]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items8/")
async def read_items(q: str = Query(default=Required, min_length=3)):
    results = {"items": [
        {"item_id": "Foo"},
        {"item_id": "Bar"}
    ]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items9/")
async def read_items_list(q: Union[List[str], None] = Query(default=None)):
    query_items = {"q": q}
    return query_items


@app.get("/items10/")
async def read_items_list(q: Union[List[str], None] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items


@app.get("/items11/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3
    )
):
    results = {"items": [
        {"item_id": "Foo"},
        {"item_id": "Bar"}
    ]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items12/")
async def read_items(q: Union[str, None] = Query(default=None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items13/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [
        {"item_id": "Foo"},
        {"item_id": "Bar"}
    ]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items14/")
async def read_items(
    hidden_query: Union[str, None] = Query(default=None, include_in_schema=False)
):
    if hidden_query:
        return {
            "hidden_query": hidden_query
        }
    else:
        return {
            "hidden_query": "Not found"
        }


@app.get("/items15/{item_id}")
async def read_items(
        item_id: int = Path(title="The ID of the item to get"),
        q: Union[str, None] = Query(default=None, alias="item-query")
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items16/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items17/{item_id}")
async def read_items(
    *, item_id: int = Path(title="The ID of the item to get", ge=1), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items18/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items19/{item_id}")
async def read_items(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5)
):
    results = {
        "item_id": item_id,
        "q": q,
        "size": size
    }
    return results
