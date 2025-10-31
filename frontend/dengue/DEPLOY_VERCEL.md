# Guia de Deploy no Vercel - Sem Backend Django

Este projeto funciona **SEM precisar do backend Django** em produção, usando dados estáticos dos arquivos JSON.

## ✅ Passos para Deploy

### 1. Copiar arquivos JSON

Copie os arquivos JSON para dentro do projeto Next.js:

```bash
# No terminal, na raiz do projeto:
cp dengue_statistics.json frontend/dengue/public/data/
cp dengue_advanced_statistics.json frontend/dengue/public/data/
```

**OU manualmente:**
- Crie a pasta `frontend/dengue/public/data/`
- Copie `dengue_statistics.json` e `dengue_advanced_statistics.json` para lá

### 2. Configurar no Vercel

1. **Root Directory**: `frontend/dengue`
2. **Framework Preset**: Next.js (detectado automaticamente)
3. **Build Command**: `npm run build` (padrão)
4. **Output Directory**: `.next` (padrão)

### 3. Variáveis de Ambiente (OPCIONAL)

Se quiser usar uma API externa no futuro:
- `NEXT_PUBLIC_API_URL` = URL da sua API

**Sem variáveis de ambiente, o projeto usa dados estáticos automaticamente!**

## 🎯 Como Funciona

- **Em desenvolvimento** (localhost): Tenta usar `http://localhost:8000/api` se o backend estiver rodando
- **Em produção** (Vercel): Usa os dados estáticos dos arquivos JSON na pasta `public/data/`

## ✅ Pronto!

Após copiar os JSONs, faça commit e push. O Vercel fará o deploy automaticamente!

---

**Nota**: Os arquivos JSON são grandes (~399 linhas cada). Certifique-se de que eles foram copiados corretamente.

