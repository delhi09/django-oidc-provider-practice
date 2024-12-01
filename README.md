# Django5のテンプレートPJ

## 起動
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
ブラウザで http://127.0.0.1:8000/sample/ にアクセス

## 仮想環境解除
```sh
deactivate
```


## format
```sh
ruff check . --fix && ruff format .
```
