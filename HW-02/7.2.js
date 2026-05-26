function calculate(a, b, operator) {
    switch (operator) {
        case "+":
            return a + b;
        case "-":
            return a - b;
        case "*":
            return a * b;
        case "/":
            return a / b;
        default:
            return "Неизвестный оператор";
    }
}


const dataObject = {
    a: 2,
    b: 3,
    operator: "+"
};


const result = calculate.apply(dataObject, [2, 3, "+"]); 

console.log(result);

//В задании: "Используйте метод apply, чтобы вызвать функцию calculate с передачей объекта
// со значениями a, b и operator в качестве первого аргумента и массива 
// с тремя значениями [2, 3, "+"] в качестве второго аргумента." 
// Это избыточность данных,
//  ошибка в условии.
