from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	# Aqui eu centralizo as configuracoes para nao espalhar valores fixos pelo projeto
	app_name: str = "Vetline API"
	api_prefix: str = "/api/v1"
	database_url: str = "sqlite:///./vetline.db"

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)


settings = Settings()
