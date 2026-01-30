from lambda_handler import classificar_texto

resultado = classificar_texto("Fui roubado e meu cartao foi clonado, quero bloquear meu cartao")
##"Fui cobrado duplicadamente,Aplicativo muito lento, Não consigo acessar minha conta"
print(resultado)