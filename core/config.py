"""
===========================================================
PRT Labs - Core / Config
Class: ConfigManager

Description:
    Gerenciador de configurações persistentes do PRT Nexus.
    Salva e carrega preferências em formato JSON (config.json).
===========================================================
"""

import os
import json
from typing import Any, Dict


class ConfigManager:
    """Gerenciador Singleton de Configurações do App."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        # Diretório raiz para salvar as configs
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(base_dir, "config.json")

        # Configurações Padrão
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "PRT_Nexus")
        
        self.default_config: Dict[str, Any] = {
            "download_directory": default_download_dir,
            "max_concurrent_downloads": 3,
            "auto_extract_audio": False,
            "theme": "dark",
            "keep_history": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Carrega do disco ou gera o arquivo padrão se não existir."""
        if not os.path.exists(self.config_file):
            self.save_config(self.default_config)
            return self.default_config.copy()

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Garante que chaves novas criadas no futuro existam no dict final
                merged = self.default_config.copy()
                merged.update(data)
                return merged
        except Exception as e:
            print(f"[Config] Erro ao ler config.json: {e}. Restaurando padrão.")
            return self.default_config.copy()

    def save_config(self, new_config: Dict[str, Any] = None) -> None:
        """Salva as configurações atuais no arquivo JSON."""
        if new_config:
            self.config.update(new_config)

        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[Config] Erro ao salvar config.json: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Obtém um valor da configuração."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Define um valor e salva no disco automaticamente."""
        self.config[key] = value
        self.save_config()


# Instância global Singleton
config_manager = ConfigManager()