from Lexer.Scanner import Scanner
import sys
if __name == "__main__":
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

else:
  print("Executado como um módulo")
