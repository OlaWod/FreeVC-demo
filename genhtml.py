#!/usr/bin/env python3

from jinja2 import FileSystemLoader, Environment

import os
from glob import glob

def gen_rows(gtype):
    ret = []

    freevc = 'data/freevc'
    freevc_spk = 'data/freevc-spk'
    freevc_sr = 'data/freevc-sr'
    vqmivc = 'data/vqmivc'
    ppgvc = 'data/bne-ppg-vc'
    yourtts = 'data/yourtts'

    wavs = sorted(glob(f'data/freevc/{gtype}/*.wav'))

    for wav in wavs:
        basename = os.path.basename(wav)
        src_basename = basename.split('-')[0]
        tgt_basename = basename.split('-')[1][:-4]
        src = os.path.join("data", "wavs", f"{src_basename}.wav")
        tgt = os.path.join("data", "wavs", f"{tgt_basename}.wav")
        row = (
                src_basename,
                tgt_basename,
                src, 
                tgt,
                os.path.join(freevc, gtype, f'{src_basename}-{tgt_basename}.wav'),
                os.path.join(freevc_spk, gtype, f'{src_basename}-{tgt_basename}.wav'),
                os.path.join(freevc_sr, gtype, f'{src_basename}-{tgt_basename}.wav'),
                os.path.join(vqmivc, gtype, f'{src_basename}-{tgt_basename}_gen.wav'),
                os.path.join(ppgvc, gtype, f'{src_basename}-{tgt_basename}.wav'),
                os.path.join(yourtts, gtype, f'{src_basename}-{tgt_basename}.wav'),
        )
        ret.append(row)
    return ret


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("base.html.jinja2")

    s2s_rows = gen_rows("s2s")
    u2s_rows = gen_rows("u2s")
    u2u_rows = gen_rows("u2u")

    html = template.render(
        s2s_rows=s2s_rows,
        u2s_rows=u2s_rows,
        u2u_rows=u2u_rows
    )
    print(html)

if __name__ == "__main__":
    main()
