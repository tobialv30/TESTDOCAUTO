#!/usr/bin/env python3
"""
Generador automático de documentación Salesforce usando Claude API
Push a GitHub → Análisis con Claude → Crear/Actualizar Confluence
"""

import os
import sys
import json
import requests
import base64
from pathlib import Path
import re
from typing import Dict, List, Optional

# Tu prompt EXACTO sin modificaciones
DOCUMENTATION_PROMPT = """Experto en Documentación Salesforce Integral
🎯 Tu Rol
Eres un Consultor Salesforce Senior especializado en crear documentación técnica clara, visual y completa que cualquier desarrollador o administrador pueda entender inmediatamente.

 

Expertise  
Documentacion V3 final.pdf 

Nubes Salesforce: Sales, Service, Marketing, Experience Cloud

Desarrollo: Flows, Apex, LWC, Aura, Visualforce

Integraciones: REST/SOAP APIs, MuleSoft, Middleware

Arquitectura: Metadata, Security, DevOps, Performance

Documentación: Confluence, Mermaid, Visual Design

🚀 Proceso de Documentación
PASO 1: Contexto Inicial
Pregunta de arranque:

"¿Esta documentación es para:

a) 📝 Nueva funcionalidad - Documentar desde cero b) 🔄 Actualización - Mejorar documentación existente
c) 📋 Auditoría - Documentar algo ya implementado sin docs d) 🔍 Análisis - Entender y explicar funcionalidad compleja"

PASO 2: Recolección de Componentes
Solicita específicamente estos elementos:

📦 METADATA SALESFORCE
[ ] Custom Objects (.object files o descripción completa)

[ ] Custom Fields (API names, tipos, validaciones)

[ ] Custom Metadata Types y Custom Settings

[ ] Permission Sets y Profiles (FLS, CRUD, configuraciones)

[ ] Named Credentials y External Data Sources

🔄 FLOWS & AUTOMATIZACIÓN
[ ] XML export del Flow O capturas de pantalla detalladas

[ ] Tipo de Flow (Record-Triggered, Screen, Scheduled, etc.)

[ ] Eventos disparadores y criterios de entrada

[ ] Variables y fórmulas utilizadas

[ ] Conexiones con otros procesos

💻 CÓDIGO APEX
[ ] Clases principales (.cls files)

[ ] Triggers (.trigger files)

[ ] Test Classes (.cls files) - Si no existen, los generaré

[ ] Utility Classes y Helper Methods

[ ] Exception Handling y Error Logging

⚡ LIGHTNING COMPONENTS
[ ] LWC: HTML, CSS, JS, XML files

[ ] Props, eventos, y lifecycle hooks

[ ] Interacción con Apex classes

[ ] Diseño responsive y accesibilidad

🔗 INTEGRACIONES
[ ] External APIs (endpoints, autenticación)

[ ] Data mapping entre sistemas

[ ] Error handling y retry logic

[ ] Monitoring y logging

PASO 3: Contexto de Negocio
Haz estas preguntas clave:

🎯 PROPÓSITO
¿Qué problema de negocio resuelve esta funcionalidad?

¿Quién la usa y cuándo?

¿Cuál es el ROI o impacto esperado?

🔄 FLUJO COMPLETO
¿Cuál es el journey completo del usuario?

¿Qué sistemas externos están involucrados?

¿Hay dependencias con otros módulos?

⚠️ CRITICIDAD
¿Qué pasa si esta funcionalidad falla?

¿Es crítica para operaciones diarias?

¿Hay procesos de rollback o contingencia?

PASO 4: Validación y Clarificación
Si algo no está claro, pregunta específicamente:

"¿Qué lógica de negocio maneja este paso del Flow?"

"¿Cómo se conecta [componente A] con [componente B]?"

"¿Qué validaciones aplicamos y por qué?"

"¿Esta integración es en tiempo real o batch?"

📋 Estructura del Documento
🔖 ENCABEZADO


# [Nombre de la Funcionalidad]
## 🎯 Presentación Ejecutiva
**¿Qué hace?** [Explicación en 2 líneas máximo]
**¿Para quién?** [Usuarios finales]  
**¿Por qué es importante?** [Valor de negocio]
**Versión Salesforce:** [Ej: Spring '25]
📊 INVENTARIO DE COMPONENTES
Tabla visual con criticidad por colores:

Componente

Tipo

Criticidad

Descripción

AccountFlow

Flow

🔴 Crítico

Automatiza creación de cuentas

LeadProcessor

Apex

🟡 Importante

Procesa leads entrantes

AccountCard

LWC

🟢 Informativo

Vista de tarjeta de cuenta

Leyenda:

🔴 Crítico: Afecta operaciones core del negocio

🟡 Importante: Impacta flujos de trabajo importantes

🟢 Informativo: Mejora experiencia de usuario

🏗️ ARQUITECTURA GENERAL


graph TB
    A[Usuario] -->|Accede| B[Lightning App]
    B -->|Ejecuta| C[Flow Principal]
    C -->|Llama| D[Apex Class]
    D -->|Integra| E[Sistema Externo]
    E -->|Responde| D
    D -->|Actualiza| F[Salesforce Records]
📦 OBJETOS Y METADATA
Para cada Custom Object:

📋 [Objeto_Name__c]
Propósito: [Por qué existe este objeto] Relaciones: [Con qué otros objetos se relaciona]

Campo

API Name

Tipo

Requerido

Propósito

Nombre

Name

Text(80)

✅

Identificador único

Estado

Status__c

Picklist

✅

Control de flujo

Validation Rules:

Rule_Name: [Qué valida y por qué es necesario]

🔄 FLOWS DETALLADOS
Para cada Flow:

⚡ [Flow Name]
Tipo: Record-Triggered Flow

Objeto: Account

Disparador: Before Save

Propósito: [Qué automatiza específicamente]

Diagrama de Flujo:



flowchart TD
    Start([Registro Creado]) --> Check{¿Cumple Criterios?}
    Check -->|Sí| Process[Procesar Datos]
    Check -->|No| End([Fin])
    Process --> Update[Actualizar Campos]
    Update --> Notify[Enviar Notificación]
    Notify --> End
Lógica Paso a Paso:

Criterios de Entrada: [Condiciones específicas]

Variables: [Qué se calcula y cómo]

Decisiones: [Lógica de branching]

Acciones: [Qué operaciones se ejecutan]

Manejo de Errores: [Qué pasa si algo falla]

Datos de Entrada:

recordId: ID del registro disparador

customField__c: [Descripción del campo]

Datos de Salida:

Campos actualizados: [Lista específica]

Registros creados: [Tipos y cantidades]

Notificaciones enviadas: [A quién y cuándo]

💻 CÓDIGO APEX
Para cada clase:

🏛️ [ClassName]
Propósito: [Qué problema resuelve] Patrón: [Singleton, Handler, Utility, etc.] Dependencies: [Qué otras clases usa]



public with sharing class AccountProcessor {
    /**
     * Procesa cuentas nuevas aplicando reglas de negocio
     * @param accounts Lista de cuentas a procesar
     * @return Map<Id, String> Resultados del procesamiento
     */
    public static Map<Id, String> processNewAccounts(List<Account> accounts) {
        // Implementación explicada paso a paso
    }
}
Métodos Principales:

processNewAccounts(): [Qué hace, cuándo se llama]

validateBusinessRules(): [Validaciones específicas]

handleExceptions(): [Cómo maneja errores]

Test Coverage:

Clase Test: AccountProcessor_Test

Coverage: 95%

Escenarios: [Lista de casos cubiertos]

⚡ LIGHTNING WEB COMPONENTS
Para cada LWC:

🎨 [componentName]
Propósito: [Qué interfaz proporciona] Ubicación: [Dónde se usa en Salesforce] Responsive: [Sí/No y consideraciones]

Estructura:



componentName/
├── componentName.html       // Template - UI Structure
├── componentName.js         // Logic - Event Handling  
├── componentName.css        // Styles - Visual Design
└── componentName.js-meta.xml // Config - Where it's used
Props y Eventos:

Prop/Event

Tipo

Descripción

Ejemplo

recordId

@api String

ID del registro actual

'0015000000XXXXX'

onSuccess

CustomEvent

Se dispara al guardar

{detail: {id: 'xxx'}}

Interacción con Apex:

Métodos llamados: [Lista de @AuraEnabled methods]

Datos intercambiados: [Qué se envía y recibe]

🔗 INTEGRACIONES
Para cada integración:

🌐 [Sistema Externo]
Propósito: [Qué datos sincroniza y por qué] Frecuencia: [Tiempo real, batch, scheduled] Criticidad: 🔴/🟡/🟢

Diagrama de Secuencia:



sequenceDiagram
    participant SF as Salesforce
    participant EXT as Sistema Externo
    SF->>SF: Trigger detecta cambio
    SF->>EXT: POST /api/endpoint
    EXT-->>SF: 200 OK + Data
    SF->>SF: Actualiza registros
    SF->>SF: Log resultado
Mapeo de Datos:

Campo SF

Campo Externo

Transformación

Requerido

Account.Name

company_name

Ninguna

✅

Account.Revenue__c

annual_revenue

String → Number

❌

Manejo de Errores:

Timeout: [Cómo se maneja]

Auth Failure: [Proceso de retry]

Invalid Data: [Validaciones aplicadas]

🔒 SEGURIDAD Y PERMISOS
Permission Sets Necesarios:
CustomApp_User: [Qué permisos incluye]

CustomApp_Admin: [Permisos adicionales]

Field Level Security:
Campo

Read

Edit

Justificación

Sensitive_Field__c

Admin Only

Admin Only

Datos financieros

⚠️ TROUBLESHOOTING
Problema

Síntomas

Causa Probable

Solución

Flow no ejecuta

Records no se actualizan

Criterios incorrectos

Revisar condiciones de entrada

Apex error

"Null pointer exception"

Falta validación

Agregar null checks

LWC no carga

Pantalla en blanco

Permisos faltantes

Asignar Permission Set

Debug y Logs:
Para Flows:



Setup → Debug Logs → New → Workflow and Flow = FINEST
Para Apex:



System.debug(LoggingLevel.INFO, '🔍 Processing: ' + recordId);
Para LWC:



console.log('🎨 Component loaded with recordId:', this.recordId);
📊 PIE DE DOCUMENTO
📌 Información del Documento
Versión: 1.0

Salesforce Release: Spring '25

Fecha Creación: [DD/MM/YYYY]

Última Actualización: [DD/MM/YYYY]

Próxima Revisión: [Fecha + 3 meses]

Elaborado por: [Team/Persona]

📝 Control de Cambios
Versión

Fecha

Autor

Cambios

1.0

[Fecha]

[Nombre]

Documentación inicial

Pregunta final: "¿Falta algún aspecto técnico o de negocio para que el equipo pueda mantener y evolucionar esta funcionalidad efectivamente?"

---

IMPORTANTE: Analiza TODOS los archivos del repositorio, identifica componentes Salesforce, y genera documentación COMPLETA siguiendo EXACTAMENTE esta estructura. Si existe documentación previa en Confluence, actualízala manteniendo historial. Si no existe, crea nueva página."""

class SalesforceDocumentationGenerator:
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.atlassian_email = os.getenv('ATLASSIAN_EMAIL')
        self.atlassian_api_token = os.getenv('ATLASSIAN_API_TOKEN')
        self.atlassian_base_url = os.getenv('ATLASSIAN_BASE_URL')
        self.confluence_space_key = os.getenv('CONFLUENCE_SPACE_KEY')
        
        if not all([self.anthropic_api_key, self.atlassian_email, 
                   self.atlassian_api_token, self.atlassian_base_url, 
                   self.confluence_space_key]):
            print("❌ ERROR: Variables de entorno faltantes")
            sys.exit(1)

    def analyze_salesforce_repository(self) -> Dict:
        """Analiza el repositorio y extrae información de componentes Salesforce"""
        salesforce_files = []
        repo_structure = {}
        
        # Patrones de archivos Salesforce
        patterns = {
            'apex_classes': '**/*.cls',
            'apex_triggers': '**/*.trigger',
            'flows': '**/*.flow-meta.xml',
            'lwc_html': '**/lwc/**/*.html',
            'lwc_js': '**/lwc/**/*.js',
            'lwc_css': '**/lwc/**/*.css',
            'objects': '**/*.object-meta.xml',
            'permission_sets': '**/*.permissionset-meta.xml',
            'custom_metadata': '**/*.md-meta.xml'
        }
        
        for component_type, pattern in patterns.items():
            files = list(Path('.').glob(pattern))
            if files:
                repo_structure[component_type] = []
                for file_path in files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        repo_structure[component_type].append({
                            'path': str(file_path),
                            'content': content[:5000]  # Limit content size
                        })
                    except Exception as e:
                        print(f"⚠️ Error leyendo {file_path}: {e}")
        
        return repo_structure

    def call_claude_api(self, repository_data: Dict) -> str:
        """Llama a Claude API para generar documentación"""
        
        # Construir contexto del repositorio
        repo_context = "CONTEXTO DEL REPOSITORIO SALESFORCE:\n\n"
        
        for component_type, files in repository_data.items():
            if files:
                repo_context += f"\n## {component_type.upper().replace('_', ' ')}\n"
                for file_info in files:
                    repo_context += f"\n### Archivo: {file_info['path']}\n"
                    repo_context += f"```\n{file_info['content']}\n```\n"
        
        # Prompt completo
        full_prompt = f"{repo_context}\n\n{DOCUMENTATION_PROMPT}"
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.anthropic_api_key,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': 'claude-3-5-sonnet-20240620',
            'max_tokens': 4000,
            'messages': [
                {
                    'role': 'user',
                    'content': full_prompt
                }
            ]
        }
        
        try:
            print("🤖 Llamando a Claude API...")
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['content'][0]['text']
            else:
                print(f"❌ Error en Claude API: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ Error llamando Claude API: {e}")
            return None

    def search_confluence_page(self, title: str) -> Optional[str]:
        """Busca si existe una página en Confluence con el título dado"""
        
        search_url = f"{self.atlassian_base_url}/rest/api/content"
        auth = (self.atlassian_email, self.atlassian_api_token)
        
        params = {
            'type': 'page',
            'spaceKey': self.confluence_space_key,
            'title': title,
            'expand': 'version'
        }
        
        try:
            response = requests.get(search_url, auth=auth, params=params)
            
            if response.status_code == 200:
                results = response.json()
                if results['results']:
                    page_id = results['results'][0]['id']
                    print(f"✅ Página existente encontrada: {title} (ID: {page_id})")
                    return page_id
                else:
                    print(f"ℹ️ No existe página con título: {title}")
                    return None
            else:
                print(f"⚠️ Error buscando página: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error en búsqueda Confluence: {e}")
            return None

    def create_confluence_page(self, title: str, content: str) -> bool:
        """Crea una nueva página en Confluence"""
        
        create_url = f"{self.atlassian_base_url}/rest/api/content"
        auth = (self.atlassian_email, self.atlassian_api_token)
        
        # Convertir markdown a Confluence storage format básico
        confluence_content = self.markdown_to_confluence_storage(content)
        
        payload = {
            'type': 'page',
            'title': title,
            'space': {'key': self.confluence_space_key},
            'body': {
                'storage': {
                    'value': confluence_content,
                    'representation': 'storage'
                }
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(
                create_url, 
                auth=auth, 
                headers=headers, 
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                page_id = result['id']
                page_url = f"{self.atlassian_base_url}/pages/viewpage.action?pageId={page_id}"
                print(f"✅ Nueva página creada: {title}")
                print(f"🔗 URL: {page_url}")
                return True
            else:
                print(f"❌ Error creando página: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Error creando página en Confluence: {e}")
            return False

    def update_confluence_page(self, page_id: str, title: str, content: str) -> bool:
        """Actualiza una página existente en Confluence"""
        
        # Primero obtener la versión actual
        get_url = f"{self.atlassian_base_url}/rest/api/content/{page_id}"
        auth = (self.atlassian_email, self.atlassian_api_token)
        
        params = {'expand': 'version'}
        
        try:
            response = requests.get(get_url, auth=auth, params=params)
            
            if response.status_code != 200:
                print(f"❌ Error obteniendo página: {response.status_code}")
                return False
            
            page_data = response.json()
            current_version = page_data['version']['number']
            
            # Actualizar página
            update_url = f"{self.atlassian_base_url}/rest/api/content/{page_id}"
            confluence_content = self.markdown_to_confluence_storage(content)
            
            payload = {
                'version': {'number': current_version + 1},
                'title': title,
                'type': 'page',
                'body': {
                    'storage': {
                        'value': confluence_content,
                        'representation': 'storage'
                    }
                }
            }
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.put(
                update_url, 
                auth=auth, 
                headers=headers, 
                json=payload
            )
            
            if response.status_code == 200:
                page_url = f"{self.atlassian_base_url}/pages/viewpage.action?pageId={page_id}"
                print(f"✅ Página actualizada: {title}")
                print(f"🔗 URL: {page_url}")
                print(f"📊 Versión: {current_version} → {current_version + 1}")
                return True
            else:
                print(f"❌ Error actualizando página: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Error actualizando página en Confluence: {e}")
            return False

    def markdown_to_confluence_storage(self, markdown_content: str) -> str:
        """Convierte markdown básico a Confluence Storage Format"""
        
        content = markdown_content
        
        # Headers
        content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        
        # Bold and italic
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        
        # Code blocks
        content = re.sub(
            r'```(\w+)?\n(.*?)\n```', 
            r'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">\1</ac:parameter><ac:plain-text-body><![CDATA[\2]]></ac:plain-text-body></ac:structured-macro>', 
            content, 
            flags=re.DOTALL
        )
        
        # Inline code
        content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
        
        # Lists (básico)
        content = re.sub(r'^- (.*?)$', r'<ul><li>\1</li></ul>', content, flags=re.MULTILINE)
        
        # Line breaks
        content = content.replace('\n', '<br/>')
        
        # Mermaid diagrams (Confluence macro)
        content = re.sub(
            r'```mermaid\n(.*?)\n```',
            r'<ac:structured-macro ac:name="mermaid"><ac:plain-text-body><![CDATA[\1]]></ac:plain-text-body></ac:structured-macro>',
            content,
            flags=re.DOTALL
        )
        
        return content

    def extract_title_from_documentation(self, content: str) -> str:
        """Extrae el título principal de la documentación generada"""
        
        # Buscar primer H1
        match = re.search(r'^# (.+?)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Fallback: usar información del repositorio
        repo_name = os.getenv('GITHUB_REPOSITORY', 'Salesforce Project')
        repo_name = repo_name.split('/')[-1] if '/' in repo_name else repo_name
        return f"Documentación Técnica - {repo_name}"

    def run(self):
        """Ejecuta el proceso completo de generación de documentación"""
        
        print("🚀 Iniciando generación automática de documentación Salesforce")
        print("=" * 60)
        
        # 1. Analizar repositorio
        print("\n📁 Paso 1: Analizando repositorio Salesforce...")
        repository_data = self.analyze_salesforce_repository()
        
        if not repository_data:
            print("⚠️ No se encontraron archivos Salesforce en el repositorio")
            return False
        
        print(f"✅ Encontrados {len(repository_data)} tipos de componentes")
        for component_type, files in repository_data.items():
            print(f"   - {component_type}: {len(files)} archivos")
        
        # 2. Generar documentación con Claude
        print("\n🤖 Paso 2: Generando documentación con Claude...")
        documentation = self.call_claude_api(repository_data)
        
        if not documentation:
            print("❌ Error generando documentación")
            return False
        
        print(f"✅ Documentación generada ({len(documentation)} caracteres)")
        
        # 3. Extraer título
        title = self.extract_title_from_documentation(documentation)
        print(f"📋 Título extraído: {title}")
        
        # 4. Buscar página existente
        print("\n🔍 Paso 3: Buscando página existente en Confluence...")
        existing_page_id = self.search_confluence_page(title)
        
        # 5. Crear o actualizar página
        print("\n📝 Paso 4: Publicando en Confluence...")
        
        if existing_page_id:
            success = self.update_confluence_page(existing_page_id, title, documentation)
        else:
            success = self.create_confluence_page(title, documentation)
        
        if success:
            print("\n🎉 ¡Proceso completado exitosamente!")
            print(f"📊 Confluence Space: {self.confluence_space_key}")
            print(f"📄 Página: {title}")
            return True
        else:
            print("\n❌ Error en el proceso de publicación")
            return False

if __name__ == "__main__":
    generator = SalesforceDocumentationGenerator()
    success = generator.run()
    sys.exit(0 if success else 1)