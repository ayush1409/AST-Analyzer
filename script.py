# Helper script to run the ast_analyser tool

import json, sys
from ast import parse
from source.ast2json.ast2json import ast2json   
from source.ast_analyser import Ast_analyzer     # getting the ast_analyser tool 

input_file = sys.argv[1]

# generating the Abstract Syntax Tree using ast2json module
ast = ast2json(parse(open(input_file).read()))

# Create an instance of tool to use it
ast_analyzer = Ast_analyzer()
ast_analyzer.ast_visitor(ast)

print('\nAssignment Statements: ')
print(*ast_analyzer.assign, sep='\n')
print('\n')

print('Branch Conditions: ')
print(*ast_analyzer.conditionals, sep='\n')
print('\n')

print('Loop Conditions:')
print(*ast_analyzer.loops, sep='\n')
print('\n')

# json_ast = json.dumps(ast)
# gives the the raw json in string form (for analysis purposes only)