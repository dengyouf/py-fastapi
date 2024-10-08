1. 安装
- pip install fastapi
- pip install "uvicorn[standard]"

2. 打开接口文档
- 在app中注册static目录
```shell
from fastapi.staticfiles import StaticFiles

app.mount('/static', StaticFiles(directory='static'), name='static')
```
- 修改fastapi源码

```shell
#文件路径Lib/site-packages/fastapi/openapi/docs.py
def get_swagger_ui_html(
  ...
    # ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    ] = "/static/swagger-ui-bundle.js",
    ...
    # ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    ] = "/static/swagger-ui.css",
    ...
    # ] = "https://fastapi.tiangolo.com/img/favicon.png",
    ] = "/static/favicon.png",
)
```

3. 启动服务
- 命令行启动
  - --reload仅用于开发调试，不推荐在生产环境中使用
```
uvicorn.exe main:app --reload
```
- 在main.py文件中启动
```shell
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True, workers=2)
```

4. 路由参数-Path
```shell
@app.get("/goods/{item}/{id}", tags=["Path路由参数"], summary="路由参数接口", description="路由参数接口详情")
def test(item:str=Path(description="商品名称"), id:Union[int, None]=Path(description="商品ID，最小为3， 最大为100", ge=3, le=100)):
    return {'status': 200, 'msg': 'success', 'data': {'id': id, 'item': item}}
```
5. 查询参数

```shell
@app.get("/q_params/", tags=["Query请求参数"], summary="请求参数", description="请求参数接口详情", response_description="响应数据详情" )
def test2(pnum:int|None=Query(default=0, description="当前页"), psize:int|None=Query(default=0, description="每页条数")):
    return {'status': 200, 'msg': 'success', 'data': {'pnum': pnum, 'psize': psize}}
```
```shell
@app.get("/q_str", tags=["字符串长度校验"])
def q_str(username: Union[str, None]=Query(description="用户名", min_length=3, max_length=8)):
    return {'status': 200, 'msg': 'success', 'data': {'username': username}}
```
```shell
@app.get('/re_str', tags=["正则表达式校验"])
def re_str(q: Union[str, None]=Query(description="查询参数", regex="^[a-zA-Z]")):
    return {'status': 200, 'msg': 'success', 'data': {'q': q}}
```
```shell
# http://127.0.0.1:8005/m_val?ids=1&ids=2&ids=3
@app.get("/m_val", tags=["请求多值"])
def m_val(ids:Union[List[int], None]=Query(default=None, description="多个IDs参数")):
    if not ids:
        return {'status': 200, 'msg': 'success', 'data': 'ids is null'}
    return {'status': 200, 'msg': 'success', 'data': {'ids': ids}}
```

6. 请求体传参
```shell
from pydantic import BaseModel
class UserInfo(BaseModel):
    name: str
    desc: str | None=None
    age: int |None=0
    sex: str| None = "M"
@app.post("/userinfo", tags="请求体参数")
def user_info(userinfo: UserInfo):
    return  {'status': 200, "msg": "success", "data": userinfo}
```

7. FORM数据参数
```shell
# pip install python-multipart
@app.post("/form_data", tags=["Form数据"])
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
```

8. 返回模板

```shell
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
@app.get("/tmpl/{msg}", tags=["返回模板"], response_class=HTMLResponse)
def tmpl_view(request:Request, msg:Union[str, None]=Path(description="路由参数msg")):
    return templates.TemplateResponse("tmpl.html", {"request": request, "msg": msg})
```

![img.png](img.png)