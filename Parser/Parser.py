class Parser:
  def __init__(self, tabTokens):
    self.tabTokens = tabTokens
    self.indexToken = 0
    self.indexLookAhead = 0
    self.tabelaDeSimbolos = []
    self.indexEscopoAtual = -1
    self.indexEscopoAntesDaFuncao = 0
    self.tabelaDeTresEnderecos = []
    self.tempTresEnderecos = ''
    self.tempAtualTresEnd = 0

  def tokenAtual(self):
    return self.tabTokens[self.indexToken]
  
  def tokenLookAhead(self):
      self.indexLookAhead = self.indexToken + 1
      return self.tabTokens[self.indexLookAhead]

  def start(self):
    escopoPai = self.indexEscopoAtual
    self.indexEscopoAtual += 1
    self.statementList()
    
    """ for linha in self.tabelaDeSimbolos:
      if(linha != None):
        print(linha) """
    print("__________-------------------------------------------_________________")  
    for linha in self.tabelaDeTresEnderecos:
      print(linha)

    print('\n')
    
    self.checkSemantica()
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
  
  def blockStatement(self, isWhile = False, isIf = False, isProc = False):  
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
        self.ifStatementWhile(temp, isProc)
        return temp
      else:
        temp = []
        temp.append(self.indexEscopoAtual)
        temp.append(self.tokenAtual().linha)
        temp.append(self.tokenAtual().tipo)
        self.ifStatement(temp, isProc)
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
      self.whileStatement(temp, isProc)
      return temp
    
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
        self.tabelaDeSimbolos.append(temp)
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
        self.declarationProcStatement(temp)
        self.tabelaDeSimbolos.append(temp)

        #  INICIO TAB 3 END - PROC
        
        nomeDaFuncao = temp[3]
        paramsDaFuncao = temp[4]

        self.tabelaDeTresEnderecos.append(('label', nomeDaFuncao, 'null'))

        for param in paramsDaFuncao:
            self.tabelaDeTresEnderecos.append(('pop', param[2], 'null'))

        self.tabelaDeTresEnderecos.append(('ret', 'null', 'null'))


        return temp
      else:
        raise Exception(
          "Erro sintático: declaração de procedimento não permitida no bloco do if/else na linha " +
          str(self.tokenAtual().linha)
          )
    if self.tokenAtual().tipo == "PROCCALL":   
      temp = []
      temp.append(self.indexEscopoAtual)
      temp.append(self.tokenAtual().linha)
      temp.append(self.tokenAtual().tipo)
      self.callProc(temp)
      self.tabelaDeSimbolos.append(temp)
      return temp
    
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
        self.tabelaDeSimbolos.append(temp)
      else:
          raise Exception(
              "Erro sintático: falta atribuição na linha " +
              str(self.tokenAtual().linha)
          )
      #  TRES END OK
      #self.tabelaDeTresEnderecos.append(('mov', temp[3], 'temp'))
      if(len(temp[5]) > 1):
        if(len(temp[5]) == 3):   
          self.tabelaDeTresEnderecos.append((temp[3]+ ' := ' + temp[5][0] + temp[5][1] + temp[5][2]))
          self.tempAtualTresEnd += 1
        else:
          self.salvarVariaveisTresEnd(temp)    
      else:
        self.tabelaDeTresEnderecos.append((temp[3] + ' := ' + temp[5][0]))
    else:
          raise Exception(
              "Erro sintático: falta ID na linha " +
              str(self.tokenAtual().linha)
          )
  def salvarVariaveisTresEnd(self, dados):
    lista = dados[5][::-1]
    contador = 0    
    self.tabelaDeTresEnderecos.append(("temp"+str(self.tempAtualTresEnd) + " := " + lista[contador] + lista[contador+1] + lista[contador+2]))
    contador += 3
    self.tempAtualTresEnd += 1
    if(contador < len(lista)):
      self.recursivo(lista, contador)
    self.tabelaDeTresEnderecos.append((dados[3] + ' := ' + "temp"+str(self.tempAtualTresEnd-1)))
      
 
  def recursivo(self, lista, contador):
    if(contador < len(lista)):
      self.tabelaDeTresEnderecos.append(("temp"+str(self.tempAtualTresEnd)  + " := " "temp"+str(self.tempAtualTresEnd-1) + lista[contador] + lista[contador+1]))
      self.tempAtualTresEnd += 1
      contador += 2
      if(contador < len(lista) + 2):
        self.recursivo(lista, contador)
      

  def typeVar(self, tempEndVar):
    if self.tokenAtual().tipo == "LOGIC":
        if (
          self.tokenAtual().lexema == "true"
          or self.tokenAtual().lexema == "false"
        ):
          tempEndVar.append(self.tokenAtual().lexema)
          self.indexToken += 1        
          return tempEndVar    
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
          return tempEndVar
      else:
          return tempEndVar
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
        tempEndVar.append(self.tokenAtual().lexema)
        self.callOpStatement(tempEndVar)
        return tempEndVar
      else:
          return tempEndVar  

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
        if self.tokenAtual().tipo == "PRIGHT":
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

      if(self.tokenAtual().tipo == "ID" and self.tokenLookAhead().tipo == "PRIGHT"):
        self.indexToken += 1
        return tempExpression
          
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

  def ifStatement(self, temp, isProc):
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
            if(self.tokenAtual().tipo == "RETURN" and isProc):
              raise Exception(
                "Erro sintático: return declarado dentro de um procedimento na linha "
                + str(self.tokenAtual().linha)
              ) 
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
  
  def ifStatementWhile(self, temp, isProc): 
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
            if(self.tokenAtual().tipo == "RETURN" and isProc):
              raise Exception(
                "Erro sintático: return declarado dentro de um procedimento na linha "
                + str(self.tokenAtual().linha)
              ) 
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
    
  def whileStatement(self, temp, isProc):
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
              if(self.tokenAtual().tipo == "RETURN" and isProc):
                raise Exception(
                  "Erro sintático: return declarado dentro de um procedimento na linha "
                  + str(self.tokenAtual().linha)
                ) 
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
      lexema = self.paramsPrintStatement()
      temp.append(lexema)
      self.indexToken += 1

      # TRES END
      self.tabelaDeTresEnderecos.append(
          ('print := '+ lexema))
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
        return tempEndVar
    else:
        raise Exception(
          "Erro sintático: falta do ID na linha",
          str(self.tokenAtual().linha)
        )  
           
  def callVarStatement(self, temp):
    self.indexToken += 1
    
    if self.tokenAtual().tipo == "ATB":  
        tempVar = []
        temp.append(self.tokenAtual().lexema)
        self.indexToken += 1
        if (
            (self.tokenAtual().tipo == "NUM")
            or (self.tokenAtual().tipo == "LOGIC")
            or (self.tokenAtual().tipo == "ID")
        ):
          tempVar.append(self.tokenAtual().lexema)
          self.indexToken += 1   
          if (
            self.tokenAtual().tipo == "ADD"
            or self.tokenAtual().tipo == "SUB"
            or self.tokenAtual().tipo == "MULT"
            or self.tokenAtual().tipo == "DIV"
          ):
            
            tempVar.append(self.tokenAtual().lexema)
           
            self.callOpStatement(tempVar)
          temp.append(tempVar)
          self.tabelaDeSimbolos.append(temp)       
         
            
          
       
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
        #  INICIO TAB 3 END
        nomeDaFuncao = temp[3]
        paramsDaFuncao = temp[4]

        self.tabelaDeTresEnderecos.append(
            ('label', nomeDaFuncao, 'null'))

        for param in paramsDaFuncao:
            self.tabelaDeTresEnderecos.append(
                ('pop', param[2], 'null'))

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
            # Adiciona na tabela de símbolos
            self.tabelaDeSimbolos.append(
                temp)
            self.tabelaDeTresEnderecos.append(
                ('return := ' + self.tempTresEnderecos))
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
        tempParentesesParamAtual.append(self.tokenAtual().linha)
        tempParentesesParamAtual.append(self.tokenAtual().tipo)
        self.indexToken += 1
        if self.tokenAtual().tipo == "ID":
            tempParentesesParamAtual.append(self.tokenAtual().lexema)
            tempParenteses.append(tempParentesesParamAtual)
            self.indexToken += 1
            self.tabelaDeSimbolos.append(tempParentesesParamAtual)
            if self.tokenAtual().tipo == "COMMA":
                self.indexToken += 1
                self.paramsStatement(tempParenteses, temp)
            elif(self.tokenAtual().tipo == "PRIGHT"):
              temp.append(tempParenteses) 
              self.tabelaDeSimbolos.append(temp)   
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
        elif (
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
      self.tempTresEnderecos = self.tokenAtual().lexema

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
              if(self.tokenAtual().tipo == "RETURN"):
                raise Exception(
                  "Erro sintático: return declarado dentro de um procedimento na linha "
                  + str(self.tokenAtual().linha)
                )                 
              tempBlock.append(self.blockStatement(isProc= True))
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
      
  def callProc(self, tempEndVar):
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
          tempEndVar.append(tempParams)
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
    
    
  ''' Semântica '''
  def checkSemantica(self):
    for linha in self.tabelaDeSimbolos:
      if(linha is not None):
        simbolo = linha[2]
        if simbolo == "PROC":
          self.declarationProcSemantico(linha)
                 
        if simbolo == "PROCCALL":
          self.callProcSemantico(linha, 4, linha[1])
        if simbolo == "FUNC":
          self.declarationFuncSemantico(linha)       
       
       
        if simbolo == "WHILE":
          self.expressionSemantico(linha)  

        if simbolo == "INT":
        # # verifica se simbolos de atribicao ja foram declarados
          self.declaration_int_semantico(linha)

        if simbolo == "BOOLEAN":
         # verifica se simbolos de atribicao ja foram declarados
          self.declaration_boolean_semantico(linha)

      #  if simbolo == "ID":
        #  self.declaration_id_semantico(linha)
      #    print("eh id")

        if simbolo == "IF":
          self.expressionSemantico(linha)
    
    print("Terminou")
    
  def declaration_boolean_semantico(self, simbolo):
    for linha in self.tabelaDeSimbolos:
      # Verificando se há duas var. com msm nome
      if linha[3] == simbolo[3]:
        # Se houver, verifica se a variavel está visivel no escopo da qual foi chamada
        
        if linha[0] <= simbolo[0] and linha[1] <= simbolo[1]:
          # verifica se as variaveis da atribuicao ja foram declaradas
          self.variaveis_atribuicao_semantico_boolean(simbolo)  
          return
        elif linha[0] == simbolo[0] and len(linha > 4):  
          raise Exception("Erro Semântico: 03variável não declarada na linha: " + str(simbolo[1]))
    return
  
  def variaveis_atribuicao_semantico_boolean(self, simbolo):
    if(len(simbolo) > 4):
      if(len(simbolo[5]) == 1):
        if(simbolo[5][0] != 'true' and simbolo[5][0] != 'false'):
          self.verifica_escopo_bool(simbolo, simbolo[5][0])
      else:
        raise Exception("Erro Semântico: expressão booleana inválida: " + str(simbolo[1]))

  def declaration_int_semantico(self, simbolo):
    for linha in self.tabelaDeSimbolos:
      # Verificando se há duas var. com msm nome
      if linha[3] == simbolo[3] and linha[2] == simbolo[2]: #linha[2] == simbolo[2] certifica que nao to comparando declaracao de uma variavel com a utilizacao dela (id)
        # Se houver, verifica se a variavel está visivel no escopo da qual foi chamada
        if linha[0] <= simbolo[0] and linha[1] <= simbolo[1]:
          # verifica se as variaveis da atribuicao ja foram declaradas
          self.variaveis_atribuicao_semantico(simbolo)
        elif linha[0] == simbolo[0] and len(linha > 4):    
          raise Exception("Erro Semântico: variável não declarada na linha: " + str(simbolo[1]))        
  
  def variaveis_atribuicao_semantico(self, simbolo):
    #percorre todos os atributos    
    if(len(simbolo) > 4):
      for i in range(0,len(simbolo[5]),2):
        #print(simbolo[5][i])
        #verifica se nao eh ineiro
        if(self.eh_inteiro(simbolo[5][i]) == False):
          #verifica escopo
          self.verifica_escopo_int(simbolo, simbolo[5][i])

  def verifica_escopo_int(self, simbolo, variavel):
    
    for linha in self.tabelaDeSimbolos:
      # Verificando se há duas var. com msm nome
      if linha[3] == variavel:
        #verifica tipo da variavel de atribuicao
        if(linha[2] == "INT"):
          
          # Se houver, verifica se a variavel está visivel no escopo da qual foi chamada
          if linha[0] <= simbolo[0] and linha[1] < simbolo[1]: #linha[1] verifica se a variavel nao ta sendo criada e atribuida na mesma linha
           
            return
          else:
            raise Exception("Erro Semântico: variável não declarada na linha: " + str(simbolo[1]))
        else:
          raise Exception("Erro Semântico: variável de tipo BOOLEAN não pode ser atribuída a INT na linha: " + str(simbolo[1]))

    raise Exception("Erro Semântico: variável não declarada na linha: " + str(simbolo[1]))

  def verifica_escopo_bool(self, simbolo, variavel):
    for linha in self.tabelaDeSimbolos:
      # Verificando se há duas var. com msm nome
      if linha[3] == variavel:
        if(linha[2] == "BOOLEAN"):
          if linha[0] <= simbolo[0] and linha[1] < simbolo[1]: #linha[1] verifica se a variavel nao ta sendo criada e atribuida na mesma linha
           return
          else:
            raise Exception("Erro Semântico: variável não declarada na linha: " + str(simbolo[1]))
        else:
          raise Exception("Erro Semântico: variável de tipo INT não pode ser atribuída a BOOLEAN na linha: " + str(simbolo[1]))
        # Se houver, verifica se a variavel está visivel no escopo da qual foi chamada  
    raise Exception("Erro Semântico: variável não declarada na linha: " + str(simbolo[1]))

  def eh_inteiro(self, valor):
    try: 
        int(valor)
        return True
    except ValueError:
        return False

  def verificar_se_declarado(self, simbolo):
      for linha in self.tabelaDeSimbolos:
          # Verificando se há duas var. com msm nome
          if linha[3] == simbolo[3] and linha[2] != simbolo[2]:
            return True
      return False

  def declaration_id_semantico(self, simbolo):
    for linha in self.tabelaDeSimbolos:
      # Verificando se há duas var. com msm nome
      if linha[3] == simbolo[3] and linha[2] == simbolo[2]: #linha[2] == simbolo[2] certifica que nao to comparando declaracao duma variavel com a utilizacao dela (id)
        #verifica se ja declarado
        if(self.verificar_se_declarado(simbolo)):
        #varre de novo pra saber se a declaracao eh valida
          for linha2 in self.tabelaDeSimbolos:
            # Verificando se há duas var. com msm nome
            if linha2[3] == simbolo[3] and linha2[2] != simbolo[2]:
              # Se houver, verifica se a variavel está visivel no escopo da qual foi chamada
              if linha2[0] >= simbolo[0] and linha2[1] < simbolo[1]:
                #verificando os atributos do id
                if(linha2[2] == "INT"):
                  self.variaveis_atribuicao_semantico(simbolo)
                elif(linha2[2] == "BOOLEAN"):
                  print("aq")
                  self.variaveis_atribuicao_semantico_boolean(simbolo)
              else:
                raise Exception("Erro Semântico: variável não declarada na linha: " + str(simbolo[1]))
        else:
          raise Exception("Erro Semântico: variável não declarada na linha: " + str(simbolo[1]))
  
    
  # TODO: Faltam expressões e funções
  def verificarTipoCallVar(self, simboloDeclaradoNaTabela, simbolo):

    if simboloDeclaradoNaTabela[2] == "INT":
      for k in range(0, len(simbolo[5]), 2):        
        if not simbolo[5][k].isnumeric():
          raise Exception(
            "Erro Semântico: variável do tipo int não recebe int na linha: "
            + str(simbolo[1])
          )        
    if simboloDeclaradoNaTabela[2] == "BOOLEAN":
        if simbolo[5][0] == "true" or simbolo[5][0] == "false":
            return True
        else:
            raise Exception(
                "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                + str(simbolo[1])
            )
            
  def buscarParamsProc(self, simbolo):
    paramsProc = self.buscarNaTabelaDeSimbolos("PROC", 2)
    if paramsProc != None:
        paramsProc = paramsProc[4]
        for k in range(len(paramsProc)):
            if simbolo[3] == paramsProc[k][2]:
                if paramsProc[k][1] == "INT":
                    if simbolo[5].isnumeric():
                        return True
                    if not simbolo[5].isnumeric():
                        raise Exception(
                            "Erro Semântico: variável do tipo int não recebe int na linha: "
                            + str(simbolo[1])
                        )
                if paramsProc[k][1] == "BOOLEAN":
                    # TODO: verificar posteriormente
                    if simbolo[5] == "True" or simbolo[5] == "False":
                        return True
                    else:
                        raise Exception(
                            "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                            + str(simbolo[1])
                        )
                break
    else:
        return False
      
  def buscarParamsFunc(self, simbolo, n):
    paramsFunc = self.buscarNaTabelaDeSimbolos("FUNC", 2)
    if paramsFunc != None:
        paramsFunc = paramsFunc[5]
        for k in range(len(paramsFunc)):
            if simbolo[n] == paramsFunc[k][2]:
                if paramsFunc[k][1] == "INT":
                    if simbolo[5].isnumeric():
                        return True
                    if not simbolo[5].isnumeric():
                        raise Exception(
                            "Erro Semântico: variável do tipo int não recebe int na linha: "
                            + str(simbolo[1])
                        )
                if paramsFunc[k][1] == "BOOLEAN":
                    # TODO: verificar posteriormente
                    if simbolo[5] == "True" or simbolo[5] == "False":
                        return True
                    else:
                        raise Exception(
                            "Erro Semântico: variável do tipo booleano não recebe booleano na linha: "
                            + str(simbolo[1])
                        )
                break
    else:
        return False
              
  def expressionSemantico(self, tabelaNoIndiceAtual):
    if(tabelaNoIndiceAtual[3][0] == "true" or tabelaNoIndiceAtual[3][0] == "false" and len(tabelaNoIndiceAtual[3]) == 1):
      return True
    buscaParam1 = self.buscarNaTabelaDeSimbolos(tabelaNoIndiceAtual[3][0], 3)
    
    if(buscaParam1[2] == "BOOLEAN" and len(tabelaNoIndiceAtual[3]) == 1):
      return True

    if(buscaParam1[2] != "BOOLEAN" and len(tabelaNoIndiceAtual[3]) == 1):
      raise Exception(
        "Erro Semântico: parametros inválidos na linha: "
        + str(tabelaNoIndiceAtual[1]))

    buscaParam2 = self.buscarNaTabelaDeSimbolos(tabelaNoIndiceAtual[3][2], 3)  
    
    if (tabelaNoIndiceAtual[3][0]).isnumeric() and (tabelaNoIndiceAtual[3][2]).isnumeric():
      return True
      
    elif (tabelaNoIndiceAtual[3][0].isalpha() and tabelaNoIndiceAtual[3][2].isalpha()):  
      if buscaParam1 != None and buscaParam2 != None:
        if buscaParam2[2] == "INT" and buscaParam1[2] != "INT":
          raise Exception(
            "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
            + str(tabelaNoIndiceAtual[1])) 
        
        if buscaParam2[2] != "INT" and buscaParam1[2] == "INT":
          raise Exception(
            "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
            + str(tabelaNoIndiceAtual[1]))
                      
        if buscaParam2[2] == "INT" and buscaParam1[2] == "INT":
          if (buscaParam1[0] <= tabelaNoIndiceAtual[0]) and (
              buscaParam2[0] <= tabelaNoIndiceAtual[0]):
              return True
          else:
            raise Exception(
              "Erro Semântico: Variável não declarada na linha: "
              + str(tabelaNoIndiceAtual[1]))  
        if buscaParam2[2] == "BOOLEAN" and buscaParam1[2] == "BOOLEAN":
          if (buscaParam1[0] <= tabelaNoIndiceAtual[0]) and (
            buscaParam2[0] <= tabelaNoIndiceAtual[0]):
            if (
              tabelaNoIndiceAtual[3][1] == "=="
              or tabelaNoIndiceAtual[3][1] == "!="):
                return True
            else:
                raise Exception(
                    "Erro Semântico: Não é possível fazer este tipo de comparação com Boolean na linha: "
                    + str(tabelaNoIndiceAtual[1]))
          else:
              raise Exception(
                  "Erro Semântico: Variável não declarada na linha: "
                  + str(tabelaNoIndiceAtual[1]))

        if buscaParam2[2] == "INT" and buscaParam1[2] == "BOOLEAN":
          raise Exception(
              "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
              + str(tabelaNoIndiceAtual[1]))
          
        if buscaParam2[2] == "BOOLEAN" and buscaParam1[2] == "INT":
          raise Exception(
            "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
            + str(tabelaNoIndiceAtual[1]))
      else:
        raise Exception(
          "Erro Semântico: variavel não declarada na linha: "
          + str(tabelaNoIndiceAtual[1]))
     
    elif tabelaNoIndiceAtual[3][0].isalpha() and tabelaNoIndiceAtual[3][2].isnumeric():     
      if buscaParam1 != None:
        if buscaParam1[2] != "INT":
          raise Exception(
            "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
            + str(tabelaNoIndiceAtual[1]))
        else:
          if buscaParam1[0] <= tabelaNoIndiceAtual[0]:
            return True
          else:
            raise Exception(
              "Erro Semântico: Variável não declarada na linha: "
              + str(tabelaNoIndiceAtual[1]))
            
      else:
        raise Exception(
          "Erro Semântico: variavel não declarada na linha: "
          + str(tabelaNoIndiceAtual[1]))  
        
    elif (tabelaNoIndiceAtual[3][0]).isnumeric() and tabelaNoIndiceAtual[3][2].isalpha():
      if buscaParam2 != None:
        if buscaParam2[2] != "INT":
          raise Exception(
            "Erro Semântico: Não é possível comparar dois tipos diferentes na linha: "
            + str(tabelaNoIndiceAtual[1]))
        else:
          if buscaParam2[0] <= tabelaNoIndiceAtual[0]:
            return True
          else:
            raise Exception(
              "Erro Semântico: Variável não declarada na linha: "
              + str(tabelaNoIndiceAtual[1]))
      else:
        raise Exception(
          "Erro Semântico: variavel não declarada na linha: "
          + str(tabelaNoIndiceAtual[1]))
   
    else:
      raise Exception(
        "Erro Semântico: parametros inválidos na linha: "
        + str(tabelaNoIndiceAtual[1]))    
      
  def buscarNaTabelaDeSimbolos(self, simbolo, indice):
    for k in range(len(self.tabelaDeSimbolos)):
      if(self.tabelaDeSimbolos[k] is not None):
        if self.tabelaDeSimbolos[k][indice] == simbolo:
            return self.tabelaDeSimbolos[k]

  def callProcSemantico(self, tabelaNoIndiceAtual, m, linha):
    flag = False
    for k in range(len(self.tabelaDeSimbolos)):
      if self.tabelaDeSimbolos[k][2] == "PROC":
        if self.tabelaDeSimbolos[k][3] == tabelaNoIndiceAtual[3]:
          if self.tabelaDeSimbolos[k][0] <= tabelaNoIndiceAtual[0]:
            flag = True
           
            self.verificarParams(
                self.tabelaDeSimbolos[k],
                tabelaNoIndiceAtual,
                4,
                "PROC",
                m,
                linha,
                tabelaNoIndiceAtual[0],
            )
            break

    # Se der errado a declaração:
    if flag == False:
        raise Exception(
            "Erro Semântico: procedimento não declarado na linha: "
            + str(tabelaNoIndiceAtual[1])
          )
  
  def verificarParams(
        self, simboloDeclaradoNaTabela, simbolo, n, tipo, m, linha, escopo
    ):    
    flag = 0
    # Verifica se a quantidade de parametros da chamada corresponde com a declaração
    if len(simboloDeclaradoNaTabela[n]) == len(simbolo[m]):
      # Se os parâmetros não for vazio:     
      if len(simbolo[m]) > 0:
        # P/ cada parâmetro        
        for k in range(len(simbolo[m])):
          if(simbolo[m][k].isnumeric()):
            if(simboloDeclaradoNaTabela[n][k][2] != "INT"):
               raise Exception(
                "Erro Semântico: tipo de variavel errada na linha: "
                + str(linha))
            else:
              flag += 1
          elif(simbolo[m][k] == "true" or simbolo[m][k] == "false"):
            if(simboloDeclaradoNaTabela[n][k][2] != "BOOLEAN"):
               raise Exception(
                "Erro Semântico: tipo de variavel errada na linha: "
                + str(linha))
            else:
              flag += 1
          else:
            
            localFlag = False
            for i in range(len(self.tabelaDeSimbolos)):
              if self.tabelaDeSimbolos[i][3] == simbolo[m][k]:
                if (self.tabelaDeSimbolos[i][0] <= escopo) and (self.tabelaDeSimbolos[i][1] <= linha):
                  if (self.tabelaDeSimbolos[i][2] == "INT" or self.tabelaDeSimbolos[i][2] == "BOOLEAN"):
                    
                    if(self.tabelaDeSimbolos[i][2] == simboloDeclaradoNaTabela[n][k][2]):
                      localFlag = True
                      flag += 1
                      break
                    else:
                      raise Exception("Erro Semântico: tipo do parâmetro inválido na linha: " + str(simbolo[1])) 
            
            if localFlag == False:
              raise Exception(
                  "Erro Semântico: parâmetro inválido na linha: "
                  + str(simbolo[1])
              )      

      # Se não tiver params
      else:
          return True
    else:
        raise Exception(
            "Erro Semântico: quantidade de parâmetros inválido na linha: "
            + str(linha)
        )
    if flag != len(simboloDeclaradoNaTabela[n]):
        raise Exception(
            "Erro Semântico: variável do parâmetro não declarada na linha: "
            + str(linha)
        )
    else:
        return True

  def declarationFuncSemantico(self, tabelaNoIndiceAtual):
    if tabelaNoIndiceAtual[3] == "INT":
      if not tabelaNoIndiceAtual[7][2][0].isnumeric():
          raise Exception(
              "Erro Semântico: O retorno espera um inteiro na linha: "
              + str(tabelaNoIndiceAtual[1])
          )

    if tabelaNoIndiceAtual[3] == "BOOLEAN":
      if (
          tabelaNoIndiceAtual[7][2][0] == "true"
          or tabelaNoIndiceAtual[7][2][0] == "false"
      ) is False:
          raise Exception(
              "Erro Semântico: O retorno espera um boolean na linha: "
              + str(tabelaNoIndiceAtual[1])
          )
          
      
  def declarationProcSemantico(self, tabelaNoIndiceAtual):
    for k in range(len(tabelaNoIndiceAtual[4])):
      if tabelaNoIndiceAtual[4][k][2] != "INT" and tabelaNoIndiceAtual[4][k][2] != "BOOLEAN":
         raise Exception(
          "Erro Semântico: Os paramêtros precisam ser INT ou BOOLEAN na linha: "
          + str(tabelaNoIndiceAtual[0])
        )       

