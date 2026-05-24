function printInfo(params) {
    console.log(`Name: ${this.name}, Age: ${this.age}`);
}

const person = {
    name: 'Sancke',
    age: 24
}

printInfo.call(person)