
from models import db, User, People, Planet, Favorite


def add_people(name, age, planet_id ):

    existing_person = People.query.filter_by(name=name).first()

    if existing_person:
        raise ValueError("This person already exists...")
    
    new_person = People(name=name, age=int(age), planet_id=int(planet_id))

    db.session.add(new_person)
    db.session.commit()

    return new_person.serialize()


def get_all_people(id):

    if id is not None:
        people = People.query.filter_by(id=id).first()
        return people.serialize()
    
    people = People.query.all()

    if not people:
        raise ValueError("There is not people")
    else:
        return [p.name for p in people]



def add_planet(name, population, weather):
    
    existing_planet = Planet.query.filter_by(name=name).first()

    if existing_planet:
        raise ValueError("This planet already exists...")
    
    new_planet = Planet(name=name, population=int(population), weather=weather)

    db.session.add(new_planet)
    db.session.commit()

    return new_planet.serialize()


def get_all_planets(id):

    if id is not None:
        planet = Planet.query.filter_by(id=id).first()
        return planet.serialize()

    planets = Planet.query.all()

    if not planets:
        raise ValueError("There are not planets")
    else:
        return [p.serialize() for p in planets]

def get_all_users():

    users = User.query.all()

    if not users:
        raise ValueError("There are no users")
    else:
        return [user.serialize() for user in users]


def get_favorites_by_user(id):
    favorites = Favorite.query.filter_by(user_id=id).all()

    if not favorites:
        raise ValueError("There are no favorites added yet")
    else:
        return [favorite.serialize() for favorite in favorites]