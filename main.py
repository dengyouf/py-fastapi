from typing import Union, List, Annotated

from fastapi import FastAPI, Path, Query, Body, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import HTMLResponse

app = FastAPI()

# /static/favicon.png
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get("/goods/{item}/{id}", tags=["Path路由参数"], summary="路由参数接口", description="路由参数接口详情")
def test(item:str=Path(description="商品名称"), id:Union[int, None]=Path(description="商品ID，最小为3， 最大为100", ge=3, le=100)):
    return {'status': 200, 'msg': 'success', 'data': {'id': id, 'item': item}}


@app.get("/q_params/", tags=["Query请求参数"], summary="请求参数", description="请求参数接口详情", response_description="响应数据详情" )
def test2(pnum:int|None=Query(default=0, description="当前页"), psize:int|None=Query(default=0, description="每页条数")):
    return {'status': 200, 'msg': 'success', 'data': {'pnum': pnum, 'psize': psize}}

@app.get("/q_str", tags=["字符串长度校验"], summary="字符串长度校验")
def q_str(username: Union[str, None]=Query(description="用户名", min_length=3, max_length=8)):
    return {'status': 200, 'msg': 'success', 'data': {'username': username}}

@app.get('/re_str', tags=["正则表达式校验"], summary="正则表达式校验")
def re_str(q: Union[str, None]=Query(description="查询参数", regex="^[a-zA-Z]")):
    return {'status': 200, 'msg': 'success', 'data': {'q': q}}

# http://127.0.0.1:8005/m_val?ids=1&ids=2&ids=3
@app.get("/m_val", tags=["请求多值"], summary="请求多值")
def m_val(ids:Union[List[int], None]=Query(default=None, description="多个IDs参数")):
    if not ids:
        return {'status': 200, 'msg': 'success', 'data': 'ids is null'}
    return {'status': 200, 'msg': 'success', 'data': {'ids': ids}}

class UserInfo(BaseModel):
    name: str
    desc: str | None=None
    age: int |None=0
    sex: str| None = "M"
@app.post("/userinfo", tags=["请求体参数"], summary="请求体参数")
def user_info(userinfo: UserInfo):
    return  {'status': 200, "msg": "success", "data": userinfo}

@app.post("/form_data", tags=["Form数据"], summary="Form数据")
def form_data(username: str=Form(), password: str=Form(), image: Union[UploadFile, None]=Form()):
    try:
        if image.filename.strip():
            load_path = f"uploads/{image.filename}"
            with open(load_path, 'wb+') as f:
                f.write(image.file.read())
            print("图片上传成功")
    except Exception as e:
        print(f"图片上传失败:{e}")
    return {"status": 200, 'msg': "success", 'data': {'username': username, "password": password}}

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
@app.get("/tmpl/{msg}", tags=["返回模板"], response_class=HTMLResponse, summary="返回模板")
def tmpl_view(request:Request, msg:Union[str, None]=Path(description="路由参数msg")):
    return templates.TemplateResponse("tmpl.html", {"request": request, "msg": msg})

# uvicorn.exe main:app --reload

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True, workers=2)
    uvicorn.run(app, port=8005)
