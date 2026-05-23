```javascript
prompt() 
alert()
``` 

## Операторы
```javascript
2 ** 4 // возведение в степень, 16;
```

// Функциональное выражение (Func expression). Не всплывают.
```javascript
let sum = function (a, b) {
    return a + b;
};

console.log(mult(2,10));
```
# Функции

## Декларативная функция (Fund declaration). Всплывает.
```javascript
function mult(a, b) {return a * b};
```

## Стрелочные функции
```javascript
const double = num => num * 2; //return не нужен: если нет "{}", то JS подставляет его неявно.
```
### Когда нужны скобки, а когда - нет
Не нужны:
```javascript
const square = x => x ** 2; 
```
Скобки нужны: 0 или более одного аргумента
```javascript
const sayHi = () => console.log("Привет!"); 

const sum = (a, b) => a + b; 
```

## в отличие от верхней, если есть "{}":
```javascript
const geDiscountPrice = (price, discount) => {
    const discountAmount = price * (discount / 100);
    const finalPrice = price - discountAmount;
    return finalPrice;
}
console.log(geDiscountPrice(1000, 20)); // 800
```

### Пример с созданием объекта и присвоением свойства. Обязательны ()
```javascript
const createUser = id => ({ user_id: id }); 

console.log(createUser(42)); // Выведет: { user_id: 42 }
```

## Использование функции в качестве возвращаемого значения

**Функция высшего порядка в JavaScript(HOF)** — это функция, которая принимает другую функцию в качестве аргумента или возвращает новую функцию в качестве результата.

### Прием функции как аргумента (Callback)
```javascript
const numbers = [1, 2, 3, 4, 5];

// map принимает функцию как аргумент
const doubled = numbers.map(function(num) {
  return num * 2;
});
```

### Методы массивов
#### map()
```javascript
const numbers = [1, 2, 3];
const squared = numbers.map(x => x ** 2); // Результат: [1, 4, 9]
```
**Продвинутые фишки**
map(element, index, array) - метод на самом деле принимает 3 аргумента
```javascript
const frameworkList = ['React', 'Vue', 'Angular'].map((item, index) => {
    return `${index + 1}. ${item}`;
});
// Результат: ['1. React', '2. Vue', '3. Angular']
```

#### reduce()
Сжатие (агрегирование) массива. 

```javascript
const результат = массив.reduce((accumulator, item, index, array) => {
    // логика трансформации
    return аккумулятор; // ВАЖНО: всегда возвращать аккумулятор!
}, initialValue);
```
Accumulator (аккумулятор): это ваша «копилка» или промежуточный результат. На каждом шаге цикла он равен тому, что вернул return на предыдущем шаге.
item: текущий элемент массива (как в map).
index и array: индекс элемента и сам исходный массив (используются редко).
initialValue (начальное значение): то, с чего стартует ваша «копилка» на первом шаге.
initialValue важно прописывать, потому что если на вход поступит пустой массив, то 
вернётся ошибка вместо значения, прописанного в initialValue.

**Примеры**<br>
Подсчёт суммы
**Возможные ошибки:**
```javascript
const orders = [120, 500, 300, 150];

const totalSum = orders.reduce((acc, currentPrice) => {
    return acc + currentPrice
}) // initialValue пропущен
console.log(totalSum); // 1070, программа сработала, но!
```

```javascript
const orders = [];

const totalSum = orders.reduce((acc, currentPrice) => {
    return acc + currentPrice
})
console.log(totalSum); // ОШИБКА
```
**Правильный вариант**
```javascript
const orders = [];

const totalSum = orders.reduce((acc, currentPrice) => {
    return acc + currentPrice
},0)
console.log(totalSum); // 0
```
**Ошибка**
```javascript
const webOrders = [{price: 120}, {price: 500}];

const total = webOrders.reduce((acc, item) => acc + item.price);
console.log(total); // ❌ Выведет: "[object Object]500"
```
**Правильно:**
```javascript
const totalCorrect = webOrders.reduce((acc, item) => acc + item.price, 0);
console.log(totalCorrect); // 620
```

#### filter()
```javascript
const отфильтрованныйМассив = массив.filter((element, index, array) => {
    // Условие проверки
    return true; // или false
});
// true - элемент копируется в массив
// false - нет

const numbers = [1, 2, 3, 4, 5, 6];

const evenNumbers = numbers.filter(num => num % 2 === 0);

console.log(evenNumbers); // [2, 4, 6]
console.log(numbers);     // [1, 2, 3, 4, 5, 6] (исходный массив не изменился!)

const evenNumbers = numbers.filter(num => !(num % 2 === 0));
//вернёт массив, в котором элементы не соответствуют условиям (нечётные в данном случае)
```

### Каррирование

```javascript
function multiply(a) {
  return function(b) {
    return function(c) {
      return a + b - c;
    };
  };
}

console.log(multiply(5)(10)(10)); // 5
```

### Замыкание

```javascript
//Варианты, где можно ошибиться:
function createCounter() {
    let count = 0;

    return function counting(count) {//Ошибка: Shadowing, перекрывание count - параметр закрывает переменную
        return count++;
    }
}

let counter1 = createCounter();
console.log(counter1());
```


### Области памяти

```javascript
function createCounter() {
    let count = 0;

    return function counting() {
        return ++count;
}
}

let counter1 = createCounter();
let counter2 = createCounter();
console.log(counter1());
console.log(counter1());
console.log(counter1());
console.log(counter2());
//При создании counter2(), создаётся новая независимая обрасть памяти, не относящаяся к 
// counter1
```
Переменная count, даже после завершения первоначальной функции, остаётся доступной для 
новой функции, которую мы создали (counter1,2). Переменная остаётся в специальном объекте
окружения (Lexical Environment). Переменная остаётся даже после завершения функции, в которой она была вызвана. Это замыкание. Доступность этой переменной для созданных функция (counter1,2) = переменная находится в их зоде видимости (Scope).

# Область видимости

```javascript
const name = "Алексей"; // Глобальная переменная

function greet() {
    const name = "Иван"; // Затенение! Создали локальную переменную
    console.log(name); // Выведет "Иван", а не "Алексей"
}
greet();
console.log(name)// Алексей. Переменная осталась не тронута. 
// При этом:
let name = "Алексей"; // Глобальная переменная

function greet() {
    name = "Иван"; // Затенение! Создали локальную переменную
    console.log(name); // Выведет "Иван", а не "Алексей"
}
greet();
console.log(name) //Иван. Глобальная переменная изменена. Отличие от С, тут внутри функции переменная может быть иземенена в глобал. 

```

# Контекст вызова
this. Это ссылка на объект, который в данный момент выполняет функцию. Он динамический.
```javascript
const user = {
    name: 'Алексей',
    greet() {
        console.log(`Привет, я ${this.name}`);
    }
};

// Вызываем напрямую от объекта:
user.greet(); // Переменная this = user. Выведет: "Привет, я Алексей"

// ❌ КОПИРУЕМ МЕТОД В ПЕРЕМЕННУЮ:
const saveGreet = user.greet; 

// Вызываем переменную:
saveGreet(); // Выведет: "Привет, я undefined" (или упадет с ошибкой в 'use strict')

```

# bind()
- метод используются для привязки this к объекту. Предотвращает потерю контекста
- используется один раз. Заново привязать к другому контексту не получится.
```javascript
//основной синтаксис
const user = {
    name: 'Алексей',
    greet() {
        console.log(`Привет, я ${this.name}`);
    }
};

// ❌ Без bind: контекст теряется
const looseGreet = user.greet; // It's "Method detachment", отрыв метода или передача метода как обычной функции
looseGreet(); // Выведет: undefined (или ошибка в strict mode)

// ✅ С bind: намертво привязываем объект user к функции
const safeGreet = user.greet.bind(user);
safeGreet(); // Выведет: "Привет, я Алексей"


// Кроме того есть интересные применения, например
function multiply(a, b) {
    return a * b;
}

// Создаем новую функцию, где первый аргумент (а) ВСЕГДА равен 2
const double = multiply.bind(null, 2);

console.log(double(5));  // Выведет: 10 (2 * 5)
console.log(double(10)); // Выведет: 20 (2 * 10)

```

```javascript
// Попытка повторной привязки объекта
const obj1 = { name: 'Иван' };
const obj2 = { name: 'Петр' };

const bind1 = showName.bind(obj1);
const bind2 = bind1.bind(obj2); // ❌ Попытка перепривязать на obj2
```

# call()
```javascript
    const obj = { name: "John Wick" };

    function sayHello() {
        console.log(`Hello, ${this.name}!`);
    }
    
    sayHello.call(obj); // вызовет "Hello, John Wick!"
    // берём функцию, вызываем объект
```
