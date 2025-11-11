#!/usr/bin/env python3
"""
Script para listar campañas de Gophish
"""
import os
import json
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client import GophishClient

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get configuration from environment variables
GOPHISH_URL = os.getenv("GOPHISH_URL", "https://localhost:3333")
GOPHISH_API_KEY = os.getenv("GOPHISH_API_KEY")

if not GOPHISH_API_KEY:
    print("❌ Error: GOPHISH_API_KEY no está configurada")
    print("   Configura las variables de entorno o crea un archivo .env")
    exit(1)

def main():
    print("Conectando a Gophish...")
    client = GophishClient(GOPHISH_URL, GOPHISH_API_KEY)
    
    print("Obteniendo campañas...\n")
    campaigns = client.get_campaigns()
    
    print(f"Total de campañas: {len(campaigns)}\n")
    
    # Ordenar por ID (la más reciente suele tener el ID más alto)
    campaigns_sorted = sorted(campaigns, key=lambda x: x.get('id', 0), reverse=True)
    
    print("=" * 80)
    print("ÚLTIMA CAMPAÑA")
    print("=" * 80)
    
    if campaigns_sorted:
        latest = campaigns_sorted[0]
        print(f"\nID: {latest.get('id')}")
        print(f"Nombre: {latest.get('name')}")
        print(f"Estado: {latest.get('status')}")
        print(f"Fecha de creación: {latest.get('created_date')}")
        print(f"Fecha de lanzamiento: {latest.get('launch_date')}")
        
        if latest.get('template'):
            print(f"Plantilla: {latest['template'].get('name', 'N/A')}")
        
        if latest.get('page'):
            print(f"Página: {latest['page'].get('name', 'N/A')}")
        
        if latest.get('smtp'):
            print(f"SMTP: {latest['smtp'].get('name', 'N/A')}")
        
        if latest.get('results'):
            print(f"\nResultados:")
            print(f"  Total de objetivos: {len(latest['results'])}")
            
            # Contar estados
            statuses = {}
            for result in latest['results']:
                status = result.get('status', 'Unknown')
                statuses[status] = statuses.get(status, 0) + 1
            
            for status, count in statuses.items():
                print(f"  - {status}: {count}")
        
        print("\n" + "=" * 80)
        print("\nÚLTIMAS 10 CAMPAÑAS:")
        print("=" * 80)
        
        for i, campaign in enumerate(campaigns_sorted[:10], 1):
            print(f"\n{i}. ID: {campaign.get('id')} - {campaign.get('name')}")
            print(f"   Estado: {campaign.get('status')} | Creada: {campaign.get('created_date')}")
    else:
        print("No se encontraron campañas")

if __name__ == "__main__":
    main()
