# Dock Backup v1.0

A small macOS utility for backing up and restoring the Dock configuration.

Небольшая утилита для macOS для создания резервных копий и восстановления настроек Dock.

---

## Features / Возможности

- 💾 Create Dock backups / Создание резервных копий Dock
- ♻️ Restore any saved backup / Восстановление любой сохранённой копии
- 🛡️ Automatic safety backup before every restore / Автоматическая страховочная копия перед восстановлением
- 📦 View available backups / Просмотр доступных копий
- ❓ Built-in help / Встроенная справка
- 🎨 Colored Terminal interface / Цветной интерфейс Terminal

---

## Backup Location / Где хранятся резервные копии

Backups are stored in the `backups` folder next to the application.

Резервные копии сохраняются в папке `backups`, расположенной рядом с программой:

```text
Dock Backup/
├── dock-backup.py
├── README.md
└── backups/
```

### Regular backups / Обычные копии

```text
dock-backup_YYYY-MM-DD_HH-MM-SS.plist
```

### Safety backups / Страховочные копии

```text
dock-before-restore_YYYY-MM-DD_HH-MM-SS.plist
```

---

## Usage / Использование

### Run from Terminal / Запуск из Terminal

```bash
python3 ~/Desktop/"Dock Backup"/dock-backup.py
```

### Using an alias / Использование alias

If the `dock` alias is configured:

Если настроен alias `dock`:

```bash
dock
```

---

## Menu / Меню

```text
0. ❓ Help
1. 💾 Create Backup
2. ♻️ Restore Backup
3. 📦 List Backups
4. ❌ Exit
```

---

## Restore / Восстановление

Option **2** lets you choose between regular and safety backups.

Пункт **2** позволяет выбрать обычную или страховочную резервную копию.

### Regular Backups / Обычные копии

Created manually using **Create Backup**.

Создаются вручную через пункт **Create Backup**.

### Safety Backups / Страховочные копии

Created automatically before every restore.

Автоматически создаются перед каждым восстановлением.

This allows you to return to the Dock configuration that existed immediately before the restore.

Это позволяет вернуть состояние Dock, которое было непосредственно перед восстановлением.

---

## Requirements / Требования

- macOS 12
- Python 3

Tested on / Протестировано на:

- macOS 12.7.6

Compatibility with other macOS versions has not been tested.

Совместимость с другими версиями macOS не проверялась.

---

## Version / Версия

`v1.0`
