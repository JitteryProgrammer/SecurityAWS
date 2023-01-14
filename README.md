# SecurityAWS
script que verifica a segurança de sua conta na AWS, ele faz isso verificando as regras de segurança de todas as instâncias e verificando se elas estão usando as regras de segurança corretas. 

# Atualizações
º Adicionei o Reservations e o Instances para percorrer as instâncias corretamente.

º Alterei os prints para usar f-strings para tornar a mensagem mais clara.

º Adicionei return False no final da função para garantir que o resultado da função sempre será um valor booleano.

º O script agora verifica se algum Elastic IP está desvinculado, o que é importante para evitar cobranças desnecessárias.

º Adicionei um armazenador para os  resultados da verificação em um arquivo CSV para que eles possam ser analisados e auditados posteriormente
