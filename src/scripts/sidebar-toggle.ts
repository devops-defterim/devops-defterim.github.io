// Sol üstteki menü düğmesi.
// Mobilde: popovertarget ile çekmece menüyü açar ve kapatır (JS olmadan da çalışır).
// Masaüstünde: menüyü gizler veya gösterir; tercih localStorage'da saklanır.
const STORAGE_KEY = 'bd-sidebar';
const root = document.documentElement;
const desktop = matchMedia('(min-width: 50rem)');

function store(value: 'open' | 'closed') {
	try {
		localStorage.setItem(STORAGE_KEY, value);
	} catch {
		// Depolama kapalıysa tercih sadece bu sayfa için geçerli olur.
	}
}

function init() {
	const button = document.querySelector<HTMLButtonElement>('[data-sidebar-toggle]');
	const pane = document.getElementById('starlight__sidebar');
	if (!button || !pane) return;

	const sync = () => {
		const open = desktop.matches
			? !root.hasAttribute('data-sidebar-collapsed')
			: pane.matches(':popover-open');
		button.setAttribute('aria-expanded', String(open));
	};

	button.addEventListener('click', (event) => {
		if (!desktop.matches) return;
		event.preventDefault();
		const collapse = !root.hasAttribute('data-sidebar-collapsed');
		root.toggleAttribute('data-sidebar-collapsed', collapse);
		store(collapse ? 'closed' : 'open');
		sync();
	});
	pane.addEventListener('toggle', sync);
	desktop.addEventListener('change', sync);
	sync();
}

init();
