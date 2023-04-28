from datetime import datetime
from sqlite3 import IntegrityError
from flask import jsonify, redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from pydantic import ValidationError
from model import Session, Tarefa, Categoria
from schema.tarefa import TarefaPtrSchema, TarefaSchema, TarefaListSchema, TarefaViewSchema
from schema.categoria import CategoriaListSchema
from schema.erro import ErroSchema
from logger import logger

info = Info(title="API - Gerenciamento de Tarefas - MVP", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tarefa_tag = Tag(name="Tarefa", description="Adição, visualização e remoção de tarefas")
categoria_tag = Tag(name="Categoria", description="Visualização de categorias")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/tarefa', tags=[tarefa_tag], responses={"200": TarefaViewSchema, "400": ErroSchema})
def adicionar_tarefa(form: TarefaSchema):
    """Adiciona uma nova tarefa
    Retorna uma representação da tarefa.
    """    
    session = Session()
    try:
        tarefa = Tarefa(
            titulo=form.titulo,
            detalhes=form.detalhes,
            data_limite=datetime.strptime(form.data_limite, "%d/%m/%Y").date(),
            categoria_id=form.categoria_id
        )
        session.add(tarefa)
        session.commit()
        logger.debug(f"Adicionando tarefa de titulo: '{tarefa.titulo}'")
        return jsonify([{
            'id': tarefa.id,            
            'titulo': tarefa.titulo,
            'detalhes': tarefa.detalhes,
            'data_limite': tarefa.data_limite.strftime('%d/%m/%Y'),
            'categoria': {
                'id': tarefa.categoria.id,
                'nome': tarefa.categoria.nome
            } 
        }]), 200 
    except ValidationError as e:
        session.rollback()    
        logger.warning(f"Requisição inválida '{tarefa.titulo}'\n {str(e)}")
        return {"erro": "requisição inválida"}, 400
    except ValueError as e:
        session.rollback()
        logger.warning(f"Requisição inválida '{tarefa.titulo}'\n {str(e)}")
        return {"erro": "requisição inválida"}, 400    
    except IntegrityError as e:
        session.rollback()
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.titulo}'\n {str(e)}")
        return {"erro": "erro ao adicionar tarefa"}, 400    
    except Exception as e:
        session.rollback()
        logger.warning(f"Erro requisição inválida '{tarefa.titulo}'\n {str(e)}")
        return {"erro": "erro ao adicionar tarefa"}, 400


@app.get('/tarefa',tags=[tarefa_tag], responses={"200": TarefaListSchema, "400": ErroSchema})
def listar_tarefa(query: TarefaPtrSchema):
    """Faz a busca por todas as tarefas ou filtra dependendo dos parametros passados
    Retorna uma representação da listagem de tarefas.
    """      
    session = Session()
    try:
        #filtro condicional por titulo, id da tarefa e por id da categoria
        filtros = []
        if query.titulo:
            filtros.append(Tarefa.titulo.ilike(f'%{query.titulo}%'))
        elif query.id:
            filtros.append(Tarefa.id==query.id)    
        elif query.categoria_id:
            filtros.append(Tarefa.categoria_id==query.categoria_id)    

        #busca as tarefas no BD utilizando os filtros, se informados    
        tarefas = session.query(Tarefa).filter(*filtros).all()            

        return jsonify([{
            'id': tarefa.id,            
            'titulo': tarefa.titulo,
            'detalhes': tarefa.detalhes,
            'data_limite': tarefa.data_limite.strftime('%d/%m/%Y'),
            'categoria': {
                'id': tarefa.categoria.id,
                'nome': tarefa.categoria.nome
            }
        } for tarefa in tarefas]), 200        
    except Exception as e:
        logger.warning(f"Erro  ao buscar tarefas\n {str(e)}")
        return {"erro": "erro ao buscar tarefas"}, 400
    
@app.get('/categoria', tags=[categoria_tag], responses={"200": CategoriaListSchema, "400": ErroSchema})
def listar_categorias():
    """Faz a busca por todas as categorias cadastradas
    Retorna uma representação da listagem de categorias.
    """      
    session = Session()
    try:
        return jsonify([
            {
                'id': categoria.id,
                'nome': categoria.nome,
            } for categoria in session.query(Categoria).all()
        ]), 200        
    except Exception as e:
        logger.warning(f"Erro  ao buscar categorias\n {str(e)}")
        return {"erro": "erro ao buscar categorias"}, 400    


@app.delete('/tarefa', tags=[tarefa_tag], responses={"200": TarefaViewSchema, "400": ErroSchema})
def deletar_tarefa(query: TarefaPtrSchema):
    """Deleta uma Tarefa a partir do id da tarefa
    Retorna uma representação da Tarefa deletada.
    """     
    session = Session()
    try:
        tarefa = session.query(Tarefa).get(query.id)
        if tarefa:
            json = jsonify([
                {
                    'id': tarefa.id,
                    'titulo': tarefa.titulo,
                    'detalhes': tarefa.detalhes,
                    'data_limite': tarefa.data_limite.strftime('%d/%m/%Y'),
                    'categoria': {
                        'id': tarefa.categoria.id,
                        'nome': tarefa.categoria.nome
                    } 
                }]), 200             
            session.query(Tarefa).filter(Tarefa.id == query.id).delete()
            session.commit()
            return json
        else:
            return {"erro":"tarefa não encontrada"}, 400
    except Exception as e:
        session.rollback()
        logger.warning(f"Erro ao buscar tarefa\n {str(e)}")
        return {"erro": "erro ao buscar tarefa"}, 400