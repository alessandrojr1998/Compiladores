class Parser:
  def __init__(self, tabTokens):
    self.tabTokens = tabTokens
    self.indexToken = 0
    self.indexLookAhead = 0
    self.indexEscopoAtual = -1
    self.tabSimbolos = []

  def tokenAtual(self):
    return self.tabTokens[self.indexToken]

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
      print("Entrou")
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
    self.indexToken +=1
    return