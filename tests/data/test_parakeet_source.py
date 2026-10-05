import pytest
import numpy as np
import mlx.core as mx
from src.data.parakeet_source import frame_count, bounded_stft, require_finite, require_development_duration


def test_fft_frame_bounds_all_residues_and_short_long_inputs():
    for samples in (16000 + r for r in range(160)):
        count = frame_count(samples, 512, 160)
        assert (count - 1) * 160 + 512 <= samples + 512
        assert count * 160 + 512 > samples + 512
    assert frame_count(77520, 512, 160) == 485
    assert frame_count(53200, 512, 160) == 333
    for samples in (1, 256, 166560, 960000):
        assert frame_count(samples, 512, 160) == samples // 160 + 1


@pytest.mark.parametrize("values", [(0,512,160), (1,0,160), (1,512,0),
                                  (True,512,160), (1.0,512,160)])
def test_frame_geometry_rejects_invalid_control_values(values):
    with pytest.raises(ValueError):
        frame_count(*values)


def test_bound_repair_matches_independent_numpy_fft_and_strided_input():
    waveform = np.sin(np.arange(16080, dtype=np.float32) * .03)
    window = np.hanning(401)[:-1].astype(np.float32)
    padded = np.pad(waveform, (256, 256), mode="reflect")
    frames = np.lib.stride_tricks.sliding_window_view(padded, 512)[::160]
    expected = np.fft.rfft(frames * np.pad(window, (0,112)))
    actual = bounded_stft(mx.array(waveform), 512, 160, 400, mx.array(window))
    np.testing.assert_allclose(np.asarray(actual), expected, atol=1e-4, rtol=1e-4)
    backing = mx.array(np.repeat(waveform, 2))
    noncontiguous = mx.as_strided(backing, shape=(waveform.size,), strides=(2,))
    other = bounded_stft(noncontiguous, 512, 160, 400, mx.array(window))
    np.testing.assert_array_equal(np.asarray(actual), np.asarray(other))


def test_nonfinite_and_outside_runtime_inputs_reject_before_fft():
    with pytest.raises(ValueError, match="nonfinite"):
        require_finite(mx.array([float("nan")]), "injection fixture")
    with pytest.raises(ValueError):
        bounded_stft(mx.ones((2,1024)), 512, 160)
    with pytest.raises(ValueError):
        bounded_stft(mx.ones((256,)), 512, 160)
    with pytest.raises(ValueError):
        bounded_stft(mx.ones((1024,)).astype(mx.bfloat16), 512, 160)


def test_measured_duration_scope_rejects_unqualified_short_long_audio():
    for count in (32000, 192000):
        require_development_duration(count, 16000)
    for count, rate in ((31999,16000), (192001,16000), (64000,32000), (True,16000)):
        with pytest.raises(ValueError):
            require_development_duration(count, rate)
