"""Validate the shared plugin package and host-specific discovery files."""
import json
import re
from pathlib import Path
import yaml

repository = Path(__file__).resolve().parents[1]
root = repository / 'plugins/unreasonable-eco'
def read(path):
    return json.loads((root / path).read_text())

portable = read('plugin.json')
codex = read('.codex-plugin/plugin.json')
claude = read('.claude-plugin/plugin.json')
for manifest in [portable, codex, claude]:
    for key in ['name', 'version', 'author', 'repository', 'license']:
        assert manifest[key] == portable[key], key
assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', portable['name'])
assert re.fullmatch(r'\d+\.\d+\.\d+', portable['version'])
assert portable['license'] == 'MIT' and (root / 'LICENSE').is_file()
assert not {'skills', 'mcpServers', 'apps', 'interface'} & portable.keys()
interface = portable['extensions']['com.openai']['interface']
assert interface == codex['interface']
assert len(interface['shortDescription']) <= 30
for key in ['logo', 'logoDark', 'composerIcon', 'composerIconDark']:
    value = interface[key]
    assert value.startswith('./') and (root / value).is_file()
assert (root / claude['icon']).is_file()
for field in ['documentationUrl', 'supportUrl', 'privacyPolicyUrl', 'termsOfServiceUrl']:
    assert claude[field].startswith('https://')

for path, transport in [('mcp.json', 'streamable-http'), ('.mcp.json', 'http')]:
    servers = read(path)['mcpServers']
    assert list(servers) == ['unreasonable-eco']
    server = servers['unreasonable-eco']
    assert server == {'type': transport, 'url': 'https://unreasonable.eco/mcp'}
assert codex['skills'] == './skills/' and codex['mcpServers'] == './.mcp.json'

skills = sorted((root / 'skills').iterdir())
assert len(skills) == 5
for skill in skills:
    text = (skill / 'SKILL.md').read_text()
    assert text.startswith('---\n')
    frontmatter = yaml.safe_load(text.split('---', 2)[1])
    assert frontmatter['name'] == skill.name
    assert isinstance(frontmatter['description'], str) and frontmatter['description']
    config = yaml.safe_load((skill / 'agents/openai.yaml').read_text())
    assert '$' + skill.name in config['interface']['default_prompt']
    assert 25 <= len(config['interface']['short_description']) <= 64
    assert config['dependencies']['tools'] == [{
        'type': 'mcp', 'value': 'unreasonable-eco',
        'description': 'Unreasonable Eco community and program tools',
        'transport': 'streamable_http', 'url': 'https://unreasonable.eco/mcp'}]

catalog = json.loads((repository / '.claude-plugin/marketplace.json').read_text())
assert catalog['plugins'][0]['source'] == './plugins/unreasonable-eco'
assert catalog['plugins'][0]['name'] == portable['name']
assert catalog['plugins'][0]['version'] == portable['version']
catalog = json.loads((repository / '.agents/plugins/marketplace.json').read_text())
assert catalog['plugins'][0]['source'] == {'source': 'local', 'path': './plugins/unreasonable-eco'}
assert catalog['plugins'][0]['name'] == portable['name']
readme = re.sub(r'```.*?```', '', (root / 'README.md').read_text(), flags=re.S)
assert len(readme.split()) >= 40

seen = set()
assert not (root / 'scripts').exists()
assert not (root / 'docs').exists()
assert not (root / 'llms.txt').exists()
assert not (root / 'hooks').exists()
assert not list(root.rglob('*.py'))
assert 'scripts/' not in (root / 'README.md').read_text()
files = [p for p in root.rglob('*') if '.git' not in p.relative_to(root).parts]
assert len(files) < 512
for path in files:
    assert not path.is_symlink(), path
    rel = path.relative_to(root).as_posix()
    assert rel.lower() not in seen, f'Case collision: {rel}'
    seen.add(rel.lower())
    assert path.name not in {'.DS_Store', 'Thumbs.db', 'desktop.ini', '__MACOSX'}
    assert ':' not in path.name and not path.name.endswith((' ', '.'))
    assert not re.fullmatch(r'(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?', path.name, re.I)
    if path.is_file():
        assert path.stat().st_size < 256 * 1024, path
        assert path.suffix not in {'.zip', '.pdf', '.exe', '.ico'}, path
    if path.suffix == '.json':
        json.loads(path.read_text())
print('Passed: manifests, transports, five skills, catalogs, assets, docs, and package layout.')
