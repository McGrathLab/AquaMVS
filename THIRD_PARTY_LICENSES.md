# Third-Party Licenses

AquaMVS itself is distributed under the MIT License (see [LICENSE](LICENSE)).
The AquaMVS source tree vendors no third-party source code or model weights;
all dependencies are installed separately at the user's request. This file
documents the licenses of the optional components AquaMVS can invoke, so that
users — especially commercial users — can choose a fully permissive
configuration.

## Feature extractors (optional, via LightGlue)

AquaMVS's sparse pathway reaches feature extractors through the
[LightGlue](https://github.com/cvg/LightGlue) package. The extractor is
selectable via `sparse_matching.extractor_type`:

| Extractor  | License                                   | Commercial use |
|------------|-------------------------------------------|----------------|
| **ALIKED** (default) | BSD-3-Clause                    | ✅ Yes         |
| **DISK**   | Apache-2.0                                | ✅ Yes         |
| SuperPoint | Magic Leap non-commercial research license | ⚠️ **No**    |

**SuperPoint** is provided by Magic Leap, Inc. under a license that permits
use for **non-commercial, academic research purposes only**. It is *not*
selected by default. AquaMVS ships no SuperPoint code or weights; they are
downloaded from Magic Leap / LightGlue only if the user explicitly selects
`extractor_type: superpoint`. Commercial users must select **ALIKED** or
**DISK** instead.

## Matchers

| Component  | License    | Notes |
|------------|------------|-------|
| **RoMa v2** (default) | MIT   | Dense matching pathway; code only, see DINOv3 below |
| **DINOv3** (via RoMa v2) | DINOv3 License (Meta, custom) | RoMa v2's default backbone |
| LightGlue  | Apache-2.0 | Sparse matching pathway |

**DINOv3** is not MIT-licensed. RoMa v2's default feature backbone
(`dinov3_vitl16`) is downloaded at runtime from
[facebookresearch/dinov3](https://github.com/facebookresearch/dinov3) via
`torch.hub`, and a few modules inside the `romav2` package (`romav2/vit/`)
are themselves under the DINOv3 License. AquaMVS ships no DINOv3 code or
weights. The [DINOv3 License](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md)
permits commercial use and modification, but it is not an open-source license:

- publications of results obtained using DINOv3 must acknowledge it;
- use must comply with sanctions and export controls, and military, weapons,
  and ITAR-regulated uses are prohibited;
- anyone redistributing DINOv3 must include a copy of the license.

Because RoMa v2 is the default matcher, every default AquaMVS run uses DINOv3.

## Other dependencies

Apart from DINOv3 (above), all remaining runtime dependencies (PyTorch, kornia, Open3D, OpenCV, NumPy,
SciPy, PyYAML, matplotlib, pydantic, tqdm, tabulate, AquaCal) are distributed
under permissive licenses (BSD, MIT, or Apache-2.0).
