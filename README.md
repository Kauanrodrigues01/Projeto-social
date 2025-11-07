# Projeto de Doações - Projeto Social

## 🎯 Sobre o Projeto

Sistema de doações online com pagamento via PIX usando Mercado Pago. O projeto permite que usuários façam doações para causas sociais de forma rápida e segura.

## 📋 Funcionalidades

### 1. Página de Doação (`/`)
- Formulário para criar doação
- Opção de escolher valor (com valores sugeridos)
- Opção de especificar destino da doação (Brinquedos, Alimentação ou Geral)
- Campos opcionais para nome e email do doador
- Design responsivo e moderno com Bootstrap 5

### 2. Página de Aguardando Pagamento (`/aguardando/<id>/`)
- Exibe informações do pagamento
- QR Code PIX (simulado - será integrado com Mercado Pago)
- Código PIX copia e cola
- Botão para verificar status do pagamento
- Instruções de como realizar o pagamento

### 3. Dashboard Administrativo (`/dashboard/`)
- Acesso restrito a usuários logados
- Estatísticas de doações (total arrecadado, pendente, quantidade)
- Filtros por status e tipo de doação
- Tabela com todas as doações
- Links para admin do Django

### 4. Admin do Django (`/admin/`)
- Gerenciamento completo de pagamentos
- Campos organizados em fieldsets
- Filtros e busca
- Visualização detalhada

## 🗄️ Modelo de Dados

### Payment (Pagamento)
- `valor`: Valor da doação (Decimal)
- `data`: Data e hora da doação (DateTime)
- `payment_id`: ID do pagamento no Mercado Pago (String, opcional)
- `payment_url`: URL do pagamento (URL, opcional)
- `tipo_doacao`: Tipo de doação - 'brinquedos', 'alimentacao' ou null (String, opcional)
- `status`: Status do pagamento - 'pending', 'approved', 'rejected', 'cancelled' (String)
- `nome_doador`: Nome do doador (String, opcional)
- `email_doador`: Email do doador (Email, opcional)

## 🚀 Como Executar o Projeto

### Opção 1: Desenvolvimento Local (Python)

1. **Clonar o repositório e criar ambiente virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Configurar variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Executar migrações e criar superusuário:**
```bash
python manage.py migrate
python manage.py create_superuser_auto
```

5. **Executar o servidor:**
```bash
python manage.py runserver
```

### Opção 2: Docker Compose - Desenvolvimento (App + PostgreSQL)

1. **Iniciar os containers:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. **Acessar o sistema:**
- **Aplicação:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
- **Credenciais:** admin / admin123

3. **Parar os containers:**
```bash
docker-compose -f docker-compose.dev.yml down
```

### Opção 3: Docker Compose - Produção (App com DATABASE_URL externa)

1. **Criar arquivo .env com suas configurações:**
```bash
cp .env.example .env
# Edite o .env e configure DATABASE_URL, SECRET_KEY, etc.
```

2. **Exemplo de .env para produção:**
```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DATABASE_URL=postgresql://user:password@db-host:5432/dbname
SUPERUSER_EMAIL=admin@seudominio.com
SUPERUSER_PASSWORD=senha-super-segura
```

3. **Iniciar o container:**
```bash
docker-compose up -d
```

4. **Ver logs:**
```bash
docker-compose logs -f
```

## 🌐 Acessar o Sistema

- **Página de Doação:** http://127.0.0.1:8000/
- **Dashboard Admin:** http://127.0.0.1:8000/dashboard/ (requer login)
- **Admin Django:** http://127.0.0.1:8000/admin/

### Credenciais Padrão (desenvolvimento)
- **Usuário:** admin
- **Email:** admin@dev.com (ou conforme .env)
- **Senha:** admin123 (ou conforme .env)

## 📦 Dependências

- Django 5.2.8
- Pillow 12.0.0
- python-decouple 3.8
- dj-database-url 2.1.0
- psycopg2-binary 2.9.9
- gunicorn 21.2.0
- whitenoise 6.6.0

## 🎨 Tecnologias Utilizadas

- **Backend:** Django 5.2.8
- **Frontend:** Bootstrap 5.3.0
- **Ícones:** Bootstrap Icons 1.10.0
- **Fontes:** Google Fonts (Poppins)
- **Banco de Dados:** SQLite3 (desenvolvimento) / PostgreSQL (produção)
- **WSGI Server:** Gunicorn
- **Static Files:** WhiteNoise

## 🐳 Arquivos Docker

### Dockerfile (Multi-Stage Build)
Imagem Docker otimizada usando **multi-stage build**:
- **Stage 1 (Builder)**: Compila dependências e cria virtual environment
- **Stage 2 (Runtime)**: Imagem final enxuta (~50% menor)
- **Usuário não-root**: Executa como usuário `django` (UID 1000)
- **Segurança**: Apenas dependências runtime necessárias

**Benefícios:**
- ✅ Imagem ~50% menor (250-350 MB vs 500-600 MB)
- ✅ Mais segura (menos pacotes = menos vulnerabilidades)
- ✅ Mais rápida para deploy
- ✅ Melhor cache de camadas

📖 **Documentação completa:** [DOCKER.md](./DOCKER.md)

### docker-compose.dev.yml
Ambiente de desenvolvimento completo com:
- Aplicação Django (porta 8000)
- PostgreSQL 16 (porta 5432)
- Volumes persistentes
- Hot reload habilitado

### docker-compose.yml
Ambiente de produção apenas com aplicação:
- Recebe DATABASE_URL externa
- Configurado para usar Gunicorn
- WhiteNoise para servir arquivos estáticos
- Healthcheck configurado

### docker-entrypoint.sh
Script de inicialização que:
- Aguarda o banco de dados estar disponível
- Executa migrações automaticamente
- Cria superusuário automaticamente
- Coleta arquivos estáticos

## ⚙️ Variáveis de Ambiente

Todas as variáveis podem ser configuradas no arquivo `.env`:

| Variável | Descrição | Padrão | Obrigatória |
|----------|-----------|--------|-------------|
| `SECRET_KEY` | Chave secreta do Django | (gerada) | Sim (produção) |
| `DEBUG` | Modo debug | True | Não |
| `ALLOWED_HOSTS` | Hosts permitidos | localhost,127.0.0.1 | Não |
| `DATABASE_URL` | URL do PostgreSQL | (SQLite) | Não |
| `SUPERUSER_EMAIL` | Email do admin | admin@example.com | Não |
| `SUPERUSER_PASSWORD` | Senha do admin | admin123 | Não |

## 🔧 Comandos Úteis

### Management Commands

```bash
# Aguardar banco de dados estar disponível
python manage.py wait_for_db --timeout=60

# Verificar saúde da aplicação (healthcheck)
python manage.py healthcheck

# Criar superusuário automaticamente
python manage.py create_superuser_auto

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Criar novas migrações
python manage.py makemigrations
```

### Docker

```bash
# Build e iniciar (desenvolvimento)
docker-compose -f docker-compose.dev.yml up --build

# Apenas iniciar containers existentes
docker-compose -f docker-compose.dev.yml up

# Parar containers
docker-compose -f docker-compose.dev.yml down

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Executar comando dentro do container
docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# Reconstruir apenas a aplicação
docker-compose -f docker-compose.dev.yml build web
```

## 📝 Próximos Passos

1. **Integração com Mercado Pago:**
   - Instalar SDK: `pip install mercadopago`
   - Configurar credenciais (Access Token)
   - Implementar criação de pagamento PIX
   - Implementar verificação de status
   - Adicionar webhooks para notificações automáticas

2. **Melhorias:**
   - Sistema de confirmação por email
   - Geração de recibos em PDF
   - Relatórios e gráficos no dashboard
   - Exportação de dados para Excel/CSV
   - Sistema de notificações em tempo real

## 🔐 Segurança

⚠️ **IMPORTANTE para Produção:**

- ✅ Gere uma nova `SECRET_KEY` segura
- ✅ Configure `DEBUG = False`
- ✅ Configure `ALLOWED_HOSTS` com seus domínios
- ✅ Use PostgreSQL (DATABASE_URL)
- ✅ Configure HTTPS (SSL/TLS)
- ✅ Use senhas fortes para SUPERUSER_PASSWORD
- ✅ Configure backup automático do banco de dados
- ✅ Monitore logs de erro
- ✅ Use variáveis de ambiente seguras (nunca commite .env)

## 📧 Suporte

Para dúvidas ou sugestões sobre o projeto, entre em contato.

---

**Desenvolvido com ❤️ para fazer a diferença!**
