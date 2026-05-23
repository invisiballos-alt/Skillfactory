const person = {
    name: 'Sancke',
    age: 24
};

function setFullName(fullName) {
    this.fullName = fullName;
}

const setPersonFullName = setFullName.bind(person);

setPersonFullName("John Smith");

console.log(person);


console.log(person.fullName);
