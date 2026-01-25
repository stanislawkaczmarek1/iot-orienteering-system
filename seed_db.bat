cd backend
del db\database.db
python -m src.app.dev_utils.seed_db
pause