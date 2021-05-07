from Lexer.Scanner import Scanner
import sys
from Parser.Parser import Parser
if __name__ == "__main__":
    path = sys.argv[1]
    try:
      fonte = open(path, 'r')
      programa = ''.join(fonte.readlines())
      fonte.close()
    except Exception:
      print("Código Fonte não encontrado")
      sys.exit(1)

    lexer = Scanner(programa)

    tabTokens = lexer.scan()
    for i in tabTokens:
        print(i)

    parser = Parser(tabTokens)

    try:
      parser.start()
    except Exception as e:
        print(e)


else:
  print("Executado como um módulo")
