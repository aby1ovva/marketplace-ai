# ADR 0004 — Рекомендации: гейт по lift, ранжирование по объёму

## Контекст
Дашборд показывал топ-рекомендацию по `together` (объёму), но подпись обещает
«lift > 1 — связь сильнее случайной». Для `bed_bath_table` топом был `furniture_decor`
(together=70, **lift=0.64 < 1**) — прямое противоречие подписи (находка cognitive-debt).

## Решение
Правило: пара **eligible только если `lift > LIFT_FLOOR` (= 1.0)**; среди прошедших
ранжируем по `together`, затем `confidence`. `LIFT_FLOOR` объявлен в `src/config.py` (SSOT).
Дашборд вызывает `top_recommendations(recs, cat, min_lift=LIFT_FLOOR)`.

Отвергнута альтернатива «ранжировать по lift»: редкие пары с высоким lift и малым объёмом
выглядят для продавца недостоверно.

## Последствия
- Для `bed_bath_table` топ теперь `home_confort` (together=43, lift=2.99) — согласуется с подписью.
- `reports/recs_categories.csv` НЕ регенерируется: гейт применяется при чтении/запросе.
- Зафиксировано тестом `test_recommend_excludes_lift_below_floor` (`tests/test_recommend.py`).
