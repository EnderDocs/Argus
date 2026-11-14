# Argus — Plataforma de Datasets de Robótica

> **Unidade Curricular:** Modelação de Sistemas de Informação (ModSI) — ISEP 2026/27  
> **Stack Tecnológica:** Django Ninja (Python 5) + React (Vite & TypeScript) + MySQL 8

---

## 1. Visão Geral da Arquitetura

O Argus adota uma **Arquitetura Baseada em Serviços (*Service Layer Architecture*) e Domínios Modulares**, seguindo uma leitura pragmática do padrão **MVC (Model-View-Controller)** adaptado a uma Single-Page Application (SPA):

- **View (Visão):** SPA desacoplada em React + Vite no cliente (`frontend/`).
- **Controller (Controlador):** Routers do Django Ninja (`api.py` nas apps) que tratam pedidos HTTP, validação de esquemas (Pydantic) e autenticação.
- **Model (Modelo):** Composto pela **Camada de Serviços** (`services.py`), que orquestra a lógica de negócio e transações atómicas, apoiada por módulos de **Domínio Puro** (`domain/`) para cálculos e algoritmos, e pelo **Django ORM** (`models.py`) para persistência no MySQL.

---

## 2. Estrutura do Projeto

```text
argus/
├── docs/                        # Documentação, modelação UML, DER e relatórios
│   ├── der/                     # Diagrama Entidade-Relação (ficheiros draw.io / imagem)
│   ├── diagrams/                # Diagramas UML (Casos de Uso, Sequência, Estados)
│   └── wireframes/              # Wireframes e fluxos de navegação (Wireflow)
│
├── db/                          # Scripts SQL exigidos pelo guião de avaliação
│   ├── schema.sql               # DDL das tabelas, chaves e restrições
│   ├── views.sql                # As 3 vistas SQL (catálogo, moderação, painel)
│   ├── transactions.sql         # Script SQL da transação atómica (RN-12)
│   └── seed.sql                 # Dados de demonstração para a defesa
│
├── storage/                     # Armazenamento físico de ficheiros (ignorado pelo Git)
│   ├── datasets/                # Ficheiros CSV de sensores versionados
│   ├── proofs/                  # Comprovativos de pagamento de acesso privado
│   └── evidence/                # Evidências para pedidos de certificação
│
├── podman/                      # Configurações de contentorização para execução rápida
│
├── frontend/                    # Aplicação cliente (React + Vite + TypeScript + Tailwind)
│   └── src/
│       ├── api/                 # Clientes HTTP e chamadas aos endpoints (/api/v1/)
│       ├── assets/              # Recursos estáticos (ícones, imagens, logos)
│       ├── components/          # Componentes partilhados e reutilizáveis
│       │   ├── ui/              # Componentes base (botões, inputs, modais, badges)
│       │   ├── feedback/        # Alertas de erro/sucesso, spinners, esqueletos
│       │   ├── charts/          # Gráficos (Recharts/ECharts) do sinal e métricas
│       │   └── layout/          # Navbar (com seletor de idioma), Sidebar, Footer
│       ├── features/            # Componentes especializados por área funcional
│       │   ├── catalog/         # Cartões de dataset, filtros técnicos, comparador
│       │   ├── dataset-form/    # Assistente de submissão em 3 passos
│       │   └── moderation/      # Fila de moderação e gavetas de decisão
│       ├── hooks/               # Custom hooks (autenticação, debouncing, etc.)
│       ├── i18n/                # Internacionalização (react-i18next)
│       │   └── locales/         # Dicionários de tradução (pt.json e en.json)
│       ├── pages/               # Ecrãs oficiais da aplicação (S01 a S13)
│       └── types/               # Tipos TypeScript alinhados com os DTOs do backend
│
└── backend/                     # Servidor aplicacional (Django 5 + Django Ninja)
    ├── manage.py
    ├── config/                  # Configuração global do projeto Django
    │   └── settings/            # Configurações de ambiente (base, dev, prod)
    ├── core/                    # Lógica transversal e contratos de infraestrutura
    │   └── storage/             # Portas (interfaces) e adaptadores de armazenamento
    └── apps/                    # Módulos verticais de negócio
        ├── users/               # Gestão de utilizadores, autenticação e papéis
        ├── catalog/             # Catálogos de referência (sensores, unidades, etc.)
        ├── datasets/            # Datasets, ficheiros, versões e download
        │   └── domain/          # PYTHON PURO: cálculo da nota Q, IC e validador CSV
        ├── access/              # Pedidos de acesso e transação atómica (RN-12)
        ├── moderation/          # Certificações, reports, reviews e moderação
        ├── audit/               # Registo de auditoria (AuditLog)
        └── analytics/           # Consultas e métricas do painel administrativo
```

---

## 3. Explicação Detalhada das Pastas

### `docs/`
Guarda os artefactos exigidos nas componentes de avaliação do guião (30% da nota do relatório):
- `der/`: Ficheiro editável do Modelo Entidade-Relação e dicionário de dados.
- `diagrams/`: Diagramas de casos de uso por ator, diagrama de estados e diagrama de sequência da transação de acesso.
- `wireframes/`: Desenho das páginas (resoluções desktop e mobile) e wireflow de navegação.

### `db/`
Reúne os ficheiros SQL exigidos para a entrega no Moodle:
- `schema.sql`: Estrutura das tabelas em 3ª Forma Normal com integridade referencial.
- `views.sql`: As 3 vistas SQL requeridas (`vw_dataset_catalog`, `vw_moderation_queue` e `vw_monthly_downloads`).
- `transactions.sql`: Demonstração da transação atómica com bloqueio `FOR UPDATE` para aprovação de acesso (RN-12).
- `seed.sql`: Carga inicial de dados para a demonstração (12 datasets, 8 utilizadores, reviews e pedidos).

### `storage/`
Pasta onde são gravados os ficheiros reais carregados na plataforma (fora do repositório Git):
- Os datasets não são servidos diretamente como ficheiros estáticos da web; o acesso é sempre protegido e auditado através de endpoints do Django Ninja.

### `backend/`
- **`config/`**: Contém as configurações do Django (`settings/`), URLs centrais e a instância principal `NinjaAPI(version="1.0.0", title="Argus API")`.
- **`core/`**: Funcionalidades partilhadas por várias apps (exceções globais de negócio, segurança de cookies/CSRF, utilitários de paginação e contratos abstratos de storage).
- **`apps/`**: Módulos organizados verticalmente por domínio funcional:
  - **`users/`**: Registo, login local, controlo de tentativas e atribuição de papéis (Visitante, Investigador, Contribuidor, Moderador, Administrador).
  - **`catalog/`**: Gestão dos valores de referência controlados (tipos de sensores, grandezas e unidades, plataformas robóticas, licenças).
  - **`datasets/`**: Módulo central da plataforma.
    - Contém a subpasta **`domain/`**, que é **código Python puro sem dependências do Django**. É aqui que residem o cálculo da qualidade técnica ($Q$), o cálculo do Índice de Confiança ($IC$) e o analisador em stream do CSV (verificação de timestamps crescentes e lacunas). Facilita testes unitários rápidos e isolados.
    - O ficheiro `services.py` orquestra a submissão, criação de novas versões imutáveis e preparação do pacote de download (`.zip` com CSV, JSON de metadados e checksum SHA-256).
  - **`access/`**: Gestão de pedidos de acesso a datasets privados, validação de comprovativos e execução da transação atómica (`RN-12`) via `select_for_update()`.
  - **`moderation/`**: Tratamento de pedidos de certificação com evidências, moderação de comentários/avaliações e gestão de denúncias (*reports*).
  - **`audit/`**: Tabela de registo imutável (*append-only*) para todas as ações sensíveis (RN-18).
  - **`analytics/`**: Endpoints de leitura agregada para alimentação do painel e estatísticas.

### `frontend/`
- **`src/pages/`**: Cada ficheiro representa diretamente um ecrã identificado no enunciado do projeto (**S01** a **S13**), garantindo rastreabilidade perfeita com os requisitos e casos de uso:
  - `S01`: Página inicial, rankings e contadores.
  - `S02`: Catálogo pesquisável com filtros e seleção para comparação.
  - `S03`: Ficha detalhada do dataset, visualizador do sinal e ações.
  - `S04`: Autenticação e registo.
  - `S05`: Assistente em 3 passos para submissão de datasets e novas versões.
  - `S06`: Gestão dos datasets do contribuidor e pedidos recebidos.
  - `S07`: Painel de perfil do utilizador.
  - `S08`: Fila de moderação e revisão.
  - `S09`: Moderação de reviews e sinalizações de utilizadores.
  - `S10`: Painel global de administração com gráficos.
  - `S11`: Gestão de utilizadores e papéis.
  - `S12`: Catálogos de referência e auditoria.
  - `S13`: Páginas de erro (403 Proibido e 404 Não Encontrado).
- **`src/features/`**: Componentes ricos agrupados pela sua função de negócio (ex.: o formulário por passos, tabela de moderação, cartões do catálogo).
- **`src/i18n/`**: Configuração do `react-i18next` com suporte obrigatório aos idiomas Português e Inglês (RN-20 / T2).
- **`src/components/`**: Componentes visuais atómicos, layouts e gráficos interativos (Recharts) reutilizáveis.

---

## 4. Benefícios desta Organização para a Equipa

1. **Sem Fricção de Merge no Git:** Cada membro do grupo pode trabalhar em verticais distintas (`apps/` no backend e `features/` ou `pages/` no frontend) em simultâneo sem causar conflitos de código.
2. **Conformidade Total com a Avaliação:** Respeita exatamente os critérios do guião de ModSI (estrutura organizada MVC, suporte de vistas/transações em SQL, testes e documentação).
3. **Equilíbrio entre Robustez e Rapidez:** Mantém regras matemáticas e de ficheiros puras e fáceis de testar em `domain/`, sem o fardo excessivo de ter dezenas de repositórios desnecessários para operações simples de base de dados.
