class Parser:
  def __init__(self, tabTokens):
    self.tabTokens = tabTokens
    self.indexToken = 0
    self.indexLookAhead = 0
    self.indexEscopoAtual = -1
    self.tabSimbolos = []

  def tokenAtual(self):
    return self.tabTokens[self.indexToken]
  def tokenLookAhead(self):
      self.indexLookAhead = self.indexToken + 1
      return self.tabTokens[self.indexLookAhead]

  def start(self):
    escopoPai = self.indexEscopoAtual #( começa com -1)
    self.indexEscopoAtual +=1
    self.statementList() # Sintática
    return

  def statementList(self):
    if self.tokenAtual().tipo == "END":
      return
    else:
      self.statement()
      self.statementList()
      return
      
  def statement(self):
    if self.tokenAtual().tipo == "MAIN":
      self.indexToken += 1
      if self.tokenAtual().tipo == "INIDEL":
        self.indexToken +=1

       # while self.tokenAtual().tipo != "FINDEL":
          #self.blockStatement()
        #if self.tokenAtual().tipo == "FINDEL":
          #self.indexToken +=1
       
        #if self.tokenAtual().tipo == "END":
          #print("\nFIM DA ANÁLISE SINTÁTICA - TUDO CERTO)\n")
        #else:
            #raise Exception(
             #   "Erro sintático: falta do end na linha", str(self.tokenAtual().linha)
            #)

        while self.tokenAtual().tipo != "END":
          self.blockStatement()
        
        if self.tokenAtual().tipo == "END":
          print("\nFIM DA ANÁLISE SINTÁTICA - Falta análisar o resto dos tokens\n")
        else:
            raise Exception(
                "Erro sintático: falta do end na linha", str(self.tokenAtual().linha)
            )

        #else:
         # raise Exception("Erro sintático na linha", str(self.tokenAtual().linha))

      else:
         raise Exception("Erro sintático: faltando INIDEL na linha", str(self.tokenAtual().linha))

    else:
      raise Exception("Erro sintático na linha", str(self.tokenAtual().linha))
  
  def blockStatement(self):
    #self.indexToken +=1
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.variable_definition(temp)      
      return temp

    if self.tokenAtual().tipo == "IF":
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.if_statement(temp)
      return temp
    
    self.indexToken +=1
    return

  def variable_definition(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      temp.append(self.tokenAtual().lexema)
      self.indexToken += 1
      if self.tokenAtual().tipo == "ATB":
        temp.append(self.tokenAtual().lexema)
        self.indexToken += 1
        tempEndVar = []
        self.type_var(tempEndVar)
        temp.append(tempEndVar)
      else:
          raise Exception(
              "Erro sintático: falta atribuição na linha",
              str(self.tokenAtual().linha)
          )
    else:
          raise Exception(
              "Erro sintático: falta ID na linha",
              str(self.tokenAtual().linha)
          )

  def type_var(self, tempEndVar):
    #bool
        if self.tokenAtual().tipo == "LOGIC":
            if (
                self.tokenAtual().lexema == "true"
                or self.tokenAtual().lexema == "false"
            ):
                tempEndVar.append(self.tokenAtual().lexema)
                self.indexToken += 1
                return
            else:
                raise Exception(
                    "Erro sintático. boolean atribuido errado na linha",
                  str(self.tokenAtual().linha)
                )
        else:
            raise Exception(
                "Erro sintático: atribuição de variavel errada na linha",
                str(self.tokenAtual().linha)
            )

  def boolean_expression(self, tempExpression):
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM":
      tempExpression.append(self.tokenAtual().lexema)
      self.indexToken += 1
      if(
        self.tokenAtual().tipo == "EQUAL"
        or self.tokenAtual().tipo == "DIF"
        or self.tokenAtual().tipo == "LESSEQUAL"
        or self.tokenAtual().tipo == "LESS"
        or self.tokenAtual().tipo == "GREATEREQUAL"
        or self.tokenAtual().tipo == "GREATER"
      ):
        tempExpression.append(self.tokenAtual().lexema)
        self.indexToken += 1
        if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM" or self.tokenAtual().tipo == "LOGIC":
          tempExpression.append(self.tokenAtual().lexema)
          self.indexToken +=1
          return tempExpression
        else:
          raise Exception(
              "Erro sintático: falta do ID na linha",
              str(self.tokenAtual().linha)
          )
      else:
        raise Exception(
            "Erro sintático: falta do operador booleano na linha",
            str(self.tokenAtual().linha)
        )

    else:
      raise Exception(
        "Erro sintático: falta do ID na linha",
        str(self.tokenAtual().linha)
      )

  def if_statement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      tempExpression = []
      tempExpression = self.boolean_expression(tempExpression)
      temp.append(tempExpression)

      if self.tokenAtual().tipo == "PRIGHT":
        lookAhead = self.tokenLookAhead()
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL":# and lookAhead.tipo != "FINDEL":
          self.indexToken +=1
          self.indexEscopoAtual +=1
          tempBlock = []
         
          while(self.tokenAtual().tipo != "FINDEL"):
            tempBlock.append(self.blockStatement3())
            temp.append(tempBlock)

          if self.tokenAtual().tipo == "FINDEL":            
            temp.append(self.tokenAtual().tipo)
            self.indexToken += 1

            tempElse = []
            if self.tokenAtual().tipo == "ELSE":
              tempElse.append(self.indexEscopoAtual)
              tempElse.append(self.tokenAtual().tipo)
              tempElse = self.else_part_statement(tempElse)
            else:
              temp.append(tempElse)
              self.tabTokens.append(temp)
              self.indexEscopoAtual -=1
              return
          else:
            raise Exception(
              "Erro sintático: falta do FINDEL na linha",
              str(self.tokenAtual().linha)
            )
        else:
          raise Exception(
              "Erro sintatico: falta do INIDEL ou bloco vazio na linha "
              + str(self.tokenAtual().linha)
          )

      else:
        raise Exception(
            "Erro sintático: falta do Parêntese direito na linha",
            str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do Parentese esquerdo na linha ",
          str(self.tokenAtual().linha)
      )

  def else_part_statement(self, tempElse):
    lookAhead = self.tokenLookAhead()
    self.indexToken += 1
    if self.tokenAtual().tipo == "INIDEL" and lookAhead != "FINDEL":      
      tempElse.append(self.tokenAtual().tipo)
      self.indexToken += 1
      return tempElse
    else:
      raise Exception(
          "Erro sintático: falta do INIDEL ou bloco vazio na linha",
          str(self.tokenAtual().linha)
      )

  def blockStatement3(self):
    if self.tokenAtual().tipo == "PRINT":
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.print_statement(temp)
      return temp
    else:      
      self.indexToken += 1
      return

    #else:      
     # raise Exception(
      #    "Erro sintático: bloco vazio na linha",
       #   str(self.tokenAtual().linha)
      #)

  def print_statement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      tempParams = []
      temp.append(self.params_print_statement(tempParams))


    else:
      raise Exception(
          "Erro sintático: falta do Parentese esquerdo na linha",
          str(self.tokenAtual().linha)
      )

  def params_print_statement(self, tempParams):
    self.indexToken += 1
    if(
       (self.tokenAtual().tipo == "NUM")
            or (self.tokenAtual().tipo == "BOOLEAN")
            or (self.tokenAtual().tipo == "ID")
    ):
      tempParams.append(self.tokenAtual().lexema)
      self.indexToken += 1
      if (
          self.tokenAtual().tipo == "ADD"
          or self.tokenAtual().tipo == "SUB"
          or self.tokenAtual().tipo == "MULT"
          or self.tokenAtual().tipo == "DIV"
      ):
          tempParams.append(self.tokenAtual().lexema)
          self.call_op_statement(tempParams)
          return tempParams
      else:
          return tempParams
    else:
      raise Exception(
        "Erro sintático: uso incorreto dos parâmetros na linha",
        str(self.tokenAtual().linha)
      )
  
  def call_op_statement(self, tempEndVar):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM":
        tempEndVar.append(self.tokenAtual().lexema)
        self.indexToken += 1
        if (
            self.tokenAtual().tipo == "ADD"
            or self.tokenAtual().tipo == "SUB"
            or self.tokenAtual().tipo == "MULT"
            or self.tokenAtual().tipo == "DIV"
        ):
            tempEndVar.append(self.tokenAtual().lexema)
            self.call_op_statement(tempEndVar)            
        else:
            return
    else:
        raise Exception(
          "Erro sintático: falta do ID na linha",
          str(self.tokenAtual().linha)
        )