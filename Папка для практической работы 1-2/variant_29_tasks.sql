-- 1. Скрипты выполнения варианта задания (Вариант 29)

-- Задание 1: Создать представление по скидкам
-- Это представление агрегирует общую сумму скидок (discount) по категориям продуктов.
-- Логика: Мы присоединяем таблицу фактов sales_fact к product_dim для получения категорий,
-- суммируем discount, группируем по category. Типы данных: discount - numeric(4,2), что подходит для суммирования.
-- Индексы: Рекомендуется индекс на prod_id в sales_fact для ускорения join.
-- Особенности: Представление позволяет быстро запрашивать агрегированные данные без повторных расчетов.
CREATE OR REPLACE VIEW dw.discounts_by_category AS
SELECT 
    p.category AS product_category,
    SUM(f.discount) AS total_discount
FROM 
    dw.sales_fact f
INNER JOIN 
    dw.product_dim p ON f.prod_id = p.prod_id
GROUP BY 
    p.category
ORDER BY 
    total_discount DESC;

-- Задание 2: Определить прибыль по категориям
-- Этот запрос рассчитывает суммарную прибыль (profit) по категориям продуктов.
-- Логика: Присоединяем sales_fact к product_dim, суммируем profit, группируем по category.
-- Типы данных: profit - numeric(21,16), подходит для финансовых расчетов с высокой точностью.
-- Индексы: Индекс на prod_id в sales_fact для join, возможно на category в product_dim для группировки.
-- Особенности: Используем ROUND для удобства чтения, если нужно ограничить decimal places.
SELECT 
    p.category AS product_category,
    SUM(f.profit) AS total_profit
FROM 
    dw.sales_fact f
INNER JOIN 
    dw.product_dim p ON f.prod_id = p.prod_id
GROUP BY 
    p.category
ORDER BY 
    total_profit DESC;

-- Задание 3: Рассчитать количество заказов по клиентам
-- Этот запрос подсчитывает количество уникальных заказов (order_id) для каждого клиента.
-- Логика: Присоединяем sales_fact к customer_dim, считаем DISTINCT order_id, группируем по customer_name.
-- Типы данных: order_id - varchar(25), customer_name - varchar(22).
-- Индексы: Индекс на cust_id в sales_fact и на order_id для ускорения DISTINCT.
-- Особенности: DISTINCT обеспечивает подсчет уникальных заказов, даже если в заказе несколько строк.
SELECT 
    c.customer_name,
    COUNT(DISTINCT f.order_id) AS order_count
FROM 
    dw.sales_fact f
INNER JOIN 
    dw.customer_dim c ON f.cust_id = c.cust_id
GROUP BY 
    c.customer_name
ORDER BY 
    order_count DESC;


-- 2. Моделирование данных (обратный реинжиниринг)

-- STG слой
-- Описание структуры таблиц staging-слоя
-- Таблицы в stg предназначены для загрузки сырых данных без трансформаций.
-- Связи: Нет явных FK, но данные из stg.orders используются для заполнения DW.
-- Особенности первичных данных: Postal_code как varchar для сохранения ведущих нулей.

-- Пример DESCRIBE (в PostgreSQL используем \d или SELECT column_name, data_type FROM information_schema.columns)
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'stg' AND table_name = 'orders';

-- DW слой
-- Описание структуры таблиц витрин данных
-- Связи: sales_fact имеет FK на dimensions (cust_id -> customer_dim, prod_id -> product_dim и т.д.).
-- Описание трансформаций: Данные из stg.orders трансформированы в dimensions (суррогатные ключи) и fact (агрегация метрик).

-- Пример DESCRIBE
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'dw' AND table_name = 'sales_fact';
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'dw' AND table_name = 'customer_dim';
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'dw' AND table_name = 'product_dim';
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'dw' AND table_name = 'geo_dim';

-- Словари (Dimensions)
-- Описание структуры справочников
-- Правила наполнения: INSERT с DISTINCT из stg.orders, суррогатные ключи генерируются с row_number().
-- Обработка медленно меняющихся измерений: Тип 1 (overwrite) для простоты, без history.

SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'dw' AND table_name = 'shipping_dim';
SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'dw' AND table_name = 'calendar_dim';

-- 3. Проверка данных

-- Количество записей
-- Проверка количества записей в источнике и приемнике
SELECT COUNT(*) AS stg_orders_count FROM stg.orders;
SELECT COUNT(*) AS dw_sales_fact_count FROM dw.sales_fact;

-- Проверка распределения данных
SELECT category, COUNT(*) AS product_count
FROM dw.product_dim
GROUP BY category;

-- Целостность данных
-- Проверка отсутствия дубликатов в customer_dim
SELECT customer_id, COUNT(*)
FROM dw.customer_dim
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Проверка ссылочной целостности (пример для customer_dim)
SELECT COUNT(*)
FROM dw.sales_fact f
LEFT JOIN dw.customer_dim c ON f.cust_id = c.cust_id
WHERE c.cust_id IS NULL;

-- Аналогично для других dimensions
SELECT COUNT(*)
FROM dw.sales_fact f
LEFT JOIN dw.product_dim p ON f.prod_id = p.prod_id
WHERE p.prod_id IS NULL;

SELECT COUNT(*)
FROM dw.sales_fact f
LEFT JOIN dw.shipping_dim s ON f.ship_id = s.ship_id
WHERE s.ship_id IS NULL;

-- 4. Корректность расчетов
-- Проверка корректности агрегатов (сверка сумм между stg и dw)
SELECT 
    SUM(sales) AS total_sales_stg,
    SUM(profit) AS total_profit_stg
FROM stg.orders;

SELECT 
    SUM(sales) AS total_sales_dw,
    SUM(profit) AS total_profit_dw
FROM dw.sales_fact;

-- Проверка основных метрик (пример: суммарная скидка)
SELECT SUM(discount) AS total_discount_stg FROM stg.orders;
SELECT SUM(discount) AS total_discount_dw FROM dw.sales_fact;

-- Сверка контрольных сумм (количество уникальных заказов)
SELECT COUNT(DISTINCT order_id) AS unique_orders_stg FROM stg.orders;
SELECT COUNT(DISTINCT order_id) AS unique_orders_dw FROM dw.sales_fact;