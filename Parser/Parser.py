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
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.variable_definition(temp)      
      return temp

    if self.tokenAtual().tipo == "IF":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.if_statement(temp)
      return temp
    
    if self.tokenAtual().tipo == "PRINT":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.print_statement(temp)
      return temp
    
    if self.tokenAtual().tipo == "WHILE":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.while_statement(temp)
      return temp
    
    if self.tokenAtual().tipo == "ID":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      temp.append(self.tokenAtual().lexema)
      self.call_var_statement(temp)
      return temp

    if self.tokenAtual().tipo == "FUNC":
      temp = []
      temp.append(self.tokenAtual().linha)
      # temp.append('FUNC')
      temp.append(self.tokenAtual().tipo)

      self.declaration_func_statement(temp)
      return temp
    
    if self.tokenAtual().tipo == "PROC":   
      self.declaration_proc_statement()
    
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
        else:
            raise Exception(
                "Erro sintático. boolean atribuido errado na linha",
              str(self.tokenAtual().linha)
            )
    elif self.tokenAtual().tipo == "NUM":
      tempEndVar.append(self.tokenAtual().lexema)
      self.indexToken += 1      
    else:
        raise Exception(
            "Erro sintático: atribuição de variavel errada na linha",
            str(self.tokenAtual().linha)
        )

  def boolean_expression(self, tempExpression):
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM" or self.tokenAtual().tipo == "LOGIC":
      tempExpression.append(self.tokenAtual().lexema)
      
      if(self.tokenAtual().tipo == "LOGIC" and self.tokenAtual().lexema != 'false'):
        self.indexToken += 1
        if self.tokenAtual().tipo == "PRIGHT":
          tempExpression.append(self.tokenAtual().lexema)
          self.indexToken += 1
          return tempExpression
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
        if self.tokenAtual().tipo == "INIDEL" and lookAhead.tipo != "FINDEL":
          self.indexToken +=1
          tempBlock = []
         
          while(self.tokenAtual().tipo != "FINDEL"
              and self.tokenLookAhead().tipo != "ENDIF"):
            tempBlock.append(self.blockStatement3())
            
          temp.append(tempBlock)

          if self.tokenAtual().tipo == "FINDEL":            
            temp.append(self.tokenAtual().tipo)
            self.indexToken += 1
            if self.tokenAtual().tipo == "ENDIF":
              temp.append(self.tokenAtual().tipo)
              self.indexToken += 1
              tempElse = []
              if self.tokenAtual().tipo == "ELSE":
                tempElse.append(self.tokenAtual().tipo)
                tempElse = self.else_part_statement(tempElse)
                temp.append(tempElse)
              else:
                #temp.append(tempElse)
                self.tabTokens.append(temp)                      
            else:
              raise Exception(
                  "Erro sintático: falta de ENDIF "
                  + str(self.tokenAtual().linha)
              )
          else:
            raise Exception(
              "Erro sintático: falta do FINDEL na linha",
              str(self.tokenAtual().linha)
            )
        else:
          raise Exception(
              "Erro sintático: falta do INIDEL ou bloco vazio na linha "
              + str(self.tokenAtual().linha)
          )

      else:
        raise Exception(
            "Erro sintático: falta do parêntese direito na linha",
            str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do parêntese esquerdo na linha",
          str(self.tokenAtual().linha)
      )

  def else_part_statement(self, tempElse):
    
    lookAhead = self.tokenLookAhead()
    self.indexToken += 1
    if self.tokenAtual().tipo == "INIDEL" and lookAhead != "FINDEL":      
      tempElse.append(self.tokenAtual().tipo)
      self.indexToken += 1
      tempBlock = []
      while(self.tokenAtual().tipo != "FINDEL" and self.tokenLookAhead().tipo != "ENDELSE"):         
        tempBlock.append(self.blockStatement3())
      tempElse.append(tempBlock)
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
          "Erro sintático: falta do INIDEL ou bloco vazio na linha",
          str(self.tokenAtual().linha)
      )
      
  def else_part_statement2(self, tempElse):
    lookAhead = self.tokenLookAhead()
    self.indexToken += 1
    if self.tokenAtual().tipo == "INIDEL" and lookAhead != "FINDEL":      
      tempElse.append(self.tokenAtual().tipo)
      self.indexToken += 1
      tempBlock = []
      while(self.tokenAtual().tipo != "FINDEL" and self.tokenLookAhead().tipo != "ENDELSE"):          
        tempBlock.append(self.blockStatement2())
      tempElse.append(tempBlock)
      
      if self.tokenAtual() == "FINDEL":
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
          "Erro sintático: falta do INIDEL ou bloco vazio na linha",
          str(self.tokenAtual().linha)
      )
  
  def while_statement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      tempExpression = []
      tempExpression.append(self.tokenAtual().lexema)
      self.indexToken += 1
      tempExpression = self.boolean_expression(tempExpression)      
      
      if self.tokenAtual().tipo == "PRIGHT":
        tempExpression.append(self.tokenAtual().lexema)
        temp.append(tempExpression)
        self.indexToken += 1      
      
        if(self.tokenAtual().tipo == "INIDEL"):
          if(self.tokenLookAhead().tipo != "FINDEL"):
            self.indexToken += 1
            tempBlock = []
            while (
            self.tokenAtual().tipo != "FINDEL"
            and self.tokenLookAhead() != "ENDWHILE"
              ):
              tempBlock.append(self.blockStatement2())
              
            temp.append(tempBlock)
            
            if self.tokenAtual().tipo == "FINDEL":
              self.indexToken += 1
              if self.tokenAtual().tipo == "ENDWHILE":
                  temp.append(self.tokenAtual().tipo)
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
      
  def blockStatement2(self):
    
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.variable_definition(temp)      
      return temp
    
    if self.tokenAtual().tipo == "IF":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.if_statement_while(temp)
      return temp
    
    if self.tokenAtual().tipo == "PRINT":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.print_statement(temp)
      return temp
    
    if self.tokenAtual().tipo == "WHILE":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.while_statement(temp)
      return temp
    
    if self.tokenAtual().tipo == "BREAK" or self.tokenAtual().tipo == "CONTINUE":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.indexToken += 1
      return temp
    
  def blockStatement3(self):   
    
    if self.tokenAtual().tipo == "PRINT":
      temp = []
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.print_statement(temp)
      return temp
    
    else:      
      #self.indexToken += 1
      #return
      raise Exception(
          "Erro sintático na linha",
          str(self.tokenAtual().linha)
      )

    #else:      
     # raise Exception(
      #    "Erro sintático: bloco vazio na linha",
       #   str(self.tokenAtual().linha)
      #)

  def print_statement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      temp.append(self.tokenAtual().lexema)
      temp.append(self.params_print_statement())
      self.indexToken += 1
      if self.tokenAtual().tipo == "PRIGHT":
        temp.append(self.tokenAtual().lexema)
        self.indexToken += 1
      else:
        raise Exception(
          "Erro sintático: falta do parêntese direito na linha",
          str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do parêntese esquerdo na linha",
          str(self.tokenAtual().linha)
      )

  def params_print_statement(self):
    self.indexToken += 1
    if(
      (self.tokenAtual().tipo == "NUM")
        or (self.tokenAtual().tipo == "LOGIC")
        or (self.tokenAtual().tipo == "ID")
    ):          
      return self.tokenAtual().lexema
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
        
  def if_statement_while(self, temp): #if que tem o block com break e continue
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1      
      tempExpression = []
      tempExpression = self.boolean_expression(tempExpression)
      temp.append(tempExpression)
      if self.tokenAtual().tipo == "PRIGHT":
        lookAhead = self.tokenLookAhead()
        self.indexToken += 1
        
        if self.tokenAtual().tipo == "INIDEL":
          if lookAhead.tipo != "FINDEL":
            self.indexToken += 1
            tempBlock = []
            
            while(self.tokenAtual().tipo != "FINDEL"
              and self.tokenLookAhead().tipo != "ENDIF"):
              tempBlock.append(self.blockStatement2())
            
            temp.append(tempBlock)
            if self.tokenAtual().tipo == "FINDEL":    
              temp.append(self.tokenAtual().tipo)
              self.indexToken += 1
              if self.tokenAtual().tipo == "ENDIF":
                temp.append(self.tokenAtual().tipo)
                self.indexToken += 1
                tempElse = []
                if self.tokenAtual().tipo == "ELSE":
                  tempElse.append(self.tokenAtual().tipo)
                  tempElse = self.else_part_statement2(tempElse)
                  temp.append(tempElse)
                else:
                  #temp.append(tempElse)
                  self.tabTokens.append(temp)
              else:
                raise Exception(
                    "Erro sintático: falta de ENDIF "
                    + str(self.tokenAtual().linha)
                )  
            else:
              raise Exception(
                "Erro sintático: falta do FINDEL na linha",
                str(self.tokenAtual().linha)
              )  
          else:
            raise Exception(
              "Erro sintático: bloco vazio na linha "
              + str(self.tokenAtual().linha)
          )
        else:
          raise Exception(
              "Erro sintático: falta do INIDEL na linha "
              + str(self.tokenAtual().linha)
          )
      else:
        raise Exception(
            "Erro sintático: falta do parêntese direito na linha",
            str(self.tokenAtual().linha)
        )
    else:
      raise Exception(
          "Erro sintático: falta do parêntese esquerdo na linha",
          str(self.tokenAtual().linha)
      )
        
  def call_var_statement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ATB":  # atribuicao
        temp.append(self.tokenAtual().lexema)
        self.indexToken += 1
        if (
            (self.tokenAtual().tipo == "NUM")
            or (self.tokenAtual().tipo == "LOGIC")
            or (self.tokenAtual().tipo == "ID")
        ):
            temp.append(self.tokenAtual().lexema)
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

  def declaration_func_statement(self, temp):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT": 
        if not(self.tokenLookAhead().tipo == "PRIGHT"):        
          self.params_statement()
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
            self.return_statement()
            self.indexToken +=1
            if not(self.tokenAtual().tipo == "FINDEL"):                       
              raise Exception(
                "Erro sintático: falta FINDEL na linha "
                + str(self.tokenAtual().linha)
              )  
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
   
  def params_statement(self):
    self.indexToken += 1
    
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":
        self.indexToken += 1
        if self.tokenAtual().tipo == "ID":
            self.indexToken += 1
            if self.tokenAtual().tipo == "COMMA":
                self.params_statement()
            elif (
                self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN"
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
  
  def return_statement(self):
    self.indexToken += 1 
    # Se for chamada de variavel/num/bool
    if (
        not((self.tokenAtual().tipo == "NUM")
        or (self.tokenAtual().tipo == "LOGIC")
        or (self.tokenAtual().tipo == "ID"))
    ):
      raise Exception(
        "Erro sintático: retorno errado na linha "
        + str(self.tokenAtual().linha)
      )
    
  def declaration_proc_statement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT":
        if not(self.tokenLookAhead().tipo == "PRIGHT"): 
          self.params_statement()
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