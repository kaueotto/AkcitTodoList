"""Script para testar rapidamente a API localmente."""
import requests
import json

BASE_URL = 'http://localhost:5000/api/tasks'


def print_response(title, response):
    """Imprime resposta formatada."""
    print(f'\n{"="*50}')
    print(f'{title}')
    print(f'{"="*50}')
    print(f'Status Code: {response.status_code}')
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


def test_api():
    """Testa os endpoints da API."""
    print('🚀 Iniciando testes da API To-Do List')

    # 1. Criar tarefas
    print('\n📝 TESTE 1: Criar Tarefas')
    task1_data = {
        'title': 'Aprender Python',
        'description': 'Estudar conceitos avançados'
    }
    response = requests.post(BASE_URL, json=task1_data)
    print_response('POST /api/tasks (Tarefa 1)', response)
    task1_id = response.json()['id']

    task2_data = {
        'title': 'Implementar API',
        'description': 'Criar endpoints RESTful'
    }
    response = requests.post(BASE_URL, json=task2_data)
    print_response('POST /api/tasks (Tarefa 2)', response)
    task2_id = response.json()['id']

    # 2. Listar todas as tarefas
    print('\n📋 TESTE 2: Listar Todas as Tarefas')
    response = requests.get(BASE_URL)
    print_response('GET /api/tasks', response)

    # 3. Obter tarefa específica
    print('\n🔍 TESTE 3: Obter Tarefa Específica')
    response = requests.get(f'{BASE_URL}/{task1_id}')
    print_response(f'GET /api/tasks/{task1_id}', response)

    # 4. Atualizar tarefa
    print('\n✏️  TESTE 4: Atualizar Tarefa')
    update_data = {
        'description': 'Aprofundar em decorators, generators e async/await'
    }
    response = requests.put(f'{BASE_URL}/{task1_id}', json=update_data)
    print_response(f'PUT /api/tasks/{task1_id}', response)

    # 5. Marcar tarefa como concluída
    print('\n✅ TESTE 5: Marcar Tarefa como Concluída')
    response = requests.patch(f'{BASE_URL}/{task1_id}/complete')
    print_response(f'PATCH /api/tasks/{task1_id}/complete', response)

    # 6. Filtrar por status
    print('\n🔎 TESTE 6: Filtrar Tarefas por Status')
    response = requests.get(f'{BASE_URL}?status=pending')
    print_response('GET /api/tasks?status=pending', response)

    response = requests.get(f'{BASE_URL}?status=completed')
    print_response('GET /api/tasks?status=completed', response)

    # 7. Obter estatísticas
    print('\n📊 TESTE 7: Obter Estatísticas')
    response = requests.get(f'{BASE_URL}/stats')
    print_response('GET /api/tasks/stats', response)

    # 8. Deletar tarefa
    print('\n🗑️  TESTE 8: Deletar Tarefa')
    response = requests.delete(f'{BASE_URL}/{task2_id}')
    print_response(f'DELETE /api/tasks/{task2_id}', response)

    # 9. Verificar estatísticas após deleção
    print('\n📊 TESTE 9: Estatísticas Após Deleção')
    response = requests.get(f'{BASE_URL}/stats')
    print_response('GET /api/tasks/stats (após deleção)', response)

    print('\n' + '='*50)
    print('✨ Testes concluídos!')
    print('='*50)


if __name__ == '__main__':
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print('❌ Erro: Não foi possível conectar à API.')
        print('Certifique-se de que o servidor está rodando em '
              'http://localhost:5000')
    except Exception as e:
        print(f'❌ Erro durante os testes: {e}')
