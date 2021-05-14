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

        elif char == ":":
            if self.lookAhead() == "=": # := (atribuição)
                self.atual += 1
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

            elif char == ":" or char == "=" or char == "!" or char == "<" or char == ">":
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
                if i.lexema == "main":
                  i.tipo = "MAIN"

                elif i.lexema == "end":
                  i.tipo = "END"

                # função
                elif i.lexema == "func":
                  i.tipo = "FUNC"
                  
                elif i.lexema == "endfunc":
                    i.tipo = "ENDFUNC"

                # procedimento
                elif i.lexema == "proc":
                  i.tipo = "PROC"

                # chamada de func
                elif i.lexema == "funccall":
                  i.tipo = "FUNCCALL"

                # chamada de proc
                elif i.lexema == "proccall":
                  i.tipo = "PROCCALL"

                # inteiros
                elif i.lexema == "int":
                  i.tipo = "INT"

                # Booleano
                elif i.lexema == "boolean":
                  i.tipo = "BOOLEAN"

                elif i.lexema == "true":
                  i.tipo = "LOGIC"

                elif i.lexema == "false":
                  i.tipo = "LOGIC"

                elif i.lexema == "return":
                  i.tipo = "RETURN"

                elif i.lexema == "if":
                    i.tipo = "IF"

                elif i.lexema == "endif":
                    i.tipo = "ENDIF"
                
                elif i.lexema == "else":
                    i.tipo = "ELSE"
                
                elif i.lexema == "endelse":
                    i.tipo = "ENDELSE"
               
                elif i.lexema == "while":
                    i.tipo = "WHILE"    
                
                elif i.lexema == "endwhile":
                    i.tipo = "ENDWHILE"          

                # Print
                elif i.lexema == "abdullah":
                    i.tipo = "PRINT"

                elif i.lexema == "break":
                    i.tipo = "BREAK"

                elif i.lexema == "continue":
                    i.tipo = "CONTINUE"

    def lookAhead(self):
        if self.atual < len(self.programa):
            return self.programa[self.atual]
        else:
            return "\0"
