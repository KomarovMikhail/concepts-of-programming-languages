## Реализация исключений

Выше представленна реализация исключений в C, с
использованием функций `setjmp` и `longjmp`.

Реализация поддерживает различные типы исключений.  
Пример работы исключений написан в "main.c". Для запуска выполнить:

```bash
$ make
$ ./main
```

Реализация поддерживает очистку стека вплоть до `TRY`,
Рекомендуется для выделения памяти использовать макрос
`SAFE_MALLOC`. Он может бросать исключение OUT_OF_MEMORY,
поэтому для корректной работы рекомендуется обрабатывать это
исключение в блоке `CATCH`

Чтобы инициализировать все необходимые для работы исключений переменные,
переменные, перед началом использования макросов вызовите функцию `init_exceptions`,
а после окончания использования - функцию `free_exceptions`.