// Existing data for notifications, orders, and shipments
const notifications = [
    { id: 1, message: 'Pesanan ID 301 telah diproses.' },
    { id: 2, message: 'Pengiriman ID 201 telah terkirim.' },
    { id: 3, message: 'Pengiriman ID 202 sedang dalam perjalanan.' }
];

const pesanan = [
    { id: 301, totalPrice: 'Rp 1.000.000', totalWeight: '5 KG', status: 'Pending' },
    { id: 302, totalPrice: 'Rp 1.500.000', totalWeight: '7 KG', status: 'Processed' },
    { id: 303, totalPrice: 'Rp 2.000.000', totalWeight: '10 KG', status: 'Shipped' }
];

// Updated data for shipments
const pengiriman = [
    { id: 201, orderid: '1', ongkir: 'Rp 5000', resi: '1', status: 'On the way' },
    { id: 202, orderid: '2', ongkir: 'Rp 5000', resi: '2', status: 'Delivered' }
];

// Function to display notification count
function updateNotificationBadge(count) {
    const badge = document.getElementById('notificationBadge');
    if (count > 0) {
        badge.textContent = count;
        badge.style.display = 'inline-block';
    } else {
        badge.style.display = 'none';
    }
}

// Function to show notification dropdown
function showNotifications() {
    const dropdown = document.getElementById('notificationDropdown');
    dropdown.innerHTML = ''; // Clear existing notifications

    if (notifications.length > 0) {
        notifications.forEach(notification => {
            const notificationItem = document.createElement('a');
            notificationItem.textContent = notification.message;
            dropdown.appendChild(notificationItem);
        });
    } else {
        dropdown.innerHTML = '<p>Tidak ada notifikasi baru.</p>';
    }
}

// Function to display order data
function tampilkanPesanan() {
    const pesananTable = document.getElementById('pesananTable');
    if (!pesananTable) return; // Guard clause in case element not found

    pesananTable.querySelector('tbody').innerHTML = ''; // Clear existing rows

    pesanan.forEach(order => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${order.id}</td> <!-- ID Pesanan -->
            <td>${order.totalPrice}</td> <!-- Total Price -->
            <td>${order.totalWeight}</td> <!-- Total Weight -->
            <td class="table-action">
                <button onclick="ubahStatusPesanan(${order.id})">Ubah Status</button> <!-- Action Button -->
            </td>
        `;
        pesananTable.querySelector('tbody').appendChild(row);
    });
}

// Function to change the status of an order
function ubahStatusPesanan(id) {
    const order = pesanan.find(item => item.id === id);
    if (!order) return;

    const newStatus = prompt(`Ubah status pesanan ID ${id}:`, order.status);
    if (newStatus) {
        order.status = newStatus;
        tampilkanPesanan(); // Refresh the table to show the updated status
    }
}

// Function to display shipment data
function tampilkanPengiriman() {
    const pengirimanTable = document.getElementById('pengirimanTable');
    if (!pengirimanTable) return; // Guard clause in case element not found

    pengirimanTable.querySelector('tbody').innerHTML = ''; // Clear existing rows

    pengiriman.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td> <!-- ID Retailer -->
            <td>${item.orderid}</td> <!-- Order ID -->
            <td>${item.ongkir}</td> <!-- Ongkir -->
            <td>${item.resi}</td> <!-- Resi -->
            <td>${item.status}</td> <!-- Status -->
            <td class="table-action">
                <button onclick="ubahStatusPengiriman(${item.id})">Ubah Status</button> <!-- Action Button -->
            </td>
        `;
        pengirimanTable.querySelector('tbody').appendChild(row);
    });
}

// Function to change shipment status
function ubahStatusPengiriman(id) {
    const shipment = pengiriman.find(item => item.id === id);
    if (!shipment) return;

    const newStatus = prompt(`Ubah status pengiriman ID ${id}:`, shipment.status);
    if (newStatus) {
        shipment.status = newStatus;
        tampilkanPengiriman(); // Refresh the table to show the updated status
    }
}

// Event listeners for notification and user menus, sidebar, etc.
document.addEventListener('DOMContentLoaded', () => {
    // Set up user menu toggle
    const userIcon = document.getElementById('userMenu');
    if (userIcon) {
        userIcon.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent click propagation
            userIcon.classList.toggle('open');
        });

        // Close the dropdown if clicked outside
        document.addEventListener('click', (event) => {
            if (!userIcon.contains(event.target)) {
                userIcon.classList.remove('open');
            }
        });
    }

    // Set up notification menu toggle
    const notificationIcon = document.getElementById('notificationMenu');
    if (notificationIcon) {
        notificationIcon.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent click propagation
            notificationIcon.classList.toggle('open');
            showNotifications();
        });

        // Close the dropdown if clicked outside
        document.addEventListener('click', (event) => {
            if (!notificationIcon.contains(event.target)) {
                notificationIcon.classList.remove('open');
            }
        });
    }

    // Load sidebar navigation if placeholder exists
    if (document.getElementById('nav-placeholder')) {
        loadNav();
    }

    // Initialize notification badge count
    updateNotificationBadge(notifications.length);

    // Display orders and shipments on page load
    tampilkanPesanan();
    tampilkanPengiriman();
});

// Function to load the sidebar navigation (existing functionality)
function loadNav() {
    fetch('/nav.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('nav-placeholder').innerHTML = data;

            // Highlight the active link based on the current URL
            const currentPath = window.location.pathname.split('/').pop();
            document.querySelectorAll('.sidebar a').forEach(link => {
                if (link.getAttribute('href') === currentPath) {
                    link.classList.add('active');
                }
            });

            // Add event listener for the hamburger button
            const hamburgerButton = document.getElementById('hamburger-button');
            if (hamburgerButton) {
                hamburgerButton.addEventListener('click', toggleSidebar);
            }
        })
        .catch(error => console.error('Error loading navigation:', error));
}

// Function to toggle sidebar
function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');
    document.querySelector('.container').classList.toggle('sidebar-active');
}

// Function to handle registration (improved)
function prosesRegister(event) {
    event.preventDefault(); // Prevent form submission
    const username = document.getElementById('newUsername').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Validate email format
    if (!emailRegex.test(email)) {
        alert('Format email tidak valid.');
        return;
    }

    // Check if password and confirm password match
    if (password !== confirmPassword) {
        alert('Password dan Konfirmasi Password tidak cocok.');
        return;
    }

    // Check password length
    if (password.length < 6) {
        alert('Password harus terdiri dari minimal 6 karakter.');
        return;
    }

    // Simulate successful registration and redirect to login page
    alert('Registrasi berhasil! Silakan login menggunakan akun Anda.');
    window.location.href = 'login.html'; // Redirect to login page after registration
}

// Function to handle login (improved)
function prosesLogin(event) {
    event.preventDefault(); // Prevent form submission
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    // Simple validation for non-empty fields
    if (username && password) {
        // Simulate successful login and redirect to dashboard
        alert('Login berhasil! Selamat datang, ' + username + '!');
        window.location.href = 'dashboard.html'; // Redirect to dashboard after successful login
    } else {
        alert('Nama Pengguna dan Password harus diisi.');
    }
}

// Display summary on dashboard (existing functionality)
function tampilkanRingkasanDashboard() {
    const totalProduk = 150;
    const productStock = 1200;
    const pesananBaru = 25;
    const pengirimanTertunda = 5;

    document.getElementById('totalProduk').innerText = totalProduk;
    document.getElementById('productStock').innerText = productStock;
    document.getElementById('pesananBaru').innerText = pesananBaru;
    document.getElementById('pengirimanTertunda').innerText = pengirimanTertunda;
}

// Function to display product data in the table
function tampilkanProduk() {
    const productTable = document.getElementById('productTable');
    if (!productTable) return; // Guard clause in case element not found

    productTable.querySelector('tbody').innerHTML = ''; // Clear existing rows
    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.nama}</td>
            <td>${product.kategori}</td>
            <td><img src="${product.gambar}" alt="${product.nama}" style="max-width: 100px; height: auto;"></td> <!-- Display the image -->
            <td>${product.stok}</td>
            <td>Rp ${product.harga.toLocaleString()}</td>
            <td class="table-action">
                <button onclick="editProduk('${product.id}')">Edit</button>
                <button onclick="hapusProduk('${product.id}')">Hapus</button>
            </td>
        `;
        productTable.querySelector('tbody').appendChild(row);
    });
}

// Store product data
const products = [];

// Placeholder function for adding a product
function tambahProduk() {
    const productId = document.getElementById('productId').value.trim();
    const productName = document.getElementById('productName').value.trim();
    const productCategory = document.getElementById('productCategory').value.trim();
    const productImage = document.getElementById('productImageUrl').value.trim(); // Get the image URL
    const productStock = document.getElementById('productStock').value.trim();
    const productPrice = document.getElementById('productPrice').value.trim();
    // Add new product to the products array
    products.push({
        id: productId,
        nama: productName,
        kategori: productCategory,
        gambar: productImage,
        stok: productStock,
        harga: productPrice

    });

    // Add product to the products array
    products.push(product);

    // Refresh the product table
    tampilkanProduk();

    // Clear form inputs
    document.getElementById('productId').value = '';
    document.getElementById('productName').value = '';
    document.getElementById('productCategory').value = '';
    document.getElementById('productImage').value = '';
    document.getElementById('productStock').value = '';
    document.getElementById('productPrice').value = '';

    // Save product data to localStorage or backend if needed

    // Notify user
    alert('Produk berhasil ditambahkan!');

    // Redirect to kelola-produk.html to view the table of products
    window.location.href = '/produk/kelola-produk.html';
}
// Placeholder function for editing a product
function editProduk(namaProduk) {
    alert('Fungsi edit produk ' + namaProduk + ' belum diimplementasikan.');
}

// Placeholder function for deleting a product
function hapusProduk(namaProduk) {
    alert('Fungsi hapus produk ' + namaProduk + ' belum diimplementasikan.');
}
