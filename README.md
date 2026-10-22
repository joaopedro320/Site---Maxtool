# SITE - Maxtool

Site institucional da **Maxtool** (ITRAC – Comércio, Importação, Exportação e Distribuição LTDA), Vitória/ES.
Ferramentas, abrasivos e máquinas para marmoraria — desenvolvido por [QH4 Growth](https://www.instagram.com/qh4growth/).

## Páginas

| Página | URL |
|---|---|
| Início | `/` |
| Produtos (guia por material, filtros, downloads) | `/produtos/` |
| A Maxtool | `/sobre/` |
| Peças & Assistência (vista explodida, garantia) | `/pecas/` |
| Max Tool Day | `/max-tool-day/` |
| Onde comprar | `/onde-comprar/` |
| Seja um revendedor | `/seja-um-revendedor/` |
| Contato | `/contato/` |
| Política de Privacidade | `/politica-de-privacidade/` |
| Exclusão de dados (URL exigida pelo app da Meta) | `/exclusao-de-dados/` |

## Como editar

Os HTMLs são **gerados**. Não edite `index.html` direto — edite a fonte e rode o build:

- `src/data.py` — dados da empresa, produtos, perguntas frequentes, guia por material, **ID do Google Tag Manager**
- `src/sections/*.html` — blocos de conteúdo
- `src/layout.html` — cabeçalho e rodapé
- `css/style.css`, `js/main.js` — visual e interações

```bash
python3 src/build.py
```

O build gera as páginas, `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, `404.html`, os dados estruturados (schema.org) e a pasta `deploy/` (para upload manual).

## Publicar (maxtool.com.br)

O deploy é **automático**: push na branch `main` → GitHub Actions
(`.github/workflows/deploy.yml`) espelha os arquivos no VPS da Hostinger
(`/var/www/site`, usuário restrito `deploy`). Detalhes e checklist de
manutenção: ver `CLAUDE.md`.

(As instruções originais da QH4 previam Vercel — não usamos; o site roda no
nosso VPS junto com a API de leads `/api/...`.)

## Visualizar localmente

```bash
python3 -m http.server 5181
```

Abra http://localhost:5181

## Pendências

- Pedir à QH4 acesso de administrador ao contêiner `GTM-WZNMHZJG` (GA4, Meta
  Pixel e Hotjar entram por ele) — o contêiner é um ativo da Maxtool.
- Formulários e busca por CEP usam a API do servidor (`/api/...`, código em
  `infra/`). Fora dele, caem no WhatsApp com os dados preenchidos.
