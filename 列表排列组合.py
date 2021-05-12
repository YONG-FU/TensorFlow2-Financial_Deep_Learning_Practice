class IceCreamMachine:

    def __init__(self, ingredients, toppings):
        self.ingredients = ingredients
        self.toppings = toppings

    def scoops(self):
        new_list = []
        import itertools
        for item in itertools.product(self.ingredients, self.toppings):
            new_list.append(item)
        return new_list


machine = IceCreamMachine(["vanilla", "chocolate"], ["chocolate sauce"])
print(machine.scoops())
# should print[['vanilla', 'chocolate sauce'], ['chocolate', 'chocolate sauce']]
