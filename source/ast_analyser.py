# Author : Ayush Singh
# Date : 22/08/2021

class Ast_analyzer():
    
    def __init__(self):
        self.assign = []
        self.conditionals = []
        self.loops = []
        self.opDict = {  'Sub' : '-', 'Mult' : '*', 'Add' : '+', 'Div' : '/', 'Mod' : '%', 'Lt' : '<', 
                        'Gt' : '>', 'Eq' : '==', 'LtE' : '<=', 'GtE' : '>=', 'NotEq' : '!=', 'FloorDiv' : '//', 
                       'Pow' : '**', 'And' : 'and', 'Or' : 'or'}
        self.unaryOp = {'Not' : 'not'}
        
    def ast_visitor(self, node):
        
        result = ''     # stores the value returned by the node
    
        # If we have a list of nodes to traverse, call ast_visitor() function one by one for each node.
        if isinstance(node, list):
            for item in node:
                self.ast_visitor(item)

        elif isinstance(node, dict):
            for key, value in node.items():

                # If the child has list of elements
                if isinstance(value, list):
                    self.ast_visitor(value)

                if key == '_type' :

                    # current node is an assignment node
                    if value == 'Assign':                           
                        left = self.ast_visitor(node['targets'][0])      # LHS of assignment
                        right = self.ast_visitor(node['value'])          # RHS of assignment
                        result = str(left) + ' = ' + str(right) 
                        self.assign.append(result)

                    # current node is an shorthand assignment for example, a += b    
                    elif value == 'AugAssign':
                        left = self.ast_visitor(node['target'])
                        right = self.ast_visitor(node['value'])
                        op = self.opDict[node['op']['_type']]
                        result = str(left) + ' ' + op + '= ' + str(right)
                        self.assign.append(result)
                    
                    # current node is a Unary operator
                    elif value == 'UnaryOp':
                        op = self.unaryOp[node['op']['_type']]
                        operand = self.ast_visitor(node['operand'])
                        result = str(op) + ' ' + str(operand)

                    elif value == 'Name':
                        result = node['id']

                    elif value == 'Constant':
                        result = node['value']

                    # current node is a binary operation node
                    elif value == 'BinOp':                          # binary operation format: a op b
                        a = self.ast_visitor(node['left'])
                        b = self.ast_visitor(node['right'])
                        result = str(a) + ' ' + self.opDict[node['op']['_type']] + ' ' + str(b)

                    # current node is a boolean operator    
                    elif value == 'BoolOp':
                        operands = []
                        op = self.opDict[node['op']['_type']]
                        for item in node['values']:
                            operands.append(self.ast_visitor(item))
                        result = (' ' + str(op) + ' ').join(operands)   # joining all operands using the Bool oerator between them

                    # current node is a If conditional node
                    elif value == 'If':
                        result = self.ast_visitor(node['test'])
                        self.conditionals.append(result)

                    # current node is a comarision operation
                    elif value == 'Compare':                        # Comparision operation format: a cmp b
                        b = self.ast_visitor(node['comparators'][0])
                        a = self.ast_visitor(node['left'])
                        result = str(a) + ' ' + self.opDict[node['ops'][0]['_type']] + ' ' + str(b)

                    # current node is a 'while' loop
                    elif value == 'While':
                        result = self.ast_visitor(node['test'])
                        self.loops.append(result)

                    # current node is a 'for' loop
                    elif value == 'For':
                        iteration = self.ast_visitor(node['iter'])       # values traversed by the iterator in the current loop
                        iterator = self.ast_visitor(node['target'])      # stores the iterator
                        result = str(iterator) + ' in ' + str(iteration)
                        self.loops.append(result)

                    # current node is a callable
                    elif value == 'Call':
                        name = self.ast_visitor(node['func'])            # to get the name of called function
                        name += '('
                        args = []                                   # list that stores all arguments passed inside the function 
                        for arg in node['args']:
                            args.append(str(self.ast_visitor(arg)))

                        if args is None:
                            name += ')'
                        else:
                            for arg in args:
                                if arg != args[-1]:
                                    name += (arg + ', ')
                                else:
                                    name += arg
                            name += ')'
                        result = name
                    
                    # current node a list datatype
                    elif value == 'List':
                        elements = '['
                        for element in node['elts']:
                            if element != node['elts'][-1]:
                                elements += str(self.ast_visitor(element)) + ', '
                            else:
                                elements += str(self.ast_visitor(element))
                        elements += ']'
                        result = elements
                        
                    # current node is a ditionary datatype
                    elif value == 'Dict':
                        elements = '{'
                        k_v_pairs = list(zip(node['keys'], node['values']))
                        for k,v in k_v_pairs:
                            a = self.ast_visitor(k)
                            b = self.ast_visitor(v)
                            elements += str(str(a) + ' : ' + str(b) + ' ,')
                        elements = elements[:-2]
                        elements += '}'
                        result = elements
                        
                    # current node is a set datatype    
                    elif value == 'Set':
                        elements = '{'
                        for element in node['elts']:
                            if element != node['elts'][-1]:
                                elements += str(self.ast_visitor(element)) + ', '
                            else:
                                elements += str(self.ast_visitor(element))
                        elements += '}'
                        result = elements
                    
                    # current node is a tuple datatype
                    elif value == 'Tuple':
                        elements = '('
                        for element in node['elts']:
                            if element != node['elts'][-1]:
                                elements += str(self.ast_visitor(element)) + ', '
                            else:
                                elements += str(self.ast_visitor(element))
                        elements += ')'
                        result = elements
                    
                    # current node stores function definition
                    elif value == 'FunctionDef':
                        self.ast_visitor(node['body'])
                    
                    # current node stores array(or list) indexing value
                    elif value == 'Subscript':
                        idx = self.ast_visitor(node['slice']['value'])
                        arr = self.ast_visitor(node['value'])
                        result = str(arr) + '[' + str(idx) + ']'

        return result     