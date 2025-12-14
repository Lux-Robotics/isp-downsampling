# isp-downsampling
test image and python scripts designed to test the ISP hardware downsampling behvaiour

Platform: RK3588 - Rockchip ISP 3 driver version: v02.09.00 - Debian Linux 6.1

Viewer used: https://github.com/IENT/YUView

- `1920x1200frame.nv12` - raw YUV full resolution greyscale ISP output
- `640x400frame.nv12` - 1/3 downsampled ISP output
- `python_avg640x400.nv12` - 1/3 downsampled Python script output using pixel averaging (low-pass filter + decimattion)
- `python_skip640x400.nv12` - 1/3 downsampled Python script output using pixel skipping (decimation)


- `nv12_downsample_avg.py` - YUV pixel averaging script
- `nv12_downsample_skip.py` - YUV pixel skipping script

example usage: `python nv12_downsample_skip.py input1920x1200.nv12 output640x400.nv12`

YUV image captured through V4L2 `--stream-to=frame.nv12`
