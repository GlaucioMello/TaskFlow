# TaskFlow — API REST de Gerenciamento de Tarefas

API REST desenvolvida em Python com FastAPI para gerenciamento de usuários e tarefas, com autenticação, validação de dados e testes automatizados.

O projeto foi desenvolvido para praticar e demonstrar conceitos de desenvolvimento backend, organização de APIs REST, segurança e qualidade de código.

## Funcionalidades

- **Gerenciamento de usuários:** criação e consulta de usuários, atualização e exclusão.
- **Autenticação:** login com geração de token JWT.
- **Rotas protegidas:** acesso às funcionalidades autenticadas por meio de token.
- **Gerenciamento de tarefas:** criação, listagem, consulta e atualização de tarefas, além de exclusão.
- **Segurança de senhas:** armazenamento de senhas utilizando hash.
- **Validação de dados:** tratamento e validação das informações recebidas pela API.
- **Testes automatizados:** testes para autenticação, rotas e operações de gerenciamento de tarefas.
- **Documentação interativa:** exploração e teste dos endpoints pela interface Swagger do FastAPI.

## Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- JWT — autenticação baseada em tokens
- Argon2 — hash de senhas
- Pytest — testes automatizados
- Uvicorn — servidor ASGI

## Requisitos

- Python 3.11 ou compatível com as dependências do projeto
- Git
- Ambiente virtual Python

## Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/GlaucioMello/TaskFlow.git
cd TaskFlow
```

### 2. Crie e ative o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Configure as variáveis necessárias conforme `app/config.py`.

Defina uma chave secreta própria para o ambiente local e mantenha credenciais e arquivos `.env` fora do controle de versão.

### 5. Inicie a API

```bash
uvicorn app.main:app --reload
```

Por padrão, a aplicação fica disponível em:

`http://127.0.0.1:8000`

### 6. Acesse a documentação

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

A documentação interativa permite consultar os endpoints e enviar requisições para testar a API.

## Principais endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/users/` | Criar usuário |
| GET | `/users/` | Listar usuários |
| GET | `/users/{user_id}` | Consultar usuário |
| PUT | `/users/{user_id}` | Atualizar usuário |
| DELETE | `/users/{user_id}` | Excluir usuário |
| POST | `/auth/login` | Autenticar e obter token |
| GET | `/users/me` | Consultar usuário autenticado |

O gerenciamento de tarefas inclui operações de criação, listagem, atualização e exclusão. Consulte `/docs` para verificar os caminhos e parâmetros exatos disponíveis na versão atual.

## Executando os testes

Com o ambiente virtual ativado, execute:

```bash
python -m pytest -v
```

Os testes verificam comportamentos da aplicação, incluindo autenticação, acesso às rotas protegidas e operações CRUD de tarefas.

## Segurança

- Autenticação baseada em JWT.
- Hash de senhas com Argon2.
- Configuração de segredo por variável de ambiente.
- Separação das configurações sensíveis do código versionado.

Este projeto é de estudo e portfólio. Antes de utilizá-lo em produção, são necessários testes e uma revisão de segurança adequados ao ambiente de implantação.

## Objetivo do projeto

O TaskFlow faz parte do meu portfólio de desenvolvimento backend e demonstra a aplicação prática de conceitos de APIs REST, Python, autenticação, segurança e testes automatizados.

## Autor

**Gláucio Melo Da Silva Assis**

- GitHub: https://github.com/GlaucioMello
- Repositório: https://github.com/GlaucioMello/TaskFlow
