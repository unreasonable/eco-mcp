"""Build a complete plugin ZIP without Git, CI, or maintainer scripts."""
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
target = Path(sys.argv[1]).resolve()
if target.is_relative_to(root):
    raise SystemExit('Write the ZIP outside the plugin folder.')
entries = ['plugin.json', 'mcp.json', '.mcp.json', '.codex-plugin',
           '.claude-plugin', '.agents', 'skills', 'assets', 'README.md',
           'LICENSE', 'llms.txt', 'docs']
with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
    for entry in entries:
        path = root / entry
        for file in sorted(path.rglob('*')) if path.is_dir() else [path]:
            if file.is_file():
                if file.is_symlink():
                    raise SystemExit(f'Symlink not permitted: {file}')
                archive.write(file, 'unreasonable-eco/' + file.relative_to(root).as_posix())
print(target)
