# SecurityAWS
Este programa é um script em Python que verifica a segurança das instâncias do Amazon Elastic Compute Cloud (EC2) em uma conta da Amazon Web Services (AWS), ele faz isso listando as regras de segurança e as instâncias em uma conta da AWS, e em seguida, verificando se as instâncias estão usando as regras de segurança corretas.

# Atualizações
Adicionei o Reservations e o Instances para percorrer as instâncias corretamente.
Alterei os prints para usar f-strings para tornar a mensagem mais clara.
Adicionei return False no final da função para garantir que o resultado da função sempre será um valor booleano.
