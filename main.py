from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor(ParseTreeVisitor):
    def visitExpr(self, ctx):
        result = self.visitTerm(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i*2-1).getText() == '+':
                result += self.visitTerm(ctx.term(i))
            else:
                result -= self.visitTerm(ctx.term(i))
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
        else:
            return self.visitExpr(ctx.expr())

def main():
    expression = input("Digite uma expressão aritmética: ")
    lexer = ArithmeticLexer(InputStream(expression))
    stream = CommonTokenStream(lexer)
    parser = ArithmeticParser(stream)
    tree = parser.expr()
    visitor = ArithmeticVisitor()
    result = visitor.visitExpr(tree)
    print("Resultado:", result)

if __name__ == '__main__':
    main()