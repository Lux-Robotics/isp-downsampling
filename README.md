# isp-downsampling
test image and python scripts designed to test the ISP hardware downsampling behvaiour

Platform: RK3588 - Debian Linux 6.1

Viewer used: https://github.com/IENT/YUView

- `1920x1200frame.nv12` - raw YUV full resolution greyscale ISP output
- `640x400frame.nv12` - 1/3 downsampled ISP output
- `python_avg640x400.nv12` - 1/3 downsampled Python script output using pixel averaging
- `python_skip640x400.nv12` - 1/3 downsampled Python script output using pixel skipping (decimation)
