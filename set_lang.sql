-- Перевірка наявності української мови
SELECT * FROM res_lang WHERE code = 'uk_UA';

-- Активація української мови, якщо вона ще не активна
UPDATE res_lang SET active = true WHERE code = 'uk_UA';

-- Встановлення української мови за замовчуванням для поточного користувача
UPDATE res_users SET lang = 'uk_UA' WHERE id = 2;  -- ID 2 зазвичай відповідає адміністратору

-- Очищення кешу перекладів
DELETE FROM ir_translation WHERE module = 'hr_hospital';
