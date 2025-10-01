# main.py - Sistema de Gestión de Inventario Empresarial (Refactorizado)
"""
Sistema completo de gestión de inventario con DearPyGUI.
Versión refactorizada con separación de responsabilidades:
- main.py: Solo inicialización y configuración
- *_manager.py: Lógica de negocio y interfaces específicas
"""

import dearpygui.dearpygui as dpg
import sys
import os
import logging
from datetime import datetime

# Importar módulos de gestión
# from modules.categorias_manager import CategoriasManager
# from modules.proveedores_manager import ProveedoresManager  
# from modules.productos_manager import ProductosManager
# from modules.movimientos_manager import MovimientosManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InventarioApp:
    """Aplicación principal del sistema de inventario empresarial"""
    
    def __init__(self):
        self.db_name = "inventario.db"
        
        try:
            # Inicializar managers con manejo de errores
            logger.info("🚀 Inicializando sistema de inventario...")
            
        except Exception as e:
            logger.error(f"❌ Error durante la inicialización: {e}")
            raise
    
    def _configure_callbacks(self):
        """Configurar callbacks entre módulos para mantener sincronización"""
        
    # ================================
    # EJECUCIÓN PRINCIPAL
    # ================================
    
    def ejecutar(self):
        """Ejecutar la aplicación"""

        # Configurar DearPyGUI
        dpg.setup_dearpygui()
        
        # Mostrar la aplicación primero
        dpg.show_viewport()
        
        try:
            # Cargar datos iniciales usando los managers DESPUÉS de mostrar la interfaz
            logger.info("🔄 Cargando datos iniciales...")
        except Exception as e:
            logger.error(f"⚠️ Error cargando datos iniciales: {e}")
            # Continuar con la aplicación aunque fallen los datos iniciales
        dpg.start_dearpygui()
        
        # Limpiar recursos al cerrar
        dpg.destroy_context()

def main():
    """Función principal"""
    try:
        app = InventarioApp()
        app.ejecutar()
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        if dpg.is_dearpygui_running():
            dpg.destroy_context()

if __name__ == "__main__":
    main()