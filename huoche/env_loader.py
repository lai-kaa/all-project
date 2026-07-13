"""
.env 文件加载器（不依赖 python-decouple）。
优先读取 .env，不存在则回退 .env.example。
"""
from pathlib import Path
import os

# 视为“未配置”的占位符值
_PLACEHOLDERS = {
    '',
    'your-deepseek-api-key',
    'your-secret-key-here',
    'sk-xxx',
    'sk-your-key',
}


def load_dotenv(base_dir: Path) -> Path | None:
    """
    将 .env 或 .env.example 中的键值对写入 os.environ。
    已存在于 os.environ 的变量不会被覆盖。
    返回实际加载的文件路径。
    """
    for name in ('.env', '.env.example'):
        env_path = base_dir / name
        if not env_path.exists():
            continue

        with open(env_path, encoding='utf-8-sig') as env_file:
            for raw_line in env_file:
                line = raw_line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue

                key, _, value = line.partition('=')
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value

        return env_path

    return None


def get_env(key: str, default=None, cast=str):
    """从 os.environ 读取配置并类型转换"""
    value = os.environ.get(key)
    if value is None or value == '':
        value = default

    if cast is bool and isinstance(value, str):
        return value.lower() in ('true', '1', 'yes')

    if value is not None and cast is not str:
        return cast(value)

    return value


def is_configured(key: str) -> bool:
    """判断某项配置是否已填写（非空且非占位符）"""
    value = os.environ.get(key, '')
    return bool(value) and value.strip() not in _PLACEHOLDERS
