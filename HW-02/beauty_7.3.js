const users = [
    { name: 'Иван', age: 24 },
    { name: 'Анна', age: 16 },
    { name: 'Олег', age: 18 },
    { name: 'Мария', age: 15 },
    { name: 'Сергей', age: 30 }
];

const shortAdultNames = users
    .filter(user => user.age >= 18)
    .map(user => user.name);        

console.log(shortAdultNames); 
