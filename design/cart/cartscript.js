let cart = [];

function addToCart(product) {
  cart.push(product);
  updateCart();
}

function removeFromCart(index) {
  cart.splice(index, 1);
  updateCart();
}

function updateCart() {
  const cartContainer = document.getElementById('cart');
  const totalElement = document.getElementById('total');
  
  // Clear the cart container
  cartContainer.innerHTML = '';

  // Display cart items
  cart.forEach((product, index) => {
    const cartItem = document.createElement('div');
    cartItem.classList.add('cart-item');
    cartItem.innerHTML = `
      <span>${product.name} - $${product.price.toFixed(2)}</span>
      <button onclick="removeFromCart(${index})">Remove</button>
    `;
    cartContainer.appendChild(cartItem);
  });

  // Calculate and display the total
  const total = cart.reduce((sum, product) => sum + product.price, 0);
  totalElement.textContent = `Total: $${total.toFixed(2)}`;
}

function proceedToPayment() {
  // Implement payment processing logic here
  alert('Proceeding to payment. Implement payment logic in the backend.');
}
