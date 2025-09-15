#!/usr/bin/env python3
"""
Script de testing para verificar configuración del sistema de documentación automática
"""

import os
import sys
import requests
import json
from pathlib import Path

def test_anthropic_api():
    """Testa conexión con Anthropic API"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY no configurado")
        return False
    
    if not api_key.startswith('sk-ant-'):
        print("❌ ANTHROPIC_API_KEY formato inválido (debe empezar con 'sk-ant-')")
        return False
    
    # Test simple API call
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01'
    }
    
    payload = {
        'model': 'claude-3-5-sonnet-20241022',
        'max_tokens': 10,
        'messages': [{'role': 'user', 'content': 'Hi'}]
    }
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Anthropic API: Conexión exitosa")
            return True
        else:
            print(f"❌ Anthropic API: Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Anthropic API: Error de conexión - {e}")
        return False

def test_confluence_api():
    """Testa conexión con Confluence API"""
    email = os.getenv('ATLASSIAN_EMAIL')
    token = os.getenv('ATLASSIAN_API_TOKEN')
    base_url = os.getenv('ATLASSIAN_BASE_URL')
    space_key = os.getenv('CONFLUENCE_SPACE_KEY')
    
    missing_vars = []
    if not email: missing_vars.append('ATLASSIAN_EMAIL')
    if not token: missing_vars.append('ATLASSIAN_API_TOKEN')
    if not base_url: missing_vars.append('ATLASSIAN_BASE_URL')
    if not space_key: missing_vars.append('CONFLUENCE_SPACE_KEY')
    
    if missing_vars:
        print(f"❌ Variables Atlassian faltantes: {', '.join(missing_vars)}")
        return False
    
    # Test API connection
    auth = (email, token)
    test_url = f"{base_url}/rest/api/space/{space_key}"
    
    try:
        response = requests.get(test_url, auth=auth, timeout=10)
        
        if response.status_code == 200:
            space_data = response.json()
            print(f"✅ Confluence API: Conexión exitosa")
            print(f"   📂 Space: {space_data.get('name', space_key)}")
            print(f"   🔗 URL: {base_url}")
            return True
        elif response.status_code == 401:
            print("❌ Confluence API: Credenciales inválidas")
            return False
        elif response.status_code == 404:
            print(f"❌ Confluence API: Space '{space_key}' no encontrado")
            return False
        else:
            print(f"❌ Confluence API: Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Confluence API: Error de conexión - {e}")
        return False

def test_salesforce_files():
    """Verifica presencia de archivos Salesforce en el repositorio"""
    
    patterns = {
        'Apex Classes': '**/*.cls',
        'Apex Triggers': '**/*.trigger',
        'Flows': '**/*.flow-meta.xml',
        'LWC HTML': '**/lwc/**/*.html',
        'LWC JavaScript': '**/lwc/**/*.js',
        'Objects': '**/*.object-meta.xml',
        'Permission Sets': '**/*.permissionset-meta.xml'
    }
    
    found_files = {}
    total_files = 0
    
    for file_type, pattern in patterns.items():
        files = list(Path('.').glob(pattern))
        found_files[file_type] = len(files)
        total_files += len(files)
    
    if total_files == 0:
        print("⚠️ No se encontraron archivos Salesforce en el repositorio")
        print("   Patrones buscados:")
        for file_type, pattern in patterns.items():
            print(f"   - {file_type}: {pattern}")
        return False
    
    print("✅ Archivos Salesforce encontrados:")
    for file_type, count in found_files.items():
        if count > 0:
            print(f"   📄 {file_type}: {count} archivos")
    
    print(f"   📊 Total: {total_files} archivos")
    return True

def test_github_context():
    """Verifica contexto de GitHub (si está disponible)"""
    
    github_vars = {
        'GITHUB_REPOSITORY': 'Repositorio',
        'GITHUB_SHA': 'Commit SHA', 
        'GITHUB_REF': 'Branch/Ref',
        'GITHUB_ACTOR': 'Actor'
    }
    
    github_context = {}
    for var, description in github_vars.items():
        value = os.getenv(var)
        if value:
            github_context[description] = value
    
    if github_context:
        print("✅ Contexto GitHub detectado:")
        for description, value in github_context.items():
            print(f"   📋 {description}: {value}")
        return True
    else:
        print("ℹ️ No hay contexto GitHub (ejecución local)")
        return True  # No es error

def test_file_structure():
    """Verifica estructura de archivos necesaria"""
    
    required_files = {
        'scripts/generate-documentation.py': 'Script principal',
        '.github/workflows/auto-documentation.yml': 'GitHub Workflow'
    }
    
    all_exist = True
    
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (no encontrado)")
            all_exist = False
    
    return all_exist

def create_sample_confluence_page():
    """Crea página de prueba en Confluence para verificar permisos"""
    
    email = os.getenv('ATLASSIAN_EMAIL')
    token = os.getenv('ATLASSIAN_API_TOKEN')
    base_url = os.getenv('ATLASSIAN_BASE_URL')
    space_key = os.getenv('CONFLUENCE_SPACE_KEY')
    
    if not all([email, token, base_url, space_key]):
        print("⚠️ No se puede crear página de prueba - variables faltantes")
        return False
    
    auth = (email, token)
    create_url = f"{base_url}/rest/api/content"
    
    test_content = """
    <h1>🧪 Página de Prueba - Sistema de Documentación Automática</h1>
    <p>Esta es una página de prueba generada para verificar permisos de escritura.</p>
    <p><strong>Timestamp:</strong> {timestamp}</p>
    <p><strong>Sistema:</strong> Auto-Documentation Test</p>
    <p>Si puedes ver esta página, el sistema tiene permisos correctos para crear y actualizar documentación.</p>
    """.format(timestamp=__import__('datetime').datetime.now().isoformat())
    
    payload = {
        'type': 'page',
        'title': '🧪 Test - Auto Documentation System',
        'space': {'key': space_key},
        'body': {
            'storage': {
                'value': test_content,
                'representation': 'storage'
            }
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(create_url, auth=auth, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            page_id = result['id']
            page_url = f"{base_url}/pages/viewpage.action?pageId={page_id}"
            print(f"✅ Página de prueba creada exitosamente")
            print(f"   🔗 URL: {page_url}")
            print(f"   📋 ID: {page_id}")
            return True
        else:
            print(f"❌ Error creando página de prueba: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error creando página de prueba: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    
    print("🧪 TESTING SISTEMA DE DOCUMENTACIÓN AUTOMÁTICA")
    print("=" * 60)
    
    tests = [
        ("📁 Estructura de archivos", test_file_structure),
        ("📄 Archivos Salesforce", test_salesforce_files),
        ("🤖 Anthropic API", test_anthropic_api),
        ("🏢 Confluence API", test_confluence_api),
        ("📋 Contexto GitHub", test_github_context),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en test: {e}")
            results.append(False)
    
    # Test opcional de creación de página
    print(f"\n🧪 Prueba de creación de página (opcional):")
    try:
        create_sample_confluence_page()
    except Exception as e:
        print(f"⚠️ No se pudo crear página de prueba: {e}")
    
    # Resumen
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 TODOS LOS TESTS PASARON ({passed}/{total})")
        print("\n✅ El sistema está listo para usar:")
        print("   1. Haz commit de tus cambios")
        print("   2. Push al repositorio")
        print("   3. Ve a GitHub Actions para ver el progreso")
        print("   4. Revisa la documentación en Confluence")
        return True
    else:
        print(f"⚠️ ALGUNOS TESTS FALLARON ({passed}/{total})")
        print("\n🔧 Acciones recomendadas:")
        if not results[0]:  # file structure
            print("   - Crear archivos faltantes del sistema")
        if not results[1]:  # salesforce files
            print("   - Verificar que el repositorio contenga código Salesforce")
        if not results[2]:  # anthropic api
            print("   - Configurar ANTHROPIC_API_KEY correctamente")
        if not results[3]:  # confluence api
            print("   - Verificar credenciales y permisos de Atlassian")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)