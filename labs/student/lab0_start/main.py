"""
[LAB 0] FastAPI 시작하기 — 첫 웹 서버와 첫 페이지
=====================================================================
목표
  - FastAPI 앱 객체를 만들고 '경로(URL) → 함수' 를 연결(라우팅)한다.
  - JSON 을 돌려주는 API 와, HTML 페이지(Jinja2 템플릿)를 돌려주는 경로를 구분한다.
  - 경로 매개변수(/hello/{name})와 쿼리 매개변수(?age=20)를 받아 본다.

실행 (이 폴더 안에서)
  uvicorn main:app --reload
    main  = main.py 파일,  app = 그 안의 FastAPI 객체,  --reload = 저장하면 자동 재시작
  브라우저:  http://127.0.0.1:8000/        홈 페이지
             http://127.0.0.1:8000/about   JSON 응답
             http://127.0.0.1:8000/docs    자동 생성되는 API 문서(Swagger UI)

점검
  python check_lab.py
=====================================================================
"""
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from datetime import date

# FastAPI 앱 객체: 이 객체에 경로들을 등록합니다. uvicorn 은 이 객체를 실행합니다.
app = FastAPI(title="마이 메모 앱")

# templates 폴더의 HTML 파일을 Jinja2 문법으로 채워서 돌려주는 도우미
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------
# [STEP 1] JSON 을 돌려주는 API
#   GET /about  →  {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}
#   - @app.get("/about") 데코레이터로 경로와 함수를 연결합니다.
#   - 파이썬 dict 를 return 하면 FastAPI 가 자동으로 JSON 으로 바꿔 보냅니다.
# ---------------------------------------------------------------
@app.get("/about")
async def about():
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}


# ---------------------------------------------------------------
# [STEP 2] HTML 페이지를 돌려주는 경로
#   GET /  →  templates/home.html 을 렌더링
#   - templates.TemplateResponse(request, "파일이름", {템플릿에 넘길 값}) 를 return
#   - home.html 안의 {{ app_name }} 자리에 "마이 메모 앱" 이 들어가도록
#     {"app_name": "마이 메모 앱"} 을 넘기세요.
#   - request 는 템플릿 렌더링에 꼭 필요해서 매개변수로 받습니다.
# ---------------------------------------------------------------
@app.get("/")
async def read_root(request: Request):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    today = date.today().strftime("%Y년 %m월 %d일")
    return templates.TemplateResponse(request, "home.html", {"app_name":"마이 메모 앱", "today": today})
s

# ---------------------------------------------------------------
# [STEP 3] 경로 매개변수 + 쿼리 매개변수
#   GET /hello/네트          →  {"greeting": "안녕하세요, 네트님!", "age": null}
#   GET /hello/네트?age=20   →  {"greeting": "안녕하세요, 네트님!", "age": 20}
#   - 경로의 {name} 은 함수의 매개변수 name 으로 들어옵니다.
#   - 경로에 없는 매개변수(age)는 '?age=20' 쿼리 문자열에서 옵니다.
#   - 타입 힌트(int)를 쓰면 FastAPI 가 자동으로 변환·검증합니다. (?age=abc → 422 오류)
# ---------------------------------------------------------------
@app.get("/hello/{name}")
async def hello(name: str, age: int | None = None):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    return {"greeting" : f"안녕하세요, {name}님!" , "age" : age}

# ---------------------------------------------------------------
# [STEP 4] 과제 GET /health → {"status": "ok"} 추가
# home.html 에 오늘 날짜를 파이썬에서 넘겨 표시하기
# ---------------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}