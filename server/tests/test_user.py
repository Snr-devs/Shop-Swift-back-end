import pytest
from werkzeug.security import check_password_hash
from .models import User

def test_user_creation_and_password_hashing():
   
    user = User(
        username="testuser",
        email="test@example.com",
        password="mypassword"
    )
    
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.phone_number is None 
    
    
    assert user.password_hash != "mypassword"  
    assert check_password_hash(user.password_hash, "mypassword")  
    
    
    assert str(user) == "<User testuser>"