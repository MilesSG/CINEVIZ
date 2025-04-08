from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'message': '缺少必要信息'}), 400
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    # 检查用户名是否已存在
    if User.get_by_username(username):
        return jsonify({'message': '用户名已存在'}), 400
    
    # 检查邮箱是否已存在
    if User.get_by_email(email):
        return jsonify({'message': '邮箱已被注册'}), 400
    
    # 创建新用户
    user = User(username=username, password=password, email=email)
    user.save()
    
    return jsonify({
        'message': '注册成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '缺少用户名或密码'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    # 查找用户
    user = User.get_by_username(username)
    
    if not user or not user.check_password(password):
        return jsonify({'message': '用户名或密码错误'}), 401
    
    # 创建JWT令牌
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'favorites': user.favorites,
            'created_at': user.created_at
        }
    }), 200

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    data = request.get_json()
    
    # 可以更新的字段
    if 'email' in data:
        # 检查邮箱是否已被使用
        existing_user = User.get_by_email(data['email'])
        if existing_user and existing_user.id != user.id:
            return jsonify({'message': '邮箱已被其他用户使用'}), 400
        user.email = data['email']
    
    if 'password' in data:
        # 更新密码（会自动哈希）
        user = User(
            username=user.username,
            password=data['password'],
            email=user.email,
            role=user.role,
            user_id=user.id,
            favorites=user.favorites,
            created_at=user.created_at
        )
    
    # 保存更新
    user.save()
    
    return jsonify({
        'message': '个人资料已更新',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@auth_bp.route('/favorites/<movie_id>', methods=['POST'])
@jwt_required()
def add_favorite(movie_id):
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    if movie_id not in user.favorites:
        user.favorites.append(movie_id)
        user.save()
    
    return jsonify({
        'message': '已添加到收藏',
        'favorites': user.favorites
    }), 200

@auth_bp.route('/favorites/<movie_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(movie_id):
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    if movie_id in user.favorites:
        user.favorites.remove(movie_id)
        user.save()
    
    return jsonify({
        'message': '已从收藏中移除',
        'favorites': user.favorites
    }), 200

@auth_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    current_user_id = get_jwt_identity()
    user = User.get_by_id(current_user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    return jsonify({
        'favorites': user.favorites
    }), 200 