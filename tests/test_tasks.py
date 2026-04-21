"""Testes unitários para as rotas de tarefas."""
import json
from app import create_app
from app.database import db


class TestTasks:
    """Testes para a API de tarefas."""

    def setup_method(self):
        """Configuração antes de cada teste."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        with self.app.app_context():
            db.create_all()

        self.client = self.app.test_client()

    def teardown_method(self):
        """Limpeza após cada teste."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_task(self):
        """Testa criação de uma tarefa."""
        response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Nova Tarefa'}),
            content_type='application/json'
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == 'Nova Tarefa'
        assert data['status'] == 'pending'

    def test_create_task_missing_title(self):
        """Testa criação de tarefa sem título."""
        response = self.client.post(
            '/api/tasks',
            data=json.dumps({'description': 'Sem título'}),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_create_task_empty_title(self):
        """Testa criação de tarefa com título vazio."""
        response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': '', 'description': 'Título vazio'}),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_create_task_only_spaces_title(self):
        """Testa criação de tarefa com título contendo apenas espaços."""
        response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': '   ', 'description': 'Apenas espaços'}),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_get_all_tasks(self):
        """Testa obtenção de todas as tarefas."""
        # Criar algumas tarefas
        self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa 1'}),
            content_type='application/json'
        )
        self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa 2'}),
            content_type='application/json'
        )

        response = self.client.get('/api/tasks')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2

    def test_get_task_by_id(self):
        """Testa obtenção de uma tarefa específica."""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Minha Tarefa'}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/api/tasks/{task_id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id
        assert data['title'] == 'Minha Tarefa'

    def test_update_task(self):
        """Testa atualização de uma tarefa."""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Antiga'}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        response = self.client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps({'title': 'Nova', 'status': 'completed'}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Nova'
        assert data['status'] == 'completed'

    def test_update_task_invalid_status(self):
        """Testa atualização com status inválido."""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa'}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        response = self.client.put(
            f'/api/tasks/{task_id}',
            data=json.dumps({'status': 'invalid_status'}),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_get_nonexistent_task(self):
        """Testa obtenção de tarefa que não existe."""
        response = self.client.get('/api/tasks/99999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_delete_task(self):
        """Testa deleção de uma tarefa."""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa a Deletar'}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        response = self.client.delete(f'/api/tasks/{task_id}')

        assert response.status_code == 200

        # Verificar que foi deletada
        get_response = self.client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404

    def test_filter_by_status(self):
        """Testa filtro de tarefas por status."""
        # Criar tarefas
        create1 = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa 1'}),
            content_type='application/json'
        )
        task_id_1 = json.loads(create1.data)['id']

        create2 = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa 2'}),
            content_type='application/json'
        )
        task_id_2 = json.loads(create2.data)['id']

        # Marcar a primeira como concluída
        self.client.patch(f'/api/tasks/{task_id_1}/complete')

        # Filtrar por pending
        response = self.client.get('/api/tasks?status=pending')
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['id'] == task_id_2

        # Filtrar por completed
        response = self.client.get('/api/tasks?status=completed')
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['id'] == task_id_1

    def test_filter_by_invalid_status(self):
        """Testa filtro com status inválido."""
        response = self.client.get('/api/tasks?status=invalid')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_complete_task(self):
        """Testa marcação de tarefa como concluída."""
        create_response = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa'}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.data)['id']

        response = self.client.patch(f'/api/tasks/{task_id}/complete')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'completed'

    def test_get_stats(self):
        """Testa obtenção de estatísticas."""
        # Criar tarefas
        create1 = self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa 1'}),
            content_type='application/json'
        )
        task_id_1 = json.loads(create1.data)['id']

        self.client.post(
            '/api/tasks',
            data=json.dumps({'title': 'Tarefa 2'}),
            content_type='application/json'
        )

        # Marcar uma como concluída
        self.client.patch(f'/api/tasks/{task_id_1}/complete')

        response = self.client.get('/api/tasks/stats')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total'] == 2
        assert data['pending'] == 1
        assert data['completed'] == 1
