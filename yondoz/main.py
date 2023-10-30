from flask import Flask, render_template, request
import os
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_project', methods=['POST'])
def create_project():
    token = request.form.get('token')
    folder_name = request.form.get('folder_name')
    creator_id = request.form.get('creator_id')

    if not token or not folder_name:
        return "Invalid input. Please enter both token and folder name."
    
    os.mkdir(folder_name)
    os.chdir(folder_name)
    
    # Create project structure
    os.mkdir('handlers')
    os.mkdir('utils')
    os.mkdir('keyboards')
    os.mkdir('data')

    # Create app.py
    with open('app.py', 'w') as f:
        f.write("from aiogram import executor\n\n\nif __name__ == '__main__':\n    executor.start_polling()")

    # Create main.py
    with open('main.py', 'w') as f:
        f.write("from aiogram import Bot, Dispatcher, types\nfrom aiogram.contrib.fsm_storage.memory import MemoryStorage\n\n\nAPI_TOKEN = ''\n\nbot = Bot(token=API_TOKEN)\ndp = Dispatcher(bot, storage=MemoryStorage())")

    # Create handlers/start.py
    with open('handlers/start.py', 'w') as f:
        f.write("from aiogram import types\nfrom main import dp\n\n\n@dp.message_handler(commands=['start'])\nasync def start(message: types.Message):\n    await message.reply('Hello!')")

    # Create handlers/help.py
    with open('handlers/help.py', 'w') as f:
        f.write("from aiogram import types\nfrom main import dp\n\n\n@dp.message_handler(commands=['help'])\nasync def help(message: types.Message):\n    await message.reply('Need help?')")

    # Create utils/config.py
    with open('utils/config.py', 'w') as f:
        f.write(f"TOKEN = '{token}'\nCREATOR_ID = '{creator_id}'" if creator_id else f"TOKEN = '{token}'")

    # Create utils/logger.py
    with open('utils/logger.py', 'w') as f:
        f.write("import logging\n\n\nlogging.basicConfig(level=logging.INFO)")
        
    return "Project created successfully."

if __name__ == '__main__':
    app.run(debug=True)
