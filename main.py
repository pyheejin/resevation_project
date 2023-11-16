import uvicorn

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
from starlette.routing import Mount
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from config.jwt_handler import JWT
from router import admin_api, api, webpage


api_tags_metadata = [
    {
        'name': 'user',
        'description': '유저'
    },
]

admin_api_tags_metadata = [
    {
        'name': 'product',
        'description': '상품'
    },
]


def create_app():
    """
    앱 함수 실행
    :return:
    """
    # 앱 api
    app = FastAPI(title='App API',
                  docs_url='/_docs',
                  openapi_tags=api_tags_metadata)
    app.include_router(api.routers)

    # 어드민 api
    admin = FastAPI(title='Admin API',
                    docs_url='/_docs',
                    openapi_tags=admin_api_tags_metadata)
    admin.include_router(admin_api.routers)

    # 웹 페이지
    web_page = FastAPI(title='Web API',
                       docs_url='/_docs')
    web_page.include_router(webpage.routers)


    app = Starlette(routes=[
        Mount('/api/v1', app),
        Mount('/admin/api/v1', admin),
        Mount('', web_page),
    ])
    return app


app = create_app()


origins = [
    'http://localhost:3000',
    'http://127.0.0.1:7000',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.middleware('http')
async def app_middleware(request: Request, call_next):
    response = await call_next(request)

    token = request.headers.get('Authorization', None)
    if token is not None:
        jwt_data = JWT()
        try:
            jwt_data.verify_token(token.split(' ')[1])
        except HTTPException as e:
            result = {
                'result_code': e.detail,
                'result_msg': e.status_code,
                'result_data': None,
            }
            response = JSONResponse(status_code=e.status_code, content=result)
    return response


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=7000, reload=True)