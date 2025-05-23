from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)

    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    planet:  Mapped["Planet"] = relationship("Planet", back_populates="people")



    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "planet": self.planet.name
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    weather: Mapped[str] = mapped_column(String(120), nullable=False)

    people: Mapped[list["People"]] = relationship("People", back_populates="planet")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "weather": self.weather,
            "people": [person.serialize() for person in self.people] if self.people else None,
        }


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    favorite_type: Mapped[str] = mapped_column(String(120), nullable=False)  # Planet o People
    favorite_id: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_type": self.favorite_type,
            "favorite_id": self.favorite_id,
        }   
