from typing import Any
def main(plpy: Any) -> None:
    plan = plpy.plan("SELECT 'Hello World' as text")