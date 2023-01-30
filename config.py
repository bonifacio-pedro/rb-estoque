from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="RB",
    settings_files=['settings.toml', '.secrets.toml'],
)
