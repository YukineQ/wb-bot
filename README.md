* ## Installation

  First, make sure you have installed git and Python version between 3.7.x to 3.11.x
  
  Open command prompt and type
  ```
  git clone https://github.com/YukineQ/wb-bot.git
  ```
  ```
  cd wb-bot
  ```
  ```
  python -m pip install --upgrade pip wheel
  ```
  ```
  pip install -r requirements.txt
  ```

* ## Setup

  ```
  create file .env into root folder
  ```
  ```
  copy the contents from .env.example to .env
  ```
  ```
  create new telegram bot from https://t.me/BotFather
  ```
  ```
  insert yout bot token into .env, like so BOT_TOKEN="your token"
  ```
  ```
  create excel file with SKU's 
  ```
  SKU Example
  | SKU  |
  | ------------- |
  | 13213121242  |
  | 21321321321  |
  ```
  add path to excel file in .env EXCEL_FILE_PATH="C:\\sku.xlt"
  ```
  ```
  download and run redis database
  ```

* ## Run

  Open command prompt in wb-bot folder and run
  
  ```
  python main.py
  ```
  ```
  add bot to any group in telegram and type @name_of_bot /start
  ```
