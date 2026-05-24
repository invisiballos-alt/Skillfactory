const users = [
    { name: 'Иван', age: 24 },
    { name: 'Анна', age: 16 },
    { name: 'Олег', age: 18 },
    { name: 'Мария', age: 15 },
    { name: 'Сергей', age: 30 }
];

const adults = users.filter(function(user) {
    return user.age >= 18;
});

const adultNames = adults.map(function(user) {
    return user.name; // map() сразу складывает каждого юзера в новый массив
});

console.log(adults); 

console.log(adultNames); 