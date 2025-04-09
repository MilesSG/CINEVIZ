import json
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'users.json')

class User:
    def __init__(self, username, password, email, role='user', user_id=None, favorites=None, created_at=None):
        self.id = user_id or str(uuid.uuid4())
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email
        self.role = role
        self.favorites = favorites or []
        self.created_at = created_at or datetime.now().isoformat()
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email,
            'role': self.role,
            'favorites': self.favorites,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        user = cls(
            username=data['username'],
            password='',  # 不直接设置密码，因为从字典创建时已有密码哈希
            email=data['email'],
            role=data['role'],
            user_id=data['id'],
            favorites=data['favorites'],
            created_at=data['created_at']
        )
        user.password_hash = data['password_hash']
        return user
    
    @classmethod
    def get_all_users(cls):
        if not os.path.exists(USERS_FILE):
            # 确保目录存在
            os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
            with open(USERS_FILE, 'w') as f:
                json.dump([], f)
            return []
        
        with open(USERS_FILE, 'r') as f:
            users_data = json.load(f)
        
        return [cls.from_dict(user_data) for user_data in users_data]
    
    @classmethod
    def get_by_id(cls, user_id):
        users = cls.get_all_users()
        for user in users:
            if user.id == user_id:
                return user
        return None
    
    @classmethod
    def get_by_username(cls, username):
        users = cls.get_all_users()
        for user in users:
            if user.username == username:
                return user
        return None
    
    @classmethod
    def get_by_email(cls, email):
        users = cls.get_all_users()
        for user in users:
            if user.email == email:
                return user
        return None
    
    def save(self):
        users = self.get_all_users()
        
        # 检查是否已存在该用户，如果存在则更新
        for i, user in enumerate(users):
            if user.id == self.id:
                users[i] = self
                break
        else:
            # 不存在则添加
            users.append(self)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        
        # 保存到文件
        with open(USERS_FILE, 'w') as f:
            json.dump([user.to_dict() for user in users], f, indent=4)
        
        return self
    
    @classmethod
    def delete(cls, user_id):
        users = cls.get_all_users()
        users = [user for user in users if user.id != user_id]
        
        with open(USERS_FILE, 'w') as f:
            json.dump([user.to_dict() for user in users], f, indent=4)
        
        return True 