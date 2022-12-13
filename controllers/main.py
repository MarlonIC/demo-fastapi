from datetime import datetime, time, timedelta

from typing import Union, List, Set, Dict
from enum import Enum
from uuid import UUID

from fastapi import FastAPI, Body, Query, Path, Cookie, Header, status
from fastapi import Form, File, UploadFile, Request
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

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


class Item3(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items20/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Union[Item3, None] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.put("/items21/{item_id}")
async def update_item(item_id: int, item: Item3, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@app.put("/items22/{item_id}")
async def update_item(item_id: int, item: Item3, user: User, importance: int = Body()):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
    return results


@app.put("/items23/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item3,
    user: User,
    importance: int = Body(gt=0),
    q: Union[str, None] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


@app.put("/items24/{item_id}")
async def update_item(item_id: int, item: Item3 = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


class Item4(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


@app.put("/items25/{item_id}")
async def update_item(item_id: int, item: Item4 = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


class Item5(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


@app.put("/items26/{item_id}")
async def update_item(item_id: int, item: Item5):
    results = {"item_id": item_id, "item": item}
    return results


class Item6(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.put("/items27/{item_id}")
async def update_item(item_id: int, item: Item6):
    results = {"item_id": item_id, "item": item}
    return results


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item7(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None


@app.put("/items28/{item_id}")
async def update_item(item_id: int, item: Item7):
    results = {"item_id": item_id, "item": item}
    return results


class Item8(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None


@app.put("/items29/{item_id}")
async def update_item(item_id: int, item: Item8):
    results = {"item_id": item_id, "item": item}
    return results


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item8]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights


class Item9(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2
            }
        }


@app.put("/items30/{item_id}")
async def update_item_30(item_id: int, item: Item9):
    results = {
        "item_id": item_id,
        "item": item
    }
    return results


class Item10(BaseModel):
    name: str = Field(example="Foo")
    description: Union[str, None] = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: Union[float, None] = Field(default=None, example=3.2)


@app.put("/items31/{item_id}")
async def update_item(item_id: int, item: Item10):
    results = {"item_id": item_id, "item": item}
    return results


class Item11(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.put("/items32/{item_id}")
async def update_item(
    item_id: int,
    item: Item11 = Body(
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items33/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item11 = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item 11",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items34/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Union[datetime, None] = Body(default=None),
    end_datetime: Union[datetime, None] = Body(default=None),
    repeat_at: Union[time, None] = Body(default=None),
    process_after: Union[timedelta, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


# Cookie
@app.get("/items35/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {
        "ads_id": ads_id
    }


# Header Parameters
@app.get("/items36/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {
        "User-Agent": user_agent
    }


@app.get("/items37/")
async def read_items(strange_header: Union[str, None] = Header(default=None, convert_underscores=False)):
    return {
        "strange_header": strange_header
    }


@app.get("/items38/")
async def read_items(x_token: Union[List[str], None] = Header(default=None)):
    return {
        "X-Token values": x_token
    }


# Response Model
class Item12(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


@app.post("/items39/", response_model=Item12)
async def create_item(item: Item12):
    return item


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


# Don't do this in production! (devolver el password en el response)
@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user1/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


class Item13(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items40/{item_id}", response_model=Item13, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


@app.get("/items41/{item_id}", response_model=Item13, response_model_exclude_defaults=True)
async def read_item(item_id: str):
    return items[item_id]


@app.get("/items42/{item_id}", response_model=Item13, response_model_exclude_none=True)
async def read_item(item_id: str):
    return items[item_id]


class Item14(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5


items2 = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get("/items43/{item_id}/name", response_model=Item14, response_model_include={"name", "description"})
async def read_item_name(item_id: str):
    return items2[item_id]


@app.get("/items44/{item_id}/public", response_model=Item14, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items2[item_id]


# Extra Models
class UserIn2(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut2(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn2):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user2/", response_model=UserOut2)
async def create_user(user_in: UserIn2):
    user_saved = fake_save_user(user_in)
    return user_saved


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn3(UserBase):
    password: str


class UserOut3(UserBase):
    pass


class UserInDB2(UserBase):
    hashed_password: str


def fake_save_user2(user_in: UserIn3):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user3/", response_model=UserOut3)
async def create_user(user_in: UserIn3):
    user_saved = fake_save_user2(user_in)
    return user_saved


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items3 = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items45/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items3[item_id]


class Item15(BaseModel):
    name: str
    description: str


items4 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items46/", response_model=List[Item15])
async def read_items():
    return items4


@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}


# Response Status Code
@app.post("/items47/", status_code=201)
async def create_item(name: str):
    return {"name": name}


@app.post("/items48/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


# Form Data
@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# Request Files
@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {
        "filename": file.filename,
        "content_type": file.content_type
    }


@app.post("/files2/")
async def create_file(file: Union[bytes, None] = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile2/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


@app.post("/files3/")
async def create_file(file: bytes = File(description="A file read as bytes")):
    return {"file_size": len(file)}


@app.post("/uploadfile3/")
async def create_upload_file(
    file: UploadFile = File(description="A file read as UploadFile"),
):
    return {"filename": file.filename}


@app.post("/files4/")
async def create_files(files: List[bytes] = File()):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles4/")
async def create_upload_files(files: List[UploadFile] = File(description="Multiple files as UploadFile")):
    return {"filenames": [file.filename for file in files]}


@app.get("/form")
async def main():
    content = """
    <body>
        <form action="/files4/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit">
        </form>
        <form action="/uploadfiles4/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit">
        </form>
    </body>
    """
    return HTMLResponse(content=content)


# Request Forms and Files
@app.post("/files5/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
