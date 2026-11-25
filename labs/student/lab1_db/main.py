"""
[LAB 1] 데이터베이스 연결과 메모 CRUD API
=====================================================================
목표
  - SQLAlchemy 로 DB 에 연결하고, 파이썬 클래스(모델)로 테이블을 정의한다.
  - Pydantic 스키마로 '요청에 들어올 데이터 모양'을 검증한다.
  - Depends(get_db) 로 요청마다 DB 세션을 열고 닫는다.
  - 메모 CRUD:  POST 생성 / GET 조회 / PUT 수정 / DELETE 삭제

MySQL 준비 (처음 한 번 · 프로젝트 루트의 setup_mysql.sql 참고)
  DB  : my_memo_app      계정 : hyundai / hyundai
  다른 계정·DB 를 쓰려면 실행 전에 환경 변수로 바꿉니다.
    PowerShell:  $env:DATABASE_URL = "mysql+pymysql://아이디:비번@localhost:3306/DB이름?charset=utf8mb4"
    mac/Linux :  export DATABASE_URL="mysql+pymysql://아이디:비번@localhost:3306/DB이름?charset=utf8mb4"

실행
  uvicorn main:app --reload   →  http://127.0.0.1:8000/docs 에서 직접 호출해 보기
점검
  python check_lab.py
=====================================================================
"""
import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

app = FastAPI(title="마이 메모 앱")
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------------
# DB 연결 설정 (완성되어 있음)
#   mysql+pymysql : MySQL 에 PyMySQL 드라이버로 접속,  charset=utf8mb4 : 한글·이모지 저장
#   pool_pre_ping : 오래 쉬어서 끊긴 연결을 자동으로 다시 맺음
#   engine       : DB 와 실제로 통신하는 객체 (연결 풀 관리)
#   SessionLocal : 요청마다 '작업 단위(세션)'를 만들어 주는 공장
#   Base         : 모든 모델 클래스의 부모. Base 를 상속하면 테이블이 된다
# ---------------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://hyundai:hyundai@localhost:3306/my_memo_app?charset=utf8mb4",
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------------------------------------------------
# [STEP 1] 모델: memo 테이블
#   id      : Integer, 기본 키(primary_key=True), index=True
#   title   : String(100)
#   content : String(1000)
#   클래스 속성 = 테이블의 컬럼,  __tablename__ = 테이블 이름
# ---------------------------------------------------------------
class Memo(Base):
    __tablename__ = "memo"
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    # TODO: title(String 100), content(String 1000) 컬럼을 추가하세요
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(1000))
    


# ---------------------------------------------------------------
# [STEP 2] 스키마: 요청/응답 데이터의 모양 (Pydantic)
#   MemoCreate : 생성할 때 받는 값   → title: str, content: str  (둘 다 필수)
#   MemoUpdate : 수정할 때 받는 값   → 둘 다 선택 (str | None = None)
#   MemoOut    : 응답으로 내보낼 값  → id, title, content
#                from_attributes=True 를 주면 DB 모델 객체를 그대로 넘겨도 변환됨
#   모델(Memo)은 'DB 테이블', 스키마는 'HTTP 로 오가는 JSON' 입니다. 둘은 다릅니다!
# ---------------------------------------------------------------
class MemoCreate(BaseModel):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    # TODO: title: str, content: str
    title: str
    content: str



class MemoUpdate(BaseModel):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    # TODO: title: str | None = None, content: str | None = None
    title: str | None = None
    content: str | None = None


class MemoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str


# 정의한 모델대로 테이블 생성 (이미 있으면 그대로 둠)
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------
# [STEP 3] DB 세션 의존성
#   요청이 들어오면 세션을 열어 '빌려주고(yield)', 응답이 끝나면 반드시 닫습니다.
#       db = SessionLocal()
#       try:     yield db
#       finally: db.close()
#   라우트 함수에서  db: Session = Depends(get_db)  로 받아 씁니다.
# ---------------------------------------------------------------
def get_db():
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 3: SessionLocal() 을 yield 하고 finally 에서 close")


# ---------------------------------------------------------------
# [STEP 4] 메모 생성   POST /memos/   body: {"title": "...", "content": "..."}
#   new_memo = Memo(title=memo.title, content=memo.content)
#   db.add(new_memo) → db.commit() → db.refresh(new_memo)  (id 가 채워짐)
#   return new_memo   (response_model=MemoOut 가 JSON 으로 변환)
# ---------------------------------------------------------------
@app.post("/memos/", response_model=MemoOut)
def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 4: 메모 생성")


# ---------------------------------------------------------------
# [STEP 5] 메모 목록   GET /memos/
#   return db.query(Memo).all()
# ---------------------------------------------------------------
@app.get("/memos/", response_model=list[MemoOut])
def list_memos(db: Session = Depends(get_db)):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 5: 전체 메모 조회")


# ---------------------------------------------------------------
# [STEP 6] 메모 수정   PUT /memos/{memo_id}   body: {"title": "..."} (일부만 보내도 됨)
#   db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
#   없으면 raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다")
#   memo.title / memo.content 가 None 이 아닌 것만 바꾸고 commit → refresh → return
# ---------------------------------------------------------------
@app.put("/memos/{memo_id}", response_model=MemoOut)
def update_memo(memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 6: 메모 수정")


# ---------------------------------------------------------------
# [STEP 7] 메모 삭제   DELETE /memos/{memo_id}
#   없으면 404, 있으면 db.delete(db_memo) → db.commit()
#   return {"message": "메모가 삭제되었습니다"}
# ---------------------------------------------------------------
@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    # ===== TODO: 이 부분을 완성하세요 (위 설명의 순서를 따라가세요) =====
    raise NotImplementedError("STEP 7: 메모 삭제")


# ---------------------------------------------------------------
# LAB 0 에서 만든 경로 (완성되어 있음)
# ---------------------------------------------------------------
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(request, "home.html", {"app_name": "마이 메모 앱"})


@app.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}
