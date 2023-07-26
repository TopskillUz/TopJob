# Topskill project API v1 version

## Разработка с Docker

#### 1) Клонировать репозиторий

```
git clone https://github.com/SirojiddinYakubov/TopJob.git
```

#### 2) В корне проекта создать deploy/.env.prod (Готовый шаблон: deploy/.env.example)

#### 3) Создать образ

```
make docker-build
```

#### 4) Запустить контейнер

```
make docker-up
```

### 5) Перейти по адресу

```
http://0.0.0.0:8000/api/v1/admin/docs
http://0.0.0.0:8000/api/v1/site/docs
```