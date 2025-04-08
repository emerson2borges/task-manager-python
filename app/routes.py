from flask import Flask, request, jsonify
from app.models import Task
from app.database import SessionLocal

app = Flask(__name__)

@app.route("/", methods=["GET"])
def test():
    return "API está funcionando!"


from flask import Flask, jsonify
from app.database import SessionLocal
from app.models import Task

app = Flask(__name__)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        session = SessionLocal()
        tasks = session.query(Task).all()
        session.close()

        # Transformar os objetos Task em JSON
        return jsonify([
            {"id": task.id, "title": task.title, "description": task.description, "done": task.done}
            for task in tasks
        ])
    except Exception as e:
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            session.close()
            return jsonify({"error": "Tarefa não encontrada"}), 404

        session.close()
        return jsonify({"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "done": task.done
        }}), 200
    except Exception as e:
        session.close()
        return jsonify({"error": "Erro ao buscar tarefa", "details": str(e)}), 500

@app.route("/tasks", methods=["POST"])
def add_task():
    session = SessionLocal()
    data = request.get_json()  # Dados enviados pelo front-end
    new_task = Task(
        title=data.get("title"),
        description=data.get("description"),
        done=data.get("done", False)  # Padrão: False
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    session.close()
    return jsonify({"message": "Tarefa adicionada com sucesso!", "task": {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "done": new_task.done
    }}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    session = SessionLocal()
    try:
        data = request.get_json()  # Dados enviados pelo front-end
        task = session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            session.close()
            return jsonify({"error": "Tarefa não encontrada"}), 404

        # Atualiza os dados da tarefa
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.done = data.get("done", task.done)

        session.commit()
        session.refresh(task)  # Atualiza o objeto atualizado na sessão
        
        return jsonify({"message": "Tarefa atualizada com sucesso!", "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "done": task.done
        }}), 200
    except Exception as e:
        session.rollback()  # Reverte alterações em caso de erro
        return jsonify({"error": "Erro ao atualizar tarefa", "details": str(e)}), 500
    finally:
        session.close()

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            session.close()
            return jsonify({"error": "Tarefa não encontrada"}), 404

        # Remove a tarefa do banco de dados
        session.delete(task)
        session.commit()
        session.close()
        
        return jsonify({"message": "Tarefa excluída com sucesso!", "task_id": task_id}), 200
    except Exception as e:
        session.rollback()  # Reverte alterações em caso de erro
        return jsonify({"error": "Erro ao excluir tarefa", "details": str(e)}), 500
    finally:
        session.close()



