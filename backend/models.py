from sqlalchemy import Column, ForeignKey, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """
    User class in DB.
    """
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=False, nullable=True)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    last_verified = Column(DateTime, nullable=True)
    login_attemtps = Column(Integer, nullable=False)


class Valut(Base):
    """
    Vault class in DB. 
    """
    __tablename__ = "vault"
    id = Column(String, primary_key=True)
    vault_name = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    open_attempts = Column(Integer, nullable=False)
    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("User", backref="vault")


class Credential(Base):
    """
    Credential class in DB.
    """
    __tablename__ = "credential"
    id = Column(String, primary_key=True)
    nickname = Column(String, nullable=True)
    category = Column(String, nullable=True)
    url = Column(String, nullable=False)
    password = Column(String, nullable=False)
    node = Column(Text, nullable=True)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    vault_id = Column(String, ForeignKey("vault.id"))
    vault = relationship("Vault", backref="vault")