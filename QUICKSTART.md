# 🚀 Quick Start - MVP To-Do List

## Instalação Rápida

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
python main.py
```

A API estará disponível em: **http://localhost:5000**

## Testando a API

### Opção 1: Script Python (Recomendado)
```bash
# Em um terminal diferente
python test_api.py
```

### Opção 2: Using cURL

**Criar tarefa:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Minha primeira tarefa", "description": "Descrição da tarefa"}'
```

**Listar tarefas:**
```bash
curl http://localhost:5000/api/tasks
```

**Listar tarefas pendentes:**
```bash
curl http://localhost:5000/api/tasks?status=pending
```

**Marcar como concluída:**
```bash
curl -X PATCH http://localhost:5000/api/tasks/1/complete
```

**Obter estatísticas:**
```bash
curl http://localhost:5000/api/tasks/stats
```

### Opção 3: Postman

Importe os endpoints abaixo no Postman:

- `POST http://localhost:5000/api/tasks` - Criar tarefa
- `GET http://localhost:5000/api/tasks` - Listar tarefas
- `GET http://localhost:5000/api/tasks/{id}` - Ver tarefa
- `PUT http://localhost:5000/api/tasks/{id}` - Atualizar
- `PATCH http://localhost:5000/api/tasks/{id}/complete` - Marcar como concluída
- `DELETE http://localhost:5000/api/tasks/{id}` - Deletar
- `GET http://localhost:5000/api/tasks/stats` - Estatísticas

## Padrões PEP 8

O código segue rigorosamente os padrões PEP 8:

✅ Indentação: 4 espaços
✅ Comprimento máximo de linha: 79 caracteres
✅ Nomes em snake_case para funções/variáveis
✅ Nomes em PascalCase para classes
✅ Docstrings documentadas
✅ Imports organizados

**Verificar conformidade:**
```bash
pip install flake8
flake8 app/
```

## Estrutura do Código

```
MVPtodolist/
├── app/
│   ├── __init__.py         # Factory da app
│   ├── database.py         # SQLAlchemy config
│   ├── models.py           # Modelo Task
│   └── routes.py           # Endpoints API
├── tests/
│   ├── __init__.py
│   └── test_tasks.py       # Testes unitários
├── main.py                 # Entry point
├── test_api.py            # Script de teste
├── requirements.txt        # Dependências
├── .env.example            # Config exemplo
├── .gitignore              # Git ignore
├── .flake8                 # PEP 8 config
└── README.md               # Documentação completa
```

## Executar Testes Unitários

```bash
pip install pytest
pytest tests/
```

## Próximos Passos

- [ ] Adicionar autenticação (JWT)
- [ ] Implementar paginação
- [ ] Adicionar validação com Marshmallow
- [ ] Deploy em produção
- [ ] Documentação Swagger/OpenAPI
- [ ] Cobertura de testes com coverage
- [ ] CI/CD com GitHub Actions

## Git

```bash
# Status
git status

# Ver commits
git log --oneline

# Criar branch
git checkout -b feature/sua-feature

# Push para remote
git push origin main
```

## Suporte

Para dúvidas ou problemas, consulte o [README.md](README.md) principal.

---

**Desenvolvido com ❤️ usando Python, Flask e SQLite**
