# FastAPI에서 데이터베이스 액세스를 하는 예제는 다음과 같습니다.

# 우선, 필요한 라이브러리를 설치해야 합니다. 다음과 같이 SQLAlchemy와 asyncpg를 설치합니다.
# pip install sqlalchemy asyncpg
# 이제, FastAPI 애플리케이션에서 SQLAlchemy를 사용하여 데이터베이스에 액세스할 수 있습니다. 다음은 PostgreSQL 데이터베이스를 사용하는 예제입니다.

# 아래 코드에서는 SQLAlchemy를 사용하여 데이터베이스에 연결하고, 데이터베이스 모델을 정의합니다. 그리고 데이터베이스 세션을 생성하여 애플리케이션에 연결합니다. 이후 경로를 연결하여 POST 요청을 처리합니다. create_user 함수에서는 데이터베이스 세션을 사용하여 새로운 사용자를 추가하고, 데이터베이스에 저장합니다.
# 이제, 위 코드를 실행하고 http://localhost:8000/docs 를 방문하여 API 문서를 확인할 수 있습니다.


from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 데이터베이스 연결
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 데이터베이스 모델 정의
Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

# 데이터베이스 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI 애플리케이션 생성
app = FastAPI()

# 경로 연결
@app.post("/users/")
async def create_user(name: str, email: str):
    db = SessionLocal()
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
