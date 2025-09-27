// Логика для страницы базы вопросов

let questionsData = null;

// Загрузка данных при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadQuestions();
});

// Функция загрузки JSON файла
async function loadQuestions() {
    try {
        const response = await fetch('../data/questions.json');
        questionsData = await response.json();
        displayQuestions();
    } catch (error) {
        console.error('Ошибка загрузки вопросов:', error);
        document.getElementById('questions-content').innerHTML = '<p>Ошибка загрузки данных</p>';
    }
}

// Функция отображения вопросов
function displayQuestions() {
    const container = document.getElementById('questions-content');
    let html = '';
    
    // Проходим по каждой теме
    for (const [topicName, subtopics] of Object.entries(questionsData)) {
        html += `<div class="topic">
            <h2 onclick="toggleTopic('${topicName}')" style="cursor: pointer;">${topicName}</h2>
            <div id="topic-${topicName}" class="topic-content" style="display: none;">`;
        
        // Проходим по подтемам
        for (const [subtopicName, questions] of Object.entries(subtopics)) {
            html += `<div class="subtopic">
                <h3 onclick="toggleSubtopic('${topicName}', '${subtopicName}')" style="cursor: pointer; margin-left: 20px;">${subtopicName}</h3>
                <div id="subtopic-${topicName}-${subtopicName}" class="subtopic-content" style="display: none; margin-left: 40px;">`;
            
            // Проходим по вопросам
            questions.forEach((item, index) => {
                const questionId = `question-${topicName}-${subtopicName}-${index}`;
                html += `<div class="question-item">
                    <p><strong>Вопрос:</strong> ${item.question}</p>
                    <button onclick="toggleAnswer('${questionId}')">Показать ответ</button>
                    <div id="${questionId}" class="answer" style="display: none;">
                        <p><strong>Ответ:</strong> ${item.answer}</p>
                    </div>
                </div>`;
            });
            
            html += `</div></div>`;
        }
        
        html += `</div></div>`;
    }
    
    container.innerHTML = html;
}

// Функция переключения видимости темы
function toggleTopic(topicName) {
    const element = document.getElementById(`topic-${topicName}`);
    element.style.display = element.style.display === 'none' ? 'block' : 'none';
}

// Функция переключения видимости подтемы
function toggleSubtopic(topicName, subtopicName) {
    const element = document.getElementById(`subtopic-${topicName}-${subtopicName}`);
    element.style.display = element.style.display === 'none' ? 'block' : 'none';
}

// Функция переключения видимости ответа
function toggleAnswer(questionId) {
    const element = document.getElementById(questionId);
    const button = element.previousElementSibling;
    
    if (element.style.display === 'none') {
        element.style.display = 'block';
        button.textContent = 'Скрыть ответ';
    } else {
        element.style.display = 'none';
        button.textContent = 'Показать ответ';
    }
}
