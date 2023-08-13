from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor(ParseTreeVisitor):
    def __init__(self) -> None:
        super().__init__()
    
    def visitProgram(self, ctx, variables) -> dict:
        self.variables = variables
        for i in range(len(ctx.statement())):
            self.visitStatement(ctx.statement(i))
        return self.variables

    def visitStatement(self, ctx):
        if ctx.assignment():
            return self.visitAssignment(ctx.assignment())
        else:
            return self.visitExpr(ctx.expr(), True)

    def visitAssignment(self, ctx):
        self.variables[ctx.VAR().getText()] = self.visitExpr(ctx.expr(), False)
        print(f'{ctx.VAR().getText()} = {self.variables[ctx.VAR().getText()]}')
        return None

    def visitExpr(self, ctx, opr: bool):
        result = self.visitTerm(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i*2-1).getText() == '+':
                result += self.visitTerm(ctx.term(i))
            else:
                result -= self.visitTerm(ctx.term(i))
        if opr:
            print(result)
        return result

    def visitTerm(self, ctx):
        result = self.visitFactor(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i*2-1).getText() == '*':
                result *= self.visitFactor(ctx.factor(i))
            else:
                result /= self.visitFactor(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            return int(self.variables[ctx.VAR().getText()])
        else:
            return self.visitExpr(ctx.expr(), False)

def main():
    result = dict()
    expression = ''
    print('Digite exit para sair do programa')
    while expression != 'exit':
        expression = input("Digite uma expressão aritmética: ")
        if expression != 'exit':
            lexer = ArithmeticLexer(InputStream(expression))
            stream = CommonTokenStream(lexer)
            parser = ArithmeticParser(stream)
            tree = parser.program()
            visitor = ArithmeticVisitor()
            result = visitor.visitProgram(tree, result)

if __name__ == '__main__':
    main()