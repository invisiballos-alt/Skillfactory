function overflowTheHeap() {
    const memoryLeaker = [];
    console.log("Поехали! Забиваем кучу памяти...");
    
    // Бесконечный цикл, который генерирует огромные строки и объекты
    while (true) {
        // Создаем объект с большим массивом случайных чисел
        const heavyObject = {
            data: new Array(1000000).fill("A"),
            timestamp: Date.now()
        };
        // Сохраняем ссылку, чтобы Garbage Collector не смог удалить объект
        memoryLeaker.push(heavyObject); 
    }
}

overflowTheHeap();
