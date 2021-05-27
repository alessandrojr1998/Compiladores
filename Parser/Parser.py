class Parser:
  def __init__(self, tabTokens):
    self.tabTokens = tabTokens
    self.indexToken = 0
    self.indexLookAhead = 0
    self.tabelaDeSimbolos = []
    self.indexEscopoAtual = -1
    self.indexEscopoAntesDaFuncao = 0

  def tokenAtual(self):
    return self.tabTokens[self.indexToken]
  
  def tokenLookAhead(self):
      self.indexLookAhead = self.indexToken + 1
      return self.tabTokens[self.indexLookAhead]

  def start(self):
    escopoPai = self.indexEscopoAtual
    self.indexEscopoAtual += 1
    self.statementList()
    
    for linha in self.tabelaDeSimbolos:
      print(linha)
    return

  def statementList(self):
    if(len(self.tabTokens) != 0):
      if self.tokenAtual().tipo == "END":
        return
      else:
        self.statement()
        self.statementList()
        return
    else:
      raise Exception(
        "Erro sintático: falta do main."
      )
      
  def statement(self):    
    if self.tokenAtual().tipo == "MAIN":
      self.indexToken += 1
      if self.tokenAtual().tipo == "INIDEL":
        self.indexToken +=1
        
        while self.tokenAtual().tipo != "FINDEL":
          self.blockStatement()
        if self.tokenAtual().tipo == "FINDEL":
          self.indexToken +=1        
          try:
            if self.tokenAtual().tipo == "END":
              print("\nAnálise Sintática Finalizada\n")
            else:
                raise Exception(
                "Erro sintático: falta do end na linha "+ str(self.tokenAtual().linha)
                )
          except Exception:
            raise Exception(
                "Erro sintático: falta do end no final do código"
                )
            
      else:
         raise Exception("Erro sintático: faltando INIDEL na linha "+ str(self.tokenAtual().linha))

    else:
      raise Exception("Erro sintático na linha " + str(self.tokenAtual().linha))
  
  def blockStatement(self, isWhile = False, isIf = False):  
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":    
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)  
      self.variableDefinition(temp)           
      return temp

    #até aqui ok
    if self.tokenAtual().tipo == "IF":
      if isWhile:
        temp = []
        temp.append(self.indexEscopoAtual)
        temp.append(self.tokenAtual().linha)
        temp.append(self.tokenAtual().tipo)
        self.ifStatementWhile(temp)
        return temp
      else:
        temp = []
        temp.append(self.indexEscopoAtual)
        temp.append(self.tokenAtual().linha)
        temp.append(self.tokenAtual().tipo)
        self.ifStatement(temp)
        return temp
    
    if self.tokenAtual().tipo == "PRINT":
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.printStatement(temp)
      return temp
    
    if self.tokenAtual().tipo == "WHILE":
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.whileStatement(temp)
      return 
    
    if self.tokenAtual().tipo == "ID":
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      temp.append(self.tokenAtual().lexema)
      self.callVarStatement(temp)
      return temp

    if self.tokenAtual().tipo == "FUNC":
      if not(isIf):
        temp = []
        temp.append(self.indexEscopoAtual)
        temp.append(self.tokenAtual().linha)
        temp.append(self.tokenAtual().tipo)
        self.declarationFuncStatement(temp)
        return temp
      else:
        raise Exception(
          "Erro sintático: declaração de função não permitida no bloco do if/else na linha " +
          str(self.tokenAtual().linha)
          ) 
    if self.tokenAtual().tipo == "PROC":  
      if not(isIf):
        temp = []
        temp.append(self.indexEscopoAtual)
        temp.append(self.tokenAtual().linha)
        temp.append(self.tokenAtual().tipo)
        temp = self.declarationProcStatement(temp)
        self.tabelaDeSimbolos.append(temp)
        return
      else:
        raise Exception(
          "Erro sintático: declaração de procedimento não permitida no bloco do if/else na linha " +
          str(self.tokenAtual().linha)
          )
    if self.tokenAtual().tipo == "PROCCALL":      
      self.callProc()
      return
    
    if self.tokenAtual().tipo == "BREAK" or self.tokenAtual().tipo == "CONTINUE":
      if isWhile:
        self.indexToken += 1
        return 
      else:
        if self.tokenAtual().tipo == "BREAK":
          raise Exception(
            "Erro sintático: BREAK chamado fora de um laço linha " +
            str(self.tokenAtual().linha)
            )    
        elif self.tokenAtual().tipo == "CONTINUE":
          raise Exception(
            "Erro sintático: CONTINUE chamado fora de um laço linha " +
            str(self.tokenAtual().linha)
            )         
    self.indexToken +=1
    return

  def variableDefinition(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      temp.append(self.tokenAtual().lexema)
      self.indexToken += 1
      if self.tokenAtual().tipo == "ATB":
        temp.append(self.tokenAtual().lexema)
        self.indexToken += 1
        tempEndVar = []
        if self.tokenAtual().tipo == "FUNCCALL":          
          self.callFunc(tempEndVar)        
        else:        
          self.typeVar(tempEndVar)
        temp.append(tempEndVar)
      else:
          raise Exception(
              "Erro sintático: falta atribuição na linha " +
              str(self.tokenAtual().linha)
          )
    else:
          raise Exception(
              "Erro sintático: falta ID na linha " +
              str(self.tokenAtual().linha)
          )

  def typeVar(self, tempEndVar):
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
              "Erro sintático. boolean atribuido errado na linha " +
            str(self.tokenAtual().linha)
          )
    if self.tokenAtual().tipo == "NUM":
      tempEndVar.append(self.tokenAtual().lexema)
      self.indexToken += 1      
      if (
          self.tokenAtual().tipo == "ADD"
          or self.tokenAtual().tipo == "SUB"
          or self.tokenAtual().tipo == "MULT"
          or self.tokenAtual().tipo == "DIV"
      ):
          tempEndVar.append(self.tokenAtual().lexema)
          self.callOpStatement(tempEndVar)
          return
      else:
          return
    if self.tokenAtual().tipo == "ID":
      tempEndVar.append(self.tokenAtual().lexema)
      self.indexToken += 1
      # <call_op>
      if (
          self.tokenAtual().tipo == "ADD"
          or self.tokenAtual().tipo == "SUB"
          or self.tokenAtual().tipo == "MULT"
          or self.tokenAtual().tipo == "DIV"
      ):
        print("ashui", self.tokenAtual().lexema)
        tempEndVar.append(self.tokenAtual().lexema)
        self.callOpStatement(tempEndVar)
        return
      else:
          return    

    else:
      raise Exception(
        "Erro sintático: atribuição de variavel errada na linha " +
        str(self.tokenAtual().linha)
      )

  def booleanExpression(self, tempExpression):
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM" or self.tokenAtual().tipo == "LOGIC":
      tempExpression.append(self.tokenAtual().lexema)
      if(self.tokenAtual().tipo == "LOGIC" and self.tokenAtual().lexema != 'false'):
        self.indexToken += 1
        tempExpression.append(self.tokenAtual().lexema)
        if self.tokenAtual().tipo == "PRIGHT":
          self.indexToken += 1
          return 
        else:
          raise Exception(
            "Erro sintático: falta do parêntese direito na linha "+
            str(self.tokenAtual().linha)
        )
      elif(self.tokenAtual().tipo == "LOGIC" and self.tokenAtual().lexema == 'false'):
        raise Exception(
          "Erro sintático: a condição do while não pode ser false, na linha "+
          str(self.tokenAtual().linha)
      )
          
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
              "Erro sintático: falta do ID na linha " +
              str(self.tokenAtual().linha)
          )      
      else:
        raise Exception(
            "Erro sintático: falta do operador booleano na linha " +
            str(self.tokenAtual().linha)
        )
     
    else:
      raise Exception(
        "Erro sintático: falta do ID na linha " +
        str(self.tokenAtual().linha)
      )

  def ifStatement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      tempExpression = []
      tempExpression = self.booleanExpression(tempExpression)
      temp.append(tempExpression)

      if self.tokenAtual().tipo == "PRIGHT":
        lookAhead = self.tokenLookAhead()
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL" and lookAhead.tipo != "FINDEL":
          self.indexToken +=1
          self.indexEscopoAtual += 1
          tempBlock = []
          
          while(self.tokenAtual().tipo != "FINDEL"
              and self.tokenLookAhead().tipo != "ENDIF"):
            tempBlock.append(self.blockStatement(isIf=True))        
            
          temp.append(tempBlock)  
          
          if self.tokenAtual().tipo == "FINDEL":    
            self.indexToken += 1
            if self.tokenAtual().tipo == "ENDIF":
              temp.append(self.tokenAtual().tipo)
              self.indexToken += 1
              
              tempElse = []
              if self.tokenAtual().tipo == "ELSE":
                tempElse.append(self.indexEscopoAtual)
                tempElse.append(self.tokenAtual().tipo)
                tempElse = self.elsePartStatement(tempElse)     
                
                temp.append(tempElse)
                self.tabelaDeSimbolos.append(temp)
                self.indexEscopoAtual -= 1   
                
              else:
                temp.append(tempElse)
                self.tabelaDeSimbolos.append(temp)
                self.indexEscopoAtual -= 1
                return             
            else:
              raise Exception(
                  "Erro sintático: falta de ENDIF "
                  + str(self.tokenAtual().linha)
              )
          else:
            raise Exception(
              "Erro sintático: falta do FINDEL na linha " +
              str(self.tokenAtual().linha)
            )
        else:
          raise Exception(
              "Erro sintático: falta do INIDEL ou bloco vazio na linha "
              + str(self.tokenAtual().linha)
          )

      else:
        raise Exception(
            "Erro sintático: falta do parêntese direito na linha " +
            str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do parêntese esquerdo na linha " +
          str(self.tokenAtual().linha)
      )
  
  def ifStatementWhile(self, temp): 
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      tempExpression = []
      tempExpression = self.booleanExpression(tempExpression)
      temp.append(tempExpression)
      
      if self.tokenAtual().tipo == "PRIGHT":
        lookAhead = self.tokenLookAhead()
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL" and lookAhead.tipo != "FINDEL":
          self.indexToken +=1
          self.indexEscopoAtual += 1
          tempBlock = []
          
          while(self.tokenAtual().tipo != "FINDEL"
            and self.tokenLookAhead().tipo != "ENDIF"):
            tempBlock.append(self.blockStatement(True, True))
          
          temp.append(tempBlock)          

          if self.tokenAtual().tipo == "FINDEL": 
            self.indexToken += 1
            if self.tokenAtual().tipo == "ENDIF":
              temp.append(self.tokenAtual().tipo)
              self.indexToken += 1
              
              tempElse = []
              if self.tokenAtual().tipo == "ELSE":
                tempElse.append(self.indexEscopoAtual)
                tempElse.append(self.tokenAtual().tipo)
                tempElse = self.elsePartStatement(tempElse)     
                
                temp.append(tempElse)
                self.tabelaDeSimbolos.append(temp)
                self.indexEscopoAtual -= 1   
              else:
                temp.append(tempElse)
                self.tabelaDeSimbolos.append(temp)
                self.indexEscopoAtual -= 1
                return                           
            else:
              raise Exception(
                "Erro sintático: falta de ENDIF "
                + str(self.tokenAtual().linha)
              )
          else:
            raise Exception(
              "Erro sintático: falta do FINDEL na linha " +
              str(self.tokenAtual().linha)
            )
        else:
          raise Exception(
              "Erro sintático: falta do INIDEL ou bloco vazio na linha "
              + str(self.tokenAtual().linha)
          )

      else:
        raise Exception(
            "Erro sintático: falta do parêntese direito na linha " + 
            str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do parêntese esquerdo na linha " +
          str(self.tokenAtual().linha)
      )

  def elsePartStatement(self, tempElse):
    
    lookAhead = self.tokenLookAhead()
    self.indexToken += 1
    if self.tokenAtual().tipo == "INIDEL" and lookAhead != "FINDEL": 
      self.indexToken += 1
      tempBlock = []
      while(self.tokenAtual().tipo != "FINDEL" and self.tokenLookAhead().tipo != "ENDELSE"):         
        tempBlock.append(self.blockStatement(isIf=True))
      if self.tokenAtual().tipo == "FINDEL":
        self.indexToken += 1
        if self.tokenAtual().tipo == "ENDELSE":  
          tempElse.append(self.tokenAtual().tipo)
          self.indexToken += 1
          return tempElse
        else:
          raise Exception(
            "Erro sintático: falta de ENDELSE na linha "
            + str(self.tokenAtual().linha)
            )
      else:
        raise Exception(
            "Erro sintático: falta do FINDEL na linha "
            + str(self.tokenAtual().linha)
        )      
    else:
      raise Exception(
          "Erro sintático: falta do INIDEL ou bloco vazio na linha " +
          str(self.tokenAtual().linha)
      )     
    
  def whileStatement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      tempExpression = []
      tempExpression = self.booleanExpression(tempExpression)   
      temp.append(tempExpression)   
      
      if self.tokenAtual().tipo == "PRIGHT":
        self.indexToken += 1      
      
        if(self.tokenAtual().tipo == "INIDEL"):
         
          if(self.tokenLookAhead().tipo != "FINDEL"):
            self.indexToken += 1
            self.indexEscopoAtual += 1
            tempBlock = []
            while (
            self.tokenAtual().tipo != "FINDEL"
            and self.tokenLookAhead() != "ENDWHILE"
              ):
              tempBlock.append(self.blockStatement(isWhile=True))
            
            temp.append(tempBlock)
            
            if self.tokenAtual().tipo == "FINDEL":
              self.indexToken += 1
              if self.tokenAtual().tipo == "ENDWHILE":
                temp.append(self.tokenAtual().tipo)
                self.indexToken += 1
                self.tabelaDeSimbolos.append(temp)
                self.indexEscopoAtual -= 1
              else:
                  raise Exception(
                      "Erro sintático: falta de ENDWHILE na linha "
                      + str(self.tokenAtual().linha)
                  )
            else:
              raise Exception(
                  "Erro sintático: falta do FINDEL na linha "
                  + str(self.tokenAtual().linha)
              )
          else:
            raise Exception(
            "Erro sintático: bloco vazio na linha "+
            str(self.tokenAtual().linha)
        )
        else:
          raise Exception(
            "Erro sintático: faltando INIDEL na linha "+
            str(self.tokenAtual().linha)
        )
      else:
        raise Exception(
        "Erro sintático: falta do parêntese direito na linha "+
        str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do parêntese esquerdo na linha "+
          str(self.tokenAtual().linha)
      ) 
      
  def printStatement(self, temp):
    self.indexToken += 1
   
    if self.tokenAtual().tipo == "PLEFT":      
      temp.append(self.paramsPrintStatement())
      self.indexToken += 1
      if self.tokenAtual().tipo == "PRIGHT":
        self.tabelaDeSimbolos.append(temp)
        self.indexToken += 1
      else:
        raise Exception(
          "Erro sintático: falta do parêntese direito na linha "+
          str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do parêntese esquerdo na linha "+
          str(self.tokenAtual().linha)
      )

  def paramsPrintStatement(self):
    self.indexToken += 1
    if(
      (self.tokenAtual().tipo == "NUM")
        or (self.tokenAtual().tipo == "LOGIC")
        or (self.tokenAtual().tipo == "ID")
    ):          
      return self.tokenAtual().lexema
    else:
      raise Exception(
        "Erro sintático: uso incorreto dos parâmetros na linha " +
        str(self.tokenAtual().linha)
      )
  
  def callOpStatement(self, tempEndVar):
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
        self.callOpStatement(tempEndVar)            
      else:          
        return
    else:
        raise Exception(
          "Erro sintático: falta do ID na linha",
          str(self.tokenAtual().linha)
        )  
           
  def callVarStatement(self, temp):
    self.indexToken += 1
    
    if self.tokenAtual().tipo == "ATB":  
        temp.append(self.tokenAtual().lexema)
        self.indexToken += 1
        if (
            (self.tokenAtual().tipo == "NUM")
            or (self.tokenAtual().tipo == "LOGIC")
            or (self.tokenAtual().tipo == "ID")
        ):
          temp.append(self.tokenAtual().lexema)
          self.indexToken += 1   
          if (
            self.tokenAtual().tipo == "ADD"
            or self.tokenAtual().tipo == "SUB"
            or self.tokenAtual().tipo == "MULT"
            or self.tokenAtual().tipo == "DIV"
          ):
            temp.append(self.tokenAtual().lexema)
            self.callOpStatement(temp)          
       
    else:
      
      raise Exception(
          "Erro sintático: símbolo de atribuição não encontrado na linha "
          + str(self.tokenAtual().linha)
      )

  def declarationFuncStatement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      temp.append(self.tokenAtual().lexema)
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT": 
        tempParenteses = []
        self.indexToken += 1   
        
        if not(self.tokenAtual().tipo == "PRIGHT"):   
          tempParenteses = []
          self.paramsStatement(tempParenteses, temp)
        if not(self.tokenAtual().tipo == "PRIGHT"):                      
          raise Exception(
            "Erro sintático: falta parêntese direito na linha "
            + str(self.tokenAtual().linha)
          )
                
          
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL":
          if(self.tokenLookAhead().tipo != "FINDEL"):  
            self.indexEscopoAntesDaFuncao = (self.indexEscopoAtual)
            self.indexEscopoAtual += 1
            self.indexToken += 1   
            tempBlock = []
            linhaReturn = str(self.tokenAtual().linha)
            while self.tokenAtual().tipo != "RETURN":
              if (self.tokenAtual().tipo == "ENDFUNC"):                       
                raise Exception(
                  "Erro sintático: falta de return na linha "
                  + linhaReturn
                ) 
              else:
                tempBlock.append(self.blockStatement())
            temp.append(tempBlock)
            tempReturn =[]
            tempReturn.append(self.indexEscopoAtual)
            tempReturn.append(self.tokenAtual().tipo)
            tempReturnParams = []
            tempReturnParams = self.returnStatement()
            tempReturn.append(tempReturnParams)
            temp.append(tempReturn)
            self.indexToken +=1  
    
            if not(self.tokenAtual().tipo == "FINDEL"):                       
              raise Exception(
                "Erro sintático: falta FINDEL na linha "
                + str(self.tokenAtual().linha)
              )  
            self.indexToken +=1
            if not(self.tokenAtual().tipo == "ENDFUNC"):
              raise Exception(
                "Erro sintático: falta de ENDFUNC na linha "
                + str(self.tokenAtual().linha)
              )
            self.indexToken +=1
          else:
            raise Exception(
              "Erro sintático: escopo vazio na linha  "
              + str(self.tokenAtual().linha)
            )
        else:
          raise Exception(
            "Erro sintático: falta INIDEL na linha "
            + str(self.tokenAtual().linha)
          )        
      else:
        raise Exception(
          "Erro sintático: falta parêntese esquerdo na linha "
          + str(self.tokenAtual().linha)
        )  
    else:
     raise Exception(
      "Erro sintático: falta identificador da função na linha "
      + str(self.tokenAtual().linha)
    ) 
   
  def paramsStatement(self, tempParenteses, temp):
    
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":
        tempParentesesParamAtual = []
        tempParentesesParamAtual.append(self.indexEscopoAtual + 1)
        tempParentesesParamAtual.append(self.tokenAtual().tipo)
        self.indexToken += 1
        if self.tokenAtual().tipo == "ID":
            tempParentesesParamAtual.append(self.tokenAtual().lexema)
            tempParenteses.append(tempParentesesParamAtual)
            self.indexToken += 1
            if self.tokenAtual().tipo == "COMMA":
                self.indexToken += 1
                self.paramsStatement(tempParenteses, temp)
                tempParenteses.pop()
                temp.append(tempParenteses)
            elif (
              not(self.tokenAtual().tipo == "PRIGHT")
            ):
                raise Exception(
                    "Erro sintático: falta vírgula na linha "
                    + str(self.tokenAtual().linha)
                )           
        else:
            raise Exception(
                "Erro sintatico: é necessário informar alguma váriavel na linha "
                + str(self.tokenAtual().linha)
            )
    else:
        raise Exception(
            "Erro sintatico: é necessário informar um tipo na linha "
            + str(self.tokenAtual().linha)
        )
        
  def argumentStatement(self, tempParams, tempEndVar):
    
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "LOGIC" or self.tokenAtual().tipo == "NUM":
        tempParams.append(self.tokenAtual().lexema)
        self.indexToken += 1
        if self.tokenAtual().tipo == "COMMA":
          self.indexToken += 1
          tempParams.append(self.argumentStatement(tempParams, tempEndVar))
          tempParams.pop()
            
        if (
          self.tokenAtual().tipo == "PRIGHT"
        ):
          self.indexToken += 1
          tempEndVar.append(tempParams)
          return tempEndVar
        else:
          raise Exception(
              "Erro sintático: falta vírgula na linha "
              + str(self.tokenAtual().linha)
          )  
              
    else:
        raise Exception(
          "Erro sintatico: é necessário informar alguma váriavel na linha "
          + str(self.tokenAtual().linha)
        )
      
  def returnStatement(self):
    self.indexToken += 1 
    if (
        not((self.tokenAtual().tipo == "NUM")
        or (self.tokenAtual().tipo == "LOGIC")
        or (self.tokenAtual().tipo == "ID"))
    ):
      raise Exception(
        "Erro sintático: retorno errado na linha "
        + str(self.tokenAtual().linha)
      )   
    else:
      return self.tokenAtual().lexema
    
  def declarationProcStatement(self, temp):
    self.indexToken += 1
    
    if self.tokenAtual().tipo == "ID":
      temp.append(self.tokenAtual().lexema)
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT":
        tempParenteses = []
        self.indexToken += 1  
        
        if not(self.tokenAtual().tipo == "PRIGHT"):
          self.paramsStatement(tempParenteses, temp)
          
        if not(self.tokenAtual().tipo == "PRIGHT"):                      
          raise Exception(
            "Erro sintático: falta parêntese direito na linha "
            + str(self.tokenAtual().linha)
          )                 
          
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL":
          if(self.tokenLookAhead().tipo != "FINDEL"): 
            self.indexEscopoAntesDaFuncao = (self.indexEscopoAtual)
            self.indexEscopoAtual += 1
            self.indexToken += 1 
            tempBlock = []
            while self.tokenAtual().tipo != "FINDEL":
              tempBlock.append(self.blockStatement())
            temp.append(tempBlock)
            self.indexToken += 1
            
          else:
            raise Exception(
              "Erro sintático: escopo vazio na linha  "
              + str(self.tokenAtual().linha)
            )
        else:
          raise Exception(
            "Erro sintático: falta INIDEL na linha "
            + str(self.tokenAtual().linha)
          ) 
      else:
        raise Exception(
          "Erro sintático: falta parêntese esquerdo na linha "
          + str(self.tokenAtual().linha)
        )  
    else:
     raise Exception(
      "Erro sintático: falta identificador da função na linha "
      + str(self.tokenAtual().linha)
    ) 
     
  def callFunc(self, tempEndVar):
    tempEndVar.append(self.tokenAtual().tipo)
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      tempEndVar.append(self.tokenAtual().lexema)
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT":
        self.indexToken += 1
        tempParams = []
        if not(self.tokenAtual().tipo == "PRIGHT"):        
          self.argumentStatement(tempParams, tempEndVar)    
        else: 
          self.indexToken += 1   
      else:
        raise Exception(
          "Erro sintático: falta parêntese esquerdo na linha "
          + str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
        "Erro sintático: falta o nome da função na linha "
        + str(self.tokenAtual().linha)
      ) 
      
  def callProc(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT":
        self.indexToken += 1
        if not(self.tokenAtual().tipo == "PRIGHT"):        
          self.argumentStatement()   
        else: 
          self.indexToken += 1  
            
      else:
        raise Exception(
          "Erro sintático: falta parêntese esquerdo na linha "
          + str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
        "Erro sintático: falta o nome da função na linha "
        + str(self.tokenAtual().linha)
      ) 
    