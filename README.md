# duodian-garden

```
生成虚拟环境依赖包requirements.txt,用于项目发布。这样即使新的环境没有安装pipenv也可以直接安装依赖包。
方法1：pipenv run pip freeze > requirements.txt
方法2：pipenv lock -r --dev > requirements.txt

虚拟环境中导入requirements.txt
pipenv install -r requirements.txt
```