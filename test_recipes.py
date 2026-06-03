import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_create():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name=="Мука"
    assert ingredient.quantity==500.0
    assert ingredient.unit=="г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient)=="Мука: 500.0 г"


def test_ingredient_wrong_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", 0, "г")

    with pytest.raises(ValueError):
        Ingredient("Мука", -10, "г")


def test_ingredient_equal():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 1000, "г")
    ingredient3 = Ingredient("Сахар", 500, "г")
    ingredient4 = Ingredient("Мука", 1, "кг")

    assert ingredient1==ingredient2
    assert ingredient1!=ingredient3
    assert ingredient1!=ingredient4


def test_recipe_create():
    ingredients=[Ingredient("Мука", 500, "г"),Ingredient("Молоко", 1, "л")]
    recipe = Recipe("Блины", ingredients)

    assert recipe.title=="Блины"
    assert len(recipe.ingredients)==2


def test_recipe_add_ingredient():
    recipe = Recipe("Блины", [])

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))

    assert len(recipe.ingredients)==1
    assert recipe.ingredients[0].name=="Мука"


def test_recipe_add_same_ingredient():
    recipe = Recipe("Блины", [])

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))

    assert len(recipe.ingredients)==1
    assert recipe.ingredients[0].quantity==800.0


def test_recipe_scale():
    recipe = Recipe("Блины", [Ingredient("Мука", 500, "г"),Ingredient("Молоко", 1, "л")])

    new_recipe = recipe.scale(2)

    assert new_recipe is not recipe
    assert new_recipe.title=="Блины"
    assert new_recipe.ingredients[0].quantity==1000.0
    assert new_recipe.ingredients[1].quantity==2.0

    assert recipe.ingredients[0].quantity==500.0
    assert recipe.ingredients[1].quantity==1.0


def test_recipe_bad_scale():
    recipe = Recipe("Блины", [Ingredient("Мука", 500, "г")])

    with pytest.raises(ValueError):
        recipe.scale(0)

    with pytest.raises(ValueError):
        recipe.scale(-2)


def test_recipe_len():
    recipe = Recipe("Блины", [Ingredient("Мука", 500, "г"),Ingredient("Молоко", 1, "л")])

    assert len(recipe)==2


def test_dietary_recipe_scale():
    recipe = DietaryRecipe("Салат", "веган", [Ingredient("Огурец", 2, "шт")])

    new_recipe = recipe.scale(3)

    assert type(new_recipe)==DietaryRecipe
    assert new_recipe.diet_type=="веган"
    assert new_recipe.ingredients[0].quantity==6.0


def test_shopping_list_add_recipe():
    recipe = Recipe("Блины", [Ingredient("Мука", 500, "г")])
    shop = ShoppingList()
    shop.add_recipe(recipe, 2)
    result = shop.get_list()

    assert len(result)==1
    assert result[0].name=="Мука"
    assert result[0].quantity==1000.0


def test_shopping_list_bad_portions():
    recipe = Recipe("Блины", [ Ingredient("Мука", 500, "г")])

    shop = ShoppingList()

    with pytest.raises(ValueError):
        shop.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    recipe1 = Recipe("Блины", [Ingredient("Мука", 500, "г")])

    recipe2 = Recipe("Омлет", [Ingredient("Яйцо", 2, "шт")])

    shop = ShoppingList()
    shop.add_recipe(recipe1, 1)
    shop.add_recipe(recipe2, 1)

    shop.remove_recipe("Блины")
    result = shop.get_list()
    assert len(result)==1
    assert result[0].name=="Яйцо"


def test_shopping_list_get_list_sum_and_sort():
    recipe1 = Recipe("Блины", [Ingredient("Мука", 500, "г"), Ingredient("Молоко", 1, "л")])

    recipe2 = Recipe("Пирог", [ Ingredient("Мука", 300, "г"), Ingredient("Яблоко", 2, "шт")])

    shop = ShoppingList()
    shop.add_recipe(recipe1, 1)
    shop.add_recipe(recipe2, 1)

    result = shop.get_list()

    assert len(result)==3
    assert result[0].name=="Молоко"
    assert result[1].name=="Мука"
    assert result[1].quantity==800.0
    assert result[2].name=="Яблоко"


def test_shopping_list_add():
    recipe1 = Recipe("Блины", [Ingredient("Мука", 500, "г")])

    recipe2 = Recipe("Омлет", [Ingredient("Яйцо", 2, "шт")])

    shop1 = ShoppingList()
    shop2 = ShoppingList()

    shop1.add_recipe(recipe1, 1)
    shop2.add_recipe(recipe2, 1)

    shop3 = shop1 + shop2

    result = shop3.get_list()

    assert len(result)==2
    assert result[0].name=="Мука"
    assert result[1].name=="Яйцо"

    assert len(shop1.get_list())==1
    assert len(shop2.get_list())==1