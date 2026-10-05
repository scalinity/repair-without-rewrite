"""Explicit, single-item development adapter for the pinned MLX source model.

This repairs FFT frame bounds only. Remaining 0.5.2 feature conventions are
deliberately retained; this identity does not assert NVIDIA/NeMo equivalence.
The installed package and its historical evidence are never modified.
"""
import contextlib
import math

RUNTIME_ID = "parakeet-mlx-0.5.2-frame-bound-v1-single-fp32-wave-bf16-weights"


def require_development_duration(samples, sample_rate):
    if sample_rate != 16000 or type(samples) is not int or not 32000 <= samples <= 192000:
        raise ValueError("qualified runtime requires 16 kHz and [2,12] seconds")


def frame_count(samples, n_fft, hop):
    if any(type(v) is not int or v <= 0 for v in (samples, n_fft, hop)):
        raise ValueError("positive integer geometry required")
    return (samples + 2 * (n_fft // 2) - n_fft) // hop + 1


def require_finite(value, stage):
    import mlx.core as mx
    if not bool(mx.all(mx.isfinite(value))):
        raise ValueError("nonfinite Parakeet " + stage)


def bounded_stft(x, n_fft, hop_length=None, win_length=None, window=None,
                 axis=-1, pad_mode="reflect"):
    import mlx.core as mx
    if x.ndim != 1 or axis != -1 or x.dtype != mx.float32:
        raise ValueError("qualified STFT requires one FP32 waveform")
    win_length = n_fft if win_length is None else win_length
    hop_length = n_fft // 4 if hop_length is None else hop_length
    if not 0 < win_length <= n_fft or pad_mode != "reflect" or x.size <= n_fft // 2:
        raise ValueError("outside qualified STFT geometry")
    require_finite(x, "waveform")
    window = mx.ones(win_length) if window is None else window
    window = mx.pad(window, [(0, n_fft - win_length)])
    half = n_fft // 2
    padded = mx.concatenate([x[1:half + 1][::-1], x, x[-half - 1:-1][::-1]])
    count = frame_count(x.size, n_fft, hop_length)
    if (count - 1) * hop_length + n_fft > padded.size:
        raise ValueError("FFT frame exceeds waveform storage")
    frames = mx.as_strided(padded, shape=(count, n_fft), strides=(hop_length, 1))
    spectrum = mx.fft.rfft(frames * window)
    require_finite(mx.view(spectrum, mx.float32), "FFT")
    return spectrum


@contextlib.contextmanager
def frame_bound_preprocessing():
    """Process-local intervention; isolated serial calls only."""
    import parakeet_mlx.audio as audio
    old = audio.stft
    audio.stft = bounded_stft
    try:
        yield
    finally:
        audio.stft = old


def transcribe_development(model, path):
    import mlx.core as mx
    from parakeet_mlx import DecodingConfig
    from parakeet_mlx.audio import load_audio, get_logmel
    from parakeet_mlx.alignment import sentences_to_result, tokens_to_sentences
    # Original loader uses ffmpeg PCM16 mono at the model sample rate. No crop.
    waveform = load_audio(path, model.preprocessor_config.sample_rate)
    require_development_duration(waveform.size, model.preprocessor_config.sample_rate)
    require_finite(waveform, "decoded waveform")
    with frame_bound_preprocessing():
        mel = get_logmel(waveform, model.preprocessor_config)
    require_finite(mel, "log-mel")
    features, lengths = model.encoder(mel)
    mx.eval(features, lengths)
    require_finite(features, "encoder")
    config = DecodingConfig()
    # Guard each joint decision before the upstream unchecked argmax can emit
    # an apparent transcription from NaN token/duration logits.
    joint = model.joint
    original_class = type(joint)

    class FiniteJoint(original_class):
        def __call__(self, *args, **kwargs):
            logits = super().__call__(*args, **kwargs)
            require_finite(logits, "joint logits")
            return logits

    joint.__class__ = FiniteJoint
    try:
        tokens, _ = model.decode(features, lengths, config=config)
    finally:
        joint.__class__ = original_class
    result = sentences_to_result(tokens_to_sentences(tokens[0], config.sentence))
    if any(not all(math.isfinite(v) for v in (t.confidence, t.start, t.duration))
           or t.duration < 0 for t in result.tokens):
        raise ValueError("nonfinite/invalid Parakeet alignment")
    return result
