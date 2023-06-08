import os

class Config:
  SQLALCHEMY_DATABASE_URI = ( 
      "postgresql://"
      f"{os.environ['POSTGRES_USER']}:"
      f"{os.environ['POSTGRES_PASSWORD']}@"
      f"{os.environ['POSTGRES_HOSTNAME']}:"
      f"{os.environ['POSTGRES_PORT']}/"
      f"{os.environ['POSTGRES_DB']}"
  )
