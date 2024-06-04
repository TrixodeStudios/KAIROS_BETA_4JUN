import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Construct the database URL (Corrected dialect)
#DATABASE_URL = f"postgresql+psycopg2://{SUPABASE_URL.replace('https://', '')}?apikey={SUPABASE_KEY}"
DATABASE_URL = f"postgresql+psycopg2://postgres:{SUPABASE_KEY}@{SUPABASE_URL.replace('https://', '')}/postgres"

# Create an engine object (add echo=True for debugging)
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

# Define your database tables
class Conversations(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    # Relationship with TokenUsage and AnalysisResults
    token_usage = relationship("TokenUsage", backref="conversation")
    analysis_results = relationship("AnalysisResults", backref="conversation")

class TokenUsage(Base):
    __tablename__ = "token_usage"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    model = Column(String)
    total_tokens = Column(Integer)
    estimated_cost = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class AnalysisResults(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    feature = Column(String)
    result = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# class UserFeedback(Base):
#     __tablename__ = "user_feedback"
#     id = Column(Integer, primary_key=True)
#     conversation_id = Column(Integer, ForeignKey("conversations.id"))
#     rating = Column(Integer)
#     comment = Column(Text)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)


# Create the tables in the database if they don't exist
Base.metadata.create_all(engine)
