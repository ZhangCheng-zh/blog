# class Function:
#     def __init__(self, name, argument_types):
#         self.name = name 
#         self.argument_types = argument_types
    
#     def __repr__(self):
#         return f"Function<{self.name}>"

# class FunctionLibrary:
#     def __init__(self):
#         self.

    
#     def register(self, list_of_function):
#         pass # todo
    
#     def find_matches(self, argument_types): # time complexity: O(m) m is size of functionLibrary space: O(1)
#         pass# todo

"""
some test
flib = FunctionLibrary()
flib.register([
Function("funA", ["Boolean", "Integer"]),
Function("funB", ["Integer"]),
Function("funC", ["Integer"])  
])

assert flib.find_matches(['Bool])
"""



### **Extended Version (with `isVariadic` support)**


"""
register([
    funA: {["Boolean", "Integer"], isVariadic: False},
    funB: {["Integer"], isVariadic: False},
    funC: {["Integer"], isVariadic: True}
])

findMatches(["Boolean", "Integer"]) -> [funA]
findMatches(["Integer"]) -> [funB, funC]
findMatches(["Integer", "Integer", "Integer"]) -> [funC]
"""

from collections import defaultdict

class Function:
    def __init__(self, name, argument_types, is_variadic):
        self.name = name
        self.argument_types = argument_types
        self.isVariadic = is_variadic

    def __repr__(self):
        return "Function<{}>".format(self.name)


class FunctionLibrary:
    def __init__(self):
        self.nonVariadic = defaultdict(list) # tuple -> [Function]
        self.isVariadic = defaultdict(list) # tuple -> [Function]

    def register(self, list_of_functions): # time: O(n) n is count of function
        for f in list_of_functions:
            sig = tuple(f.argument_types)
            if not f.isVariadic:
                self.nonVariadic[sig].append(f)
            else:
                prefix = sig[:-1]
                varType = sig[-1]
                self.isVariadic[(prefix, varType)].append(f)

    def findMatches(self, argument_types):
        args = tuple(argument_types)
        matches = []

        # find all matched nonVariadic function
        matches.extend(self.nonVariadic[args])

        if args:
            prefix = args[:-1]
            last = args[-1]
            # find the head of same arg tail
            s = len(args) - 1
            while s > 0 and args[s - 1] == last:
                s -= 1
            
            for j in range(s, len(args)):
                prefix = args[:j]
                matches.extend(self.isVariadic[(prefix, last)])
        print([f.name for f in matches])
        return [f.name for f in matches] # each match time complexity:  O(k) k is length of argument_types of find_match


flib =  FunctionLibrary() 
fa = Function('funA', ["Boolean", "Integer"], False)
fb = Function('funB', ["Integer"], False)
fc = Function('funC', ["Integer"], True)
flib.register([fa, fb, fc]) 

assert flib.findMatches(["Boolean", "Integer"]) == ['funA']
assert flib.findMatches(["Integer"]) == ['funB', 'funC']
assert flib.findMatches(["Integer", "Integer", "Integer"]) == ['funC']