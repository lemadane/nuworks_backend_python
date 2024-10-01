
from fastapi import APIRouter, HTTPException # type: ignore
from db.mongo import todo_collection
from models.todo_model import TodoCreate, TodoUpdate
from datetime import datetime 
from bson import ObjectId # type: ignore
from fastapi import Response # type: ignore

todo_routes = APIRouter()

def todo_helper(todo: dict) -> dict:
   return {
      'id': str(todo['_id']).upper(),
      'description': todo['description'],
      'completed': todo['completed'],
      'created_at': todo['created_at'],
   } 


def timestamp():
   return datetime.now().isoformat()


@todo_routes.post('/todos')
async def create_todo(todo: TodoCreate, res: Response):
   try:
      todo.created_at = timestamp()
      todo.completed = False
      print(f'todo: {todo}')
      todo_dict = todo.model_dump(exclude_unset=True)
      print(f'todo_dict: {todo_dict}')
      result = await todo_collection.insert_one(todo_dict)
      print(f'result: {result}')
      print(f'result.inserted_id: {result.inserted_id}')
      if result.inserted_id:
         res.status_code = 201
         return      
   except Exception as error:
      print(f'error: {str(error)}')
      raise HTTPException(
         status_code=422, 
         detail='Something wrong happened')
      
      
@todo_routes.get('/todos')
async def getall_todos(offset: int = 0, limit: int = 100):
   try:
      todos = []
      async for todo in todo_collection.find().skip(offset).limit(limit):
         todos.append(todo_helper(todo)
      )
      return {
         'todos': todos,
         'count': len(todos),
         'offset': offset, 
         'limit': limit,
      }
   except Exception as error:
      print(f'error: {str(error)}')
      raise HTTPException(
         status_code=422,
         detail=f'Something wrong happened')
      
      
@todo_routes.get('/todos/{todo_id}')
async def get_todo(todo_id: str):
   try:
      todo = await todo_collection.find_one({
         '_id': ObjectId(todo_id)
      })
      if not todo:
         raise HTTPException(
            status_code=404,
            detail='Todo not found')
      return todo_helper(todo)
   except Exception as error:
      print(f'error: {str(error)}')   
      raise HTTPException(
         status_code=422,
         detail=f'Something wrong happened')


@todo_routes.put('/todos/{todo_id}')
async def update_todo(todo_id: str, todo: TodoUpdate, res: Response):
   try:
      print(f'todo_id: {todo_id}')
      print(f'todo: {todo}')
      todo_dict = todo.model_dump(exclude_unset=True)   
      print(f'todo_dict: {todo_dict}')
      has_updates =  len(todo_dict) >= 1
      print(f'has_updates: {has_updates}')
      if not has_updates:
         raise HTTPException(
         status_code=400, 
         detail='Nothing to update'
      )
      update_result = await todo_collection.update_one(
         { '_id': ObjectId(todo_id) },
         { '$set': todo_dict }
      )
      print(f'update_result: {update_result}')
      update_success = update_result.modified_count == 1
      print(f'update_success: {update_success}')
      if not update_success:
         raise HTTPException(
            status_code=404, 
            detail='Todo not found'
         )
      res.status_code = 204
      return
   except Exception as error:
      print(f'error: {str(error)}')
      raise HTTPException(
         status_code=422,
         detail=f'Something wrong happened')
   

@todo_routes.delete('/todos/{todo_id}')
async def delete_todo(todo_id: str, res: Response):
   try:
      delete_result = await todo_collection.delete_one(
         { '_id': ObjectId(todo_id) }
      )
      print(f'delete_result: {delete_result}')  
      delete_success = delete_result.deleted_count == 1
      print(f'delete_success: {delete_success}')
      if not delete_success:
         raise HTTPException(
            status_code=404,
            detail='Todo not found'
      )
      res.status_code = 204
      return
   except Exception as error:
      print(f'error: {str(error)}')
      raise HTTPException(
         status_code=422,
         detail=f'Something wrong happened')


@todo_routes.post('/todos/delete')
async def delete_todos(todo:TodoUpdate, res: Response):
   try:
      print(f'todo: {todo}')
      todo_dict = todo.model_dump(exclude_unset=True)   
      print(f'todo_dict: {todo_dict}')
      has_deletes =  len(todo_dict) >= 1
      print(f'has_deletes: {has_deletes}')
      if not has_deletes:
         raise HTTPException(
         status_code=400, 
         detail='Nothing to delete'
      )
      delete_result = await todo_collection.delete_many(
         todo_dict
      )
      print(f'delete_result: {delete_result}')
      delete_success = delete_result.deleted_count > 0
      print(f'has_deletes: {has_deletes}')
      if not delete_success:
         raise HTTPException(
            status_code=404,
            detail='Todo not found'
         )     
      res.status_code = 204
      return { 'deleted': delete_result.deleted_count }
   except Exception as error:
      print(f'error: {str(error)}')
      raise HTTPException(
         status_code=422,
         detail=f'Something wrong happened')