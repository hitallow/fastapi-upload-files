## Exemplo de aplicação de upload de arquivo

Essa é um exemplo de aplicação que faz a extração de dados de um arquivo grande CSV utilizando um conjunto de ferramentas interressantes no desenvolvimento de software.

## Arquitetura usada

Para o desenvolvimento desta aplicação, foram aplicados os princípios da Clean Architecture. Alguns dos conceitos utilizados incluem:

- Independência de bibliotecas externas: O código limpo está claramente separado das dependências externas. Utilizamos arquivos de configuração para realizar a integração do código Python puro com bibliotecas como o FastAPI, mantendo a modularidade e a flexibilidade do sistema.

- Independência de Banco de Dados: A aplicação não possui conhecimento sobre a implementação específica do banco de dados. Utilizamos repositórios para encapsular a lógica de acesso aos dados, permitindo que a aplicação apenas interaja com interfaces abstratas para manipulação dos dados.

- Inversão de Dependência: A comunicação entre os componentes da aplicação é realizada por meio de interfaces, implementadas na camada de infraestrutura. Isso permite que o núcleo central da aplicação seja totalmente independente das implementações concretas, promovendo a modularidade e a reutilização do código.

- Testabilidade: Todos os componentes da aplicação foram devidamente testados, garantindo sua qualidade e robustez.

- Separação de Responsabilidades: A aplicação é dividida em módulos Python, cada um com uma responsabilidade específica e bem definida. Isso facilita a manutenção do código e promove a coesão e a baixo acoplamento entre os componentes.
- Padrões de Projeto: Utilizamos padrões de projeto como Factory, Singleton e Repository para promover a reutilização de código, simplificar o desenvolvimento e aumentar a flexibilidade da aplicação.


### Modulos e arquivos

- **main**: Este é basicamente o ponto de entrada para o mundo externo. Ele fornece o aplicativo que é executado e as filas que leem as mensagens em fila.

- **domain**: O núcleo da aplicação, onde estão os casos de uso, modelos, entidades, exceções e contratos. Basicamente, o código é independente da aplicação e não depende de nenhuma outra camada.

- **infra**: Implementação dos contratos definidos na camada de domínio. Esta é a camada mais "suja" da aplicação, pois implementa os contratos usando as interfaces definidas no domínio.

- **presentation**: Este é o lugar onde é implementada a exposição dos casos de uso, onde o FastAPI (neste caso) monta os endpoints e fornece ao mundo externo todos os casos de uso. Também implementa métodos exclusivos do FastAPI como por exemplo o middleware de gerenciamento de erros.


# Setup 

## Executando projeto

Para rodar a aplicação locamente, você só deve ter instalado e configurado o docker.
#### Variaveis de ambiente 

Configure as Variaveis de ambiente, preencha com base no seu uso, suas funções são:

| Chave                 | Funcionalidade                                    |
|-----------------------|---------------------------------------------------|
| APP_PORT              | Porta onde o projeto deverá rodar na sua máquina  |
| AWS_ACCESS_KEY_ID     | ID AWS para acesso ao servidor AWS                |
| AWS_SECRET_ACCESS_KEY | Secret AWS para acesso ao servidor                |
| AWS_URL               | URL do servidor AWS                               |
| MAIL_HOST             | servidor de email                                 |
| MAIL_USERNAME         | email ou username para acesso ao servidor de email| 
| MAIL_PASSWORD         | Senha para acesso ao servidor de email            | 
| MAIL_PORT             | Porta para acesso ao servidor de email            | 
| MAIL_FROM             | Remetente dos email                               | 

A aplicação pode utilizar localmente o container do localstack, dessa forma, o .env.example já utiliza as credenciais que devem funcionar localmente.

Dessa forma, utilize:

```bash
$ docker compose build
```

e logo depois

```bash
$ docker compose up
```


#### Migrações
Após rodar a aplicação, é nescessário criar as informações de banco de dados.

A aplicação tem um mini gerenciador de migrações, que rodar arquivos SQL e os controla para que executem apenas uma vez.
No entanto é nescessário criar a tabela de migrações manualmente, por questão de exemplo eu fiz uso do SQLite, há um arquivo chamado `execute-manual.sql` dentro da pasta sql. Execute ele manualmente.


Após isso, você deve rodar as migrações, utilize o comando:
```bash
$ make run-migration
```

## Testes

Aplicação foi totalmente testada utilizando pytest e algumas funcionalidades do unitest, para rodar os testes e obter o coverage utilize o comando

```bash
$ make run-tests
```
