var currentModal = null;
var isFirstTime = true;

function openWindow(category) {
    if (currentModal) {
        document.body.removeChild(currentModal);
        document.body.classList.remove('modal-open');
        currentModal = null;
    }
    openNewModal(category);
}

function openNewModal(category) {
    var windowHeight = window.innerHeight;
    var modalContainer = document.createElement('div');
    modalContainer.classList.add('modal-container');

    var modal = document.createElement('div');
    modal.classList.add('modal');
    modal.style.height = '0';

    // Create a title element
    var titleElement = document.createElement('h2');
    titleElement.classList.add('modal-title');
    titleElement.textContent = getTitleText(category);
    modal.appendChild(titleElement);

    // Create a list of clickable categories in a row
    var categoriesRow = document.createElement('div');
    categoriesRow.classList.add('category-row');

    var categories;

    switch (category) {
        case 'men':
            categories = [
                'Basketball', 'Casual', 'Cross-training', 'Crossfit',
                'Fashion', 'Lifestyle', 'Racing', 'Retro', 'Running',
                'Skate', 'Trail', 'Trail Running', 'Training', 'Walking', 'Weightlifting'
            ];
            break;
        case 'women':
            categories = [
                'Basketball', 'Casual', 'Crossfit', 'Fashion', 'Hiking',
                'Lifestyle', 'Retro', 'Running', 'Skate', 'Slides',
                'Trail', 'Trail Running', 'Training', 'Walking'
            ];
            break;
        case 'brands':
            categories = [
                'Adidas', 'Asics', 'Converse', 'Fila', 'New Balance',
                'Nike', 'Puma', 'Reebok', 'Skechers', 'Vans'
            ];
            break;
    }

    // Populate the row with clickable items
    categories.forEach(function (categoryName) {
        var categoryItem = document.createElement('div');
        categoryItem.innerText = categoryName;
        categoryItem.classList.add('category-item');
        categoryItem.onclick = function () {
            var filePath = '../' + category + '/' + categoryName + '.html';
            window.location.href = filePath;
        };

        categoriesRow.appendChild(categoryItem);
    });

    var closeButton = document.createElement('span');
    closeButton.classList.add('close-button');
    closeButton.innerHTML = '×';
    closeButton.onclick = function () {
        document.body.removeChild(modalContainer);
        document.body.classList.remove('modal-open');
        currentModal = null;
        isFirstTime = true;
    };

    modal.appendChild(categoriesRow);
    modal.appendChild(closeButton);
    modalContainer.appendChild(modal);
    document.body.appendChild(modalContainer);

    // Animate the modal height only for the first window
    if (isFirstTime) {
        modal.style.transition = 'height 0.5s ease-out';
        setTimeout(function () {
            modal.style.height = windowHeight + 'px';
            document.body.classList.add('modal-open');
            currentModal = modalContainer;
        }, 50);
        isFirstTime = false;
    } else {
        modal.style.height = windowHeight + 'px';
        document.body.classList.add('modal-open');
        currentModal = modalContainer;
    }
}

function getTitleText(category) {
    switch (category) {
        case 'men':
            return "Men's Shoes";
        case 'women':
            return "Women's Shoes";
        case 'brands':
            return "Brands";
        default:
            return "Category";
    }
}
