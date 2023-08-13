# compiladores-10.08.23
Para testar esse repositório, basta rodar python main.py no terminal

### Tutorial: ANTLR Usando Python

### Parte 1: Configurando o Ambiente

#### 1.1 Java

ANTLR depende de Java, então o Java Development Kit (JDK) deve ser instalado primeiro.

- Baixe o JDK do site oficial.
- Siga as instruções para instalar no seu sistema operacional específico.

#### 1.2 ANTLR

- Baixe o arquivo jar do ANTLR no site oficial.
- Mova o arquivo jar para um diretório (por exemplo, `~/antlr4`).
- Adicione o ANTLR ao PATH do sistema (possível exemplo a seguir, adapte de acordo com seu sistema operacional):
  ```bash
  export CLASSPATH=".:/usr/local/lib/antlr-4.x-complete.jar:$CLASSPATH"
  alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.x-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
  alias grun='java -Xmx500M -cp "/usr/local/lib/antlr-4.x-complete.jar:$CLASSPATH" org.antlr.v4.gui.TestRig'
  ```

#### 1.3 Instalando a Runtime do ANTLR em Python

- *Opcional, mas recomendado:* Crie um ambiente virtual para o seu projeto.
- Instale a runtime do ANTLR em Python via pip:
  ```bash
  pip install antlr4-python3-runtime
  ```

### Parte 2: Criando uma Gramática para Expressões Aritméticas

#### 2.1 Defina a Gramática

Crie um arquivo chamado `Arithmetic.g4` e escreva a seguinte gramática:

```antlr
grammar Arithmetic;

// Regras do Parser
expr: term ( (PLUS | MINUS) term )* ;
term: factor ( (MUL | DIV) factor )* ;
factor: INT | LPAREN expr RPAREN ;

// Regras do Lexer
PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
INT: [0-9]+ ;
LPAREN: '(' ;
RPAREN: ')' ;
WS: [ \t\r\n]+ -> skip ;
```

#### 2.2 Gere o Parser e o Lexer

Execute o seguinte comando para gerar o código do parser e do lexer:

```bash
antlr4 -Dlanguage=Python3 Arithmetic.g4
```

### Parte 3: Escrevendo o Programa Principal

Crie um arquivo Python chamado `main.py` com o seguinte código:

```python
from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor(ParseTreeVisitor):
    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i*2-1).getText() == '+':
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i*2-1).getText() == '*':
                result *= self.visit(ctx.factor(i))
            else:
                result /= self.visit(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        else:
            return self.visit(ctx.expr())

def main():
    expression = input("Digite uma expressão aritmética: ")
    lexer = ArithmeticLexer(InputStream(expression))
    stream = CommonTokenStream(lexer)
    parser = ArithmeticParser(stream)
    tree = parser.expr()
    visitor = ArithmeticVisitor()
    result = visitor.visit(tree)
    print("Resultado:", result)

if __name__ == '__main__':
    main()
```

### Parte 4: Executando o Programa

Execute o programa `main.py`:

```bash
python main.py
```

Agora você pode inserir expressões aritméticas, e o programa avaliará e imprimirá o resultado.

### Exercício: Evoluindo a Gramática Aritmética

**Objetivo:** Evoluir a gramática para suportar variáveis, atribuições e um ambiente REPL (Read-Eval-Print Loop) simples. Isso permitirá explorar como lidar com o estado dentro da gramática e como construir um interpretador mais interativo.

**Instruções:**

1. **Evolua a Gramática:** Modifique o arquivo `Arithmetic.g4` para incluir regras para variáveis e atribuições. Eis um ponto de partida:

   ```antlr
   // Novas Regras do Parser
   program: statement+ ;
   statement: assignment | expr ;
   assignment: VAR ASSIGN expr ;
   
   // Novas Regras do Lexer
   VAR: [a-zA-Z]+ ;
   ASSIGN: '=' ;
   ```

2. **Modifique o Visitante:** Atualize a classe `ArithmeticVisitor` para lidar com variáveis e atribuições. Você precisará armazenar variáveis em um dicionário e atualizá-las conforme as atribuições forem feitas.

3. **Implemente um REPL:** Modifique o programa principal para ler e avaliar instruções em um loop, imprimindo os resultados das expressões e permitindo que as variáveis persistam entre as entradas.

4. **Teste a nova gramática:** Forneça exemplos que demonstrem a nova funcionalidade, como:
   ```plaintext
   x = 5
   y = x + 3
   y * 2
   ```

**Critérios de Avaliação:**

- Implementação correta das novas regras da gramática.
- Tratamento adequado de variáveis e atribuições.
- Implementação de um ambiente REPL funcional.
- Organização do código, clareza e aderência às melhores práticas de programação.

**Desafio Bônus:** Evolua ainda mais a gramática para suportar construções mais complexas, como expressões condicionais (`if`/`else`), loops ou funções.
