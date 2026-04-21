# MVP To-Do List API

Uma API RESTful simples para gerenciamento de tarefas, construída com Python, Flask e SQLite.

## Stack Tecnológico

- **Python 3.8+**
- **Flask 2.3.3** - Framework web
- **Flask-SQLAlchemy 3.0.5** - ORM para SQLite
- **SQLite** - Banco de dados
- **Git** - Versionamento

## Funcionalidades

✅ **CRUD Completo de Tarefas**
- Criar novas tarefas
- Ler/Listar tarefas
- Atualizar tarefas existentes
- Deletar tarefas

✅ **Gerenciamento de Status**
- Marcar tarefas como concluídas
- Filtrar tarefas por status (pending/completed)

✅ **Estatísticas**
- Visualizar total de tarefas
- Contar tarefas pendentes
- Contar tarefas concluídas

## Estrutura do Projeto

```
MVPtodolist/
├── app/
│   ├── __init__.py          # Factory da aplicação
│   ├── database.py          # Configuração SQLAlchemy
│   ├── models.py            # Modelo Task
│   └── routes.py            # Rotas da API
├── data/                    # Banco de dados SQLite
├── tests/                   # Testes unitários
├── main.py                  # Ponto de entrada
├── requirements.txt         # Dependências do projeto
├── .env.example             # Variáveis de ambiente exemplo
├── .gitignore               # Arquivo para Git
└── README.md                # Este arquivo
```

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
   ```bash
   git clone <seu-repositorio>
   cd MVPtodolist
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Ativar no Windows
   venv\Scripts\activate
   
   # Ativar no macOS/Linux
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```

5. **Execute a aplicação**
   ```bash
   python main.py
   ```

A API estará disponível em: `http://localhost:5000`

## Endpoints da API

### Base URL
```
http://localhost:5000/api/tasks
```

### 1. Listar Tarefas
```http
GET /api/tasks
```

**Query Parameters (opcional):**
- `status`: Filtra por status (`pending` ou `completed`)

**Exemplo:**
```bash
curl http://localhost:5000/api/tasks
curl http://localhost:5000/api/tasks?status=pending
```

**Resposta (200):**
```json
[
  {
    "id": 1,
    "title": "Aprender Python",
    "description": "Estudar conceitos avançados",
    "status": "pending",
    "created_at": "2026-04-21T10:30:00",
    "updated_at": "2026-04-21T10:30:00"
  }
]
```

### 2. Obter Tarefa Específica
```http
GET /api/tasks/{id}
```

**Exemplo:**
```bash
curl http://localhost:5000/api/tasks/1
```

**Resposta (200):**
```json
{
  "id": 1,
  "title": "Aprender Python",
  "description": "Estudar conceitos avançados",
  "status": "pending",
  "created_at": "2026-04-21T10:30:00",
  "updated_at": "2026-04-21T10:30:00"
}
```

### 3. Criar Tarefa
```http
POST /api/tasks
```

**Request Body:**
```json
{
  "title": "Aprender Python",
  "description": "Estudar conceitos avançados"
}
```

**Exemplo:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender Python", "description": "Estudar conceitos avançados"}'
```

**Resposta (201):**
```json
{
  "id": 1,
  "title": "Aprender Python",
  "description": "Estudar conceitos avançados",
  "status": "pending",
  "created_at": "2026-04-21T10:30:00",
  "updated_at": "2026-04-21T10:30:00"
}
```

### 4. Atualizar Tarefa
```http
PUT /api/tasks/{id}
```

**Request Body (todos os campos opcionais):**
```json
{
  "title": "Aprender Python Avançado",
  "description": "Estudar decorators e generators",
  "status": "completed"
}
```

**Exemplo:**
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

**Resposta (200):**
```json
{
  "id": 1,
  "title": "Aprender Python",
  "description": "Estudar conceitos avançados",
  "status": "completed",
  "created_at": "2026-04-21T10:30:00",
  "updated_at": "2026-04-21T10:35:00"
}
```

### 5. Marcar Tarefa como Concluída
```http
PATCH /api/tasks/{id}/complete
```

**Exemplo:**
```bash
curl -X PATCH http://localhost:5000/api/tasks/1/complete
```

**Resposta (200):**
```json
{
  "id": 1,
  "title": "Aprender Python",
  "description": "Estudar conceitos avançados",
  "status": "completed",
  "created_at": "2026-04-21T10:30:00",
  "updated_at": "2026-04-21T10:35:00"
}
```

### 6. Deletar Tarefa
```http
DELETE /api/tasks/{id}
```

**Exemplo:**
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

**Resposta (200):**
```json
{
  "message": "Tarefa deletada com sucesso"
}
```

### 7. Obter Estatísticas
```http
GET /api/tasks/stats
```

**Exemplo:**
```bash
curl http://localhost:5000/api/tasks/stats
```

**Resposta (200):**
```json
{
  "total": 5,
  "pending": 3,
  "completed": 2
}
```

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 201 | Recurso criado |
| 400 | Requisição inválida |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

## Padrões de Código

O projeto segue os padrões **PEP 8** para estilo de código Python:

- **Indentação**: 4 espaços
- **Comprimento de linha**: máximo 79 caracteres
- **Nomes de funções**: snake_case
- **Nomes de classes**: PascalCase
- **Docstrings**: No formato Google Style
- **Imports**: Organizados e agrupados

## Desenvolvendo

### Executar Testes
```bash
python -m pytest tests/
```

### Usando o Git

```bash
# Inicializar repositório (se necessário)
git init

# Adicionar arquivos
git add .

# Commit inicial
git commit -m "Initial commit: MVP To-Do List API"

# Criar branch para desenvolvimento
git checkout -b develop
```

## Licença

Este projeto é livre para uso educacional e comercial.

## Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request