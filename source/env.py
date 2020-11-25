import os

def init_env():
    os.environ['DB_HOST'] = "database-newsagg.cetpuuxvmlii.ap-southeast-1.rds.amazonaws.com"
    os.environ['DB_USER'] = "nakarinh14"
    os.environ['DB_PASSWORD'] = "Nakarinh198799"
    os.environ['DB_PORT'] = "5432"
    os.environ['DB_DATABASE'] = "postgres"