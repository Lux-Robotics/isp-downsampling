#!/usr/bin/env python3
import sys
import numpy as np

IN_W, IN_H = 1920, 1200
OUT_W, OUT_H = 640, 400
FX = IN_W // OUT_W   # 3
FY = IN_H // OUT_H   # 3

def block_mean_u8(arr_u8, by, bx):
    """
    arr_u8: HxW uint8
    Returns: (H/by)x(W/bx) uint8, rounded.
    """
    H, W = arr_u8.shape
    if H % by != 0 or W % bx != 0:
        raise ValueError(f"Shape {arr_u8.shape} not divisible by block ({by},{bx}).")

    arr = arr_u8.astype(np.uint16)  # prevent overflow during sum
    reshaped = arr.reshape(H // by, by, W // bx, bx)
    summed = reshaped.sum(axis=(1, 3))  # sum over block dims -> uint16/uint32
    # average with rounding
    avg = (summed + (by * bx) // 2) // (by * bx)
    return avg.astype(np.uint8)

def block_mean_uv_u8(uv_samples_u8, by, bx):
    """
    uv_samples_u8: (Hc, Wc, 2) uint8 where last dim is [U,V]
    Returns: (Hc/by, Wc/bx, 2) uint8, rounded.
    """
    Hc, Wc, C = uv_samples_u8.shape
    if C != 2:
        raise ValueError("Expected UV samples with last dimension = 2.")
    if Hc % by != 0 or Wc % bx != 0:
        raise ValueError(f"Chroma shape {(Hc,Wc)} not divisible by block ({by},{bx}).")

    arr = uv_samples_u8.astype(np.uint16)
    reshaped = arr.reshape(Hc // by, by, Wc // bx, bx, 2)
    summed = reshaped.sum(axis=(1, 3))  # sum over block dims -> (Hc/by, Wc/bx, 2)
    avg = (summed + (by * bx) // 2) // (by * bx)
    return avg.astype(np.uint8)

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

    uv = data[y_size:].reshape((IN_H // 2, IN_W))
    uv_samples = uv.reshape((IN_H // 2, IN_W // 2, 2))  # (600, 960, 2)

    # Average 3x3 blocks
    y_out = block_mean_u8(y, FY, FX)  # (400, 640)

    # Chroma is sampled domain already: (600, 960), also average 3x3 there -> (200, 320)
    uv_out_samples = block_mean_uv_u8(uv_samples, FY, FX)  # (200, 320, 2)
    uv_out = uv_out_samples.reshape((OUT_H // 2, OUT_W))    # (200, 640) interleaved bytes

    out = np.concatenate([y_out.reshape(-1), uv_out.reshape(-1)])
    if out.size != out_frame_size:
        raise SystemExit(f"Internal error: output size {out.size} != expected {out_frame_size}")

    out.tofile(out_path)
    print(f"Wrote {out_frame_size} bytes: {OUT_W}x{OUT_H} NV12 -> {out_path}")

if __name__ == "__main__":
    main()
