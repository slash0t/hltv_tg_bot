from sqlmodel import create_engine, SQLModel

from data.config import POSTGRES_URL

import utils.db_api.models

engine = create_engine(POSTGRES_URL)
