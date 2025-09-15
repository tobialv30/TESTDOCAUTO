#!/usr/bin/env python3
"""
Generador automático de documentación Salesforce usando Claude API
Push a GitHub → Análisis con Claude → Crear/Actualizar Confluence
Version 3.0 - Super Complete Documentation + Consistent Naming
"""

import os
import sys
import json
import requests
import base64
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple
import hashlib

# SUPER PROMPT COMPLETO - Basado en el original pero sin interacción
SUPER_DOCUMENTATION_PROMPT = """Eres un Consultor Salesforce Senior especializado en crear documentación técnica integral, visual y completa que cualquier desarrollador o administrador pueda entender inmediatamente.

🎯 CONTEXTO Y OBJETIVO
Analiza COMPLETAMENTE todos los componentes Salesforce proporcionados y genera documentación técnica DEFINITIVA y EXHAUSTIVA. NO hagas preguntas. NO solicites información adicional. Genera documentación completa basada ÚNICAMENTE en los archivos proporcionados, aplicando tu expertise en Salesforce para llenar cualquier gap con mejores prácticas estándar.

🏗️ ESTRUCTURA DE DOCUMENTACIÓN REQUERIDA

# [Nombre del Componente Principal]

## 🎯 Presentación Ejecutiva
**¿Qué hace?** [Explicación clara en 2 líneas máximo]
**¿Para quién?** [Usuarios finales específicos]  
**¿Por qué es importante?** [Valor de negocio concreto]
**Tipo de Componente:** [LWC/Apex/Flow/Object/etc.]
**Criticidad:** 🔴 Crítico / 🟡 Importante / 🟢 Informativo
**Versión Salesforce:** Spring '25 (o inferir del código)

## 📊 Inventario de Componentes
[Genera tabla visual con TODOS los archivos encontrados]

| Componente | Tipo | Criticidad | Propósito | Dependencias |
|------------|------|-----------|-----------|---------------|
| [Nombre] | [Tipo] | 🔴/🟡/🟢 | [Función específica] | [Lista componentes] |

**Leyenda:**
- 🔴 **Crítico:** Afecta operaciones core del negocio
- 🟡 **Importante:** Impacta flujos de trabajo importantes  
- 🟢 **Informativo:** Mejora experiencia de usuario

## 🏗️ Arquitectura General

```mermaid
graph TB
    A[Usuario] -->|Interactúa| B[Lightning App]
    B -->|Ejecuta| C[Componente Principal]
    C -->|Llama| D[Dependencias]
    D -->|Integra| E[Sistemas Externos]
    E -->|Responde| D
    D -->|Actualiza| F[Salesforce Records]
```

## 📦 Análisis Detallado de Componentes

### [Para CADA componente encontrado - NO omitas ninguno]

#### 📋 [Tipo_Componente - Nombre]
**📍 Ubicación:** `ruta/completa/del/archivo`
**🎯 Propósito:** [Función específica y detallada]
**🔗 Relaciones:** [Con qué otros componentes se relaciona]
**📊 Tamaño:** [Líneas de código/tamaño del archivo]

**📝 Análisis Línea por Línea:**
[Explica las partes más importantes del código, línea por línea]

**⚡ Funcionalidades Clave:**
- [Lista todas las funciones/métodos principales]
- [Explica qué hace cada uno]
- [Parámetros que recibe]
- [Qué devuelve]

**🔧 Configuración Técnica:**
- [Propiedades @api si es LWC]
- [Decoradores si es Apex]
- [Configuraciones XML]
- [Permisos requeridos]

**⚠️ Validaciones y Reglas:**
- [Validaciones implementadas]
- [Reglas de negocio aplicadas]
- [Manejo de errores]

## 🔄 Flujos y Procesos

### [Si hay Flows]
⚡ **[Nombre del Flow]**
- **Tipo:** [Record-Triggered/Screen/Scheduled/etc.]
- **Objeto:** [Objeto que dispara]
- **Disparador:** [Before/After Save/etc.]
- **Propósito:** [Qué automatiza específicamente]

**📋 Diagrama de Flujo:**
```mermaid
flowchart TD
    Start([Trigger Event]) --> Check{Criteria Met?}
    Check -->|Yes| Process[Process Records]
    Check -->|No| End([End])
    Process --> Update[Update Fields]
    Update --> Notify[Send Notifications]
    Notify --> End
```

**🔍 Lógica Detallada:**
1. **Criterios de Entrada:** [Condiciones específicas]
2. **Variables:** [Qué se calcula y cómo]
3. **Decisiones:** [Lógica de branching completa]
4. **Acciones:** [Operaciones ejecutadas paso a paso]
5. **Manejo de Errores:** [Qué pasa si algo falla]

## 💻 Código Apex Detallado

### [Para cada clase Apex]
🏛️ **[ClassName.cls]**
**🎯 Propósito:** [Qué problema resuelve específicamente]
**🏗️ Patrón de Diseño:** [Singleton/Handler/Utility/Controller/etc.]
**🔗 Dependencias:** [Otras clases que usa]

```apex
// Código completo con comentarios explicativos
[Incluir el código completo aquí con explicaciones]
```

**📊 Métodos Principales:**
- `methodName()`: [Descripción completa, parámetros, retorno]
- `anotherMethod()`: [Descripción completa, parámetros, retorno]

**🧪 Test Coverage:**
- **Clase Test:** [Nombre de la clase test]
- **Coverage:** [Porcentaje estimado]
- **Escenarios Cubiertos:** [Lista casos de prueba]

**🚨 Exception Handling:**
- [Cómo maneja errores]
- [Tipos de excepciones capturadas]
- [Logging implementado]

## ⚡ Lightning Web Components

### [Para cada LWC]
🎨 **[componentName]**
**🎯 Propósito:** [Qué interfaz proporciona exactamente]
**📍 Ubicación:** [Dónde se usa en Salesforce]
**📱 Responsive:** [Sí/No y consideraciones móviles]

**🏗️ Estructura de Archivos:**
```
componentName/
├── componentName.html       // UI Structure & Template
├── componentName.js         // Logic & Event Handling  
├── componentName.css        // Styling & Visual Design
└── componentName.js-meta.xml // Metadata & Configuration
```

**⚙️ Propiedades y Eventos:**

| Prop/Event | Tipo | Descripción | Ejemplo de Uso |
|------------|------|-------------|----------------|
| recordId | @api String | ID del registro actual | '0015000000XXXXX' |
| onSuccess | CustomEvent | Se dispara al guardar | {detail: {id: 'xxx'}} |

**🔄 Lifecycle Hooks:**
- `connectedCallback()`: [Qué inicializa]
- `disconnectedCallback()`: [Cleanup que hace]
- `renderedCallback()`: [Operaciones post-render]

**📡 Interacción con Apex:**
- **Métodos llamados:** [Lista de @AuraEnabled methods]
- **Datos intercambiados:** [Qué se envía y recibe]
- **Error Handling:** [Cómo maneja errores de Apex]

**🎨 Estilos CSS:**
[Analiza los estilos principales y su propósito]

## 🔗 Integraciones y APIs

### [Para cada integración]
🌐 **[Sistema Externo]**
**🎯 Propósito:** [Qué datos sincroniza y por qué exactamente]
**⏰ Frecuencia:** [Tiempo real/batch/scheduled con detalles]
**🚨 Criticidad:** 🔴/🟡/🟢

**📊 Diagrama de Secuencia:**
```mermaid
sequenceDiagram
    participant SF as Salesforce
    participant EXT as Sistema Externo
    SF->>SF: Trigger detecta cambio
    SF->>EXT: POST /api/endpoint
    EXT-->>SF: 200 OK + Data
    SF->>SF: Actualiza registros
    SF->>SF: Log resultado
```

**🗺️ Mapeo de Datos Completo:**

| Campo Salesforce | Campo Externo | Transformación | Requerido | Validación |
|------------------|---------------|----------------|-----------|------------|
| Account.Name | company_name | Ninguna | ✅ | Max 80 chars |
| Account.Revenue__c | annual_revenue | String → Decimal | ❌ | > 0 |

**🔧 Configuración Técnica:**
- **Endpoint:** [URL completa]
- **Autenticación:** [Método usado]
- **Headers:** [Headers requeridos]
- **Rate Limits:** [Limitaciones conocidas]

**⚠️ Manejo de Errores Completo:**
- **Timeout (30s):** [Proceso de retry automático]
- **Auth Failure:** [Reautenticación y reintentos]
- **Invalid Data:** [Validaciones aplicadas]
- **Network Issues:** [Fallback strategies]

## 🔒 Seguridad y Permisos

**👥 Permission Sets Requeridos:**
- **[PermissionSet_Name]**: [Descripción completa de permisos]
  - Object Permissions: [CRUD específicos]
  - Field Level Security: [Campos y niveles]
  - System Permissions: [APIs, features]
  - Custom Permissions: [Permissions customizados]

**🛡️ Field Level Security:**

| Campo | Read | Edit | Admin Only | Justificación |
|-------|------|------|------------|---------------|
| Sensitive_Field__c | Admin | Admin | ✅ | Datos financieros confidenciales |
| Status__c | All Users | Manager+ | ❌ | Control de workflow |

**🔐 Sharing y Visibility:**
- [OWD settings]
- [Sharing Rules aplicables]
- [Role hierarchy considerations]

## 📱 Experiencia de Usuario

**🎯 User Journey Completo:**
1. **Punto de Entrada:** [Cómo llega el usuario al componente]
2. **Interacciones:** [Pasos que realiza el usuario]
3. **Validaciones:** [Qué validaciones ve]
4. **Confirmaciones:** [Mensajes de éxito/error]
5. **Siguiente Paso:** [A dónde va después]

**📊 Casos de Uso Principales:**
- **Caso de Uso 1:** [Escenario detallado]
- **Caso de Uso 2:** [Escenario detallado]
- **Casos Edge:** [Situaciones límite]

## ⚠️ Troubleshooting y Mantenimiento

### 🔧 Problemas Comunes y Soluciones

| Problema | Síntomas | Causa Más Probable | Solución Paso a Paso | Prevention |
|----------|-----------|-------------------|---------------------|------------|
| Component no carga | Pantalla blanca | Permisos faltantes | 1. Verificar Permission Set<br/>2. Asignar al usuario<br/>3. Refrescar página | Documentar permisos requeridos |
| Flow no ejecuta | Records no se procesan | Criterios de entrada incorrectos | 1. Debug Flow Builder<br/>2. Verificar criterios<br/>3. Probar con record test | Usar naming conventions claros |

### 📊 Debug y Logging

**Para Flows:**
```
Setup → Debug Logs → New → Workflow and Flow = FINEST
Ejecutar proceso → Revisar logs → Buscar "FLOW_START"
```

**Para Apex:**
```apex
System.debug(LoggingLevel.INFO, 'Debug: Processing recordId: ' + recordId);
System.debug(LoggingLevel.ERROR, 'Error: ' + e.getMessage());
```

**Para LWC:**
```javascript
console.log('Component loaded:', this.recordId);
console.error('Error occurred:', error);
```

### 📈 Monitoreo y Performance

**🔍 Métricas Clave:**
- **Response Time:** [Tiempo esperado]
- **Error Rate:** [Tasa aceptable]
- **Usage Statistics:** [Cómo medir adoption]

**⚡ Optimizaciones Implementadas:**
- [Lista optimizaciones de performance]
- [Caching strategies]
- [Query optimizations]

## 🔄 DevOps y Deployment

**📦 Componentes a Deployar:**
```xml
<!-- Package.xml para deployment -->
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>[ComponentName]</members>
        <name>[ComponentType]</name>
    </types>
    <version>59.0</version>
</Package>
```

**🧪 Testing Strategy:**
1. **Unit Tests:** [Coverage mínimo 75%]
2. **Integration Tests:** [Pruebas end-to-end]
3. **UAT:** [User acceptance testing]

**🚀 Deployment Checklist:**
- [ ] Unit tests passing
- [ ] Permission sets updated
- [ ] Documentation updated
- [ ] Backup completed
- [ ] Rollback plan ready

## 📊 Información del Documento

**📋 Metadatos:**
- **Última Actualización:** [FECHA_ACTUAL]
- **Versión:** [VERSION]
- **Autor:** Generado automáticamente por Claude API
- **Próxima Revisión:** [FECHA_ACTUAL + 3 meses]

**📝 Componentes Documentados:**
[LISTA_COMPONENTES_DETALLADA]

**🔄 Historial de Cambios:**

| Versión | Fecha | Cambios Realizados | Impacto |
|---------|-------|-------------------|---------|
| 1.0 | [FECHA_ACTUAL] | Documentación inicial completa | N/A |

**🎯 Próximos Pasos Recomendados:**
1. [Implementar mejoras identificadas]
2. [Optimizaciones sugeridas]
3. [Funcionalidades adicionales]

---

**⚠️ IMPORTANTE PARA EL ANÁLISIS:**
Documenta CADA archivo encontrado, no omitas ningún componente. Si un archivo parece incompleto o tiene errores, documenta los issues encontrados y sugiere correcciones. Aplica tu conocimiento de Salesforce para inferir contexto cuando falte información específica."""

class SuperSalesforceDocumentationGenerator:
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
        """Analiza el repositorio y extrae información COMPLETA de componentes Salesforce"""
        repo_structure = {}
        
        # Patrones más completos de archivos Salesforce
        patterns = {
            'apex_classes': ['**/*.cls'],
            'apex_triggers': ['**/*.trigger'],
            'flows': ['**/*.flow-meta.xml'],
            'lwc_components': {
                'html': '**/lwc/**/*.html',
                'js': '**/lwc/**/*.js', 
                'css': '**/lwc/**/*.css',
                'xml': '**/lwc/**/*.js-meta.xml'
            },
            'aura_components': {
                'cmp': '**/aura/**/*.cmp',
                'js_controller': '**/aura/**/*Controller.js',
                'js_helper': '**/aura/**/*Helper.js',
                'css': '**/aura/**/*.css'
            },
            'visualforce': ['**/*.page', '**/*.component'],
            'objects': ['**/*.object-meta.xml'],
            'fields': ['**/*.field-meta.xml'],
            'permission_sets': ['**/*.permissionset-meta.xml'],
            'profiles': ['**/*.profile-meta.xml'],
            'custom_metadata': ['**/*.md-meta.xml'],
            'custom_labels': ['**/*.labels-meta.xml'],
            'static_resources': ['**/*.resource-meta.xml'],
            'email_templates': ['**/*.email-meta.xml'],
            'reports': ['**/*.report-meta.xml'],
            'dashboards': ['**/*.dashboard-meta.xml'],
            'workflow_rules': ['**/*.workflow-meta.xml'],
            'validation_rules': ['**/*.validation-meta.xml']
        }
        
        # Función para procesar archivos normales
        def process_files(pattern_list, component_type):
            files_found = []
            for pattern in pattern_list:
                for file_path in Path('.').glob(pattern):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        files_found.append({
                            'path': str(file_path),
                            'content': content,
                            'size': len(content),
                            'lines': len(content.splitlines())
                        })
                    except Exception as e:
                        print(f"⚠️ Error leyendo {file_path}: {e}")
            return files_found

        # Función para procesar componentes con subtipos (LWC, Aura)
        def process_component_files(component_patterns, component_type):
            components = {}
            for subtype, pattern in component_patterns.items():
                for file_path in Path('.').glob(pattern):
                    # Extraer nombre del componente del path
                    component_name = self.extract_component_name(file_path, component_type)
                    
                    if component_name not in components:
                        components[component_name] = {}
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        components[component_name][subtype] = {
                            'path': str(file_path),
                            'content': content,
                            'size': len(content),
                            'lines': len(content.splitlines())
                        }
                    except Exception as e:
                        print(f"⚠️ Error leyendo {file_path}: {e}")
            return components

        # Procesar cada tipo de componente
        for component_type, pattern_config in patterns.items():
            if isinstance(pattern_config, dict):
                # Componentes con subtipos (LWC, Aura)
                components = process_component_files(pattern_config, component_type)
                if components:
                    repo_structure[component_type] = components
            else:
                # Archivos simples
                files = process_files(pattern_config, component_type)
                if files:
                    repo_structure[component_type] = files
        
        return repo_structure

    def extract_component_name(self, file_path: Path, component_type: str) -> str:
        """Extrae el nombre del componente del path del archivo"""
        path_parts = Path(file_path).parts
        
        if component_type == 'lwc_components' and 'lwc' in path_parts:
            lwc_index = list(path_parts).index('lwc')
            if lwc_index + 1 < len(path_parts):
                return path_parts[lwc_index + 1]
        
        elif component_type == 'aura_components' and 'aura' in path_parts:
            aura_index = list(path_parts).index('aura')
            if aura_index + 1 < len(path_parts):
                return path_parts[aura_index + 1]
        
        # Fallback: usar nombre del archivo
        return Path(file_path).stem

    def generate_consistent_title(self, repository_data: Dict) -> str:
        """Genera un título consistente basado en el componente principal"""
        
        # Prioridad para identificar componente principal
        priority_components = [
            ('lwc_components', 'LWC'),
            ('apex_classes', 'Apex'),
            ('flows', 'Flow'),
            ('apex_triggers', 'Trigger'),
            ('aura_components', 'Aura'),
            ('objects', 'Object')
        ]
        
        for component_type, prefix in priority_components:
            if component_type in repository_data and repository_data[component_type]:
                
                if component_type in ['lwc_components', 'aura_components']:
                    # Para componentes con subtipos, tomar el primero
                    component_names = list(repository_data[component_type].keys())
                    if component_names:
                        main_component = component_names[0]
                        # FORMATO CONSISTENTE: [Tipo] [Nombre]
                        return f"{prefix} {main_component}"
                else:
                    # Para archivos simples
                    first_file = repository_data[component_type][0]
                    file_name = Path(first_file['path']).stem
                    # FORMATO CONSISTENTE: [Tipo] [Nombre]
                    return f"{prefix} {file_name}"
        
        # Fallback consistente
        return "Salesforce Documentation"

    def search_existing_documentation(self, title: str) -> Optional[str]:
        """Busca documentación existente con múltiples variaciones del título"""
        
        search_url = f"{self.atlassian_base_url}/rest/api/content/search"
        auth = (self.atlassian_email, self.atlassian_api_token)
        
        # Generar variaciones del título para buscar páginas existentes
        title_variations = self.generate_title_variations(title)
        
        print(f"🔍 Buscando páginas existentes para: {title}")
        print(f"   Variaciones a buscar: {title_variations}")
        
        for variation in title_variations:
            params = {
                'cql': f'space = "{self.confluence_space_key}" AND type = "page" AND title ~ "{variation}"',
                'limit': 50
            }
            
            try:
                response = requests.get(search_url, auth=auth, params=params)
                if response.status_code == 200:
                    results = response.json()
                    
                    # Buscar coincidencia exacta primero
                    for page in results.get('results', []):
                        if page['title'] == variation:
                            print(f"✅ Página existente encontrada (exacta): {page['title']} (ID: {page['id']})")
                            return page['id']
                    
                    # Si no hay exacta, buscar similar
                    for page in results.get('results', []):
                        page_title_clean = self.normalize_title(page['title'])
                        variation_clean = self.normalize_title(variation)
                        
                        if page_title_clean == variation_clean:
                            print(f"✅ Página existente encontrada (similar): {page['title']} (ID: {page['id']})")
                            return page['id']
                            
            except Exception as e:
                print(f"⚠️ Error buscando '{variation}': {e}")
        
        print(f"ℹ️ No se encontró documentación existente")
        return None

    def generate_title_variations(self, title: str) -> List[str]:
        """Genera todas las variaciones posibles del título para búsqueda"""
        
        # Extraer partes del título
        parts = title.split()
        if len(parts) < 2:
            return [title]
        
        component_type = parts[0]  # LWC, Apex, Flow, etc.
        component_name = parts[1]  # languageSelector, etc.
        
        variations = [
            title,  # "LWC languageSelector"
            f"{component_name}",  # "languageSelector"
            f"{component_name} ({component_type})",  # "languageSelector (LWC)"
            f"{component_type} - {component_name}",  # "LWC - languageSelector"
            f"{component_type}_{component_name}",  # "LWC_languageSelector"
            f"{component_name}_{component_type}",  # "languageSelector_LWC"
        ]
        
        return list(set(variations))  # Remover duplicados

    def normalize_title(self, title: str) -> str:
        """Normaliza títulos para comparación"""
        # Convertir a minúsculas, remover espacios extra, caracteres especiales
        normalized = title.lower().strip()
        normalized = re.sub(r'[^\w\s]', '', normalized)  # Remover caracteres especiales
        normalized = re.sub(r'\s+', ' ', normalized)  # Espacios únicos
        return normalized

    def call_claude_api(self, repository_data: Dict, main_component: str) -> str:
        """Llama a Claude API para generar documentación SUPER completa"""
        
        # Construir contexto del repositorio con TODOS los datos
        repo_context = f"REPOSITORIO SALESFORCE COMPLETO - COMPONENTE PRINCIPAL: {main_component}\n"
        repo_context += "=" * 100 + "\n\n"
        
        total_files = 0
        total_size = 0
        
        for component_type, data in repository_data.items():
            repo_context += f"\n{'#' * 50}\n"
            repo_context += f"## {component_type.upper().replace('_', ' ')}\n"
            repo_context += f"{'#' * 50}\n"
            
            if isinstance(data, dict) and any(isinstance(v, dict) for v in data.values()):
                # Componentes con subtipos (LWC, Aura)
                for component_name, files in data.items():
                    repo_context += f"\n### COMPONENTE: {component_name}\n"
                    for file_type, file_info in files.items():
                        repo_context += f"\n#### {file_type.upper()}: {file_info['path']} ({file_info['size']} chars, {file_info['lines']} lines)\n"
                        repo_context += f"```{self.get_file_extension(file_info['path'])}\n{file_info['content']}\n```\n"
                        total_files += 1
                        total_size += file_info['size']
            else:
                # Archivos simples
                for file_info in data:
                    repo_context += f"\n### ARCHIVO: {file_info['path']} ({file_info['size']} chars, {file_info['lines']} lines)\n"
                    repo_context += f"```{self.get_file_extension(file_info['path'])}\n{file_info['content']}\n```\n"
                    total_files += 1
                    total_size += file_info['size']
        
        repo_context += f"\n\n{'=' * 100}\n"
        repo_context += f"RESUMEN DEL ANÁLISIS:\n"
        repo_context += f"- TOTAL ARCHIVOS ANALIZADOS: {total_files}\n"
        repo_context += f"- TOTAL TAMAÑO CÓDIGO: {total_size:,} caracteres\n"
        repo_context += f"- COMPONENTE PRINCIPAL IDENTIFICADO: {main_component}\n"
        repo_context += f"- TIPOS DE COMPONENTES: {list(repository_data.keys())}\n"
        repo_context += f"{'=' * 100}\n\n"
        
        # Agregar contexto temporal
        from datetime import datetime
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Personalizar el super prompt
        contextualized_prompt = SUPER_DOCUMENTATION_PROMPT.replace('[FECHA_ACTUAL]', current_date)
        contextualized_prompt = contextualized_prompt.replace('[VERSION]', '1.0')
        componentes_lista = []
        for comp_type, data in repository_data.items():
            if isinstance(data, dict) and any(isinstance(v, dict) for v in data.values()):
                componentes_lista.extend([f"{comp_type}:{name}" for name in data.keys()])
            else:
                componentes_lista.append(f"{comp_type}:{len(data)} files")
        
        contextualized_prompt = contextualized_prompt.replace('[LISTA_COMPONENTES_DETALLADA]', ', '.join(componentes_lista))
        
        # Prompt completo
        full_prompt = f"{repo_context}\n\n{contextualized_prompt}"
        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.anthropic_api_key,
            'anthropic-version': '2023-06-01'
        }
        
        payload = {
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 4000,
            'messages': [
                {
                    'role': 'user',
                    'content': full_prompt
                }
            ]
        }
        
        try:
            print("🤖 Generando SUPER documentación con Claude API...")
            print(f"📊 Contexto enviado: {len(full_prompt):,} caracteres")
            print(f"📁 Archivos analizados: {total_files}")
            print(f"💾 Tamaño total código: {total_size:,} caracteres")
            
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=payload,
                timeout=180  # Más tiempo para documentación completa
            )
            
            if response.status_code == 200:
                result = response.json()
                documentation = result['content'][0]['text']
                print(f"✅ SUPER documentación generada: {len(documentation):,} caracteres")
                return documentation
            else:
                print(f"❌ Error en Claude API: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ Error llamando Claude API: {e}")
            return None

    def get_file_extension(self, file_path: str) -> str:
        """Obtiene la extensión del archivo para syntax highlighting"""
        extension_map = {
            '.cls': 'apex',
            '.trigger': 'apex', 
            '.js': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.xml': 'xml',
            '.cmp': 'xml',
            '.page': 'html',
            '.component': 'html'
        }
        
        suffix = Path(file_path).suffix
        return extension_map.get(suffix, 'text')

    def run(self):
        """Ejecuta el proceso completo de generación de SUPER documentación"""
        
        print("🚀 Iniciando generación de SUPER DOCUMENTACIÓN Salesforce v3.0")
        print("=" * 80)
        
        # 1. Análisis completo del repositorio
        print("\n📁 Paso 1: Análisis COMPLETO del repositorio Salesforce...")
        repository_data = self.analyze_salesforce_repository()
        
        if not repository_data:
            print("⚠️ No se encontraron archivos Salesforce en el repositorio")
            return False
        
        # 2. Generar título consistente
        print("\n🎯 Paso 2: Generando título CONSISTENTE...")
        consistent_title = self.generate_consistent_title(repository_data)
        print(f"✅ Título consistente: '{consistent_title}'")
        
        # Mostrar estadísticas
        total_files = 0
        for comp_type, data in repository_data.items():
            if isinstance(data, dict) and any(isinstance(v, dict) for v in data.values()):
                count = len(data)
                total_files += sum(len(files) for files in data.values())
                print(f"   - {comp_type}: {count} componentes")
            else:
                count = len(data)
                total_files += count
                print(f"   - {comp_type}: {count} archivos")
        
        print(f"📊 TOTAL: {total_files} archivos a documentar")
        
        # 3. Buscar documentación existente con múltiples variaciones
        print("\n🔍 Paso 3: Buscando documentación existente...")
        existing_page_id = self.search_existing_documentation(consistent_title)
        
        # 4. Generar SUPER documentación
        print("\n🤖 Paso 4: Generando SUPER documentación completa...")
        documentation = self.call_claude_api(repository_data, consistent_title)
        
        if not documentation:
            print("❌ Error generando documentación")
            return False
        
        # 5. Limpiar título de la documentación generada
        final_title = self.clean_documentation_title(documentation, consistent_title)
        print(f"📋 Título final: '{final_title}'")
        
        # 6. Crear o actualizar con título consistente
        print("\n📝 Paso 5: Publicando en Confluence...")
        
        if existing_page_id:
            success = self.update_confluence_page(existing_page_id, final_title, documentation)
            print("🔄 Documentación ACTUALIZADA")
        else:
            success = self.create_confluence_page(final_title, documentation)
            print("🆕 Nueva documentación CREADA")
        
        if success:
            print("\n🎉 ¡SUPER documentación completada exitosamente!")
            print(f"📊 Confluence Space: {self.confluence_space_key}")
            print(f"📄 Página: '{final_title}'")
            print(f"🎯 Componente Principal: {consistent_title}")
            print(f"📁 Total Archivos Documentados: {total_files}")
            return True
        else:
            print("\n❌ Error en el proceso de publicación")
            return False

    def clean_documentation_title(self, documentation: str, fallback_title: str) -> str:
        """Limpia y normaliza el título extraído de la documentación"""
        
        # Buscar primer H1 en la documentación
        match = re.search(r'^# (.+?)$', documentation, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # Limpiar emojis y caracteres especiales 
            title = re.sub(r'[🎯🏗️📦💻⚠️🔧📊🚀⚡🔒🔗🎨📊📱🔄🌐🔍]', '', title).strip()
            # Limpiar corchetes y contenido
            title = re.sub(r'\[.*?\]', '', title).strip()
            
            if title and len(title) > 3:  # Título válido
                return title
        
        # Usar título consistente como fallback
        return fallback_title

    # Resto de métodos (mantener los existentes)
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
            response = requests.post(create_url, auth=auth, headers=headers, json=payload)
            
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
            
            response = requests.put(update_url, auth=auth, headers=headers, json=payload)
            
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
        """Convierte markdown a Confluence Storage Format con mejor soporte"""
        
        content = markdown_content
        
        # Headers con mejor manejo
        content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        
        # Bold and italic
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        
        # Tables - mejor conversión
        content = self.convert_markdown_tables(content)
        
        # Code blocks con mejor manejo de lenguajes
        content = re.sub(
            r'```(\w+)?\n(.*?)\n```', 
            lambda m: f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{m.group(1) or "text"}</ac:parameter><ac:plain-text-body><![CDATA[{m.group(2)}]]></ac:plain-text-body></ac:structured-macro>', 
            content, 
            flags=re.DOTALL
        )
        
        # Inline code
        content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
        
        # Lists con mejor estructura
        content = self.convert_markdown_lists(content)
        
        # Mermaid diagrams
        content = re.sub(
            r'```mermaid\n(.*?)\n```',
            r'<ac:structured-macro ac:name="mermaid"><ac:plain-text-body><![CDATA[\1]]></ac:plain-text-body></ac:structured-macro>',
            content,
            flags=re.DOTALL
        )
        
        # Links
        content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', content)
        
        # Line breaks
        content = content.replace('\n', '<br/>')
        
        return content

    def convert_markdown_tables(self, content: str) -> str:
        """Convierte tablas markdown a formato Confluence"""
        
        def table_replacer(match):
            lines = match.group(0).strip().split('\n')
            if len(lines) < 2:
                return match.group(0)
            
            # Header
            headers = [cell.strip() for cell in lines[0].split('|')[1:-1]]
            
            # Skip separator line
            data_lines = lines[2:]
            
            table_html = '<table><thead><tr>'
            for header in headers:
                table_html += f'<th>{header}</th>'
            table_html += '</tr></thead><tbody>'
            
            for line in data_lines:
                if line.strip():
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    table_html += '<tr>'
                    for cell in cells:
                        table_html += f'<td>{cell}</td>'
                    table_html += '</tr>'
            
            table_html += '</tbody></table>'
            return table_html
        
        # Pattern para detectar tablas markdown
        table_pattern = r'\|.*?\|\n\|[-\s|:]+\|\n(?:\|.*?\|\n)+'
        content = re.sub(table_pattern, table_replacer, content, flags=re.MULTILINE)
        
        return content

    def convert_markdown_lists(self, content: str) -> str:
        """Convierte listas markdown a formato Confluence"""
        
        # Listas con bullets
        content = re.sub(r'^- (.*?)$', r'<ul><li>\1</li></ul>', content, flags=re.MULTILINE)
        
        # Listas numeradas  
        content = re.sub(r'^\d+\. (.*?)$', r'<ol><li>\1</li></ol>', content, flags=re.MULTILINE)
        
        # Consolidar listas consecutivas
        content = re.sub(r'</ul><br/><ul>', '', content)
        content = re.sub(r'</ol><br/><ol>', '', content)
        
        return content

if __name__ == "__main__":
    generator = SuperSalesforceDocumentationGenerator()
    success = generator.run()
    sys.exit(0 if success else 1)