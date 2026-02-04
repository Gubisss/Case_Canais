from lambda_handler import classificar_texto

resultado = classificar_texto("Fui roubado e meu cartao foi clonado, quero bloquear meu cartao")
##"Fui cobrado duplicadamente,Aplicativo muito lento, Não consigo acessar minha conta"
#"Fui roubado e meu cartao foi clonado, quero bloquear meu cartao"
#"Estou insatisfeito com o banco em geral"
#"Estou com problemas para acessar o aplicativo, ele está travado e lento"
print(resultado)