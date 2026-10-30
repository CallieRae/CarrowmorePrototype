"""Rebuild the illustration's background as color columns only: no lighthouse, rock or beams.
Each column is a vertical gradient, so every pixel is replaced by its column's color at that height:
the median across the column's clean pixels at that row, then a smooth curve fitted down the
column that ignores anything brighter than the column (beams, light cones, the lamp halo).

Run: python3 prototype/make_gradient_plate.py prototype/assets/lighthouse.webp prototype/assets/lighthouse-gradient.webp
"""
import sys
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert("RGB")).astype(float)
H, W, _ = im.shape
edges = [0, 315, 625, 740, 830, 1000, 1100, 1300, 1720, W]

# Rock top as a piecewise-linear contour (x, y), traced from the art; pixels below it are rock.
cx = [0, 230, 820, 1000, 1290, 1340, 1450, 1700, W]
cy = [H, 1080, 830, 740, 668, 740, 960, 1080, H]
rock_top = np.interp(np.arange(W), cx, cy) - 12
mask = np.zeros((H, W), bool)
mask[np.arange(H)[:, None] < rock_top[None, :]] = True     # keep only above the rock
mask[200:850, 860:1050] = False                             # tower, lantern and finial

plate = np.zeros_like(im)
for a, b in zip(edges[:-1], edges[1:]):
    prof = np.full((H, 3), np.nan)
    for y in range(H):
        px = im[y, a:b][mask[y, a:b]]
        if len(px) >= 4:
            prof[y] = np.median(px, axis=0)
    # Beams, light cones and the lamp halo only ever ADD light, so fit a smooth curve to each
    # column and repeatedly drop rows that sit above it: what survives is the column itself.
    ys = np.arange(H)
    ok = ~np.isnan(prof[:, 0])
    lum = prof @ np.array([.2126, .7152, .0722])
    keep = ok.copy()
    for _ in range(12):
        coef = np.polyfit(ys[keep] / H, lum[keep], 3)
        resid = lum - np.polyval(coef, ys / H)
        keep = ok & (resid < 4)
    smooth = np.zeros((H, 3))
    for c in range(3):
        cc = np.polyfit(ys[keep] / H, prof[keep, c], 3)
        smooth[:, c] = np.polyval(cc, ys / H)
    lo, hi = ys[keep].min(), ys[keep].max()          # never extrapolate past the clean rows
    smooth[:lo] = smooth[lo]; smooth[hi:] = smooth[hi]
    plate[:, a:b] = smooth[:, None, :]

Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8)).save(out, "WEBP", quality=90)
for a, b in zip(edges[:-1], edges[1:]):
    t, m, bt = plate[60, (a + b) // 2], plate[540, (a + b) // 2], plate[1060, (a + b) // 2]
    print(f"{a:>4}-{b:<4} top #{int(t[0]):02X}{int(t[1]):02X}{int(t[2]):02X}  mid #{int(m[0]):02X}{int(m[1]):02X}{int(m[2]):02X}  foot #{int(bt[0]):02X}{int(bt[1]):02X}{int(bt[2]):02X}")
