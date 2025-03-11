async function loginFunction(event) {
    event.preventDefault();  // Предотвращаем стандартное действие формы

    // Получаем форму и собираем данные из неё
    const form = document.getElementById('login-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/patients/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Проверяем успешность ответа
        if (!response.ok) {
            // Получаем данные об ошибке
            const errorData = await response.json();
            displayErrors(errorData);  // Отображаем ошибки
            return;  // Прерываем выполнение функции
        }

        const result = await response.json();

//        if (result.message) {  // Проверяем наличие сообщения о успешной регистрации
//            window.location.href = '/pages/profile';  // Перенаправляем пользователя на страницу логина
//        } else {
//            alert(result.message || 'Неизвестная ошибка');
//        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при входе. Пожалуйста, попробуйте снова.', error);
    }
}