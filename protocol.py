"""FunASR provider 内部协议定义。"""

from __future__ import annotations

from typing import Any, Protocol


class AdapterAudioConfigLike(Protocol):
    """adapter 音频采集配置协议。"""

    sample_rate: int
    channels: int
    device: str
    block_size: int
    queue_max_chunks: int


class AdapterConfigLike(Protocol):
    """FunASR provider 需要的 adapter 配置协议。"""

    audio: AdapterAudioConfigLike


class ASRProviderRegistryLike(Protocol):
    """asr_adapter provider registry 所需的最小协议。"""

    def register_provider(self, provider: Any, *, default: bool = False) -> None:
        """注册 provider。"""

        ...

    def unregister_provider(self, provider_name: str) -> None:
        """注销 provider。"""

        ...


__all__ = [
    "ASRProviderRegistryLike",
    "AdapterAudioConfigLike",
    "AdapterConfigLike",
]