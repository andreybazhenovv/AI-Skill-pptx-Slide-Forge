# Content outline — «Spec-Driven Development с AI-агентами»

Approved outline (2026-10-29). Ghost deck test passes: the action titles alone tell
the argument — implementation can be delegated to an agent, the silent change of a
task's meaning cannot.

| # | Action title | Content | Visual form |
|---|---|---|---|
| 1 | *(cover)* От промпта к инженерному процессу: Spec-Driven Development с AI-агентами | Central thesis: implementation can be delegated; silent meaning-change cannot | Hero cover, liquid ribbons, glass chip, outlined CTA |
| 2 | Правильно реализованная догадка всё равно остаётся догадкой | Case: «add a retry» → tests pass → a second target VM; the four unanswered meanings of "retry" | Case card + pill stack + accent strip |
| 3 | Ошибки возникают на трёх уровнях — контроль нужен на каждом | meaning → discovery; contract → plan/TDD/spec review; readiness → evidence matrix, adversarial review | Three glass level cards |
| 4 | Спецификация определяет обязательства, план организует работу, код исполняет | Proposal → Specs → Design → Tasks → Implementation plan chain; good requirement (bad/good pair) | Chain with dots + requirement card |
| 5 | Факты ≠ решения. Менять контракт можно, незаметно — нельзя | FACT/INFERENCE/UNKNOWN/CONFLICT/DECISION/ASSUMPTION cards; SPEC_DRIFT loop; freeze thesis | 2×3 fact cards + node flow + accent card |
| 6 | Исполнение проверяется дважды: соответствие контракту и качество | Coordinator/Executor/Reviewer roles; RED → GREEN → REFACTOR; useful vs useless RED | Role cards + capsule row + two mini blocks |
| 7 | Готовность объявляется только по свежим доказательствам | Evidence matrix R-01..R-04 with honest `NOT RUN`; finding CLAIM → EVIDENCE → VERDICT `GAP` | Dark table + finding card + accent verdict |
| 8 | Масштабировать следует церемонию, а не ответственность | Six process phases (contract phase active); Lightweight/Standard/High-risk/Incident; final thesis | Roadmap timeline + 2×2 mode cards + accent card |

Content discipline: ~40 words of body text max per slide; one visual idea per slide;
every status is honest (`NOT RUN` means "not run"); slide 8 is the conclusions slide —
it stays up for Q&A, there is no "thank you" slide.

Source material: `data.md` in the parent project — a 24-slide plan compressed into
these 8 (one argument, not the whole paper).
