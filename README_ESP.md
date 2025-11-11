# Gophish MCP Server

Un servidor MCP (Model Context Protocol) completo para interactuar con todas las funcionalidades de la API de GoPhish.

## Características Principales

- **Gestión Completa de Campañas**: CRUD completo + análisis avanzado y estadísticas
- **Gestión de Grupos**: Administrar grupos de usuarios objetivo con búsqueda
- **Plantillas de Email**: Crear, editar y gestionar plantillas de correo electrónico
- **Páginas de Aterrizaje**: Administrar landing pages para campañas
- **Perfiles SMTP**: Configurar perfiles de envío de correo
- **Gestión de Usuarios**: Administrar usuarios y administradores del sistema
- **Análisis y Reportes**: Estadísticas detalladas, exportación de datos y análisis global
- **Herramientas de Utilidad**: Búsqueda, validación, duplicación y diagnóstico

## Instalación

1. Clona este repositorio
2. Instala las dependencias:
```bash
pip install -e .
```

## Configuración

### Opción 1: Archivo .env (Recomendado)
1. Copia el archivo de ejemplo:
```bash
cp env.example .env
```

2. Edita `.env` con tus credenciales:
```bash
GOPHISH_URL=https://tu-servidor-gophish:3333
GOPHISH_API_KEY=tu-api-key-aqui
```

### Opción 2: Variables de entorno
```bash
export GOPHISH_URL="https://tu-servidor-gophish:3333"
export GOPHISH_API_KEY="tu-api-key"
```

## Uso con Claude, Cursor, VSCode, Kiro

### 1. Configurar Credenciales (Solo una vez)
Crea un archivo `.env` en el directorio del proyecto:
```bash
cp env.example .env
# Edita .env con tus credenciales reales
```

### 2. Configurar Cliente MCP
Agrega el servidor a tu configuración MCP (sin credenciales):

```json
{
  "mcpServers": {
    "gophish": {
      "command": "python",
      "args": ["/ruta/absoluta/a/server.py"],
      "cwd": "/ruta/absoluta/al/proyecto",
      "disabled": false,
      "autoApprove": [
        "gophish_get_campaigns",
        "gophish_get_groups", 
        "gophish_get_templates",
        "gophish_get_pages",
        "gophish_get_smtp_profiles"
      ]
    }
  }
}
```

### 3. Reiniciar Cliente MCP
Reinicia tu cliente MCP (Claude, Cursor, etc.)

**Nota**: Las credenciales solo se configuran en el archivo `.env` del servidor, no en el JSON del cliente.

## Categorías de Herramientas

- ***(SOLO LECTURA - Auto-aprobadas)***: Estas herramientas solo leen datos y son aprobadas automáticamente por el cliente MCP
- ***(ESCRITURA - Requiere aprobación manual)***: Estas herramientas modifican datos y requieren aprobación manual por seguridad

## Herramientas Disponibles

### 🎯 Campañas (Gestión Completa)
**Operaciones Básicas:**
- `gophish_get_campaigns`: Obtener todas las campañas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaign`: Obtener detalles de una campaña específica *(SOLO LECTURA - Auto-aprobada)*
- `gophish_create_campaign`: Crear nueva campaña *(ESCRITURA - Requiere aprobación manual)*
- `gophish_update_campaign`: Actualizar campaña existente *(ESCRITURA - Requiere aprobación manual)*
- `gophish_delete_campaign`: Eliminar campaña *(ESCRITURA - Requiere aprobación manual)*

**Análisis y Estadísticas:**
- `gophish_get_latest_campaign`: Obtener la campaña más reciente con estadísticas completas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaigns_summary`: Obtener resumen de las últimas N campañas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaign_results`: Obtener resultados detallados de una campaña *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaign_summary`: Obtener resumen con estadísticas de una campaña *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaign_analytics`: Obtener análisis completo de una campaña *(SOLO LECTURA - Auto-aprobada)*

**Filtros y Búsqueda:**
- `gophish_get_active_campaigns`: Obtener campañas activas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_completed_campaigns`: Obtener campañas completadas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaign_by_status`: Filtrar campañas por estado *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_recent_campaigns`: Obtener campañas de los últimos N días *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaign_by_date_range`: Obtener campañas en rango de fechas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_search_campaigns`: Buscar campañas por nombre *(SOLO LECTURA - Auto-aprobada)*

**Utilidades:**
- `gophish_get_campaign_targets`: Obtener todos los objetivos de una campaña *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_campaign_events`: Obtener eventos de una campaña *(SOLO LECTURA - Auto-aprobada)*

### 👥 Grupos (Gestión Completa)
- `gophish_get_groups`: Obtener todos los grupos *(SOLO LECTURA - Auto-aprobada)*
- `gophish_create_group`: Crear nuevo grupo *(ESCRITURA - Requiere aprobación manual)*
- `gophish_update_group`: Actualizar grupo existente *(ESCRITURA - Requiere aprobación manual)*
- `gophish_delete_group`: Eliminar grupo *(ESCRITURA - Requiere aprobación manual)*
- `gophish_search_groups`: Buscar grupos por nombre *(SOLO LECTURA - Auto-aprobada)*

### 📧 Plantillas de Email (Gestión Completa)
- `gophish_get_templates`: Obtener todas las plantillas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_create_template`: Crear nueva plantilla *(ESCRITURA - Requiere aprobación manual)*
- `gophish_update_template`: Actualizar plantilla existente *(ESCRITURA - Requiere aprobación manual)*
- `gophish_delete_template`: Eliminar plantilla *(ESCRITURA - Requiere aprobación manual)*
- `gophish_search_templates`: Buscar plantillas por nombre o asunto *(SOLO LECTURA - Auto-aprobada)*

### 🌐 Páginas de Aterrizaje (Gestión Completa)
- `gophish_get_pages`: Obtener todas las páginas *(SOLO LECTURA - Auto-aprobada)*
- `gophish_create_page`: Crear nueva página *(ESCRITURA - Requiere aprobación manual)*
- `gophish_update_page`: Actualizar página existente *(ESCRITURA - Requiere aprobación manual)*
- `gophish_delete_page`: Eliminar página *(ESCRITURA - Requiere aprobación manual)*

### 📮 Perfiles SMTP (Gestión Completa)
- `gophish_get_smtp_profiles`: Obtener todos los perfiles SMTP *(SOLO LECTURA - Auto-aprobada)*
- `gophish_create_smtp_profile`: Crear nuevo perfil SMTP *(ESCRITURA - Requiere aprobación manual)*
- `gophish_update_smtp_profile`: Actualizar perfil SMTP existente *(ESCRITURA - Requiere aprobación manual)*
- `gophish_delete_smtp_profile`: Eliminar perfil SMTP *(ESCRITURA - Requiere aprobación manual)*

### 👤 Gestión de Usuarios
- `gophish_get_users`: Obtener todos los usuarios/administradores *(SOLO LECTURA - Auto-aprobada)*
- `gophish_create_user`: Crear nuevo usuario *(ESCRITURA - Requiere aprobación manual)*
- `gophish_update_user`: Actualizar usuario existente *(ESCRITURA - Requiere aprobación manual)*

### 📊 Análisis y Reportes Globales
- `gophish_get_system_status`: Obtener estado del sistema y estadísticas generales *(SOLO LECTURA - Auto-aprobada)*
- `gophish_get_global_analytics`: Obtener análisis global de todas las campañas *(SOLO LECTURA - Auto-aprobada)*

## Ejemplos de Uso

Una vez configurado, puedes usar comandos como:

### Gestión Básica
```
Muéstrame todas las campañas de Gophish
```

```
Crea una nueva campaña llamada "Test Campaign" usando la plantilla con ID 1
```

```
Actualiza la campaña con ID 5 para cambiar su nombre a "Updated Campaign"
```

### Análisis y Reportes
```
Muéstrame el análisis completo de la campaña con ID 3
```

```
Obtén las estadísticas globales de todas las campañas
```

```
Muéstrame los eventos de la campaña 2
```

### Búsqueda y Filtros
```
Busca campañas que contengan "phishing" en el nombre
```

```
Muéstrame todas las campañas activas
```

```
Obtén las campañas creadas en los últimos 7 días
```

### Gestión de Usuarios
```
Lista todos los usuarios del sistema
```

```
Crea un nuevo usuario administrador
```

### Búsqueda Avanzada
```
Busca plantillas que contengan "urgente" en el asunto
```

```
Encuentra grupos que contengan "marketing" en el nombre
```

## Seguridad

- El servidor desactiva la verificación SSL por defecto para desarrollo local
- Asegúrate de usar HTTPS en producción
- Mantén tu API key segura y no la compartas
- Todas las operaciones de escritura requieren autenticación válida

## Testing

### Ejecutar Tests
```bash
# Ejecutar todos los tests
python test.py all

# Ejecutar tests de solo lectura
python test.py readonly

# Ejecutar demo verbose
python test.py demo

# Ejecutar tests comprehensivos
python test.py comprehensive
```

### Requisitos para Testing
- Servidor GoPhish funcionando
- Credenciales válidas en `.env`
- Dependencias instaladas: `pip install -e .`

Ver `tests/README.md` para más detalles sobre testing.

## Utilidades

### Scripts de Utilidad
```bash
# Listar campañas
python utils/list_campaigns.py
```

## Desarrollo

Para desarrollo local:

```bash
# Instalar en modo desarrollo
pip install -e .

# Ejecutar el servidor directamente
python server.py

# Ejecutar tests
python test.py all
```