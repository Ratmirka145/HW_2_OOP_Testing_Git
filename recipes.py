class Ingredient:
    def __init__(self,name,quantity,unit):
        self.name=name
        self.quantity=quantity
        self.unit=unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self,quantity):
        quantity=float(quantity)
        if quantity<=0:
            raise ValueError("Количество должно быть положительным")
        self._quantity=quantity

    def __str__(self):
        return self.name+": "+str(self.quantity)+" "+self.unit

    def __repr__(self):
        return "Ingredient("+repr(self.name)+", "+repr(self.quantity)+", "+repr(self.unit)+")"

    def __eq__(self,other):
        if type(other)!=Ingredient:
            return False
        if self.name==other.name and self.unit==other.unit:
            return True
        return False

class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients=[]

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient):
        for item in self.ingredients:
            if item==ingredient:
                item.quantity = item.quantity + ingredient.quantity
                return

        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if type(ratio)==int or type(ratio)==float:
            if ratio > 0:
                return True
        return False

    def scale(self, ratio):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")

        new_ingredients=[]

        for ingredient in self.ingredients:
            new_ingredient = Ingredient(ingredient.name, ingredient.quantity*ratio, ingredient.unit)
            new_ingredients.append(new_ingredient)

        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = self.title + "\n"

        for ingredient in self.ingredients:
            result = result + str(ingredient) + "\n"

        return result