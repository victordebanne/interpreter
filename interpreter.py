class Var():
    def __init__(self):
        self.name = None
        self.value = None
        
class Dict():
    def __init__(self):
        self.dict = []
        self.func_dict = [("add", self.add), 
                          ("minus", self.minus), 
                          ("assign", self.assign), 
                          ("display", self.display)]
        self.user_functions = []
        
        self.current_dict = []
        
    def call(self, var):
        for i in range(len(self.dict)):
            if self.dict[i].name == var:
                return self.dict[i].value
            
    def assign(self, var, val):
        var_exist = False
        if type(val) == int:
            pass
        else :
            val = self.call(val)
        for i in range(len(self.dict)):
            if self.dict[i].name == var:
                self.dict[i].value = val
                var_exist = True
                break
        if not var_exist:
            new_var = Var()
            new_var.name = var
            new_var.value = val
            self.dict.append(new_var)
            
    def display_dict(self):
        for i in range(len(self.dict)):
            print(self.dict[i].name," : " ,self.dict[i].value)
            
    def add(self, a, b):
        if type(a) != int:
            a = self.call(a)
        if type(b) != int:
            b = self.call(b)
            
        return a + b
    
    def minus(self, a, b):
        if type(a) != int:
            a = self.call(a)
        if type(b) != int:
            b = self.call(b)
            
        return a - b
    
    def display(self, var):
        print(self.call(var))
        return None
    
    def user_function(self, UserFunc, arguments):
        
       
       
        temp_dict = Dict()
        temp_dict.assign("return", 0)
        temp_dict.user_functions = self.user_functions  
        temp_code_tree = CodeTree(UserFunc.node.code, temp_dict)
        
        for i in range(len(arguments)):
            if type(arguments[i]) == int:
                pass
            else :
                if arguments[i].isdigit():
                    arguments[i] = int(arguments[i])
                else : 
                    arguments[i] = self.call(arguments[i])
            
        for i, arg in enumerate(UserFunc.args):
            temp_dict.assign(arg, arguments[i])
            
        
            
        temp_code_tree.bloc_parser2()
        temp_code_tree.evaluate2()
        
         
        return temp_dict.call("return")
    
    def user_function2(self, UserFunc, arguments):
        #la user function utilise son propre dictionnaire.
        #la valeur des arguments est hérité du bloc ou fonction dans laquelle elle est contenue
        #elle utilise les fonctions déclarées dans le bloc principal
        #elle possède une variable speciale, return qui donne la valeur
        #au bloc dans lequel elle est contenue
        #on utilisera la variable current_dict pour identifier le dictionnaire à utiliser
       
        #on supprime le dictionnaire de la fontion:
        UserFunc.dict = Dict()
        
        #variable return
        UserFunc.dict.assign("return", 0)
        
        #hérite des fonctions du bloc principal
        UserFunc.dict.user_functions = self.user_functions  
        
        #on hérite les arguments du dernier dictionnaire
        if self.current_dict == []:
            for i in range(len(arguments)):
                if type(arguments[i]) == int:
                    pass
                else :
                    if arguments[i].isdigit():
                        arguments[i] = int(arguments[i])
                    else : 
                        arguments[i] = self.call(arguments[i])
        else : 
            for i in range(len(arguments)):
                if type(arguments[i]) == int:
                    pass
                else :
                    if arguments[i].isdigit():
                        arguments[i] = int(arguments[i])
                    else : 
                        arguments[i] = self.current_dict[-1].call(arguments[i])
                        
        for i, arg in enumerate(UserFunc.args):
            UserFunc.dict.assign(arg, arguments[i])
        
        #donne son dictionnaire:
        self.current_dict.append(UserFunc.dict)
        
        #on créé un arbre d'execution temporaire pour le bloc de code 
        temp_code_tree = CodeTree(UserFunc.node.code, UserFunc.dict)
        
        #on evalue le bloc de code
        temp_code_tree.bloc_parser2()
        temp_code_tree.evaluate2()
        
        #supprime son dictionnaire:
        self.current_dict.pop()
        
        #retourne return
        return UserFunc.dict.call("return")       

class Node():
    def __init__(self):
        self.type = None #'var' or 'function'
        self.value = None
        
        self.nodes = None
        
    def display(self):
        print(self.type)
        print(self.value)
        if self.nodes != None:
            print("len = ",len(self.nodes))
        
class AST():
    def __init__(self, dictionnary):
        self.root = Node()
        self.dict = dictionnary
        
    def parenthesis_counter(self, line):
        counter = 0
        for i in range(len(line)):
            if line[i] == "(":
                counter += 1
        return counter
    
    def function_parser(self, line):
        p_counter = 0
        args = []
        function = ""
        arg = ""
        for i in range(len(line)):
            if line[i] == '(':
                p_counter += 1
                if p_counter == 1:
                    continue
            elif line[i] == ')':
                p_counter -= 1
                if p_counter == 0:
                    continue
                
            if p_counter == 0:
                function += line[i]
                
            elif (line[i] == ',') and (p_counter == 1):
                args.append(arg)
                arg = ""
            else : 
                arg += line[i]
                
        if arg != "":
            args.append(arg)
            return [function, args]
        
                
    def parser(self, line, node = None):
        if node == None:
            node = self.root
            
        
            
        arg = ""
        
        
        
        if line == "":
            return
        
        
        else : 
            p = self.parenthesis_counter(line)
            if p == 0:
                for i in range(len(line)):
                    arg += line[i]
                if arg != "": 
                    node.type = 'var'
                    node.value = arg
            else : 
                temp = self.function_parser(line)
                node.type = 'function'
                node.value = temp[0] #type de fonction
                
                node.nodes = [Node() for i in range(len(temp[1]))]
                
                for i in range(len(temp[1])):
                    
                    self.parser(temp[1][i] ,node.nodes[i]) 
                    
    def evaluate(self, node = None):
        if node == None:
            node = self.root
            
       
        
        
        
        if node.type == 'function':
            for i in range(len(self.dict.func_dict)):
                if node.value == self.dict.func_dict[i][0]:
        
                    args = []
                    for j in range(len(node.nodes)):
                        args.append(self.evaluate(node.nodes[j]))
                    return self.dict.func_dict[i][1](*args)
                
            for i in range(len(self.dict.user_functions)):
                
                if node.value == self.dict.user_functions[i][0].name:
                    args = []
                    for j in range(len(node.nodes)):
                        args.append(self.evaluate(node.nodes[j]))
                    return self.dict.user_functions[i][1](self.dict.user_functions[i][0], args)
            
        elif node.type == 'var':
            if node.value.isdigit(): 
                return int(node.value)
            else :
                return node.value
        
    def clear(self):
        self.root = Node()
        
def line_parser(code):
    array = []
    line = ""
    for i in range(len(code)):
        if code[i] != ";":
            line += code[i]
        else : 
            array.append(line)
            line = ""
    return array

def code_interpreter(code, dictionnary):
    lines = line_parser(code)
    tree = AST(dictionnary)
    for i in range(len(lines)):
        tree.parser(lines[i])
        tree.evaluate()
        tree.clear()
        
class CodeNode():
    def __init__(self, code):
        self.function = None #'casual' 'if', 'while'...
        self.code = code
        
        self.nodes = []
        
        self.evaluated = False
        
class UserFunction():
    def __init__(self):
        self.name = None
        self.args = None
        self.node = None #contient le code
        self.dict = Dict()
        
class CodeTree():
    def __init__(self, code, dictionnary):
        self.root = CodeNode(self.first_parser(code))
        self.bloc_types = (("casual", self.casual), 
                           ("ifi", self.ifi), 
                           ("ifs", self.ifs), 
                           ("ife", self.ife), 
                           ("ifn", self.ifn), 
                           ("root", self.casual), 
                           ("whilei", self.whilei))
        
        self.dict = dictionnary
        
    def first_parser(self, code):
        temp = ""
        for i in range(len(code)):
            if code[i] == '\n':
                pass
            elif code[i] == ' ':
                pass
            else : 
                temp += code[i]
        return temp    
                      
    def bloc_parser2(self, node = None):
        #étape 1 : regarder si le bloc est fonctionnalisé (if, while...)
        #etape 2 : passer le sous bloc au noeud
        #étape 3 : recursion sur le sous bloc 
        if node == None:
            node = self.root
            node.function = "root"
        
        if "user_function" in node.function : 
            return
        
        blocs = []
        function = ""
        code = ""
        cr_counter = 0
        
        has_bloc = False
        
        for i in range(len(node.code)):
            if node.code[i] == '[':
                cr_counter += 1
                if cr_counter == 1:
                    has_bloc = True
                    #on néglige le premier crochet
                    continue
                
            elif node.code[i] == ']':
                cr_counter -= 1
                if cr_counter == 0:
                    #quand le niveau de crochet = 0 
                    #on passe la fonction et le code
                    blocs.append((function, code))
                    function = ""
                    code = ""
                    #on néglige le dernier crochet
                    continue
                
            if cr_counter == 0:
                function += node.code[i]
            else : 
                code += node.code[i]
                
        
        
        if not has_bloc:
            #si le bloc de code ne contient pas de bloc
            #on arrete la récursion
            return
                
        for i in range(len(blocs)):
            if blocs[i][1] != "":
                new_node = CodeNode(blocs[i][1])
                if blocs[i][0] == "":
                    new_node.function = "casual"
                else : 
                    new_node.function = blocs[i][0]
                node.nodes.append(new_node)
    

                    
            self.bloc_parser2(new_node)
            if len(node.nodes) > 0:
                node.code = None
                
    def evaluate(self, node = None):
        if node == None:
            node = self.root
            
        exec_bloc = False    
        exec_while = False
        
            
        f = self.bloc_function_parser(node.function)
        function = f[0]
        args = f[1]
        if "user_function" in function:
            
            fo = node.function[14:len(node.function) - 1]
            
            
            user_function_f = self.bloc_function_parser(fo)
  
            new_function = UserFunction() 
            new_function.name = user_function_f[0]
            new_function.args = user_function_f[1]
            new_function.node = node
            
            self.dict.user_functions.append((new_function, self.dict.user_function2))
            
        else : 
            for bloc_type in self.bloc_types:
                if function == bloc_type[0]:
                    if bloc_type[1](*args):
                        exec_bloc = True
                        if function == "whilei":
                            exec_while = True
                      
        if exec_bloc:
            if node.code != None:
 
                code_interpreter(node.code, self.dict)
                    
            for i in range(len(node.nodes)):
                self.evaluate(node.nodes[i])
                
        if exec_while : 
            self.evaluate(node)
            
    def evaluate2(self, node = None):
        if node == None:
            node = self.root
            
            
        exec_bloc = False    
        exec_while = False
            
        f = self.bloc_function_parser(node.function)
        function = f[0]
        args = f[1]
        
            
        
    
        for bloc_type in self.bloc_types:
            if function == bloc_type[0]:
                if bloc_type[1](*args):
                    exec_bloc = True
                    if function == "whilei":
                        exec_while = True
            else : 
                exec_bloc = True
                      
        if exec_bloc:
            if node.code != None:
                code_interpreter(node.code, self.dict)
                    
            for i in range(len(node.nodes)):
                self.evaluate2(node.nodes[i])
                
                
        if exec_while : 
            self.evaluate2(node)
            
    def bloc_function_parser(self, function):
        func = ""
        args = []
        arg = ""
        p = False
        for i in range(len(function)):
            if function[i] == '(':
                p = True
                continue
            elif function[i] == ')':
                continue
            
            if function[i] == ',':
                args.append(arg)
                arg = ""
                continue
            
            if p : 
                arg += function[i]
            else : 
                func += function[i]
            
        if arg != "":
            args.append(arg)
            
        return func, args
    
    def casual(self):
        return True
    
    def ifi(self, a, b):
        if a.isdigit():
            a = int(a)
        else : 
            a = self.dict.call(a)
        if b.isdigit():
            b = int(b)
        else : 
            b = self.dict.call(b)
        return a < b
    
    def ifs(self, a, b):
        if a.isdigit():
            a = int(a)
        else : 
            a = self.dict.call(a)
        if b.isdigit():
            b = int(b)
        else : 
            b = self.dict.call(b)
        return a > b
            
    def ife(self, a, b):
        if a.isdigit():
            a = int(a)
        else : 
            a = self.dict.call(a)
        if b.isdigit():
            b = int(b)
        else : 
            b = self.dict.call(b)
        return a == b
    
    def ifn(self, a, b):
        if a.isdigit():
            a = int(a)
        else : 
            a = self.dict.call(a)
        if b.isdigit():
            b = int(b)
        else : 
            b = self.dict.call(b)
        return a != b
    
    def whilei(self, a, b):
        if a.isdigit():
            a = int(a)
        else : 
            a = self.dict.call(a)
        if b.isdigit():
            b = int(b)
        else : 
            b = self.dict.call(b)
        return a < b

    
    def display_tree(self, node = None):
        if node == None:
            node = self.root
           
        print("\nBLOC\n-----\n")
        print(node.function)
        print(node.code)
        print(len(node.nodes))
        for i in range(len(node.nodes)):
            self.display_tree(node.nodes[i])
        

#les fonctions primaires du langage : 
    #assign -> créé une variable et lui assigne une valeur
    #add -> additionne deux entier ou variables
    #minus -> soustrait deux entiers ou variabels
    #display -> affiche dans la console la valeur d'une variable
    
#les déclarations sont suivies par un ';'
    
    
code0 = """
assign(x, 1);
assign(y, 2);
assign(x, add(x, 1)); 
assign(y, minus(y, x));
display(y);
display(x);
"""

#la mémoire du langage se fait dans une classe Dict()

print("\ncode 0 : les déclarations simples\n")
D = Dict()
code_tree = CodeTree(code0, D)
code_tree.bloc_parser2()
code_tree.evaluate()

#le code est évalué sur deux niveaux.
    #le niveau local, ligne par ligne
    #le niveau global, bloc par bloc.
    
#un bloc de code est délimité par ['bloc de code']
#les blocs de code permettent d'utiliser les conditions 
    #whilei(a, b) -> tant que a < b : executer le bloc de code
    #ifi(a, b) -> si a < b : executer le bloc de code


code1 = """
[assign(i, 0);]
whilei(i, 10)[display(i);assign(i, add(i, 1));]
"""

print("\ncode 1 : les blocs de code\n")
D = Dict()
code_tree = CodeTree(code1, D)
code_tree.bloc_parser2()
code_tree.evaluate()

#les fonctions utilisateur sont des blocs de code.
#comme whilei et ifi, ces blocs doivent être nommé par 
#leur usage. ici user_function().
#à l'interieur des parenthèses de user_function, il est possible de 
#nommer la fonction, définir le nombre d'argument et le nom de ces arguments. 
#la portée des variables utilisées dans une fonction est réstreinte au bloc fonction
#les fonctions utilisateur peuvent appeler d'autres fonctions utilisateurs. 


code2 = """
user_function(mult(a,b))[
    [assign(x, a);
     assign(i, 1);
     assign(out, 0);]
    
    whilei(i, b)[
        assign(i, add(i, 1));
        assign(out, add(out, x));
        ]
    [assign(return, out);]
]

user_function(pow(a))[
    assign(out, mult(a, a));
    assign(return, out);
    ]

[assign(x, mult(3, 4));
 display(x);]

[assign(y, pow(4));
 display(y);]
"""

print("\ncode 2 : les fonctions \n")
D = Dict()
code_tree = CodeTree(code2, D)
code_tree.bloc_parser2()
code_tree.evaluate()













    


