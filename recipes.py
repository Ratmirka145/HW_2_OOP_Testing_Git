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
    
class DietaryRecipe(Recipe):
    def __init__(self,title, diet_type,ingredients=None):
        if ingredients is None:
            ingredients=[]

        super().__init__(title,ingredients)
        self.diet_type=diet_type

    def scale(self, ratio):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        new_ingredients=[]

        for ingredient in self.ingredients:
            new_ingredient = Ingredient(ingredient.name, ingredient.quantity*ratio, ingredient.unit)
            new_ingredients.append(new_ingredient)
        return DietaryRecipe(self.title, self.diet_type, new_ingredients)

    def __str__(self):
        result = "["+self.diet_type+"] "+self.title+"\n"
        for ingredient in self.ingredients:
            result=result+str(ingredient)+"\n"

        return result

class ShoppingList:
    def __init__(self):
        self._items=[]

    def add_recipe(self, recipe, portions):
        if portions<=0:
            raise ValueError("Количество порций должно быть положительным")

        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, scaled_recipe.title))

    def remove_recipe(self, title):
        new_items=[]
        for ingredient, recipe_title in self._items:
            if recipe_title != title:
                new_items.append((ingredient, recipe_title))
        self._items = new_items

    def get_list(self):
        result=[]
        for ingredient, recipe_title in self._items:
            was_found=False

            for item in result:
                if item==ingredient:
                    item.quantity = item.quantity + ingredient.quantity
                    was_found=True
                    break

            if not was_found:
                new_ingredient = Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
                result.append(new_ingredient)
        result.sort(key=lambda ingredient: ingredient.name)
        return result

    def __add__(self, other):
        new_list = ShoppingList()
        for ingredient, recipe_title in self._items:
            new_ingredient=Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
            new_list._items.append((new_ingredient, recipe_title))
        for ingredient, recipe_title in other._items:
            new_ingredient=Ingredient(ingredient.name,ingredient.quantity, ingredient.unit)
            new_list._items.append((new_ingredient, recipe_title))
        return new_list