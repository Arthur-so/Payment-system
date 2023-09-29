## Instalação

1. Clone o repositório:

```bash
$ git clone https://github.com/Arthur-so/Payment-system.git
```

2. Instale as dependências com Maven

## Utilização

1. Instale as dependências com o Maven
2. A API estará acessível em http://localhost:8080
3. Navegue até ./mock e execute:
   ```python
   python mockTransaction.py
    `````

## Objetivo: PicPay Simplificado

Temos 2 tipos de usuários, os comuns e lojistas, ambos têm carteira com dinheiro e realizam transferências entre eles. Vamos nos atentar **somente** ao fluxo de transferência entre dois usuários.

Requisitos:

- Para ambos tipos de usuário, precisamos do Nome Completo, CPF, e-mail e Senha. CPF/CNPJ e e-mails devem ser únicos no sistema. Sendo assim, seu sistema deve permitir apenas um cadastro com o mesmo CPF ou endereço de e-mail.

- Usuários podem enviar dinheiro (efetuar transferência) para lojistas e entre usuários.

- Lojistas **só recebem** transferências, não enviam dinheiro para ninguém.

- Validar se o usuário tem saldo antes da transferência.

- Antes de finalizar a transferência, deve-se consultar um serviço autorizador externo, use este mock para simular (https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6).

- A operação de transferência deve ser uma transação (ou seja, revertida em qualquer caso de inconsistência) e o dinheiro deve voltar para a carteira do usuário que envia.

- No recebimento de pagamento, o usuário ou lojista precisa receber notificação (envio de email, sms) enviada por um serviço de terceiro e eventualmente este serviço pode estar indisponível/instável. Use este mock para simular o envio (http://o4d9z.mocklab.io/notify).

- Este serviço deve ser RESTFul.

## Observação
Como os mocks https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6 e http://o4d9z.mocklab.io/notify não estão mais disponíveis foi criado um servidor python para representá-los.
Por isso é necessário executar ./mock/mockTransaction.py, ele foi criado para simular o acesso aos mocks inacessíveis.

## API Endpoints
A API disponibiliza os seguintes endpoints:

```markdown
POST /users - Registra um novo usuário.

GET /users - Recebe uma lista de todos os usuários registrados.

POST /transactions - Realiza uma nova transação entre dois usuários.
```

## Exemplo de requisições e respostas:
 
### POST /users
#### Requisição

````json
{
  "firstName": "Arthur",
  "lastName": "Oliveira",
  "document": "123456789",
  "password": "65dgbf9",
  "email": "arthur@oliveira.com",
  "userType": "COMMON",
  "balance": 50
}
````

#### Resposta
- Em caso de sucesso
    - Status code: 201
    - Dados do usuário cadastrados
- Em caso de tentativa de registro de usuário já cadastrado:
  - Status code: 400 
  - ````json
      {
          "message": "Usuário já cadastrado",
          "statusCode": "400"
      }
      ````

### GET /users
#### Resposta
````json
[
	{
		"id": 1,
		"firstName": "ArtTecnology",
		"lastName": "SA",
		"document": "481984868",
		"email": "art@tecnology.com",
		"password": "55d4cv4d9vd",
		"balance": 2000.00,
		"userType": "MERCHANT"
	},
	{
		"id": 2,
		"firstName": "Arthur",
		"lastName": "Oliveira",
		"document": "123456789",
		"email": "arthur@oliveira.com",
		"password": "65dgbf9",
		"balance": 50.00,
		"userType": "COMMON"
	}
]
````

### POST /transactions
#### Requisição
````json
{
    "senderId": 2,
	"receiverId": 1,
	"value": 10
}
````

#### Resposta
- Em caso de sucesso
  - Status code: 200
  - ````json
      {
          "id": 1,
          "amount": 10,
          "sender": {
              "id": 2,
              "firstName": "Arthur",
              "lastName": "Oliveira",
              "document": "123456789",
              "email": "arthur@oliveira.com",
              "password": "65dgbf9",
              "balance": 40.00,
              "userType": "COMMON"
          },
          "receiver": {
              "id": 1,
              "firstName": "ArtTecnology",
              "lastName": "SA",
              "document": "481984868",
              "email": "art@tecnology.com",
              "password": "55d4cv4d9vd",
              "balance": 2010.00,
              "userType": "MERCHANT"
          },
          "timestamp": "2023-09-29T17:01:21.8777936"
      }
      ````
    - Em caso de ID não encontrado:
      - Status code: 500
      - ````json
        {
            "message": "Usuário não encontrado",
            "statusCode": "500"
        }
        ````
    - Em caso de saldo insuficiente
      - Status code: 500
      - ````json
        {
            "message": "Saldo insuficiente",
            "statusCode": "500"
        }
        ````
    - Em caso de tentativa de lojista realizar envio de dinheiro
      - Status code: 500
      - ````json
        {
            "message": "Usuário do tipo lojista não está autorizado a realizar transação.",
            "statusCode": "500"
        }
        ````
    - Em caso de transação não autorizada pelo mock
      - Status code: 500
      - ````json
        {
             "message": "Transação não autorizada.",
             "statusCode": "500"
        }
        ````