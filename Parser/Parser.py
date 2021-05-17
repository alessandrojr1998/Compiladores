class Parser:
  def __init__(self, tabTokens):
    self.tabTokens = tabTokens
    self.indexToken = 0
    self.indexLookAhead = 0

  def tokenAtual(self):
    return self.tabTokens[self.indexToken]
  
  def tokenLookAhead(self):
      self.indexLookAhead = self.indexToken + 1
      return self.tabTokens[self.indexLookAhead]

  def start(self):
    self.statementList()
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
      self.variableDefinition()           
      return 

    if self.tokenAtual().tipo == "IF":
      if isWhile:
        self.ifStatementWhile()
        return 
      else:
        self.ifStatement()
        return 
    
    if self.tokenAtual().tipo == "PRINT":
      self.printStatement()
      return 
    
    if self.tokenAtual().tipo == "WHILE":
      self.whileStatement()
      return 
    
    if self.tokenAtual().tipo == "ID":
      self.callVarStatement()
      return 

    if self.tokenAtual().tipo == "FUNC":
      if not(isIf):

        self.declarationFuncStatement()
        return 
      else:
        raise Exception(
          "Erro sintático: declaração de função não permitida no bloco do if/else na linha " +
          str(self.tokenAtual().linha)
          ) 
    if self.tokenAtual().tipo == "PROC":  
      if not(isIf):
        self.declarationProcStatement()
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

  def variableDefinition(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "ATB":
        self.indexToken += 1
        if self.tokenAtual().tipo == "FUNCCALL":          
          self.callFunc()        
        else:        
          self.typeVar()
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

  def typeVar(self):
    if self.tokenAtual().tipo == "LOGIC":
        if (
          self.tokenAtual().lexema == "true"
          or self.tokenAtual().lexema == "false"
        ):
          self.indexToken += 1            
        else:
          raise Exception(
              "Erro sintático. boolean atribuido errado na linha " +
            str(self.tokenAtual().linha)
          )
    elif self.tokenAtual().tipo == "NUM":
      self.indexToken += 1      
    else:
      raise Exception(
        "Erro sintático: atribuição de variavel errada na linha " +
        str(self.tokenAtual().linha)
      )

  def booleanExpression(self):
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM" or self.tokenAtual().tipo == "LOGIC":
      
      if(self.tokenAtual().tipo == "LOGIC" and self.tokenAtual().lexema != 'false'):
        self.indexToken += 1
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
        self.indexToken += 1
        if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM" or self.tokenAtual().tipo == "LOGIC":
          self.indexToken +=1
          return 
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

  def ifStatement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      self.booleanExpression()

      if self.tokenAtual().tipo == "PRIGHT":
        lookAhead = self.tokenLookAhead()
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL" and lookAhead.tipo != "FINDEL":
          self.indexToken +=1
         
          while(self.tokenAtual().tipo != "FINDEL"
              and self.tokenLookAhead().tipo != "ENDIF"):
            self.blockStatement(isIf=True)        

          if self.tokenAtual().tipo == "FINDEL":    
            self.indexToken += 1
            if self.tokenAtual().tipo == "ENDIF":
              self.indexToken += 1
              if self.tokenAtual().tipo == "ELSE":
                self.elsePartStatement()                    
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
  
  def ifStatementWhile(self): 
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      self.booleanExpression()

      if self.tokenAtual().tipo == "PRIGHT":
        lookAhead = self.tokenLookAhead()
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL" and lookAhead.tipo != "FINDEL":
          self.indexToken +=1
         
          while(self.tokenAtual().tipo != "FINDEL"
            and self.tokenLookAhead().tipo != "ENDIF"):
            self.blockStatement(True, True)          

          if self.tokenAtual().tipo == "FINDEL": 
            self.indexToken += 1
            if self.tokenAtual().tipo == "ENDIF":
              self.indexToken += 1
              if self.tokenAtual().tipo == "ELSE":
                self.elsePartStatement()                                   
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

  def elsePartStatement(self):
    
    lookAhead = self.tokenLookAhead()
    self.indexToken += 1
    if self.tokenAtual().tipo == "INIDEL" and lookAhead != "FINDEL": 
      self.indexToken += 1
      while(self.tokenAtual().tipo != "FINDEL" and self.tokenLookAhead().tipo != "ENDELSE"):         
        self.blockStatement(isIf=True)
      if self.tokenAtual().tipo == "FINDEL":
        self.indexToken += 1
        if self.tokenAtual().tipo == "ENDELSE":   
          self.indexToken += 1
          return 
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
      
  def elsePartStatement2(self):
    lookAhead = self.tokenLookAhead()
    self.indexToken += 1
    if self.tokenAtual().tipo == "INIDEL" and lookAhead != "FINDEL":  
      self.indexToken += 1
      while(self.tokenAtual().tipo != "FINDEL" and self.tokenLookAhead().tipo != "ENDELSE"):          
        self.blockStatement(isWhile=True)
      
      if self.tokenAtual() == "FINDEL":
        self.indexToken += 1
        if self.tokenAtual().tipo == "ENDELSE":   
          self.indexToken += 1
          return 
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
          "Erro sintático: falta do INIDEL ou bloco vazio na linha",
          str(self.tokenAtual().linha)
      )
  
  def whileStatement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      self.booleanExpression()      
      
      if self.tokenAtual().tipo == "PRIGHT":
        self.indexToken += 1      
      
        if(self.tokenAtual().tipo == "INIDEL"):
          if(self.tokenLookAhead().tipo != "FINDEL"):
            self.indexToken += 1
            while (
            self.tokenAtual().tipo != "FINDEL"
            and self.tokenLookAhead() != "ENDWHILE"
              ):
              self.blockStatement(isWhile=True)
            
            if self.tokenAtual().tipo == "FINDEL":
              self.indexToken += 1
              if self.tokenAtual().tipo == "ENDWHILE":
                  self.indexToken += 1
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
      
  def printStatement(self):
    self.indexToken += 1
   
    if self.tokenAtual().tipo == "PLEFT":
      self.paramsPrintStatement()
      self.indexToken += 1
      if self.tokenAtual().tipo == "PRIGHT":
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
  
  def callOpStatement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM":
        self.indexToken += 1
        if (
          self.tokenAtual().tipo == "ADD"
          or self.tokenAtual().tipo == "SUB"
          or self.tokenAtual().tipo == "MULT"
          or self.tokenAtual().tipo == "DIV"
        ):
          self.callOpStatement()            
        else:          
          return
    else:
        raise Exception(
          "Erro sintático: falta do ID na linha",
          str(self.tokenAtual().linha)
        )  
           
  def callVarStatement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ATB":  
        self.indexToken += 1
        if (
            (self.tokenAtual().tipo == "NUM")
            or (self.tokenAtual().tipo == "LOGIC")
            or (self.tokenAtual().tipo == "ID")
        ):
            self.indexToken += 1            
        else:
            raise Exception(
                "Erro sintático: variável não atribuída na linha "
                + str(self.tokenAtual().linha)
            )
    else:
        raise Exception(
            "Erro sintático: símbolo de atribuição não encontrado na linha "
            + str(self.tokenAtual().linha)
        )

  def declarationFuncStatement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT": 
        if not(self.tokenLookAhead().tipo == "PRIGHT"):        
          self.paramsStatement()
          if not(self.tokenAtual().tipo == "PRIGHT"):                      
            raise Exception(
              "Erro sintático: falta parêntese direito na linha "
              + str(self.tokenAtual().linha)
            )
        else:          
          self.indexToken += 1
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL":
          if(self.tokenLookAhead().tipo != "FINDEL"):  
            self.indexToken += 1   
            linhaReturn = str(self.tokenAtual().linha)
            while self.tokenAtual().tipo != "RETURN":
              if (self.tokenAtual().tipo == "ENDFUNC"):                       
                raise Exception(
                  "Erro sintático: falta de return na linha "
                  + linhaReturn
                ) 
              else:
                self.blockStatement()
            self.returnStatement()
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
   
  def paramsStatement(self):
    self.indexToken += 1
    
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":
        self.indexToken += 1
        if self.tokenAtual().tipo == "ID":
            self.indexToken += 1
            if self.tokenAtual().tipo == "COMMA":
                self.paramsStatement()
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
        
  def argumentStatement(self):
    
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "LOGIC" or self.tokenAtual().tipo == "NUM":
        self.indexToken += 1
        if self.tokenAtual().tipo == "COMMA":
          self.indexToken += 1
          self.argumentStatement()
            
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
    
  def declarationProcStatement(self):
    self.indexToken += 1
    
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT":
        if not(self.tokenLookAhead().tipo == "PRIGHT"): 
          self.paramsStatement()
          if not(self.tokenAtual().tipo == "PRIGHT"):                      
            raise Exception(
              "Erro sintático: falta parêntese direito na linha "
              + str(self.tokenAtual().linha)
            )
        else:          
          self.indexToken += 1
        self.indexToken += 1
        if self.tokenAtual().tipo == "INIDEL":
          if(self.tokenLookAhead().tipo != "FINDEL"): 
            self.indexToken += 1 
            while self.tokenAtual().tipo != "FINDEL":
              self.blockStatement()
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
     
  def callFunc(self):
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
    