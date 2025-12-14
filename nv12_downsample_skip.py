#!/usr/bin/env python3
import sys
import numpy as np

IN_W, IN_H = 1920, 1200
OUT_W, OUT_H = 640, 400
FX = IN_W // OUT_W   # 3
FY = IN_H // OUT_H   # 3

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_nv12.raw output_nv12.raw")
        sys.exit(2)

    in_path, out_path = sys.argv[1], sys.argv[2]

    in_frame_size = IN_W * IN_H * 3 // 2
    out_frame_size = OUT_W * OUT_H * 3 // 2

    data = np.fromfile(in_path, dtype=np.uint8)
    if data.size != in_frame_size:
        raise SystemExit(
            f"Expected {in_frame_size} bytes for one {IN_W}x{IN_H} NV12 frame, got {data.size} bytes."
        )

    y_size = IN_W * IN_H
    y = data[:y_size].reshape((IN_H, IN_W))

    # NV12 UV plane: H/2 rows, W bytes per row (interleaved U,V)
    uv = data[y_size:].reshape((IN_H // 2, IN_W))

    # --- Downsample Y by skipping ---
    y_out = y[0:IN_H:FY, 0:IN_W:FX]  # (OUT_H, OUT_W)

    # --- Downsample UV by skipping in chroma-sample domain ---
    # Interpret UV as (H/2, W/2, 2) chroma samples
    uv_samples = uv.reshape((IN_H // 2, IN_W // 2, 2))  # (600, 960, 2)

    # Need output chroma samples: (OUT_H/2, OUT_W/2, 2) = (200, 320, 2)
    uv_out_samples = uv_samples[0:(IN_H//2):FY, 0:(IN_W//2):FX, :]  # (200, 320, 2)

    uv_out = uv_out_samples.reshape((OUT_H // 2, OUT_W))  # interleaved bytes

    out = np.concatenate([y_out.reshape(-1), uv_out.reshape(-1)])
    if out.size != out_frame_size:
        raise SystemExit(f"Internal error: output size {out.size} != expected {out_frame_size}")

    out.tofile(out_path)
    print(f"Wrote {out_frame_size} bytes: {OUT_W}x{OUT_H} NV12 -> {out_path}")

if __name__ == "__main__":
    main()
