export function formatDate(date) {
	const today = new Date();
	const tomorrow = new Date(today);
	const tomorrows = new Date(today);
	tomorrow.setDate(today.getDate() + 1);
	tomorrows.setDate(today.getDate() + 2);

	const formatDate = d =>
		`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

	return {
		today: formatDate(today),
		tomorrow: formatDate(tomorrow),
		tomorrows: formatDate(tomorrows)
	};
}