import os
import sys

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User

def create_admin_user():
    # 检查是否已存在管理员用户
    admin = User.get_by_username('admin')
    
    if not admin:
        # 创建新管理员
        admin = User(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='admin'
        )
        admin.save()
        print("管理员用户创建成功! 用户名: admin, 密码: admin123")
    else:
        print("管理员用户已存在!")

if __name__ == "__main__":
    create_admin_user() 