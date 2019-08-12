# はろー、じゃんご

## 「ベストプラクティス」について

正直、変にこねくり回すよりも「[cookiecutter-django](https://qiita.com/ping2shi2/items/e3366bf9600bddeede07)」を使うのが一番だと思う（今回は使っていない）。

settings.pyも、標準では環境ごとに分かれていないので（分ければいいだけだけど）めんどくさい。

今回は素の状態で進めている。

ただし、cookiecutter-djangoではパッケージ管理に素の`pip`を使っているが、ここでは`pipenv`使っている。

## Dockerfileについて

環境変数設定の意図は以下の通り

```
ENV PYTHONDONTWRITEBYTECODE 1 # [Python]コンパイルキャッシュ（*.pycファイル）を作成しない：邪魔
ENV PYTHONUNBUFFERED 1        # [Python]stdoutへのprintにバッファを使わない：ログ出力が早くなる
ENV PIPENV_VENV_IN_PROJECT 1  # [Pipenv]プロジェクトの直下に仮想環境を作る：Pipfile更新のたびにイメージの再ビルドをしなくて済む
```

## コマンドリファレンス

### clone直後には以下を行う

```sh
# migrate前にDBを作成しておく必要がある
# migrate後にテストデータを入れておく
docker-compose build
docker-compose run app pipenv install
docker-compose run app psql -U postgres -h db -c "create database mydatabase;"
docker-compose run app pipenv run python manage.py migrate
docker-compose run app pipenv run python manage.py loaddata polls/fixtures/test_data.json
docker-compose up
```

### appにアクセスするとき

```sh
# 他のサーバと競合しそうにない7000番を指定している
# /は未実装、/pollsはpollsアプリ、/adminはDjango標準の管理画面
open http://localhost:7000/polls
```

### 管理画面にアクセスするとき

```sh
# まず管理者ユーザを作成する必要がある（パスワードは必須）
docker-compose exec app pipenv run python manage.py createsuperuser
open http://localhost:7000/admin
```

### テストするとき

```sh
# テストを実行する
docker-compose exec app pipenv run test
```

### サーバに接続するとき

```sh
# app（pythonなので、抜ける時はexit()関数）
docker-compose exec app pipenv run python manage.py shell

# db（psqlなので、抜ける時は\qコマンド）
docker-compose exec app pipenv run python manage.py dbshell
```

### マイグレーション関連

```sh
# 「0001_initial」実行時に流れるSQLを確認する
docker-compose exec app pipenv run python manage.py sqlmigrate polls 0001_initial

# マイグレーションをすべて実行する
docker-compose exec app pipenv run python manage.py migrate

# マイグレーション履歴を確認する
docker-compose exec app pipenv run python manage.py showmigrations

# 「0001_initial」へロールバックする
docker-compose exec app pipenv run python manage.py migrate polls 0001_initial

# すべてのマイグレーションを取り消す
docker-compose exec app pipenv run python manage.py migrate polls zero
```

### パッケージ関連

```sh
# 新しいパッケージ（例：psycopg2-binary）をインストールしてPipfile.lockを更新する
docker-compose run app pipenv install psycopg2-binary
```

### データ操作

```sh
# データをエクスポートする
docker-compose exec app pipenv run python manage.py dumpdata polls -o fixture.json

# データをインポートする
docker-compose exec app pipenv run python manage.py loaddata fixture.json
```

### プロジェクト操作

```sh
# 新しいアプリを作成する
docker-compose run app pipenv run python manage.py startapp my_great_app
```
