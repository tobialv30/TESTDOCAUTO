#!/usr/bin/env python3
"""
Generador automático de documentación Salesforce usando Claude API
Push a GitHub → Análisis con Claude → Crear/Actualizar Confluence
Version 2.0 - Fixed issues
"""

import os
import sys
import json
import requests
import base64
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple

# Prompt MODIFICADO para ser directo y no interactivo
DOCUMENTATION_PROMPT = """Eres un Consultor Salesforce Senior especializado en crear documentación técnica clara, visual y completa.

INSTRUCCIONES:
- Analiza TODOS los componentes Salesforce proporcionados
- Genera documentación COMPLETA y DEFINITIVA (no preguntas)
- Identifica el componente principal y úsalo como título
- Si hay múltiples componentes, documenta cada uno en secciones separadas
- Incluye diagramas Mermaid cuando sea apropiado
- Asume contexto típico de Salesforce cuando falte información específica

ESTRUCTURA REQUERIDA:

# [Nombre del Componente Principal]

## 🎯 Resumen Ejecutivo
**¿Qué hace?** [Explicación clara en 2 líneas]
**Tipo:** [LWC/Apex/Flow/etc.]
**Criticidad:** 🔴/🟡/🟢

## 🏗️ Arquitectura y Diseño

```mermaid
graph TB
    A[Usuario] --> B[Componente Principal]
    B --> C[Dependencias]
```

## 📦 Componentes Técnicos

### [Para cada componente encontrado]
**Archivo:** `nombreArchivo.ext`
**Propósito:** [Función específica]
**Dependencias:** [Otros componentes que usa]

## 💻 Implementación

[Código principal con explicaciones línea por línea]

## ⚠️ Consideraciones y Limitaciones

- [Limitaciones conocidas]
- [Dependencias críticas]
- [Posibles puntos de falla]

## 🔧 Mantenimiento y Troubleshooting

### Problemas Comunes
- **Problema:** [Descripción]
- **Causa:** [Por qué ocurre]  
- **Solución:** [Cómo solucionarlo]

## 📊 Información del Documento
- **Última actualización:** [FECHA_ACTUAL]
- **Versión:** [VERSION]
- **Componentes analizados:** [LISTA_COMPONENTES]

---

IMPORTANTE: 
- NO hagas preguntas
- NO solicites información adicional  
- Genera documentación completa basada SOLO en los archivos proporcionados
- Si falta contexto, haz suposiciones razonables basadas en mejores prácticas de Salesforce"""

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
        """Analiza el repositorio y extrae información COMPLETA de componentes Salesforce"""
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
            'lwc_xml': '**/lwc/**/*.js-meta.xml',  # AÑADIDO: metadata de LWC
            'objects': '**/*.object-meta.xml',
            'permission_sets': '**/*.permissionset-meta.xml',
            'custom_metadata': '**/*.md-meta.xml',
            'custom_labels': '**/*.labels-meta.xml',  # AÑADIDO: labels
            'static_resources': '**/*.resource-meta.xml'  # AÑADIDO: static resources
        }
        
        for component_type, pattern in patterns.items():
            files = list(Path('.').glob(pattern))
            if files:
                repo_structure[component_type] = []
                for file_path in files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()  # CAMBIO: Lee archivo completo
                        repo_structure[component_type].append({
                            'path': str(file_path),
                            'content': content,
                            'size': len(content)
                        })
                    except Exception as e:
                        print(f"⚠️ Error leyendo {file_path}: {e}")
        
        return repo_structure

    def identify_main_component(self, repository_data: Dict) -> str:
        """Identifica el componente principal para usar como título"""
        
        # Prioridad de tipos de componentes
        component_priority = [
            'lwc_js',        # Lightning Web Components (más específicos)
            'apex_classes',  # Apex Classes
            'flows',         # Flows
            'apex_triggers', # Triggers
            'objects'        # Custom Objects
        ]
        
        for component_type in component_priority:
            if component_type in repository_data and repository_data[component_type]:
                files = repository_data[component_type]
                
                # Para LWC, extraer nombre del componente
                if component_type == 'lwc_js':
                    for file_info in files:
                        path_parts = Path(file_info['path']).parts
                        if 'lwc' in path_parts:
                            lwc_index = list(path_parts).index('lwc')
                            if lwc_index + 1 < len(path_parts):
                                component_name = path_parts[lwc_index + 1]
                                return f"LWC - {component_name}"
                
                # Para otros tipos, usar nombre de archivo
                first_file = files[0]
                file_name = Path(first_file['path']).stem
                component_type_name = component_type.replace('_', ' ').title()
                return f"{component_type_name} - {file_name}"
        
        # Fallback
        return "Salesforce Components Documentation"

    def search_component_specific_pages(self, component_name: str) -> List[str]:
        """Busca páginas existentes relacionadas con el componente específico"""
        
        search_url = f"{self.atlassian_base_url}/rest/api/content/search"
        auth = (self.atlassian_email, self.atlassian_api_token)
        
        # Buscar páginas con términos relacionados al componente
        search_terms = [
            component_name,
            component_name.replace('-', ' '),
            component_name.split('-')[-1] if '-' in component_name else component_name
        ]
        
        existing_pages = []
        
        for term in search_terms:
            params = {
                'cql': f'space = "{self.confluence_space_key}" AND type = "page" AND title ~ "{term}"',
                'limit': 10
            }
            
            try:
                response = requests.get(search_url, auth=auth, params=params)
                if response.status_code == 200:
                    results = response.json()
                    for page in results.get('results', []):
                        existing_pages.append({
                            'id': page['id'],
                            'title': page['title'],
                            'url': f"{self.atlassian_base_url}{page['_links']['webui']}"
                        })
            except Exception as e:
                print(f"⚠️ Error buscando páginas para '{term}': {e}")
        
        return existing_pages

    def call_claude_api(self, repository_data: Dict, main_component: str) -> str:
        """Llama a Claude API para generar documentación"""
        
        # Construir contexto del repositorio con TODOS los datos
        repo_context = f"REPOSITORIO SALESFORCE - COMPONENTE PRINCIPAL: {main_component}\n\n"
        
        total_files = 0
        for component_type, files in repository_data.items():
            if files:
                repo_context += f"\n## {component_type.upper().replace('_', ' ')}\n"
                for file_info in files:
                    repo_context += f"\n### 📄 {file_info['path']} ({file_info['size']} chars)\n"
                    repo_context += f"```\n{file_info['content']}\n```\n"
                    total_files += 1
        
        repo_context += f"\n\nTOTAL ARCHIVOS ANALIZADOS: {total_files}\n"
        repo_context += f"COMPONENTE PRINCIPAL IDENTIFICADO: {main_component}\n"
        
        # Agregar contexto de fecha y versión
        from datetime import datetime
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Prompt personalizado con contexto
        contextualized_prompt = DOCUMENTATION_PROMPT.replace('[FECHA_ACTUAL]', current_date)
        contextualized_prompt = contextualized_prompt.replace('[VERSION]', '1.0')
        contextualized_prompt = contextualized_prompt.replace('[LISTA_COMPONENTES]', str(list(repository_data.keys())))
        
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
            print("🤖 Llamando a Claude API...")
            print(f"📊 Contexto enviado: {len(full_prompt)} caracteres")
            print(f"📁 Archivos analizados: {total_files}")
            
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                documentation = result['content'][0]['text']
                print(f"✅ Documentación generada: {len(documentation)} caracteres")
                return documentation
            else:
                print(f"❌ Error en Claude API: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ Error llamando Claude API: {e}")
            return None

    def extract_title_from_documentation(self, content: str, main_component: str) -> str:
        """Extrae el título de la documentación o usa el componente principal"""
        
        # Buscar primer H1
        match = re.search(r'^# (.+?)$', content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # Limpiar emojis y caracteres especiales para Confluence
            title = re.sub(r'[🎯🏗️📦💻⚠️🔧📊]', '', title).strip()
            return title
        
        # Usar componente principal identificado
        return main_component

    def run(self):
        """Ejecuta el proceso completo de generación de documentación"""
        
        print("🚀 Iniciando generación automática de documentación Salesforce v2.0")
        print("=" * 70)
        
        # 1. Analizar repositorio
        print("\n📁 Paso 1: Analizando repositorio Salesforce...")
        repository_data = self.analyze_salesforce_repository()
        
        if not repository_data:
            print("⚠️ No se encontraron archivos Salesforce en el repositorio")
            return False
        
        # 2. Identificar componente principal
        print("\n🎯 Paso 2: Identificando componente principal...")
        main_component = self.identify_main_component(repository_data)
        print(f"✅ Componente principal: {main_component}")
        
        print(f"📊 Archivos encontrados:")
        for component_type, files in repository_data.items():
            print(f"   - {component_type}: {len(files)} archivos")
        
        # 3. Buscar documentación existente específica
        print("\n🔍 Paso 3: Buscando documentación existente...")
        existing_pages = self.search_component_specific_pages(main_component)
        
        if existing_pages:
            print(f"📄 Páginas relacionadas encontradas:")
            for page in existing_pages:
                print(f"   - {page['title']} (ID: {page['id']})")
        else:
            print("ℹ️ No se encontró documentación existente específica")
        
        # 4. Generar documentación con Claude
        print("\n🤖 Paso 4: Generando documentación con Claude...")
        documentation = self.call_claude_api(repository_data, main_component)
        
        if not documentation:
            print("❌ Error generando documentación")
            return False
        
        # 5. Extraer título final
        final_title = self.extract_title_from_documentation(documentation, main_component)
        print(f"📋 Título final: {final_title}")
        
        # 6. Decidir crear o actualizar
        print("\n📝 Paso 5: Publicando en Confluence...")
        
        # Buscar página específica con el título exacto
        specific_page_id = self.search_confluence_page(final_title)
        
        if specific_page_id:
            success = self.update_confluence_page(specific_page_id, final_title, documentation)
            print("🔄 Página actualizada")
        else:
            success = self.create_confluence_page(final_title, documentation)
            print("🆕 Nueva página creada")
        
        if success:
            print("\n🎉 ¡Proceso completado exitosamente!")
            print(f"📊 Confluence Space: {self.confluence_space_key}")
            print(f"📄 Página: {final_title}")
            print(f"🎯 Componente: {main_component}")
            return True
        else:
            print("\n❌ Error en el proceso de publicación")
            return False

    # ... resto de métodos sin cambios (search_confluence_page, create_confluence_page, etc.)
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

if __name__ == "__main__":
    generator = SalesforceDocumentationGenerator()
    success = generator.run()
    sys.exit(0 if success else 1)