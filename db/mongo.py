import motor.motor_asyncio # type: ignore

mongo_uri = 'mongodb+srv://lem:m0ng0@cluster0.9ot2a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
todo_db = mongo_client.todo_db
todo_collection = todo_db.get_collection('todos')