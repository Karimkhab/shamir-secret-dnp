# Frontend Task

## Ответственный

Руслан

## Цель

Сделать простой UI для двух сценариев:

- split secret
- recover secret

UI должен быть клиентом backend и не должен знать детали алгоритма Shamir.

## Что пользователь вводит

### Split

- `secret: string`
- `threshold: number`
- `totalShares: number`

### Recover

- `shares: string[]`

## Какие запросы отправлять

### `POST /api/v1/secrets/split`

```json
{
  "secret": "text",
  "threshold": 3,
  "totalShares": 5
}
```

### `POST /api/v1/secrets/recover`

```json
{
  "shares": ["share1", "share2", "share3"]
}
```

## Что приходит с backend

### Split response

```json
{
  "shares": ["share1", "share2", "share3", "share4", "share5"],
  "shareCount": 5,
  "requestId": "req-123"
}
```

### Recover response

```json
{
  "secret": "text",
  "requestId": "req-124"
}
```

### Error response

```json
{
  "code": "INVALID_REQUEST",
  "message": "text",
  "requestId": "req-125"
}
```

## Что должен показывать UI

Для `split`:

- форму ввода
- список полученных `shares`
- количество `shares`
- `requestId`

Для `recover`:

- форму ввода списка `shares`
- восстановленный `secret`
- `requestId`

Для ошибки:

- `message`
- `requestId`

## Что входит в задачу

- формы для двух сценариев
- отправка запросов в backend
- отображение success/error state
- базовая клиентская валидация


## Критерий готовности

- UI работает только через backend
- запросы и ответы совпадают с backend-контрактом
- пользователь понимает, что вводить и что получил в ответ

## Полезная практика DNP

- `clear service boundary`: UI не зависит от реализации core
- `contract-driven integration`: UI собирается по фиксированному JSON-контракту
