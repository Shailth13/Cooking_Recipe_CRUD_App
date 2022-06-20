from exts import db

"""data model

class Recepie:
    ind:int primary key
    name:str
    ingredients:str(text)
    instructions:str(text)
    serving_size:str(text)
    category:str(text)
    notes:str(text)
    date_added:str(text)
    date_modified:str(text)
"""
class Recipe(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    ingredients=db.Column(db.Text(),nullable=False)
    instructions=db.Column(db.Text(),nullable=False)
    serving_size=db.Column(db.Text(),nullable=False)
    category=db.Column(db.Text(),nullable=False)
    notes=db.Column(db.Text(),nullable=False)
    date_added=db.Column(db.Text(),nullable=False)
    date_modified=db.Column(db.Text(),nullable=False)

    # we will be writing methods for CRUD operations next
    def __repr__(self):
        return f"<Recipe {self.name} >"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, name, ingredients, instructions,serving_size,category,notes,date_added,date_modified):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.serving_size = serving_size
        self.category = category
        self.notes = notes
        self.date_added = date_added
        self.date_modified = date_modified

# expose this model using the serializer on our API


