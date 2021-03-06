## Эмулятор машины Фон-Неймана

Данный класс моделирует виртуальную машину с архитектурой
Фон Неймана. Чтобы получить список команд для управления
машиной, введите `help`. Ниже предоставлен список ассемблерных
команд для написания собственных программ на машине:

* `mov [dest] [src]` - копирует значение из [dest] в [src]  
* `add [dest] [src]` - прибавляет к [dest] значение [src]  
* `inp [dest]` - просит значение на ввод и кладет его в [dest]  
* `out [src]` - выводит значение [src]  
* `[label]:` - устанавливает label, на который можно будет делать jmp
* `jmp [label]` - перенаправляет поток выполнения на label
* `if [arg1] [arg2]` - проверяет arg1 и arg2 на равенство  
**Примечание:** при выходе из `if` делать `jmp` на лейбл, выставленный  
после секции `else` (смотри пример "iftest")
* `stop` - завершение программы  
* `return [var]` - возвращает значение переменной [var]

Все команды принимают на вход имена переменных, перед тем как использовать
переменную необходимо объявить ее следующим образом:

> [var_name] = [value]

Все переменные могут иметь только целочисленное значение. Имя переменной
не должно совпадать с именем существующей команды.

#### Регистры и их назначение

`_mem[0]` - указатель на неиспользованный кусок памяти   
`_mem[3]` - указатель на текущую выполняемую ячейку памяти

#### Примр запуска программы
> read [prog_name]   
> run [prog_name]

Программа может принимать аргументы.  
Уразанные имена переменных можно использовать в коде программы  

> read [prog_name] [arg1] [arg2]  
> run [prog_name] 30 20

В примере выше аргументам `arg1` и `arg2` будут присвоены значения  
30 и  20 соответственно 

Уже написанные программы можно вызывать, как функции в других программах

#### Примеры программ

**1. "test" и "sum"**   
Для запуска выполнить:

> read sum a b  
> read test  
> run test  

**2. "iftest"**

> read iftest  
> run iftest

**3. "fib"**
Просит на ввод число "n" и выводит n-ое число Фибоначчи

> read fib  
> run fib