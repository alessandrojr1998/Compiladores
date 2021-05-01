from Lexer.Token import Token


class Scanner:
    # Construtor
    def __init__(self, programa):
        self.tokens = []
        self.programa = programa
        self.inicio = 0
        self.atual = 0
        self.linha = 1

    def nextChar(self):
        self.atual += 1
        return self.programa[self.atual - 1]

    def scan(self):
        self.scanTokens()
        self.scanReserved()
        return self.tokens

    def delimitadoresToken(self, char):        
        if char == "(":  # Parentese esquerdo
            return "PLEFT"

        elif char == ")":  # Parentese direito
            return "PRIGHT"

        elif char == "{":  # Chaves esquerdo
            return "INIDEL"

        elif char == "}":  # Chaves direito
            return "FINDEL"

    def opAritmeticaToken(self, char):
        # Operações Aritméticas
        if char == "+":  # Soma
            return "ADD"

        elif char == "-":  # Subtração
            return "SUB"

        elif char == "*":  # Multiplicação
            return "MULT"

        elif char == "/":  # Divisão
            return "DIV"

    def opBolleanaToken(self, char):
      # Operações Booleanas
      if char == "=":  # Igual ou Atribuição
          if self.lookAhead() == "=":  # == (comparação)
              self.atual += 1
              return "EQUAL"

          else:  # = (atribuição)
              return "ATB"

      elif char == "!":  # Diferente ("!=")
          if self.lookAhead() == "=":
              self.atual += 1
              return "DIF"

      elif char == "<":  # Menor ou igual, menor
          if self.lookAhead() == "=":  # ("<= ")
              self.atual += 1
              return "LESSEQUAL"

          else:  # ("<")
              return "LESS"

      elif char == ">":  # Maior ou igual, Maior
          if self.lookAhead() == "=":  # (">=")
              self.atual += 1
              return "GREATEREQUAL"
          else:  # (">")
              return "GREATER"

    # Procura tokens até chegar no Fim
    def scanTokens(self):
        while self.atual < len(self.programa):
            self.inicio = self.atual
            char = self.nextChar()

            if char == " " or char == "\t" or char == "\r":
              pass
            elif char == "\n":
              self.linha += 1

            elif char == "(" or char == ")" or char == "{" or char == "}":
                self.tokens.append(
                    Token(
                        self.delimitadoresToken(char),
                        self.programa[self.inicio : self.atual],
                        self.linha,
                    )
                )

            elif char == "+" or char == "-" or char == "*" or char == "/":
                self.tokens.append(
                    Token(
                        self.opAritmeticaToken(char),
                        self.programa[self.inicio : self.atual],
                        self.linha,
                    )
                )

            elif char == "=" or char == "!" or char == "<" or char == ">":
                self.tokens.append(
                    Token(
                        self.opBolleanaToken(char),
                        self.programa[self.inicio : self.atual],
                        self.linha,
                    )
                )

            # Separador
            elif char == ",": 
                self.tokens.append(
                    Token("COMMA", self.programa[self.inicio : self.atual], self.linha)
                )

            # Fim de bloco 
            elif char == ";": 
                self.tokens.append(
                    Token(
                        "SEMICOLON", self.programa[self.inicio : self.atual], self.linha
                    )
                )

            # Números
            elif char >= "0" and char <= "9":
                while self.lookAhead() >= "0" and self.lookAhead() <= "9":
                    self.nextChar()
                self.tokens.append(
                    Token("NUM", self.programa[self.inicio : self.atual], self.linha)
                )

            # Letras / Identificadores / Palavras Reservadas
            elif char.isalpha():
                while self.lookAhead().isalnum():
                    self.nextChar()
                self.tokens.append(
                    Token("ID", self.programa[self.inicio : self.atual], self.linha)
                )

            # Outros
            else:
                print("Caractere inválido na linha ", self.linha)
                exit(2)

   

    def scanReserved(self):
        for i in self.tokens:
            if i.tipo == "ID":
                # Inicio do programa
                if i.lexema == "program":
                  i.tipo = "PROGRAM"

                # Fim do programa
                elif i.lexema == "end":
                  i.tipo = "END"

                # Identificador de função
                elif i.lexema == "func":
                  i.tipo = "FUNC"

                # Identificador de procedimento
                elif i.lexema == "proc":
                  i.tipo = "PROC"

                # Identificador de chamada para func
                elif i.lexema == "funccall":
                  i.tipo = "FUNCCALL"

                # Identificador de chamada para proc
                elif i.lexema == "proccall":
                  i.tipo = "PROCCALL"

                # Identificador de inteiros
                elif i.lexema == "int":
                  i.tipo = "INT"

                # Tipo Booleano
                elif i.lexema == "logic":
                  i.tipo = "LOGIC"

                # Booleano Verdadeiro
                elif i.lexema == "True":
                  i.tipo = "BOOLEAN"

                # Booleano Falso
                elif i.lexema == "False":
                  i.tipo = "BOOLEAN"

                # Retorno da função
                elif i.lexema == "return":
                  i.tipo = "RETURN"

                # Condicional IF
                elif i.lexema == "if":
                    i.tipo = "IF"

                # Condicional ELSE
                elif i.lexema == "else":
                    i.tipo = "ELSE"
               
                # Condicional WHILE
                elif i.lexema == "while":
                    i.tipo = "WHILE"              

                # Escrita na tela
                elif i.lexema == "abdullah":
                    i.tipo = "ABDULLAH"

                # Incondicional BREAK
                elif i.lexema == "break":
                    i.tipo = "BREAK"

                # Incondicional CONTINUE
                elif i.lexema == "continue":
                    i.tipo = "CONTINUE"

       # Verifica o simbolo a frente e se está no final do programa
    def lookAhead(self):
        if self.atual < len(self.programa):
            return self.programa[self.atual]
        else:
            return "\0"
