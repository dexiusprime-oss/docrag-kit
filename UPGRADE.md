# DocRAG Kit - Обновление до новой версии

## Быстрое обновление

Для обновления существующих проектов DocRAG Kit до последней версии:

### 1. Обновить пакет
```bash
pip install --upgrade docrag-kit
```

### 2. Обновить проект
```bash
docrag update
```

### 3. Перезапустить MCP сервер
В Kiro IDE:
- Откройте Command Palette (Cmd/Ctrl + Shift + P)
- Найдите "MCP: Reload Servers"
- Или полностью перезапустите Kiro IDE

## Что нового

После обновления вы получите:

### Новый MCP инструмент `reindex_docs`
- **Автоматическое обнаружение изменений** в документах
- **Умная переиндексация** только при необходимости
- **Режим проверки** без выполнения действий

```python
# Проверить, нужна ли переиндексация
reindex_docs(check_only=True)

# Выполнить умную переиндексация
reindex_docs()

# Принудительная полная переиндексация
reindex_docs(force=True)
```

### Новая команда `docrag fix-database`
Решает проблемы с базой данных:
- "Readonly database" ошибки
- Проблемы с правами доступа
- Заблокированные файлы базы данных
- Поврежденная база данных

```bash
# Автоматическое исправление проблем с БД
docrag fix-database
```

### Улучшенные существующие инструменты
- `search_docs` и `answer_question` теперь предупреждают об устаревших данных
- Автоматические рекомендации по переиндексации
- Лучшая производительность для больших проектов

## Решение проблем

### Если обновление не работает

1. **Принудительная переустановка:**
```bash
pip uninstall docrag-kit -y
pip install docrag-kit
```

2. **Обновление MCP конфигурации:**
```bash
docrag mcp-config --update --non-interactive
```

3. **Полный перезапуск Kiro IDE**

### Если появились ошибки базы данных

```bash
# Диагностика и исправление
docrag fix-database

# Или полная переиндексация
docrag reindex
```

### Если не видно новых инструментов

1. Убедитесь, что пакет обновлен: `pip show docrag-kit`
2. Перезапустите MCP серверы в Kiro
3. Проверьте MCP конфигурацию: `docrag mcp-config`

## Проверка обновления

После обновления проверьте:

```bash
# Версия пакета
docrag --version

# Состояние системы
docrag doctor

# Список доступных команд
docrag --help
```

В Kiro IDE должно быть доступно 4 MCP инструмента:
- `search_docs`
- `answer_question`
- `list_indexed_docs`
- `reindex_docs` ← **новый**

## Откат (если нужен)

Если возникли проблемы, можно откатиться:

```bash
# Установить предыдущую версию
pip install docrag-kit==0.1.4

# Восстановить MCP конфигурацию
docrag mcp-config --non-interactive
```

## Получить помощь

- **Диагностика:** `docrag doctor`
- **Проблемы с БД:** `docrag fix-database`
- **Документация:** [docs/UPGRADE_GUIDE.md](docs/UPGRADE_GUIDE.md)
- **Issues:** https://github.com/docrag-kit/docrag-kit/issues