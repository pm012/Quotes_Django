document.addEventListener("DOMContentLoaded", () => {
    const filterType = document.querySelector("[data-filter-type]");
    const filterItem = document.querySelector("[data-filter-item]");
    const filterSearch = document.querySelector("#filter-item-search");
    const filterOptionsElement = document.querySelector("#quote-filter-options");

    if (filterType && filterItem && filterSearch && filterOptionsElement) {
        const optionsByType = JSON.parse(filterOptionsElement.textContent);
        const renderFilterOptions = (selectedValue = "") => {
            const items = optionsByType[filterType.value] || [];
            filterItem.replaceChildren(new Option("Choose an item", ""));
            for (const [value, label] of items) {
                filterItem.add(new Option(label, value, false, value === selectedValue));
            }
            filterItem.disabled = items.length === 0;
            filterSearch.disabled = items.length === 0;
            filterSearch.value = "";
        };

        renderFilterOptions(filterItem.value);
        filterType.addEventListener("change", () => renderFilterOptions());
        filterSearch.addEventListener("input", () => {
            const query = filterSearch.value.trim().toLocaleLowerCase();
            for (const option of filterItem.options) {
                option.hidden = Boolean(option.value) &&
                    !option.text.toLocaleLowerCase().includes(query);
            }
        });
    }

    for (const picker of document.querySelectorAll(".tag-picker")) {
        const search = picker.querySelector("[data-tag-search]");
        const summary = picker.querySelector("[data-tag-summary]");
        const checkboxes = picker.querySelectorAll('.tags-checkboxes input[type="checkbox"]');
        const labels = picker.querySelectorAll(".tags-checkboxes label");
        if (!search || !summary) continue;

        const updateSummary = () => {
            const selected = [...checkboxes]
                .filter((checkbox) => checkbox.checked)
                .map((checkbox) => checkbox.closest("label")?.textContent.trim())
                .filter(Boolean);
            summary.textContent = selected.length ? selected.join(", ") : "Choose tags";
        };

        search.addEventListener("input", () => {
            const query = search.value.trim().toLocaleLowerCase();
            for (const label of labels) {
                label.hidden = !label.textContent.toLocaleLowerCase().includes(query);
            }
        });
        for (const checkbox of checkboxes) {
            checkbox.addEventListener("change", updateSummary);
        }
        updateSummary();
    }
});
