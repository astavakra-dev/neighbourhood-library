import configparser
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Load config.properties
config = configparser.ConfigParser()
config.read("config.properties")

driver = config.get("database", "db.driver")
host = config.get("database", "db.host")
port = config.get("database", "db.port")
name = config.get("database", "db.name")
user = config.get("database", "db.user")
password = config.get("database", "db.password")
echo = config.getboolean("database", "db.echo", fallback=False)

DATABASE_URL = f"{driver}://{user}:{password}@{host}:{port}/{name}"


engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session