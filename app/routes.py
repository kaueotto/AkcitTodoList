"""Rotas da API RESTful para gerenciamento de tarefas."""
from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Task

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@task_bp.route('', methods=['GET'])
def get_tasks():
    """
    Obtém lista de tarefas com filtro opcional por status.

    Query Parameters:
        status (str, optional): Filtra por 'pending' ou 'completed'

    Returns:
        JSON: Lista de tarefas
    """
    status_filter = request.args.get('status')

    try:
        if status_filter:
            if status_filter not in ['pending', 'completed']:
                return jsonify({
                    'error': 'Status inválido. Use "pending" ou "completed"'
                }), 400
            tasks = Task.query.filter_by(status=status_filter).all()
        else:
            tasks = Task.query.all()

        return jsonify([task.to_dict() for task in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Obtém uma tarefa específica pelo ID.

    Args:
        task_id (int): ID da tarefa

    Returns:
        JSON: Dados da tarefa
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarefa não encontrada'}), 404

        return jsonify(task.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_bp.route('', methods=['POST'])
def create_task():
    """
    Cria uma nova tarefa.

    JSON Body:
        title (str, required): Título da tarefa
        description (str, optional): Descrição da tarefa

    Returns:
        JSON: Dados da tarefa criada
    """
    try:
        data = request.get_json()

        if not data or 'title' not in data:
            return jsonify({'error': 'Campo "title" é obrigatório'}), 400

        if not data['title'].strip():
            return jsonify({'error': 'O título não pode estar vazio'}), 400

        task = Task(
            title=data['title'],
            description=data.get('description', '')
        )
        db.session.add(task)
        db.session.commit()

        return jsonify(task.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Atualiza uma tarefa existente.

    Args:
        task_id (int): ID da tarefa

    JSON Body:
        title (str, optional): Novo título
        description (str, optional): Nova descrição
        status (str, optional): Novo status ('pending' ou 'completed')

    Returns:
        JSON: Dados da tarefa atualizada
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarefa não encontrada'}), 404

        data = request.get_json()

        if not data:
            return jsonify({'error': 'Nenhum dado para atualizar'}), 400

        if 'title' in data:
            if not data['title'].strip():
                return jsonify({'error': 'O título não pode estar vazio'}), 400
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if data['status'] not in ['pending', 'completed']:
                return jsonify({
                    'error': 'Status inválido. Use "pending" ou "completed"'
                }), 400
            task.status = data['status']

        db.session.commit()

        return jsonify(task.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@task_bp.route('/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """
    Marca uma tarefa como concluída.

    Args:
        task_id (int): ID da tarefa

    Returns:
        JSON: Dados da tarefa atualizada
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarefa não encontrada'}), 404

        task.status = 'completed'
        db.session.commit()

        return jsonify(task.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Deleta uma tarefa.

    Args:
        task_id (int): ID da tarefa

    Returns:
        JSON: Mensagem de sucesso
    """
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Tarefa não encontrada'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Tarefa deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@task_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Retorna estatísticas sobre as tarefas.

    Returns:
        JSON: Estatísticas (total, pendentes, concluídas)
    """
    try:
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        completed = Task.query.filter_by(status='completed').count()

        return jsonify({
            'total': total,
            'pending': pending,
            'completed': completed
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
