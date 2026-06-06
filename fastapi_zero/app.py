from fastapi import FastAPI
from http import HTTPStatus

app = FastAPI()


@app.get('/',status_code=HTTPStatus.OK)   
def read_root():
    return {'message': 'Hello world!'}
