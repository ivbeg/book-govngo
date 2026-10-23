# Прежние адреса

Сайт собирает Docusaurus. Числовой префикс папки и файла в адрес не входит.

`docs/04-classification/02-by-founder.md` открывается как `/classification/by-founder/`.

Старые страницы mdBook, и плоские `ch_01.html`, и собранные с префиксом `04-classification/02-by-founder.html`, ведут на новые адреса. Файлы лежат в `static/`, список для меню — в `redirects.ts`. Префикс сайта `/book-govngo/` в этих файлах и в `docusaurus.config.ts` один и тот же.

| Было в mdBook | Стало |
| --- | --- |
| `short.html`, `01-about/01-start.html` | `/` |
| `limitations.html` | `/about/limitations/` |
| `ch_01.html` | `/boundary/what-it-is/` |
| `ch_02_001.html` | `/classification/by-founder/` |
| `ch_02_002.html` | `/classification/by-mandate/` |
| `ch_05.html` | `/identification/methods/` |
| `ch_06_001.html` | `/openness/versus-nko/` |
| `ch_07_001.html` | `/finance/federal/` |
| `finalwords.html` | `/policy/decisions/` |
| `appendixes_01.html` | `/appendices/federal-top-2019/` |

Главы с номером 4 в плоской нумерации не было. Полная карта файлов — в `stable-paths.md`.
