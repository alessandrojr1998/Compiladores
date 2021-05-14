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

        while self.tokenAtual().tipo != "END":
          self.blockStatement()
        
        if self.tokenAtual().tipo == "END":
          print("\nAnálise Sintática Finalizada\n")
        else:
            raise Exception(
                "Erro sintático: falta do end na linha", str(self.tokenAtual().linha)
            )
      else:
         raise Exception("Erro sintático: faltando INIDEL na linha", str(self.tokenAtual().linha))

    else:
      raise Exception("Erro sintático na linha", str(self.tokenAtual().linha))
  
  def blockStatement(self, isWhile = False, isIf = False):  
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":      
      self.variable_definition()           
      return 

    if self.tokenAtual().tipo == "IF":
      if isWhile:
        self.if_statement_while()
        return 
      else:
        self.if_statement()
        return 
    
    if self.tokenAtual().tipo == "PRINT":
      self.print_statement()
      return 
    
    if self.tokenAtual().tipo == "WHILE":
      self.while_statement()
      return 
    
    if self.tokenAtual().tipo == "ID":
      self.call_var_statement()
      return 

    if self.tokenAtual().tipo == "FUNC":
      if not(isIf):

        self.declaration_func_statement()
        return 
      else:
        raise Exception(
          "Erro sintático: declaração de função não permitida no bloco do if/else na linha " +
          str(self.tokenAtual().linha)
          ) 
    if self.tokenAtual().tipo == "PROC":  
      if not(isIf):
        self.declaration_proc_statement()
        return
      else:
        raise Exception(
          "Erro sintático: declaração de procedimento não permitida no bloco do if/else na linha " +
          str(self.tokenAtual().linha)
          )
    if self.tokenAtual().tipo == "PROCCALL":      
      self.call_proc()
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

  def variable_definition(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "ATB":
        self.indexToken += 1
        if self.tokenAtual().tipo == "FUNCCALL":          
          self.call_func()        
        else:        
          self.type_var()
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

  def type_var(self):
    if self.tokenAtual().tipo == "LOGIC":
        if (
          self.tokenAtual().lexema == "true"
          or self.tokenAtual().lexema == "false"
        ):
          self.indexToken += 1            
        else:
          raise Exception(
              "Erro sintático. boolean atribuido errado na linha",
            str(self.tokenAtual().linha)
          )
    elif self.tokenAtual().tipo == "NUM":
      self.indexToken += 1      
    else:
      raise Exception(
        "Erro sintático: atribuição de variavel errada na linha",
        str(self.tokenAtual().linha)
      )

  def boolean_expression(self):
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

  def if_statement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      self.boolean_expression()

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
                self.else_part_statement()                    
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
  
  def if_statement_while(self): 
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      self.boolean_expression()

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
                self.else_part_statement()                                   
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

  def else_part_statement(self):
    
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
          "Erro sintático: falta do INIDEL ou bloco vazio na linha",
          str(self.tokenAtual().linha)
      )
      
  def else_part_statement2(self):
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
  
  def while_statement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "PLEFT":
      self.indexToken += 1
      self.boolean_expression()      
      
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
      
  def print_statement(self):
    self.indexToken += 1
   
    if self.tokenAtual().tipo == "PLEFT":
      self.params_print_statement()
      self.indexToken += 1
      if self.tokenAtual().tipo == "PRIGHT":
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
  
  def call_op_statement(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "NUM":
        self.indexToken += 1
        if (
          self.tokenAtual().tipo == "ADD"
          or self.tokenAtual().tipo == "SUB"
          or self.tokenAtual().tipo == "MULT"
          or self.tokenAtual().tipo == "DIV"
        ):
          self.call_op_statement()            
        else:          
          return
    else:
        raise Exception(
          "Erro sintático: falta do ID na linha",
          str(self.tokenAtual().linha)
        )  
           
  def call_var_statement(self):
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

  def declaration_func_statement(self):
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
   
  def params_statement(self):
    self.indexToken += 1
    
    if self.tokenAtual().tipo == "INT" or self.tokenAtual().tipo == "BOOLEAN":
        self.indexToken += 1
        if self.tokenAtual().tipo == "ID":
            self.indexToken += 1
            if self.tokenAtual().tipo == "COMMA":
                self.params_statement()
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
        
  def argument_statement(self):
    
    if self.tokenAtual().tipo == "ID" or self.tokenAtual().tipo == "LOGIC" or self.tokenAtual().tipo == "NUM":
        self.indexToken += 1
        if self.tokenAtual().tipo == "COMMA":
          self.indexToken += 1
          self.argument_statement()
            
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
      
  def return_statement(self):
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
     
  def call_func(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT":
        self.indexToken += 1
        if not(self.tokenAtual().tipo == "PRIGHT"):        
          self.argument_statement()    
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
      
  def call_proc(self):
    self.indexToken += 1
    if self.tokenAtual().tipo == "ID":
      self.indexToken += 1
      if self.tokenAtual().tipo == "PLEFT":
        self.indexToken += 1
        if not(self.tokenAtual().tipo == "PRIGHT"):        
          self.argument_statement()   
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
    