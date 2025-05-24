const photoInnerEl = document.querySelector('.add-product__box-inner');
const fileInput = document.querySelector('input[type="file"]');

// Инициализация шаблона
const template = document.querySelector('.add-product__photo-box');

fileInput.addEventListener('change', () => {
    // Клонируем шаблон
    const newPreview = template.cloneNode(true);
    newPreview.classList.remove('add-product__hidden');

    // Находим элементы внутри клонированного шаблона
    const newImgFile = newPreview.querySelector('.add-product__image');
    const deleteBtn = newPreview.querySelector('.add-product__delete-image');

    const file = fileInput.files[0];
    if (!file) return;

    // Загрузка и отображение изображения
    const reader = new FileReader();
    reader.onload = e => {
        newImgFile.src = e.target.result;
        newImgFile.style.display = 'block'; // Добавляем отображение изображения
    };
    reader.readAsDataURL(file);

    // Добавляем превью в начало контейнера
    photoInnerEl.prepend(newPreview);
});

// Обработчик удаления фотографии
document.addEventListener('click', (event) => {
    if(event.target.closest('.add-product__delete-image')) {
        const previewBox = event.target.closest('.add-product__photo-box');
        if(previewBox) {
            previewBox.remove();
        }
    }
});

// Обработчик для поля цены
const priceInput = document.getElementById('id_price');
if(priceInput) {
    priceInput.addEventListener('input', () => {
        let val = priceInput.value.replace(/[^\d]/g, '');
        priceInput.value = val;
    });
}