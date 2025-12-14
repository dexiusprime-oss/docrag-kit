# Обновление DocRAG Kit

## Быстрое обновление (3 команды)

```bash
# 1. Обновить пакет
pip install --upgrade docrag-kit

# 2. Обновить проект  
docrag update

# 3. Перезапустить MCP сервер в Kiro IDE
# Command Palette → "MCP: Reload Servers"
```

## Что получите после обновления

### Новый MCP инструмент `reindex_docs`
- Автоматически проверяет, какие документы изменились
- Переиндексирует только при необходимости
- Экономит время и ресурсы

### Новая команда `docrag fix-database`
- Исправляет ошибки "readonly database"
- Решает проблемы с правами доступа
- Восстанавливает поврежденную базу данных

### Улучшенные существующие инструменты
- Предупреждения об устаревших данных
- Лучшая производительность
- Более точные результаты поиска

## Если что-то не работает

```bash
# Диагностика проблем
docrag doctor

# Диагностика проблем CLI vs MCP синхронизации
docrag debug-mcp

# Исправление проблем с базой данных
docrag fix-database

# Полная переустановка (крайний случай)
pip uninstall docrag-kit -y && pip install docrag-kit
docrag mcp-config --non-interactive
```

### Если MCP видит не все документы

Это критическая проблема - CLI и MCP работают с разными данными:

```bash
# 1. Диагностика проблемы
docrag debug-mcp

# 2. Исправление MCP конфигурации
docrag mcp-config --update --non-interactive

# 3. Полный перезапуск Kiro IDE
```

## Проверка успешного обновления

В Kiro IDE должно быть **4 инструмента** вместо 3:
- search_docs
- answer_question  
- list_indexed_docs
- reindex_docs ← **новый**

---

**Подробная документация:** [docs/UPGRADE_GUIDE.md](docs/UPGRADE_GUIDE.md)