const API = '/products';

// ===== СПИСОК =====
async function loadProducts() {
    const tbody = document.getElementById('products-tbody');
    const empty = document.getElementById('empty-state');
    const loading = document.getElementById('loading');
    if (!tbody) return;

    try {
        const res = await fetch(API);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const products = await res.json();

        loading.classList.add('d-none');
        tbody.innerHTML = '';

        if (!products.length) {
            empty.classList.remove('d-none');
            return;
        }
        empty.classList.add('d-none');

        products.forEach(p => {
            const tr = document.createElement('tr');
            tr.dataset.title = (p.title || '').toLowerCase();
            tr.innerHTML = `
                <td>${p.id}</td>
                <td>${escapeHtml(p.title)}</td>
                <td>${p.price}</td>
                <td>${p.quantity}</td>
                <td class="text-truncate" style="max-width: 300px;">${escapeHtml(p.description || '')}</td>
                <td>
                    <a href="/ui/products/edit?id=${p.id}" class="btn btn-sm btn-outline-primary">✏️</a>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct(${p.id})">🗑️</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        loading.textContent = 'Ошибка загрузки: ' + e.message;
    }
}

async function deleteProduct(id) {
    if (!confirm(`Удалить продукт #${id}?`)) return;
    const res = await fetch(`${API}/${id}`, { method: 'DELETE' });
    if (res.ok) {
        loadProducts();
    } else {
        const err = await res.json().catch(() => ({}));
        alert('Ошибка: ' + (err.detail || res.status));
    }
}

function filterTable(query) {
    const q = query.toLowerCase().trim();
    document.querySelectorAll('#products-tbody tr').forEach(tr => {
        tr.style.display = tr.dataset.title.includes(q) ? '' : 'none';
    });
}

// ===== ФОРМА =====
function getEditId() {
    const id = new URLSearchParams(window.location.search).get('id');
    return id ? parseInt(id, 10) : null;
}

async function loadProductForEdit(id) {
    const res = await fetch(`${API}/${id}`);
    if (!res.ok) {
        alert('Продукт не найден');
        window.location.href = '/ui/products';
        return;
    }
    const p = await res.json();
    const form = document.getElementById('product-form');
    form.title.value = p.title;
    form.price.value = p.price;
    form.quantity.value = p.quantity;
    form.description.value = p.description || '';
    document.getElementById('form-title').textContent = `Редактировать продукт #${id}`;
}

async function submitForm(event) {
    event.preventDefault();
    const form = event.target;
    const errorBox = document.getElementById('form-error');
    errorBox.classList.add('d-none');

    const data = {
        title: form.title.value.trim(),
        price: parseFloat(form.price.value),
        quantity: parseInt(form.quantity.value, 10),
        description: form.description.value.trim(),
    };

    const id = getEditId();
    const url = id ? `${API}/${id}` : API;
    const method = id ? 'PUT' : 'POST';

    const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });

    if (res.ok) {
        window.location.href = '/ui/products';
    } else {
        const err = await res.json().catch(() => ({}));
        errorBox.textContent = err.detail || `Ошибка ${res.status}`;
        errorBox.classList.remove('d-none');
    }
}

// ===== ИНИЦИАЛИЗАЦИЯ =====
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('products-tbody')) {
        loadProducts();
        const search = document.getElementById('search');
        if (search) search.addEventListener('input', e => filterTable(e.target.value));
    }

    const form = document.getElementById('product-form');
    if (form) {
        form.addEventListener('submit', submitForm);
        const id = getEditId();
        if (id) loadProductForEdit(id);
    }
});

// ===== УТИЛИТЫ =====
function escapeHtml(str) {
    return String(str)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;');
}
