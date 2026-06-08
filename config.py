"""Configuration for the local ASR adapter."""

from __future__ import annotations

from typing import ClassVar

from src.core.components.base.config import BaseConfig, Field, SectionBase, config_section


class AsrAdapterConfig(BaseConfig):
    """Runtime configuration for microphone ASR and local playback."""

    config_name: ClassVar[str] = "config"
    config_description: ClassVar[str] = "Configuration for the ASR adapter"

    @config_section("plugin", title="Plugin", tag="plugin")
    class PluginSection(SectionBase):
        enabled: bool = Field(
            default=True,
            description="Whether the ASR adapter is enabled.",
            label="Enabled",
            tag="plugin",
        )
        config_version: str = Field(
            default="1.0.0",
            description="Configuration file version.",
            label="Config Version",
            disabled=True,
            tag="general",
        )

    @config_section("bot", title="Speaker Identity", tag="user")
    class BotSection(SectionBase):
        bot_id: str = Field(
            default="local_asr_bot",
            description="Bot id used when writing outgoing messages into history.",
            label="Bot ID",
            tag="user",
        )
        bot_name: str = Field(
            default="MoFox",
            description="Bot display name used when writing outgoing messages into history.",
            label="Bot Name",
            tag="user",
        )
        speaker_id: str = Field(
            default="local_microphone",
            description="Speaker id used for recognized microphone input.",
            label="Speaker ID",
            tag="user",
        )
        speaker_name: str = Field(
            default="Local Microphone",
            description="Speaker display name used for recognized microphone input.",
            label="Speaker Name",
            tag="user",
        )

    @config_section("audio", title="Audio Capture", tag="performance")
    class AudioSection(SectionBase):
        sample_rate: int = Field(
            default=16000,
            description="Microphone sample rate.",
            label="Sample Rate",
            ge=8000,
            le=48000,
            tag="performance",
        )
        channels: int = Field(
            default=1,
            description="Input channel count. The adapter will convert to mono when needed.",
            label="Channels",
            ge=1,
            le=2,
            tag="performance",
        )
        device: str = Field(
            default="",
            description="sounddevice input device name or index. Leave empty for the system default input.",
            label="Input Device",
            tag="performance",
        )
        block_size: int = Field(
            default=8000,
            description="Samples per capture block.",
            label="Block Size",
            ge=160,
            le=16000,
            tag="performance",
        )
        queue_max_chunks: int = Field(
            default=80,
            description="Maximum buffered audio blocks before old chunks are dropped.",
            label="Queue Size",
            ge=1,
            le=200,
            tag="performance",
        )

    @config_section("activation", title="Activation", tag="performance")
    class ActivationSection(SectionBase):
        mode: str = Field(
            default="vad",
            description="Activation mode: vad, push_to_talk, toggle_key, or always_on.",
            label="Mode",
            input_type="select",
            choices=["vad", "push_to_talk", "toggle_key", "always_on"],
            tag="performance",
        )
        hotkey: str = Field(
            default="space",
            description="Hotkey used by push_to_talk or toggle_key modes.",
            label="Hotkey",
            tag="performance",
        )
        vad_threshold: float = Field(
            default=0.003,
            description="RMS threshold used by VAD activation. Set to 0 to disable the threshold.",
            label="VAD Threshold",
            ge=0.0,
            le=1.0,
            tag="performance",
        )
        toggle_initially_active: bool = Field(
            default=False,
            description="Whether toggle mode starts in the active state.",
            label="Toggle Starts Active",
            tag="performance",
        )
        preroll_ms: int = Field(
            default=500,
            description="Audio preroll kept before VAD activation to avoid clipping sentence starts.",
            label="Preroll (ms)",
            ge=0,
            le=2000,
            tag="performance",
        )

    @config_section("asr", title="Recognizer", tag="ai")
    class AsrSection(SectionBase):
        provider: str = Field(
            default="funasr",
            description="ASR provider name resolved through the provider registry.",
            label="ASR Provider",
            tag="ai",
        )

    @config_section("message", title="Message Injection", tag="text")
    class MessageSection(SectionBase):
        min_text_length: int = Field(
            default=2,
            description="Minimum recognized text length before submission.",
            label="Min Text Length",
            ge=1,
            le=100,
            tag="text",
        )
        commit_partial_results: bool = Field(
            default=False,
            description="Whether partial ASR results should also be submitted.",
            label="Commit Partials",
            tag="text",
        )
        partial_emit_interval: float = Field(
            default=1.0,
            description="Minimum interval between partial result submissions.",
            label="Partial Interval",
            ge=0.1,
            le=10.0,
            tag="text",
        )
        enable_quality_filter: bool = Field(
            default=False,
            description="Whether to filter obviously bad ASR text.",
            label="Quality Filter",
            tag="text",
        )
        enable_confidence_filter: bool = Field(
            default=True,
            description="Whether to filter recognized text using token confidence.",
            label="Confidence Filter",
            tag="text",
        )
        min_avg_confidence: float = Field(
            default=-0.6,
            description="Minimum average token confidence.",
            label="Min Avg Confidence",
            ge=-20.0,
            le=1.0,
            tag="text",
            depends_on="enable_confidence_filter",
            depends_value=True,
        )
        min_token_confidence: float = Field(
            default=-3.0,
            description="Minimum per-token confidence. -20 is effectively disabled.",
            label="Min Token Confidence",
            ge=-20.0,
            le=1.0,
            tag="text",
            depends_on="enable_confidence_filter",
            depends_value=True,
        )
        max_ascii_ratio: float = Field(
            default=0.2,
            description="Maximum ASCII letter ratio allowed by the quality filter.",
            label="Max ASCII Ratio",
            ge=0.0,
            le=1.0,
            tag="text",
            depends_on="enable_quality_filter",
            depends_value=True,
        )
        min_cjk_ratio: float = Field(
            default=0.65,
            description="Minimum CJK character ratio allowed by the quality filter.",
            label="Min CJK Ratio",
            ge=0.0,
            le=1.0,
            tag="text",
            depends_on="enable_quality_filter",
            depends_value=True,
        )
        min_common_cjk_ratio: float = Field(
            default=0.45,
            description="Minimum common CJK character ratio allowed by the quality filter.",
            label="Min Common CJK Ratio",
            ge=0.0,
            le=1.0,
            tag="text",
            depends_on="enable_quality_filter",
            depends_value=True,
        )
        inject_stream_platform: str = Field(
            default="",
            description="Optional target platform for direct stream injection, for example bilibili_live. If stream_id and group_id are blank, the runtime tries to auto-resolve the active target stream.",
            label="Inject Platform",
            tag="text",
        )
        inject_stream_id: str = Field(
            default="",
            description="Optional explicit target stream_id for direct stream injection.",
            label="Inject Stream ID",
            tag="text",
            depends_on="inject_stream_platform",
        )
        inject_stream_group_id: str = Field(
            default="",
            description="Optional target group or room id used to derive the injected stream when stream_id is omitted. Leave blank to auto-resolve from the active adapter when supported.",
            label="Inject Group ID",
            tag="text",
            depends_on="inject_stream_platform",
        )
        inject_stream_group_name: str = Field(
            default="",
            description="Optional display name used when creating a missing injected stream.",
            label="Inject Group Name",
            tag="text",
            depends_on="inject_stream_platform",
        )

    @config_section("playback", title="Playback", tag="performance")
    class PlaybackSection(SectionBase):
        enabled: bool = Field(
            default=True,
            description="Whether outgoing voice/TTS messages should be played locally.",
            label="Enable Playback",
            tag="performance",
        )
        output_device: str = Field(
            default="",
            description="sounddevice output device name or index. Leave empty for the system default output.",
            label="Output Device",
            tag="performance",
        )
        blocking: bool = Field(
            default=True,
            description="Whether local playback waits for each clip to finish before returning.",
            label="Blocking Playback",
            tag="performance",
        )
        duplicate_mono_to_stereo: bool = Field(
            default=True,
            description="Whether mono audio should be duplicated into stereo before playback.",
            label="Duplicate Mono To Stereo",
            tag="performance",
        )
        fallback_sample_rate: int = Field(
            default=24000,
            description="Fallback sample rate for raw PCM audio that is not packaged as WAV.",
            label="Fallback Sample Rate",
            ge=8000,
            le=48000,
            tag="performance",
        )

    plugin: PluginSection = Field(default_factory=PluginSection)
    bot: BotSection = Field(default_factory=BotSection)
    audio: AudioSection = Field(default_factory=AudioSection)
    activation: ActivationSection = Field(default_factory=ActivationSection)
    asr: AsrSection = Field(default_factory=AsrSection)
    message: MessageSection = Field(default_factory=MessageSection)
    playback: PlaybackSection = Field(default_factory=PlaybackSection)


__all__ = ["AsrAdapterConfig"]
