#!/usr/bin/env python3
"""Makes public/img/envelope-front-open-{1200,2400}.webp from envelope-front-{1200,2400}.webp.

The original front has two raised side "wings" that hide the lower corners of the photo frame and card once the
envelope is open. This flattens the top edge to the height of the middle of the pocket (rows above that go
transparent) and rebuilds a soft lip along the new edge from the middle section. The closed envelope keeps the
original image; the open one fades to this version (see .env-front-open in src/save-the-date.html).
"""
from PIL import Image
import numpy as np
for scale, name in ((1, '1200'), (2, '2400')):
    a = np.array(Image.open('public/img/envelope-front-%s.webp' % name).convert('RGBA')).astype(np.float32)
    H, W, _ = a.shape
    first = lambda x: int(np.argmax(a[:, x, 3] > 128))
    p = int(np.median([first(x) for x in range(int(W * .45), int(W * .55))]))   # top edge row of the flat middle
    L, pre = 14 * scale, 3 * scale
    prof = a[p - pre:p + L, int(W * .45):int(W * .55), :].mean(axis=1)            # the edge's lip, averaged
    out = a.copy(); out[:p - pre, :, 3] = 0
    for x in range(W):
        t = first(x) if (a[:, x, 3] > 128).any() else 10 ** 6
        if t < p - 2:                                                           # a wing or slope column
            for i, y in enumerate(range(p - pre, p + L)):
                w = 1.0 if y < p + L - 6 * scale else (p + L - y) / (6.0 * scale)
                out[y, x, :] = prof[i] * w + a[y, x, :] * (1 - w) if i >= pre else prof[i]
            for i, y in enumerate(range(p - pre, p)): out[y, x, 3] = prof[i, 3]
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA').save('public/img/envelope-front-open-%s.webp' % name, 'WEBP', quality=92, method=6)
    print('wrote', name)
