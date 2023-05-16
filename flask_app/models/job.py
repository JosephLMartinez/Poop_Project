from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Job:
    schema="poop_project"
    def __init__( self , data ):
        self.id = data['id']
        self.dog_name = data['dog_name']
        self.pickup_date = data['pickup_date']
        self.instructions= data['instructions']
        self.puppy_parent_id=['puppy_parent_id']
        self.picker_upper_id=data['picker_upper_id']
        self.finished=data['finished']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # CREATE
    @classmethod
    def save(cls,data):
        query= "INSERT INTO jobs (puppy_parent_id, dog_name, instructions, pickup_date, picker_upper_id, finished, created_at, updated_at) VALUES (%(puppy_parent_id)s, %(dog_name)s,  %(instructions)s, %(pickup_date)s, %(picker_upper_id)s, %(finished)s, NOW(), NOW() );"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results

    # validate dog doodoo
    @staticmethod
    def validate_job_posting(job_posting):
        is_valid=True
        if len(job_posting['dog_name']) < 1:
            flash('First name cannot be blank.')
            is_valid=False
        elif len(job_posting['dog_name']) < 2:
            flash("The Dog's name must be atleast 2 characters long.")
            is_valid=False
        if not job_posting['pickup_date']:
            flash('Invalid pickup date')
            is_valid=False
        if len(job_posting['instructions']) < 5:
            flash('Instructions cannot be blank.')
            is_valid=False
        return is_valid

    # READ one
    @classmethod
    def get_one(cls, id):
        query= "SELECT * FROM jobs WHERE puppy_parent_id= %(id)s;"
        # query= "SELECT id, puppy_parent_id, picker_upper_id, dog_name, instructions, DATE_FORMAT(pickup_date, '%M %d %Y') FROM jobs WHERE puppy_parent_id= %(id)s;"
        results= connectToMySQL(cls.schema).query_db(query, {"id":id})
        print(results)
        if not results:
            return False
        return cls(results[0])
    


    # UPDATE
    @classmethod
    def update(cls, data):
        print(data)
        query="UPDATE jobs SET dog_name= %(dog_name)s, instructions= %(instructions)s, pickup_date=%(pickup_date)s, updated_at=NOW() WHERE puppy_parent_id=%(puppy_parent_id)s;"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results
    
    # DELETE
    @classmethod
    def delete(cls,id):
        print (id)
        query= "DELETE FROM jobs WHERE puppy_parent_id= %(id)s;"
        results= connectToMySQL(cls.schema).query_db(query, {"id":id})
        return results
    
    # READ All
    @classmethod
    def get_all(cls):
        query = "SELECT id,dog_name, picker_upper_id, puppy_parent_id, instructions, DATE_FORMAT(pickup_date, '%M %d %Y') FROM jobs;"
        results = connectToMySQL(cls.schema).query_db(query)
        data=[]
        for row  in results:
            this={
                "id": row["id"],
                "picker_upper_id": row["picker_upper_id"],
                "dog_name": row["dog_name"],
                "instructions": row["instructions"],
                "pickup_date": row["DATE_FORMAT(pickup_date, '%M %d %Y')"],
                "puppy_parent_id": row["puppy_parent_id"]
            }
            if not this['picker_upper_id']:
                data.append(this)
            print(data)
        return data
    
    # UPDATE to claim
    @classmethod
    def claim(cls, data):
        query="UPDATE jobs SET picker_upper_id= %(picker_upper_id)s, updated_at=NOW() WHERE id=%(id)s;"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results
    
    # UPDATE to unclaim
    @classmethod
    def unselect(cls, data):
        query="UPDATE jobs SET picker_upper_id=%(picker_upper_id)s, updated_at=NOW() WHERE id=%(id)s;"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results
    
    # UPDATE to finished
    @classmethod
    def finished_assignment(cls,data):
        query="UPDATE jobs SET finished= %(finished)s, updated_at=NOW() WHERE id=%(id)s;"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results
    
    # READ All of MINE
    @classmethod
    def get_all_of_mine(cls,id):
        query = "SELECT id,dog_name,picker_upper_id, puppy_parent_id, instructions, DATE_FORMAT(pickup_date, '%M %d %Y'),finished FROM jobs;"
        results = connectToMySQL(cls.schema).query_db(query)
        data=[]
        for row  in results:
            this={
                "id": row["id"],
                "picker_upper_id": row["picker_upper_id"],
                "dog_name": row["dog_name"],
                "instructions": row["instructions"],
                "pickup_date": row["DATE_FORMAT(pickup_date, '%M %d %Y')"],
                "puppy_parent_id": row["puppy_parent_id"],
                "finished":row['finished']
            }
            if this['picker_upper_id']==id:
                data.append(this)
                print(data)
        return data