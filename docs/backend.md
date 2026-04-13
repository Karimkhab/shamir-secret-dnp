# Backend Task

## Ответственный

Артур

## Цель

Реализовать Spring Boot backend как тонкий orchestration-слой между UI и core.

## Зона ответственности

- принять HTTP-запрос
- провалидировать вход
- вызвать нужный core-метод
- вернуть ответ в фиксированном JSON-формате
- залогировать метаданные запроса

Backend не должен реализовывать сам алгоритм Shamir.

## Endpoint 1

### `POST /api/v1/secrets/split`

Вход:

```json
{
  "secret": "text",
  "threshold": 3,
  "totalShares": 5
}
```

Выход:

```json
{
  "shares": ["share1", "share2", "share3", "share4", "share5"],
  "shareCount": 5,
  "requestId": "req-123"
}
```

## Endpoint 2

### `POST /api/v1/secrets/recover`

Вход:

```json
{
  "shares": ["share1", "share2", "share3"]
}
```

Выход:

```json
{
  "secret": "text",
  "requestId": "req-124"
}
```

## Формат ошибки

```json
{
  "code": "INVALID_REQUEST",
  "message": "text",
  "requestId": "req-125"
}
```

## Вызовы core

```python
split_secret(secret: str, threshold: int, total_shares: int) -> list[str]
recover_secret(shares: list[str]) -> str
```

## Обязательные проверки на границе backend

- `secret` не пустой
- `threshold >= 2`
- `totalShares >= 2`
- `threshold <= totalShares`
- `shares` это не пустой массив

## Что приходит из core

Для `split`:

- `list[str]`

Для `recover`:

- `str`

Backend оборачивает эти значения в HTTP-ответ и сам добавляет:

- `requestId`
- `shareCount`

## Нагрузочные и системные решения

- асинхронность здесь не нужна
- многопоточность специально проектировать не нужно
- брокер не нужен
- сервис остается stateless

Причина простая: здесь короткие синхронные запросы без очередей, стриминга и фоновых задач.

## Что входит в задачу

- controller
- request/response DTO
- validation
- error handling
- integration с encoder и decoder
- безопасное логирование

## Критерий готовности

- оба endpoint работают по зафиксированному контракту
- формат ошибок единый
- в логах нет `secret` и полного списка `shares`

## Полезная практика DNP

- `client-server`
- `stateless service`
- `versioned API` через `/api/v1`
- `validation at boundaries`
