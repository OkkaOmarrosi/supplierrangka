document.addEventListener("DOMContentLoaded", function () {
    // Load products from API
    fetch('/api/products')
        .then(response => response.json())
        .then(data => {
            const productList = document.getElementById('product-list');
            productList.innerHTML = '';

            data.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.namaproduk}</td>
                    <td>${product.kategori}</td>
                    <td>${product.stok}</td>
                    <td>${product.harga}</td>
                    <td>${product.berat}</td>
                    <td><button data-id="${product.idproduk}" class="add-to-order">Add to Order</button></td>
                `;
                productList.appendChild(row);
            });

            // Add event listeners for 'Add to Order' buttons
            document.querySelectorAll('.add-to-order').forEach(button => {
                button.addEventListener('click', addToOrder);
            });
        });

    // Handle adding items to order
    function addToOrder(event) {
        const productId = event.target.getAttribute('data-id');
        const productName = event.target.closest('tr').children[0].textContent;
        
        const orderItems = document.getElementById('order-items');
        const orderItem = document.createElement('div');
        orderItem.innerHTML = `
            <label>${productName}</label>
            <input type="hidden" name="items[][idproduk]" value="${productId}">
            <input type="number" name="items[][jumlah]" placeholder="Quantity" required>
        `;
        orderItems.appendChild(orderItem);
    }

    // Handle order submission
    const orderForm = document.getElementById('order-form');
    orderForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const retailerId = document.getElementById('retail-id').value;
        const formData = new FormData(orderForm);

        // Convert form data to JSON
        const orderData = {
            idretail: retailerId,
            items: []
        };

        formData.forEach((value, key) => {
            if (key.startsWith('items')) {
                const index = key.match(/\d+/)[0];
                const field = key.split('][')[1].slice(0, -1);

                if (!orderData.items[index]) {
                    orderData.items[index] = {};
                }

                orderData.items[index][field] = value;
            }
        });

        // Send order data to API
        fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                window.location.reload(); // Reload the page after successful order
            })
            .catch(error => console.error('Error:', error));
    });
});


document.getElementById("menu-toggle").addEventListener("click", function() {
    document.getElementById("wrapper").classList.toggle("toggled");
});
