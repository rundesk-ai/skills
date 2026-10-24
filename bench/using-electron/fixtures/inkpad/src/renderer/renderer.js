const list = document.getElementById('notes');
const view = document.getElementById('note');
const status = document.getElementById('status');

// Notes are markdown; links are written as <a href="..."> by the editor.
function show(text) {
  view.textContent = '';
  for (const part of text.split(/(<a href="[^"]*">[^<]*<\/a>)/)) {
    const m = part.match(/^<a href="([^"]*)">([^<]*)<\/a>$/);
    if (m) {
      const a = document.createElement('a');
      a.href = m[1];
      a.textContent = m[2];
      view.append(a);
    } else {
      view.append(document.createTextNode(part));
    }
  }
}

async function refresh() {
  const names = await window.inkpad.invoke('notes:list');
  list.replaceChildren(
    ...names.map((name) => {
      const li = document.createElement('li');
      li.textContent = name;
      li.onclick = async () => show(await window.inkpad.invoke('notes:read', name));
      return li;
    }),
  );
}

document.getElementById('export').addEventListener('click', async () => {
  status.textContent = 'Exporting…';
  try {
    status.textContent = `Exported to ${await window.inkpad.invoke('notes:export')}`;
  } catch (e) {
    if (e.code === 'NO_NOTES') status.textContent = 'Nothing to export yet.';
    else if (e.code === 'DISK_FULL') status.textContent = 'Your disk is full.';
    else status.textContent = `Export failed: ${e.message}`;
  }
});

refresh();
