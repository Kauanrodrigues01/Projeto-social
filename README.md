# Projeto Social - Plataforma de Doações

<div align="center">
  <img src="docs/images/home-page.png" alt="Página de Doação" width="800"/>
</div>

<br>

> 🎁 Uma plataforma web completa para gerenciar doações via PIX com integração ao Mercado Pago

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Mercado_Pago-00B1EA?style=for-the-badge&logo=mercadopago&logoColor=white" alt="Mercado Pago">
</div>

<br>

## 🎯 Sobre o Projeto

O **Projeto Social** é uma plataforma desenvolvida para facilitar doações através de pagamentos PIX. Com interface simples e intuitiva, permite que qualquer pessoa possa fazer doações de forma rápida e segura, com confirmação automática via webhook do Mercado Pago.

<div align="center">
  <img src="docs/images/payment-page.png" alt="Página de Pagamento" width="800"/>
</div>


### 🎨 Principais Funcionalidades

- 💸 **Doações via PIX** - Pagamento instantâneo com QR Code
- � **Webhook Automático** - Confirmação de pagamento em tempo real
- 📊 **Dashboard Administrativo** - Visualização de estatísticas e doações
- 🎯 **Destino da Doação** - Escolha entre Brinquedos ou Alimentação
- ✅ **Verificação de Status** - Consulta manual do status do pagamento
- 🚫 **Zero Burocracia** - Apenas valor obrigatório, sem campos desnecessários
- 📱 **Responsivo** - Interface adaptável a qualquer dispositivo
- 🐳 **Containerizado** - Deploy fácil com Docker
- 🔐 **Seguro** - Integração oficial com Mercado Pago

## 🛠 Tecnologias Utilizadas

### Backend

- **Python 3.12** - Linguagem principal
- **Django 5.2.8** - Framework web
- **Mercado Pago API** - Processamento de pagamentos PIX
- **python-decouple** - Gerenciamento de variáveis de ambiente
- **requests** - Chamadas HTTP para API do Mercado Pago

### Banco de Dados

- **PostgreSQL 17.2** - Banco principal (produção)
- **SQLite** - Desenvolvimento local (fallback automático)
- **dj-database-url** - Parsing de URLs de conexão

### Frontend

- **Bootstrap 5.3.0** - Framework CSS
- **Bootstrap Icons** - Ícones
- **HTML5/CSS3** - Estrutura e estilo
- **JavaScript** - Interatividade

### DevOps & Infraestrutura

- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers
- **Gunicorn** - WSGI server para produção
- **Whitenoise** - Servir arquivos estáticos
- **Multi-stage Build** - Otimização de imagem Docker (50% menor)

## 🏗 Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Doador Web    │───▶│  Django App     │───▶│   PostgreSQL    │
│  (Bootstrap)    │    │  (Gunicorn)     │    │    Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Mercado Pago   │
                       │      API        │
                       │   (Webhook)     │
                       └─────────────────┘
                              │
                       ┌──────┴──────┐
                       │   Docker    │
                       │ Container   │
                       └─────────────┘
```

## ⚙️ Instalação e Configuração

### 📋 Pré-requisitos

- Python 3.12+
- Docker & Docker Compose (opcional)
- Conta no Mercado Pago (para integração PIX)
- Git

### 🚀 Configuração Rápida

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/projeto-social-back.git
cd projeto-social-back
```

2. **Configure o ambiente virtual**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:

```bash
# Django Settings
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (opcional - deixe comentado para usar SQLite)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Superuser credentials
SUPERUSER_EMAIL=admin
SUPERUSER_PASSWORD=admin123

# Mercado Pago
MP_ACCESS_TOKEN=TEST-seu-token-aqui
MP_BASE_API_URL=https://api.mercadopago.com
NOTIFICATION_URL=https://seu-dominio.com/services/webhook/mercadopago/
BASE_APPLICATION_URL=http://localhost:8000
```

5. **Execute as migrações**

```bash
python manage.py migrate
```

6. **Inicie o servidor**

```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

### 🐳 Executar com Docker

#### Desenvolvimento (com PostgreSQL)

```bash
docker-compose -f docker-compose.dev.yml up --build
```

#### Produção (banco externo)

```bash
# Configure DATABASE_URL no .env com sua URL do PostgreSQL
docker-compose up --build
```

## 📚 Estrutura do Projeto

```
projeto-social-back/
├── 📁 app/                    # Configurações Django
│   ├── settings.py           # Settings com variáveis ambiente
│   ├── urls.py               # URLs principais
│   └── wsgi.py               # WSGI application
├── 📁 donations/              # App de doações
│   ├── models.py             # Modelo Payment
│   ├── views.py              # Views de doação e dashboard
│   ├── admin.py              # Admin customizado
│   ├── urls.py               # URLs de doações
│   ├── signals.py            # Signal para criar superuser
│   └── management/           # Comandos Django
│       └── commands/
│           ├── wait_for_db.py      # Aguardar DB
│           └── healthcheck.py      # Health check
├── 📁 services/               # Integração Mercado Pago
│   ├── mercadopago.py        # MercadoPagoService
│   ├── views.py              # Webhook handler
│   └── urls.py               # URLs de webhook
├── 📁 templates/              # Templates HTML
│   ├── base.html             # Template base
│   └── donations/
│       ├── donation_page.html      # Página de doação
│       ├── waiting_payment.html    # Aguardando pagamento
│       └── dashboard.html          # Dashboard admin
├── 📁 static/                 # Arquivos estáticos
├── 🐳 Dockerfile              # Multi-stage build
├── 🐳 docker-compose.yml      # Produção
├── 🐳 docker-compose.dev.yml  # Desenvolvimento
├── 🔧 docker-entrypoint.sh    # Entrypoint script
├── 📋 requirements.txt        # Dependências Python
└── ⚙️ manage.py               # CLI do Django
```

## 🔗 Rotas Principais

### 🎁 Páginas Públicas

```http
GET  /                        # Página de doação
GET  /aguardando/{id}/        # Aguardando confirmação do pagamento
POST /aguardando/{id}/        # Verificar status do pagamento
```

### 🔐 Área Administrativa

```http
GET  /admin/                  # Login do admin
GET  /dashboard/              # Dashboard de doações (requer autenticação)
```

### 🔔 Webhook

```http
POST /services/webhook/mercadopago/  # Webhook do Mercado Pago
```

## 💳 Modelo de Dados

### Payment (Doação)

```python
class Payment(models.Model):
    valor = DecimalField              # Valor da doação (min: R$ 0,10)
    data = DateTimeField             # Data da confirmação
    payment_id = CharField           # ID do pagamento no Mercado Pago
    payment_url = URLField           # URL do pagamento
    qr_code = TextField              # Código PIX copia e cola
    qr_code_base64 = TextField       # QR Code em base64
    tipo_doacao = CharField          # 'brinquedos' ou 'alimentacao'
    status = CharField               # 'pending', 'approved', 'rejected', 'cancelled'
    nome_doador = CharField          # Nome do doador (opcional)
```

## 🌟 Funcionalidades Especiais

### 💸 Processo de Doação

1. **Escolha o valor** - Mínimo de R$ 0,10
2. **Selecione o destino** (opcional) - Brinquedos ou Alimentação
3. **Informe seu nome** (opcional) - Para registro da doação
4. **Gere o PIX** - QR Code instantâneo via Mercado Pago
5. **Pague** - Escaneie o QR Code ou copie o código PIX
6. **Confirmação automática** - Via webhook do Mercado Pago

### 📊 Dashboard Administrativo

- **Total arrecadado** - Soma de todas as doações aprovadas
- **Total pendente** - Doações aguardando confirmação
- **Quantidade de doações** - Contador de doações aprovadas
- **Lista de pagamentos** - Tabela com filtros por status e tipo
- **Estatísticas visuais** - Cards informativos

### 🔔 Webhook Inteligente

- Suporte a **formato antigo e novo** do Mercado Pago
- Atualização automática de status
- Registro da data de confirmação
- Tratamento de erros robusto

## 🐳 Docker - Multi-stage Build

O Dockerfile usa build em múltiplos estágios para otimização:

### Estágio 1: Builder
- Instala dependências de compilação
- Cria ambiente virtual
- Instala pacotes Python

### Estágio 2: Runtime
- Imagem final leve (~250-350MB vs 500-600MB)
- Apenas dependências de runtime
- Usuário não-root (`django:1000`)
- Segurança aprimorada

### Health Check Integrado

```yaml
healthcheck:
  test: ["CMD", "python", "manage.py", "healthcheck"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🔐 Segurança

- ✅ CSRF Protection habilitado
- ✅ Secret key via variável de ambiente
- ✅ Debug mode configurável
- ✅ Allowed hosts restritos
- ✅ Usuário não-root no container
- ✅ Sanitização de inputs
- ✅ Validação de dados do webhook

## 🚀 Deploy em Produção

### Checklist de Produção

- [ ] Configurar `DEBUG=False` no `.env`
- [ ] Definir `SECRET_KEY` forte e única
- [ ] Configurar `ALLOWED_HOSTS` com seu domínio
- [ ] Usar PostgreSQL (configurar `DATABASE_URL`)
- [ ] Obter **Access Token de Produção** do Mercado Pago
- [ ] Configurar `NOTIFICATION_URL` com domínio público (HTTPS)
- [ ] Usar serviço de túnel (ngrok) ou domínio real para webhook
- [ ] Configurar SSL/TLS (HTTPS obrigatório para webhook)
- [ ] Executar `collectstatic` para arquivos estáticos
- [ ] Configurar backup do banco de dados

### Variáveis de Ambiente - Produção

```bash
SECRET_KEY=gere-uma-chave-complexa-e-unica
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DATABASE_URL=postgresql://user:senha@host:5432/banco
MP_ACCESS_TOKEN=APP_USR-seu-token-de-producao
NOTIFICATION_URL=https://seudominio.com/services/webhook/mercadopago/
BASE_APPLICATION_URL=https://seudominio.com
```

## 🧪 Comandos Úteis

```bash
# Criar superusuário manualmente
python manage.py createsuperuser

# Executar migrations
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Verificar configuração
python manage.py check

# Aguardar banco de dados
python manage.py wait_for_db

# Health check
python manage.py healthcheck
```

## 📝 Configuração do Mercado Pago

### Obter Credenciais

1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials
2. Escolha **Credenciais de Teste** (desenvolvimento) ou **Produção**
3. Copie o **Access Token**
4. Cole no `.env` como `MP_ACCESS_TOKEN`

### Configurar Webhook

1. Acesse: https://www.mercadopago.com.br/developers/panel/webhooks
2. Adicione novo webhook
3. URL: `https://seu-dominio.com/services/webhook/mercadopago/`
4. Eventos: `payment`
5. Salve

## 🎨 Customização

### Alterar Valor Mínimo

No arquivo `donations/views.py`:

```python
if valor < 0.10:  # Altere aqui
    messages.error(request, "O valor mínimo é R$ 0,10.")
```

### Adicionar Novos Tipos de Doação

No arquivo `donations/models.py`:

```python
TIPO_DOACAO_CHOICES = [
    ('brinquedos', 'Brinquedos'),
    ('alimentacao', 'Alimentação'),
    ('roupas', 'Roupas'),  # Adicione aqui
]
```

## 👨‍💻 Autor

**Kauan Rodrigues Lima**

- GitHub: [@Kauanrodrigues01](https://github.com/Kauanrodrigues01)
- LinkedIn: [Kauan Rodrigues](https://www.linkedin.com/in/kauan-rodrigues-lima/)

---

<div align="center">
  <p>Feito com ❤️ para ajudar quem precisa</p>
  <p>⭐ Se este projeto foi útil, considere dar uma estrela!</p>
</div>
````

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
