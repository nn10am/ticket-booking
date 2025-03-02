from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

plain_password = "12345678"
hashed_password = bcrypt_context.hash(plain_password)

print(hashed_password)