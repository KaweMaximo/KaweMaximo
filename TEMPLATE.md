# Make your own animated profile

The banner and the terminal on this profile are two SVG files generated from one config file, [`profile.toml`](profile.toml). You can have your own in a few minutes, without installing anything.

1. Click **Use this template → Create a new repository** at the top of this repository. Name the new repository exactly like your GitHub username (for `octocat`, that is `octocat/octocat`) and make it public: that special repository is the one GitHub shows on your profile.
2. In your new repository, open `profile.toml`, click the pencil, change the name, the subtitle, the corner labels and the terminal lines, and commit.
3. Wait about a minute. The **build profile** workflow regenerates `assets/banner.svg` and `assets/terminal.svg` and commits them. Then open your profile.
4. Edit `README.md` for the text under the images. The "Rules of engagement" note is mine: change it or delete it.

If the images don't change, open the **Actions** tab: the workflow has to be enabled, and if it fails with a permission error, set **Settings → Actions → General → Workflow permissions** to **Read and write**.

## What you can change

**`[banner]`**

| Key | What it is |
|---|---|
| `name` | The big glitching title. Long names shrink to fit. |
| `subtitle` | The line typed out under the name. |
| `motto` | The small spaced line that fades in. Empty hides it. |
| `top_left`, `top_right`, `bottom_left`, `bottom_right` | The corner labels. Empty hides one. |
| `description` | Text for screen readers. |
| `seed` | Changes the pattern of the falling characters. |

**`[terminal]`**

| Key | What it is |
|---|---|
| `user`, `host` | The prompt, as in `user@host:~$`. |
| `title` | The window title. Defaults to `user@host: ~ — zsh`. |
| `description` | Text for screen readers. |
| `[[terminal.lines]]` | One block per line: `cmd = "..."` is typed after the prompt, `out = [["text", "color"], ...]` is printed. |

Colors: `green`, `cyan`, `purple`, `yellow`, `red`, `white`, `gray`, `dim`, or any `#rrggbb`. The timing is computed for you: each command is typed out, then its output follows. A terminal line fits about 95 characters, and the generator warns when one is longer.

## Building locally

```sh
python3 scripts/gen_svgs.py
```

Python 3.11 or newer, no dependencies. GitHub caches profile images by URL, so after building by hand, bump the `?v=` of both images in `README.md` (the workflow does it for you).

## How it works

Plain SVG with SMIL animations: no JavaScript and no web fonts, so it keeps animating inside GitHub's image sandbox, which blocks scripts and external files.

If you use it, a ⭐ on this repository is appreciated.
