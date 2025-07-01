from abc import ABC, abstractmethod
from typing import Any, List, Dict


class BaseDatabase(ABC):
    """
    数据库操作基类，定义通用接口
    """
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql: str, params: Any = None) -> List[Dict]:
        pass

    @abstractmethod
    def close(self):
        pass
