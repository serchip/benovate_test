# Решение задачи от benovate.ru

## [Видео решения](https://www.youtube.com/watch?v=mgwTN_quIh0&feature=youtu.be)

## Задание
Напишите код приложения для Django (Python 3), в котором у пользователей есть помимо основных полей 2 дополнительных: ИНН (может повторяться у разных пользователей, пользователей в системе может быть очень много) и счет (в рублях, с точностью до копеек). Также есть форма состоящая из полей:

* Выпадающий список со всеми пользователями в системе, со счета которого нужно перевести деньги
* Текстовое поле для ввода ИНН пользователей, на счета  которых будут переведены деньги
* Текстовое поле для указания какую сумму нужно перевести с одного счета на другие

Необходимо проверять есть ли достаточная сумма у пользователя, со счета которого списываются средства, и есть ли пользователи с указанным ИНН в БД. При валидности введенных данных необходимо указанную сумму списать со счета указанного пользователя и перевести на счета пользователей с указанным ИНН в равных частях (если переводится 60 рублей 10ти пользователям, то каждому попадет 6 рублей на счет). 

Было бы неплохо, если бы форма работала без перезагрузки страницы.

Обязательно наличие unit-тестов.
