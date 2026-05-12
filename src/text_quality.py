"""FunASR provider 内部文本质量过滤。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TextQualityDecision:
    """文本质量判断结果。"""

    accepted: bool
    reason: str = ""


def is_obviously_invalid_asr_text(text: str, *, min_chars: int = 2) -> TextQualityDecision:
    """判断 ASR 文本是否明显无效。"""

    normalized = "".join(ch for ch in text.strip() if not ch.isspace())
    if len(normalized) < min_chars:
        return TextQualityDecision(True, "too_short")

    content_chars = [ch for ch in normalized if not _is_punctuation(ch)]
    if len(content_chars) < min_chars:
        return TextQualityDecision(True, "punctuation_only")

    if _has_excessive_repetition(list(normalized)):
        return TextQualityDecision(True, "excessive_repetition")

    cjk_count = sum(1 for ch in content_chars if _is_cjk(ch))
    ascii_letters = sum(1 for ch in content_chars if ch.isascii() and ch.isalpha())
    if cjk_count == 0 and ascii_letters == 0:
        return TextQualityDecision(True, "no_language_chars")

    return TextQualityDecision(False)


def _is_cjk(ch: str) -> bool:
    """判断字符是否为常用 CJK 统一表意文字。"""

    return "\u4e00" <= ch <= "\u9fff"


def _is_punctuation(ch: str) -> bool:
    """判断字符是否为常见中英文标点。"""

    return ch in "，。！？、；：,.!?;:()（）[]【】'\"“”‘’《》<>-—_~`!@#$%^&*+=|\\/"


def _has_excessive_repetition(chars: list[str]) -> bool:
    """检测明显异常的重复字符。"""

    if len(chars) < 5:
        return False
    previous = ""
    run = 0
    for ch in chars:
        if ch == previous:
            run += 1
            if run >= 4:
                return True
        else:
            previous = ch
            run = 1
    return False


__all__ = ["TextQualityDecision", "is_obviously_invalid_asr_text"]