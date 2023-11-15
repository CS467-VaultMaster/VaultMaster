from sqlalchemy import Column, ForeignKey, String, DateTime, Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    User class in DB.
    """

    # DONE: Add first name and last name.
    # TODO: Add regex.
    __tablename__ = "site_user"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # DONE: remove phone_number.
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    last_verified = Column(DateTime, nullable=True)
    last_login_attempt = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    otp_secret = Column(String, nullable=False)
    # DONE: Add MFA token.


class Vault(Base):
    """
    Vault class in DB.
    """

    __tablename__ = "vault"
    id = Column(String, primary_key=True)
    vault_name = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    open_attempts = Column(Integer, nullable=False)
    user_id = Column(String, ForeignKey("site_user.id"))
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
    note = Column(Text, nullable=True)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    fernet_key = Column(String, nullable=False)
    vault_id = Column(String, ForeignKey("vault.id"))
    vault = relationship("Vault", backref="vault")


class Admin(Base):
    """
    Admin class in DB.
    """
    __tablename__ = "admin"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    last_accessed = Column(DateTime, nullable=False)
