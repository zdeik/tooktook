# DB/DB_main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, create_engine, text, Date, TIMESTAMP, DECIMAL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
import uvicorn
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# 데이터베이스 설정을 직접 포함
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 모든 테이블 모델 정의 (실제 MySQL 스키마와 정확히 일치)
class Consultants(Base):
    __tablename__ = "consultants"
    consultant_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    major = Column(String(255), nullable=True)
    join_date = Column(Date, nullable=True)
    team = Column(String(255), nullable=True)

class Customers(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    name = Column(String(255), nullable=True)
    region = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    business_type = Column(String(255), nullable=True)

class FundTypes(Base):
    __tablename__ = "fund_types"
    fund_type_id = Column(Integer, primary_key=True)
    fund_type_name = Column(String(255), nullable=False)

class Documents(Base):
    __tablename__ = "documents"
    document_id = Column(Integer, primary_key=True)
    document_name = Column(String(255), nullable=True)
    is_required = Column(Boolean, nullable=True)
    is_submitted = Column(Boolean, nullable=True)
    submission_date = Column(Date, nullable=True)

class Consultations(Base):
    __tablename__ = "consultations"
    consultation_id = Column(Integer, primary_key=True)
    consultant_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=True)
    consultation_date = Column(Date, nullable=True)
    resolution_type = Column(String(50), nullable=True)
    satisfaction_score = Column(Integer, nullable=True)

class ConsultationFundTypes(Base):
    __tablename__ = "consultation_fund_types"
    consultation_id = Column(Integer, primary_key=True)
    fund_type_id = Column(Integer, primary_key=True)

class ConsultationDocuments(Base):
    __tablename__ = "consultation_documents"
    consultation_id = Column(Integer, primary_key=True)
    document_id = Column(Integer, primary_key=True)

class ConversationLogs(Base):
    __tablename__ = "conversation_logs"
    log_id = Column(Integer, primary_key=True)
    consultation_id = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    log_type = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)

class Statistics(Base):
    __tablename__ = "statistics"
    statistic_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    total_consultations = Column(Integer, nullable=True)
    avg_consultation_time = Column(Integer, nullable=True)
    completed_consultations = Column(Integer, nullable=True)
    avg_satisfaction_score = Column(DECIMAL(5, 2), nullable=True)
    category = Column(String(255), nullable=True)

class Predictions(Base):
    __tablename__ = "predictions"
    prediction_id = Column(Integer, primary_key=True)
    ts_slot = Column(TIMESTAMP, nullable=False)
    weekday = Column(Integer, nullable=True)
    slot_hour = Column(Integer, nullable=True)
    label_lag7 = Column(String(255), nullable=True)
    pred_label = Column(String(255), nullable=True)
    top1 = Column(String(255), nullable=True)
    p1 = Column(DECIMAL(10, 8), nullable=True)
    top2 = Column(String(255), nullable=True)
    p2 = Column(DECIMAL(10, 8), nullable=True)
    top3 = Column(String(255), nullable=True)
    p3 = Column(DECIMAL(10, 8), nullable=True)
    weekday_ko = Column(String(10), nullable=True)

class TomorrowPredictions(Base):
    __tablename__ = "tomorrow_predictions"
    prediction_id = Column(Integer, primary_key=True)
    ts_slot = Column(TIMESTAMP, nullable=False)
    weekday = Column(Integer, nullable=True)
    slot_hour = Column(Integer, nullable=True)
    y_pred = Column(DECIMAL(15, 10), nullable=True)

# Pydantic 모델들 (실제 MySQL 스키마에 맞춤)
class ConsultantResponse(BaseModel):
    consultant_id: int
    name: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    join_date: Optional[date] = None
    team: Optional[str] = None
    class Config:
        from_attributes = True

class CustomerResponse(BaseModel):
    customer_id: int
    age: Optional[int] = None
    gender: Optional[str] = None
    name: Optional[str] = None
    region: Optional[str] = None
    phone_number: Optional[str] = None
    business_type: Optional[str] = None
    class Config:
        from_attributes = True

class FundTypeResponse(BaseModel):
    fund_type_id: int
    fund_type_name: str
    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    document_id: int
    document_name: Optional[str] = None
    is_required: Optional[bool] = None
    is_submitted: Optional[bool] = None
    submission_date: Optional[date] = None
    class Config:
        from_attributes = True

class ConsultationResponse(BaseModel):
    consultation_id: int
    consultant_id: int
    customer_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    consultation_date: Optional[date] = None
    resolution_type: Optional[str] = None
    satisfaction_score: Optional[int] = None
    class Config:
        from_attributes = True

class ConsultationFundTypeResponse(BaseModel):
    consultation_id: int
    fund_type_id: int
    class Config:
        from_attributes = True

class ConsultationDocumentResponse(BaseModel):
    consultation_id: int
    document_id: int
    class Config:
        from_attributes = True

class ConversationLogResponse(BaseModel):
    log_id: int
    consultation_id: int
    timestamp: datetime
    log_type: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class StatisticResponse(BaseModel):
    statistic_id: int
    date: date
    total_consultations: Optional[int] = None
    avg_consultation_time: Optional[int] = None
    completed_consultations: Optional[int] = None
    avg_satisfaction_score: Optional[float] = None
    category: Optional[str] = None
    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    prediction_id: int
    ts_slot: datetime
    weekday: Optional[int] = None
    slot_hour: Optional[int] = None
    label_lag7: Optional[str] = None
    pred_label: Optional[str] = None
    top1: Optional[str] = None
    p1: Optional[float] = None
    top2: Optional[str] = None
    p2: Optional[float] = None
    top3: Optional[str] = None
    p3: Optional[float] = None
    weekday_ko: Optional[str] = None
    class Config:
        from_attributes = True

class TomorrowPredictionResponse(BaseModel):
    prediction_id: int
    ts_slot: datetime
    weekday: Optional[int] = None
    slot_hour: Optional[int] = None
    y_pred: Optional[float] = None
    class Config:
        from_attributes = True

app = FastAPI(title="Consultation Management API")

# 모든 API 엔드포인트 정의
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/api/consultants", response_model=List[ConsultantResponse])
def get_consultants(db: Session = Depends(get_db)):
    try:
        consultants = db.query(Consultants).all()
        print(f"Found {len(consultants)} consultants")  # 디버그 로그
        
        # 데이터를 안전하게 변환
        result = []
        for consultant in consultants:
            try:
                consultant_data = {
                    "consultant_id": consultant.consultant_id,
                    "name": consultant.name,
                    "department": consultant.department, 
                    "major": consultant.major,
                    "join_date": consultant.join_date,
                    "team": consultant.team
                }
                result.append(consultant_data)
            except Exception as item_error:
                print(f"Error processing consultant {consultant.consultant_id}: {item_error}")
                continue
                
        print(f"Successfully processed {len(result)} consultants")
        return result
        
    except Exception as e:
        print(f"Database query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/customers", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    try:
        customers = db.query(Customers).all()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fund_types", response_model=List[FundTypeResponse])
def get_fund_types(db: Session = Depends(get_db)):
    try:
        fund_types = db.query(FundTypes).all()
        return fund_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents", response_model=List[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    try:
        documents = db.query(Documents).all()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/consultations", response_model=List[ConsultationResponse])
def get_consultations(db: Session = Depends(get_db)):
    try:
        consultations = db.query(Consultations).all()
        return consultations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/consultation_fund_types", response_model=List[ConsultationFundTypeResponse])
def get_consultation_fund_types(db: Session = Depends(get_db)):
    try:
        consultation_fund_types = db.query(ConsultationFundTypes).all()
        return consultation_fund_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/consultation_documents", response_model=List[ConsultationDocumentResponse])
def get_consultation_documents(db: Session = Depends(get_db)):
    try:
        consultation_documents = db.query(ConsultationDocuments).all()
        return consultation_documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversation_logs", response_model=List[ConversationLogResponse])
def get_conversation_logs(db: Session = Depends(get_db)):
    try:
        conversation_logs = db.query(ConversationLogs).all()
        return conversation_logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/statistics", response_model=List[StatisticResponse])
def get_statistics(db: Session = Depends(get_db)):
    try:
        statistics = db.query(Statistics).all()
        return statistics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predictions", response_model=List[PredictionResponse])
def get_predictions(db: Session = Depends(get_db)):
    try:
        predictions = db.query(Predictions).all()
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tomorrow_predictions", response_model=List[TomorrowPredictionResponse])
def get_tomorrow_predictions(db: Session = Depends(get_db)):
    try:
        tomorrow_predictions = db.query(TomorrowPredictions).all()
        return tomorrow_predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 헬스체크 엔드포인트
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 디버깅용 간단한 엔드포인트
@app.get("/debug/consultants")
def debug_consultants(db: Session = Depends(get_db)):
    try:
        from sqlalchemy import text
        # 원시 SQL로 직접 조회 (text()로 감싸기)
        result = db.execute(text("SELECT * FROM consultants LIMIT 1"))
        row = result.fetchone()
        if row:
            return {"raw_data": str(row), "columns": list(result.keys())}
        else:
            return {"message": "No data found"}
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}

# 테이블 구조 확인 엔드포인트
@app.get("/debug/table-info")
def debug_table_info(table: str = "consultants", db: Session = Depends(get_db)):
    try:
        result = db.execute(text(f"DESCRIBE {table}"))
        columns = []
        for row in result:
            columns.append({
                "field": row[0],
                "type": row[1], 
                "null": row[2],
                "key": row[3],
                "default": row[4],
                "extra": row[5]
            })
        return {"table": table, "table_structure": columns}
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}

# 모든 테이블 목록 확인
@app.get("/debug/tables")
def debug_tables(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return {"tables": tables}
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}

# 서버 실행을 위한 코드
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)